# Ledger definition library
Proxima ledger definitions are contained in the ledger definition file, also known as the _ledger ID_,
which is usually YAML. It is used to create a database with genesis ledger state for the first node in the network.

Besides hardcoded functions, the transaction validity rules, are written in _EasyFL_, a simple scripting language with functional syntax and semantics. We introduced it [here](txdocs/easyfl.md).

Here we provide the entire [proxima.genesis.id](ledgerdocs/genesis.id.md) file as an example of ledger definitions. It lists all embedded (hardcoded) functions as well as source and bytecode forms of the EasyFL formulas. 

The ledger definitions becomes an immutable part of ledger state (we will skip hardfork/upgrade topic here). It is also always a part of the snapshot.

The Proxima ledger definitions is an extension of the base EasyFL library of functions. It is crucial, that all nodes in the network share the ledger definitions with exactly the same hash of the library. 

We will go through many of the functions, defined in the ledger ID. Those functions encode rules of how assets on the ledger can be created and modified, together with inflation rules and on-ledger incentives. All this is designed with the intention to impose certain behavior of token holders in the ledger, that leads to the cooperative consensus. 

One may think about ledger definitions as core set of smart contracts, that defines core concepts on the ledger.

## Embedded functions

We already introduced [validation process](txdocs/validation.md) of a transaction $T$: all formulas are evaluated in each of the consumed and produced UTXOs. Transaction is valid if all evaluations return `true`. 

Proxima ledger definitions embeds two special embedded functions, which enables access to the evaluation context and the transaction context in the EasyFL formulas:

### Evaluation context: `at`
Each time constraint script is evaluated in the transaction context$, its path in $T^{ctx} is provided in the context.

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

## Helper functions

## Mandatory UTXO constraints

## Amount

## Locks

### AddressED25519 lock

### Stem lock

## Chain constraint

### Chain lock

## Sequencer constraint

## Inflation

