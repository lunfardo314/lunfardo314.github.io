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




## Ledger constants

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

