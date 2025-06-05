# Ledger definition library
Proxima ledger definitions are contained in the ledger definition file, also known as the _ledger ID_,
which is usually YAML. It is used to create a database with genesis ledger state for the first node in the network.

Here we provide the entire [proxima.genesis.id](ledgerdocs/genesis.id.md) file as an example of ledger definitions.

The ledger definitions becomes an immutable part of ledger state (we will skip hardfork/upgrade topic here). It is also a part of the snapshot.

The Proxima ledger ID is an extension of the base EasyFL library of functions. It is crucial, that all node in the network share the ledger ID with exactly the same hash of the library. 

We will go through many of the functions, defined in the ledger ID, because they define behavior of token holders in the ledger. One may think about ledger definitions as core set of smart contracts, that defines core concepts on the ledger.

## Embedded functions

## Ledger constants

## Transaction context functions

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

