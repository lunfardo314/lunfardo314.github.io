# UTXO constraints

## Trust-less evidence of transaction data in UTXO 
In order to demonstrate power of UTXO programming with EasyFL constraint scripts, we will describe two examples. Both are implemented as standard functions in the ledger definition library, however they also can be put entirely inline, into the UTXO with relatively small overhead.

The problem of trust-less data in the UTXO is that in the ledger state where UTXO resides we do not have the transaction anymore. The transaction exists somewhere, because UTXO commits to the transaction with its *output ID*. However, the transaction is one "data availability trust assumption away": we know the transaction exists, but we cannot check its data without retrieving from somewhere. 

### Total produced amount
An example of the transaction level data we may want to use in the UTXO script, would be _total produced amount_, always available and enforced in the $T_6 = T^{ctx}_{0,6}$ of each transaction. Standard ledger function `txTotalProducedAmount` retrieves it in the context of the producing transaction: 
```
func txTotalProducedAmount : uint8Bytes(atPath(pathToTotalProducedAmount))
```

But when consumed, UTXO has no access to the transaction which produced it. If we just replicate the total produced amount value in the UTXO data, who could check if its is genuine.

The UTXO scripting comes to rescue. There's special validity constraint defined in the library:
```
// $0 - total amount uint64 big-endian
// $0 must be equal to the total amount value in the transaction
func total: require(
	or(
		selfIsConsumedOutput,
        equalUint($0, txTotalProducedAmount)
	),
    !!!total_amount_constraint_failed
)
```
This script fails in the produced UTXO, if argument of it is not equal to the total amount value, specified in the $T_6$ for the transaction. 

So, if somebody retrieves UTXO from the ledger state and finds constraint for example `total(1000000)` in it, she is absolutely confident that the total amount of produced outputs in the transaction was equal to exactly `1000000`, because if not, transaction would not be valid.    

## Mandatory UTXO constraints

## Amount

## Locks

### AddressED25519 lock

### Stem lock

## Chain constraint

### Chain lock

## Sequencer constraint

## Inflation

