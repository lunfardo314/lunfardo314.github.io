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
Another example would be `selfOutputPath` and `selfSiblingConstraint`:

Their definitions:

```
// selfOutputPath returns first 3 bytes of 4 byte-long current evaluation context path
func selfOutputPath : slice(at,0,2)

// selfSiblingConstraint returns bytecode of the constraint script on the current UTXO with the index $0
func selfSiblingConstraint : atPath(concat(selfOutputPath, $0))
```

It just returns the bytecode of the constraint script on the same UTXO, where the caller is located, with specified index. For example `selfSiblingConstraint(0)` will always return bytecode of the `amount` constraint and `selfSiblingConstraint(1)` will always return bytecode of the lock constraint on the same UTXO.

## Bytecode manipulation

Bytecode manipulation functions allow the script formula to analyze bytecodes of scripts itself. This is powerful feature, which enables rich programmability of the transaction constraints.

For example, a particular constraint may require another constraint, on the same or another UTXO, to be of particular kind or have particular parameters.

### parsePrefixBytecode
Function `parsePrefixBytecode` treats its only argument as a bytecode of the formula and returns call prefix of that bytecode as its value. One may think the call prefix is an encoded function name. 

For example, the following expression will check if constraint at index 3 on the same UTXO  is a `chain` constraint: `equal(parsePrefixBytecode(selfSiblingConstraint, 3), #chain)`

Remember, literal `#chain` is constant bytecode value of the call prefix of the function `chain`.
Here, the helper function `selfSiblingConstraint` is defined the following way:

### parseArgumentBytecode
Function `parseArgumentBytecode` takes 3 arguments. 1st argument is treated as a bytecode of the formula. 2nd argument must be one byte and it s interpreted as index of the formula argument.
3rd argument is treated as a function call prefix.

It is enforced, that call prefixes in the 1st and 3rd argument should be equal, otherwise call panics. 

Function returns bytecode of the argument with number specified in the 2nd argument.  

### parseInlineData

Let's say,amount constraint at index 0 of some UTXO is bytecode of `amount(z64/1337)`.

Expression `selfSiblingConstraint(0)` will always return bytecode of the `amount` constraint, with actual amount data as the argument.

However, formula `parseArgumentBytecode(selfSiblingConstraint(0))` will not return bytes of number `1337`, but instead a literal formula, which, upon evaluation, returns `1337`. It is because bytecode of the literal `z64/1337` is also a formula, which return trat value, not the value itself 

To retrieve the value itself, we have function `parseInlineData`.

It treats its single argument as a formula bytecode, which is literal (aka inlinde data). It checks if it is indeed a data function. If it is, it returns the data by stripping the data call prefix. Otherwise, panics.  

So, expression `parseInlineData(parseArgumentBytecode(selfSiblingConstraint(0)))` will always return bytes of the amount, a big-endian bytes of an integer.

For example, `parseInlineDataArgument` retrieves inline data from the particular output
```
// in bytecode $0, 
// function parses argument with index $2, treats it as inline data call, 
// returns the inline data, Enforces call prefix is equal to $1
func parseInlineDataArgument : parseInlineData(parseArgumentBytecode($0,$1,$2))
```
Other functions helps to retrieve amount value from any UTXO: 
```
// $0 is a path to output
// Returns amount value 8 bytes from the output at path given in $0
func amountValueByOutputPath : 
    uint8Bytes(parseInlineDataArgument(atPath(concat($0, amountConstraintIndex)), #amount,0))

func selfAmountValue: amountValueByOutputPath(selfOutputPath)

```