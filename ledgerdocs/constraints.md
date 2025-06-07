# UTXO constraints and programmability

## Trust-less evidence of transaction data in UTXO 
In order to demonstrate power of UTXO programming with EasyFL constraint scripts, we will describe two examples. Both are implemented as standard functions in the ledger definition library, however they also can be put entirely inline, into the UTXO with relatively small overhead.

The problem of trust-less data in the UTXO is that in the ledger state where UTXO resides we do not have the transaction anymore. The transaction exists somewhere, because UTXO commits to the transaction with its *output ID*. However, the transaction is one "data availability trust assumption away": we know the transaction exists, but we cannot check its data without retrieving from somewhere. 

### Total produced amount
An example of the transaction level data we may want to use in the UTXO script, would be _total produced amount_, always available and enforced in the $T_6 = T^{ctx}_{0,6}$ of each transaction. Standard ledger function `txTotalProducedAmount` retrieves it in the context of the producing transaction: 
```
func txTotalProducedAmount : uint8Bytes(atPath(pathToTotalProducedAmount))
```

But when consumed, UTXO has no access to the transaction which produced it. If we just replicate the total produced amount value in the UTXO data, who could check if its is genuine.

The UTXO scripting comes to rescue. There's special validity constraint function `total` defined in the library:
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

So, if somebody retrieves UTXO from the ledger state and finds constraint for example `total(1000000)` in it, she is absolutely confident that the total amount of produced outputs in the transaction was equal to exactly `1000000`, because if not, transaction would be invalid.    

### Trust-less message sender identity  
Another example of trust-less transaction data evidence on UTXO is UTXO messages with known sender. We want to include into the UTXO arbitrary data (message) together with secure evidence who produced the message, at least commitment to public key of the producer.

Note, that simply include message is not enough, because in general UTXO does not contain identity of the producer.

The natural use case for such a feature would be "sending" secure requests to L2 entities _on ledger_. Receiver of such a message can be a custodian of the tokens on behalf of the owner of the private key (who also owns account on L1). The custodian may take such messages embedded in UTXOs as commands to be performed on the assets owned by the same private key on L2: by retrieving UTXO the command will be secure, i.e. coming from the owner of the account.

(off-topic, in Proxima, _sequencers_ are an example of such L2 entities, that is how fund withdrawal from the sequnecers works)

Special constraint `msgED25519` function implemented in ledger definition library provides such functionality. 

```
// Contains arbitrary message and enforces valid sender (originator) as part of the message.
// Once output is in the state, it is guaranteed to have the real sender
// $0 - blake2b hash of the signature's public key (not an address, just data)
// $1 - arbitrary data
func msgED25519: or(
    // always valid on consumed output
	selfIsConsumedOutput,
    // valid on produced output only if public key of the signature of the transaction equal to $0
	and(
		selfIsProducedOutput,
		equal(
       		$0, 
			blake2b(publicKeyED25519(txSignature))
		),
        $1 // to enforce mandatory second parameter. It is evaluated
	)
)
```

Constraint script, say `msgED25519(0x1ce4df1ded3a8cebd503adb255bda0c949121bece9639363e940fbf1727472d6, 0x0102ff)`, when added to the produced output, means secure message `0x0102ff` from account `addressED25519(0x1ce4df1ded3a8cebd503adb255bda0c949121bece9639363e940fbf1727472d6)`. 

## Mandatory UTXO constraints
During transaction validation, it is enforced that in each UTXO constraint script at index `0` must be `amount` script and at the index `1` must be one of known lock scripts.

### Amount

### Locks

### AddressED25519 lock

### Stem lock

## Chain constraint

### Chain lock

## Sequencer constraint

## Inflation

