# General purpose ledger definitions

## Embedded functions
We already introduced the transaction [validation process](txdocs/validation.md): all formulas are evaluated within each of the consumed and produced UTXOs. A transaction is valid if all evaluations return true.

The Proxima ledger includes two special embedded functions that allow access to the evaluation and transaction context from within EasyFL formulas:

### Evaluation context path: `at`
Each time a constraint script is evaluated, its path within the transaction context $T^{ctx}$  is provided. The path has one of the following forms:

* $(0, 2, i, j)$ for the constraint $j$ of the **produced** UTXO $i$.
* $(1, 0, i, j)$ for the constraint $j$ of the **consumed** UTXO $i$.

The `at` function (with no parameters) returns this evaluation context path, allowing a formula to determine where it is being evaluated—specifically, in which UTXO and at what index.

A formula can identify whether it is in the "consumed" or "produced" context using helper functions defined in the library:
```yaml
func pathToConsumedOutputs : 0x0100
func pathToProducedOutputs : 0x0002
func isPathToConsumedOutput : hasPrefix($0, pathToConsumedOutputs)
func isPathToProducedOutput : hasPrefix($0, pathToProducedOutputs)
func selfIsConsumedOutput : isPathToConsumedOutput(at)
func selfIsProducedOutput : isPathToProducedOutput(at)
```
Here, `hasPrefix` is a standard EasyFL predicate that checks if a value starts with a specific prefix. The `selfIsConsumedOutput` and `selfIsProducedOutput` predicates allow a formula to distinguish between consumed and produced contexts — useful when scripts should behave differently depending on the context.

### Access to the transaction context: `atPath`

The `atPath` function takes a single argument interpreted as a path in the transaction context $T^{ctx}$, and returns the corresponding byte value. It will panic if the path is invalid.

For example, to retrieve its own bytecode, a script can use the following helper function `self`:
```go
func self : atPath(at)
```

## Ledger constants
At genesis, several fixed values must be set — such as the initial token supply and the genesis public key. These immutable values are known as ledger constants and are encoded directly into the ledger definitions.

Each constant is represented as a parameterless EasyFL function with a name prefixed by `const`. Here are some typical examples from the [proxima.genesis.id](ledgerdocs/genesis.id.md) YAML file:

```yaml
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
* `constInitialSupply` defined initial token supply. 
* `constGenesisTimeUnix` sets the Unix time reference for the ledger time axis.
* `constTickDuration` (in nanoseconds), defined correspondence between ledger time duration and clock duration.

While the ledger is agnostic about real clock, sharing the correspondence between ledger time and real-world clock between nodes is critical to cooperative consensus: token holders must coordinate under roughly the same clock assumptions to interact effectively.

The `constGenesisControllerPublicKey` represents the public key of the genesis token holder. This key is embedded in the genesis output's lock script and remains on the ledger for a lifetime of the ledger, even after token ownership changes.

## Helper functions
Besides embedded functions and ledger constraints, the Proxima ledger includes many helper functions defined in EasyFL. These can be found in the [proxima.genesis.id](ledgerdocs/genesis.id.md) file. A few examples are provided here:

Functions with the names starting with `path` define paths of various parts of the $T^{ctx}$. For example:
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
        atPath(pathToInputIDs), 
        atPath(pathToUnlockParams),
        atPath(pathToProducedOutputs), 
        atPath(pathToSeqAndStemOutputIndices),
        atPath(pathToTimestamp),
        atPath(pathToTotalProducedAmount),
        atPath(pathToInputCommitment), 
        atPath(pathToEndorsements),
        atPath(pathToExplicitBaseline),
        atPath(pathToLocalLibraries)
     )

func txIDPrefix : if(isSequencerTransaction, bitwiseOR(txTimestampBytes, 0x0000000001), txTimestampBytes)

func txID : 
    concat(
        txIDPrefix, 
        byte(sub(numProducedOutputs,1), 7), 
        slice(blake2b(txEssenceBytes),6,31)
    )
```
Another examples would be `selfOutputPath` and `selfSiblingConstraint`:
```
// selfOutputPath returns first 3 bytes of 4 byte-long current evaluation context path
func selfOutputPath : slice(at,0,2)

// selfSiblingConstraint returns bytecode of the constraint script on the current UTXO with the index $0
func selfSiblingConstraint : atPath(concat(selfOutputPath, $0))
```
These allow scripts to access other constraints within the same UTXO.

## Bytecode manipulation

Bytecode manipulation functions allow constraint scripts to inspect other scripts' structure, enabling rich programmable behavior.

### parsePrefixBytecode
Extracts the function call prefix (like an encoded function name):
This checks whether the 3rd constraint is a `chain` constraint:
```
equal(parsePrefixBytecode(selfSiblingConstraint, 3), #chain)
```

### parseArgumentBytecode
Function `parseArgumentBytecode` takes 3 arguments. 1st argument is treated as a bytecode of the formula. 2nd argument interpreted as index of the formula argument.
3rd argument is treated as a function call prefix.

It is enforced, that call prefixes in the 1st and 3rd argument should be equal, otherwise call panics. 

Function returns bytecode of the argument with number specified in the 2nd argument.  

### parseInlineData

Let's say,amount constraint at index 0 of some UTXO is bytecode of `amount(z64/1337)`.

Expression `selfSiblingConstraint(0)` will always return bytecode of the `amount` constraint, with actual amount data as the argument.

However, formula `parseArgumentBytecode(selfSiblingConstraint(0))` will not return bytes of number `1337`, but instead a literal formula, which, upon evaluation, returns `1337`. It is because bytecode of the literal `z64/1337` is also a formula, which return trat value, not the value itself. 

To retrieve the value itself, we have function `parseInlineData`.

It treats its single argument as a formula bytecode, which is literal (aka inline data). It checks if it is indeed a data function. If it is, it returns the data by stripping the data call prefix. Otherwise, panics.  

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