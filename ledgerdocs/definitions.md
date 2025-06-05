# Ledger definition library
Proxima ledger definitions are contained in the ledger definition file, also known as the _ledger ID_,
which is usually YAML. It is used to create a database with genesis ledger state for the first node in the network.

Here we provide the entire [proxima.genesis.id](ledgerdocs/genesis.id.md) file as an example of ledger definitions.

The ledger definitions becomes an immutable part of ledger state (we will skip hardfork/upgrade topic here). It is also a part of the snapshot.

The Proxima ledger ID is an extension of the base EasyFL library of functions. It is crucial, that all node in the network share the ledger ID with exactly the same hash of the library. 

We will go through many of the functions, defined in the ledger ID, because they define behavior of token holders in the ledger. One may think about ledger definitions as core set of smart contracts, that defines core concepts on the ledger.

## Embedded functions for the evaluation context

We already introduced validation process of a transaction $T$: all formulas are evaluated in each of consumed and produced UTXOs. Transaction valid if all evaluations return `true`. In each such evaluation the transaction context $T^{ctx}$ and path of the currently evaluated expression is provided in the context.

The path always have the form $(0, 2, i, j)$ for the constraints $j$ of the **produced** UTXO $i$.
The path always have the form $(1, 0, i, j)$ for the constraints $j$ of the **consumed** UTXO $i$.

Proxima ledger definitions embeds two special embedded functions, which enables access to the evaluation context and transaction context from the EasyFL formulas:

### Evaluation context: `at`
Function `at` (without parameters) returns the context path in the $T^{ctx}$ of to the UTXO being evaluated. Each formula "known" where it is located: in which UTXO, and its index in the UTXO. 

By the path returned by function `at`, formula can determine if it is evaluated in the consumed context, or in the produced one. There are special helper functions for this in the Proxima ledger  definitions:  
```go
func pathToConsumedOutputs : 0x0100

func pathToProducedOutputs : 0x0002

func isPathToConsumedOutput : hasPrefix($0, pathToConsumedOutputs)

func isPathToProducedOutput : hasPrefix($0, pathToProducedOutputs)

func selfIsConsumedOutput : isPathToConsumedOutput(at)

func selfIsProducedOutput : isPathToProducedOutput(at)
```

`hasPrefix` is standard EasyFL predicate to check is argument has the particular prefix.
Predicates `selfIsConsumedOutput` and `selfIsProducedOutput` determines the constraint being evaluated, if it is evaluated as a consumed, or as a produced output. It is common, that UTXO constraint scripts check different things in different evaluation contexts. 

### Access to the transaction context: `atPath`

Embedded function `atPath` with the single argument, interpreted as a path in the transaction context $T^{ctx}$, returns bytes of the corresponding element or panics if path is incorrect.

Each script formula can retrieve its own bytecode with the function `self`, defined the following way:  
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

