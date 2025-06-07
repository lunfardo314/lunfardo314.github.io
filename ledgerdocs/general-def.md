# General purpose ledger definitions

## Embedded functions
We already introduced [validation process](txdocs/validation.md) of a transaction $T$: all formulas are evaluated in each of the consumed and produced UTXOs. Transaction is valid if all evaluations return `true`. 

Proxima ledger definitions embeds two special embedded functions, which enables access to the evaluation context and the transaction context in the EasyFL formulas:

### Evaluation context: `at`
Each time constraint script is evaluated in the transaction context, its path in $T^{ctx}$ is provided in the context.

The path always have the form $(0, 2, i, j)$ for the constraint $j$ of the **produced** UTXO $i$.
The path always have the form $(1, 0, i, j)$ for the constraint $j$ of the **consumed** UTXO $i$.

Function `at` (without parameters) returns the evaluation context path in the $T^{ctx}$ of to the UTXO being evaluated. Each formula "knows" where it is located: in which UTXO and its index in the UTXO. 

Formula can determine its location by analyzing the path returned by function `at`. In particular, formula "knows" if it is evaluated in the consumed" context (as an input fetched from the ledger state), or in the produced one (as UTXO produced by the transaction being validated). 

There are special helper functions for this in the Proxima ledger  definitions:  

```go
func pathToConsumedOutputs : 0x0100

func pathToProducedOutputs : 0x0002

func isPathToConsumedOutput : hasPrefix($0, pathToConsumedOutputs)

func isPathToProducedOutput : hasPrefix($0, pathToProducedOutputs)

func selfIsConsumedOutput : isPathToConsumedOutput(at)

func selfIsProducedOutput : isPathToProducedOutput(at)
```

`hasPrefix` is a standard EasyFL predicate to check if argument has a particular prefix.
Predicates `selfIsConsumedOutput` and `selfIsProducedOutput` allows to distinguish between "consumed" and "produced" evaluation context. It is common, that UTXO constraint scripts check different things in different evaluation contexts. 

### Access to the transaction context: `atPath`

Embedded function `atPath` with the single argument, that is interpreted as a path in the transaction context $T^{ctx}$, returns bytes of the corresponding element. It panics if path is incorrect.

For example, each script formula can retrieve its own bytecode with the function. There's special function `self`, provided by the ledger definitions:  
```go
func self : atPath(at)
```

### Access to the tuple element: `atTuple8`

Embedded function `atTuple8` treats its argument `$0` as a serialized tuple and argument `$1` as index of the element. The index must be 1 byte-long. 

Function returns element of the tuple. 

## Ledger constants
At genesis, number of values, such as initial supply and genesis public key, must be set up in for the ledger. These values are called *ledger constants*. The values of the ledger constants are encoded right in the ledger definitions and therefore are immutable.  

Constants are represented by EasyFL functions without parameters with name starting with `const`. Here are examples of typical definitions of ledger constants in EasyFL (they can also be found in the [proxima.genesis.id](ledgerdocs/genesis.id.md) YAML file):

```go
func constInitialSupply : u64/1000000000000000
func constGenesisControllerPublicKey : 0x9ad4caddd2356a7853eb038a5b4fd3197522af51af4073584260c53bbfaf1816
func constGenesisTimeUnix : u64/1749146740
func constTickDuration : u64/80000000
func constMaxTickValuePerSlot : u64/127
func ticksPerSlot64 : add(constMaxTickValuePerSlot, u64/1)
func constSlotInflationBase : u64/33000000
func constLinearInflationSlots : u64/3
func constBranchInflationBonusBase : u64/5000000
func constMinimumAmountOnSequencer : u64/1000000000000
func constMaxNumberOfEndorsements : u64/8
func constPreBranchConsolidationTicks : u64/25
func constPostBranchConsolidationTicks : u64/12
func constTransactionPace : u64/64
func constTransactionPaceSequencer : u64/2
func constVBCost16 : u16/1
```
Constant `constInitialSupply` sets the initial supply of tokens on the genesis output. 
Constant `constGenesisTimeUnix` sets the absolute time reference in Unix seconds for the ledger.
Constant `constTickDuration` is a constant in nanoseconds, which determines correspondence between ledger time duration and clock duration.

The correspondence between ledger time and clock time is crucial for the cooperative consensus, because token holder must come together "in real time and space" with approximately the same assumptions about clock time in order to be able to cooperate.

Genesis controller public key belongs to the owner of all tokens at genesis and is also provided in the lock script of the genesis output. Later, the owner of tokens will change, but the public key of the originator will remain in the ledger forever. 

## Helper functions
Apart from embedded (hardcoded) function and ledger validity constraints, Proxima ledger definitions contain many EasyFL definition of the helper functions. All of it can be found in [proxima.genesis.id](ledgerdocs/genesis.id.md). Some of it we will describe here:

Functions with the names starting with `path` represent paths of various parts of the $T^{ctx}$. For example:
```go
func pathToTimestamp : 0x0005
```
Function `mustSize` enforces certain size of the data:
```go
func mustSize : if(equalUint(len($0), $1), $0, !!!wrong_data_size)
```

Transaction ID calculation (needed for checking the signature) is defined the following way:
```
func txTimestampBytes : atPath(pathToTimestamp)
	
func txEssenceBytes :
    concat( 
        concat( 
            atPath(pathToInputIDs), 
            atPath(pathToUnlockParams), 
            atPath(pathToProducedOutputs), 
            atPath(pathToSeqAndStemOutputIndices), 
            atPath(pathToTimestamp) 
        ), 
        concat( 
            atPath(pathToTotalProducedAmount), 
            atPath(pathToInputCommitment), 
            atPath(pathToEndorsements), 
            atPath(pathToExplicitBaseline), 
            atPath(pathToLocalLibraries) 
        ) 
    )

func txIDPrefix : if(isSequencerTransaction, bitwiseOR(txTimestampBytes, 0x0000000001), txTimestampBytes)

func txID : 
    concat(
        txIDPrefix, 
        byte(sub(numProducedOutputs,1), 7), 
        slice(blake2b(txEssenceBytes),6,31)
    )
```

## Bytecode manipulation
