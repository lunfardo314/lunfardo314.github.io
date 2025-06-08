# Chain lock source

```
func selfReferencedChainData : 
	parseInlineDataArgument(
		consumedConstraintByIndex(selfUnlockParameters),
		#chain,
		0
	)

// $0 - parsed referenced chain constraint
func selfReferencedChainIDAdjusted : if(
	isZero($0),
	blake2b(inputIDByIndex(byte(selfUnlockParameters, 0))),
	$0
)

// $0 - chainID
// $1 - self unlock parameters
func validChainUnlock : and(
    equal(len($1), u64/2),                          // prevent panic in compound locks
	equal($0, selfReferencedChainIDAdjusted(slice(selfReferencedChainData,0,31))), // chain id must be equal to the referenced chain id 
	equal(
		// the chain must be unlocked for state transition (mode = 0) 
		byte(unlockParamsByConstraintIndex($1),2),
		0
	)
)

// $0 - chainID
// Unlock parameters 2 bytes: [unlocked chain output index, chain constraint index]
func chainLock : and(
	require(equal(selfBlockIndex,1), !!!locks_must_be_at_block_1), 
	enforceMinimumStorageDeposit,
	or(
		and(
			selfIsProducedOutput, 
			require(equal(len($0),u64/32), !!!32-byte_long_argument_expected),
            require(not(isZero($0)), !!!non_zero_argument_expected)   // to prevent common error
		),
		and(
			selfIsConsumedOutput,
			not(equal(selfOutputIndex, byte(selfUnlockParameters,0))), // prevent self referencing 
			validChainUnlock($0, selfUnlockParameters)
		)
	)
)

// short version of chainLock
// $0 - chainID
// Unlock parameters 2 bytes: [unlocked chain output index, chain constraint index]
func c : chainLock($0)
```
