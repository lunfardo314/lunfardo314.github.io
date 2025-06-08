# Chain constraint source

```
// chain(<chain constraint data>)
// <chain constraint data: 35 bytes:
// - 0-31 bytes chain id 
// - 32 byte predecessor input index 
// - 33 byte predecessor block index 
// - 34 byte transition mode 

// reserved value of the chain constraint data at origin
func originChainData: concat(repeat(0,32), 0xffffff)
func destroyUnlockParams : 0xffffff

// parsing chain constraint data
// $0 - chain constraint data
func chainID : slice($0, 0, 31)

// $0 - chain constraint data
func transitionMode: byte($0, 34)
func predecessorConstraintIndex : slice($0, 32, 33) // 2 bytes

// unlock parameters for the chain constraint. 3 bytes: 
// 0 - successor output index 
// 1 - successor constraint block index
// 2 - transition mode must be equal to the transition mode in the successor constraint data 

// only called for produced output
// $0 - self produced constraint data
// $1 - predecessor data
func validPredecessorData : and(
	if(
		isZero(chainID($1)), 
		and(
			// case 1: predecessor is origin. ChainID must be blake2b hash of the corresponding input id 
			equal($1, originChainData),
			equal(chainID($0), blake2b(inputIDByIndex(byte($0,32))))
		),
		and(
			// case 2: normal transition
			equal(chainID($0), chainID($1)),
		)
	),
	equal(
		// enforcing equal transition mode on unlock data and on the produced output
		transitionMode($0),
		byte(unlockParamsByConstraintIndex(predecessorConstraintIndex($0)),2)
	)
)

// $0 - predecessor constraint index
func chainPredecessorData:
	parseInlineDataArgument(
		consumedConstraintByIndex($0),
		selfBytecodePrefix,
		0
	)

// $0 - self chain data (consumed)
// $1 - successor constraint parsed data (produced)
func validSuccessorData : and(
		if (
			// if chainID = 0, it must be origin data
			// otherwise chain IDs must be equal on both sides
			isZero(chainID($0)),
			equal($0, originChainData),
			equal(chainID($0),chainID($1))
		),
		// the successor (produced) must point to the consumed (self)
		equal(predecessorConstraintIndex($1), selfConstraintIndex)
)

// chain successor data is computed in the context of the consumed output
// from the selfUnlock data
func chainSuccessorData : 
	parseInlineDataArgument(
		producedConstraintByIndex(slice(selfUnlockParameters,0,1)),
		selfBytecodePrefix,
		0
	)

// Constraint Source: chain($0)
// $0 - 35-bytes data: 
//     32 bytes chain id
//     1 byte predecessor input index 
//     1 byte predecessor constraint index
//     1 byte transition mode
// Transition mode: 
//     0x00 - state transition
//     0xff - origin state, can be any other values. 
// -----
// unlock parameters for the chain constraint. 3 bytes:
// 0 - successor output index
// 1 - successor block index
// 2 - transition mode must be equal to the transition mode in the successor constraint data
func chain: and(
      // chain constraint cannot be on output with index 0xff = 255
   not(equal(selfOutputIndex, 0xff)),  
   or(
      if(
        // if it is produced output with zero-chainID, it is chain origin.
         and(
            isZero(chainID($0)),
            selfIsProducedOutput
         ),
         or(
            // enforcing valid constraint data of the origin: concat(repeat(0,32), 0xffffff)
            equal($0, originChainData), 
            !!!chain_wrong_origin
         ),
         nil
       ),
        // check validity of chain transition. Unlock data of the constraint 
        // must point to the valid successor (in case of consumed output) 
        // or predecessor (in case of produced output) 
       and(
           // 'consumed' side case, checking if unlock params and successor is valid
          selfIsConsumedOutput,
          or(
               // consumed chain output is being destroyed (no successor)
            equal(selfUnlockParameters, destroyUnlockParams),
               // or it must be unlocked by pointing to the successor
            validSuccessorData($0, chainSuccessorData),     
            !!!chain_wrong_successor
          )	
       ), 
       and(
          // 'produced' side case, checking if predecessor is valid
           selfIsProducedOutput,
           or(
              // 'produced' side case checking if predecessor is valid
              validPredecessorData($0, chainPredecessorData( predecessorConstraintIndex($0) )),
              !!!chain_wrong_predecessor
           )
       ),
       !!!chain_constraint_failed
   )
)

```