# General purpose ledger definitions

## Embedded functions
We already introduced the transaction [validation process](txdocs/validation.md): constraint formulas are evaluated within each consumed and produced UTXO (and at the transaction level). A transaction is valid if all evaluations succeed.

The Proxima ledger includes special embedded functions that give EasyFL formulas access to the evaluation and transaction context.

### Evaluation context path: `at`
Each time a constraint script is evaluated, its path within the transaction context $T^{ctx}$ is provided. The path has one of the following forms:

- $(0, 8, i, j)$ — constraint $j$ of the **produced** UTXO $i$ (produced outputs are element 8 of the transaction).
- $(1, 0, i, j)$ — constraint $j$ of the **consumed** UTXO $i$.

The `at` function (with no parameters) returns this evaluation-context path, allowing a formula to determine where it is being evaluated — specifically, in which UTXO and at which constraint index.

A formula can identify whether it is in the consumed or produced context using helper functions defined in the library:
```
func pathToConsumedOutputs : 0x0100
func pathToProducedOutputs : 0x0008
func isPathToConsumedOutput : hasPrefix($0, pathToConsumedOutputs)
func isPathToProducedOutput : hasPrefix($0, pathToProducedOutputs)
func selfIsConsumedOutput : isPathToConsumedOutput(at)
func selfIsProducedOutput : isPathToProducedOutput(at)
```
Here, `hasPrefix` is a standard EasyFL predicate that checks if a value starts with a specific prefix. The `selfIsConsumedOutput` and `selfIsProducedOutput` predicates allow a formula to distinguish between consumed and produced contexts — useful when scripts should behave differently depending on the context.

### Access to the transaction context: `atPath`

The `atPath` function takes a single argument interpreted as a path in the transaction context $T^{ctx}$, and returns the corresponding byte value. It panics if the path is invalid.

For example, to retrieve its own bytecode, a script can use the helper function `self`:
```
func self : atPath(at)
```

## Ledger constants
At genesis, several fixed values must be set — such as the initial token supply and the genesis public key. These immutable values are known as ledger constants and are encoded directly into the JSON ledger definitions file.

Each constant is a parameterless EasyFL function whose name is prefixed with `const`. Some are hard-coded; others are filled in from the genesis configuration when the ledger is created. Examples:

```
func constInitialSupply : u64/1000000000000000
func constMaxNumberOfEndorsements : u64/8
func constPreBranchConsolidationTicks : u64/25
func constMaxTickValuePerSlot : u64/127
func ticksPerSlot64 : add(constMaxTickValuePerSlot, u64/1)
func constTransactionPace : u64/...                  // ticks, from genesis config
func constTransactionPaceSequencer : u64/...         // ticks, from genesis config
func constTickDuration : u64/...                     // nanoseconds per tick, from genesis config
func constGenesisTimeUnix : u64/...                  // Unix reference time, from genesis config
func constGenesisControllerPublicKey : 0x...         // genesis token holder public key
```
Other constants include `constAttachmentCostBudget`, `constTxIDStateTTLSlots`, `constBootstrapChainID`, `constHealthyCoverageNumerator` / `constHealthyCoverageDenominator` and `constDescription`.

* `constInitialSupply` defines the initial token supply.
* `constGenesisTimeUnix` sets the Unix-time reference for the ledger-time axis.
* `constTickDuration` (in nanoseconds) defines the correspondence between ledger-time duration and clock duration.

While the ledger is agnostic about the real clock, sharing the correspondence between ledger time and the real-world clock between nodes is critical to cooperative consensus: token holders must coordinate under roughly the same clock assumptions to interact effectively.

The `constGenesisControllerPublicKey` is the public key of the genesis token holder. This key is embedded in the genesis output's lock and remains on the ledger for the lifetime of the ledger, even after token ownership changes.

## Helper functions
Besides embedded functions and ledger constraints, the Proxima ledger includes many helper functions defined in EasyFL. A few examples are provided here.

Functions whose names start with `pathTo` define paths to various parts of $T^{ctx}$. For example:
```
func pathToTimestamp : 0x0001
```
The function `mustSize` enforces a certain size of the data:
```
func mustSize : if(equalUint(len($0), $1), $0, !!!wrong_data_size)
```

The **transaction ID** is no longer assembled by an EasyFL formula — `txID` is now an **embedded** function. It returns the 32-byte ID: the transaction-ID prefix (the timestamp with the sequencer flag in its last byte), the produced-output-count byte, and the last 26 bytes of `blake2b` of the transaction essence (all transaction elements except the signature). See [Base data elements](txdocs/base.md) and [Validation of transaction](txdocs/validation.md).

Other examples are `selfOutputPath` and `selfSiblingConstraint`:
```
// selfOutputPath returns the first 3 bytes of the 4-byte current evaluation-context path
func selfOutputPath : slice(at,0,2)

// selfSiblingConstraint returns the bytecode of the constraint at index $0 on the current UTXO
func selfSiblingConstraint : atPath(concat(selfOutputPath, $0))
```
These allow scripts to access other constraints within the same UTXO.

## Bytecode manipulation

Bytecode manipulation functions allow constraint scripts to inspect other scripts' structure, enabling rich programmable behavior.

### parseBytecode
`parseBytecode($0, $1 [, $2 …])` treats $0 as a bytecode. The second argument $1 is either a 1-byte index selecting an argument of the call, or `0x` to select the **call prefix** (the encoded function identity). Any further arguments are expected call prefixes that the bytecode must match — otherwise the call panics.

For example, this checks whether the chain constraint (at index 3 of the current UTXO) really is a `chain` call:
```
equal(parseBytecode(selfSiblingConstraint(3), 0x), #chain)
```

### parseInlineData and parseInlineDataArgument
A literal such as `z64/1337` does not compile to the raw value — it compiles to a small **formula** that returns that value when evaluated. To recover the underlying bytes:

* `parseInlineData($0)` strips the call prefix of such an inline-data bytecode and returns the data.
* `parseInlineDataArgument($0, $1, $2)` combines the two steps: it parses argument $1 of bytecode $0, enforces that the argument is inline data with call prefix $2, and returns the data.

### Reading the token balance of an output
The **amounts vector** lives at index 0 of every output (token balance, inflation, frozen coverage). The function `amountAt(vector, i)` returns element $i$ of that vector. Helper functions read the token balance (element 0) of any output:
```
// $0 - path to an output. Returns its 8-byte token balance.
func tokenBalanceByOutputPath : amountAt(atPath(concat($0, amountsConstraintIndex)), 0)

func selfTokenBalanceValue : amountAt(selfSiblingConstraint(amountsConstraintIndex), 0)
```
Here `amountsConstraintIndex` is `0` — the fixed position of the amounts vector in the output tuple.
