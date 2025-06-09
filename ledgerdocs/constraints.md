# UTXO constraints and ledger programmability
Proxima UTXO transactions are programmable. By adding validity constraints to UTXOs, a user can define the conditions under which a transaction is valid, as well as the specific unlock conditions for UTXOs. This allows users to predefine the future behavior of an asset — effectively programming it.

UTXO transactions can only update (consume) a finite, bounded, and deterministic fragment of an otherwise unbounded ledger state. This restriction makes the state-update machine non-Turing complete. Consequently, the EasyFL language intentionally excludes loops and recursion.

The programmability of the UTXO ledger in Proxima can be described as non-Turing complete, parallel, and asynchronous smart contracts, akin to finite state machines or even cellular automata. 

However, we avoid the term "smart contract" in this context, as it typically refers to Ethereum-style SCs, which assume and can update (consume) unbounded infinite state, they are synchronous (atomically-composable) and therefore they need Turing-complete engine (a VM) with loops or recursion and unbounded data structures, to be able to perform their logic.

Instead, UTXO programmability can be seen as **emergent behavior** on the ledger, driven by multiple asynchronous and independent agents. In aggregate, these behaviors can approximate arbitrary complexity, rendering the entire system **quasi-Turing complete**.

## Trust-less evidence of transaction data in UTXO 
To demonstrate the expressive power of UTXO scripting with EasyFL, we describe two examples. Both are implemented as standard functions in the ledger definition library but can also be included inline within a UTXO with minimal overhead.

A challenge in UTXO-based systems is that once an output resides in the ledger, the transaction that created it is no longer directly available. The UTXO commits to the transaction via its _output ID_, but verifying transaction-level data requires retrieving the transaction from external storage—introducing a trust assumption.

### Total produced amount
One commonly needed transaction-level field is the total produced amount, always available in field $T_6 = T^{ctx}_{0,6}$ of each transaction. The standard function `txTotalProducedAmount` retrieves it: 
```
func txTotalProducedAmount : uint8Bytes(atPath(pathToTotalProducedAmount))
```
Because a consumed UTXO cannot access its producing transaction directly, merely duplicating the total produced amount in the UTXO would be insecure — anyone could forge it.

Instead, we use the constraint function `total`:
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

If a UTXO contains `total(1000000)`, the ledger guarantees that the producing transaction's total output was exactly 1,000,000 — otherwise, the transaction would be invalid.

### Trust-less message sender identity  
Another example is UTXO messages with verifiable sender identity. We may wish to include arbitrary data in a UTXO and associate it securely with its producer's public key. Simply including the message isn’t sufficient—UTXOs don't inherently include the sender’s identity.

A practical use case is sending authenticated requests to L2 entities on-ledger. For example, an L2 custodian might act on behalf of an L1 account owner, and a UTXO message with verifiable sender identity serves as a secure command.

> _(Off-topic: In Proxima, sequencers are one such L2 entity, used during fund withdrawals.)_

The `msgED25519` constraint enables this functionality:
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
A UTXO with `msgED25519(0x1ce4..., 0x0102ff)` proves that the message `0x0102ff` was issued by the account whose address is `addressED25519(0x1ce4...)`.

## Mandatory UTXO constraints
Constraints at indices 0 and 1 are mandatory:
* Index 0 must hold the amount constraint.
* Index 1 must hold a valid **lock script**.


### Amount
The amount constraint is a placeholder that enforces the value and its position:
```
// $0 - amount up to 8 bytes big-endian. Will be expanded to 8 bytes by padding
func amount: 
   require(
       // constraint must be at index 0 and arg0 must no more than 8 byte-long 
       and(equal(selfBlockIndex,0), lessOrEqualThan(len($0), u64/8)), 
       !!!amount_constraint_must_be_at_index_0_and_len_arg0<=8
   )
```
The value can be 0. Minimum deposit requirements are enforced by the lock script.

### Locks
Locks define the minimum conditions for consuming an output. The current version includes:

* `addressED25519` (alias `a`), signature lock (siglock) (see [AddressED25519 lock](#addressed25519-lock)))
* `chainLock` -  requires a specific chain output to be consumed in the same transaction. Will be introduced together with the [chain constraint](#chain-constraint).
* `stemLock` -  used for branch transactions; unlockable without a signature.  
* `delegationLock` - allows two different keys to unlock it, depending on timing. 

### Unlock parameters
Constraints can’t dynamically inspect transactions. Instead, they must be statically linked to known paths. For example, if a constraint is at path $(1,0,i,j)$, then its unlock parameters at $(0,1,i,j)$ may contain static references to the data in the consuming transaction, required by the constraint.

### AddressED25519 lock
This lock ensures that an output can only be consumed by a transaction signed with a specific ED25519 key:

```
// $0 self unlock parameters
func unlockedByReference: and(
    equal(len($0), u64/1),                     // prevent panic in compound locks
	lessThan($0, selfOutputIndex),             // unlock parameter must point to another input with 
                                               // strictly smaller index. This prevents reference cycles	
	equal(self, consumedLockByInputIndex($0))  // the referenced constraint bytes must be equal to the self constraint bytes
)

// $0 - ED25519 address, 32 byte blake2b hash of the public key
// Unlock data is 1 byte with reference index to the previous input or signature unlock with 0xff
func addressED25519: and(
	require(equal(selfBlockIndex,1), !!!locks_must_be_at_block_1), 
	enforceMinimumStorageDeposit,
	or(
		and(
			selfIsProducedOutput, 
			equal(len($0), u64/32) 
		),
		and(
			selfIsConsumedOutput, 
			or(
					// if it is unlocked with reference, the signature is not checked
				unlockedByReference(selfUnlockParameters),
					// checked if tx signature corresponds to the address
                equal($0, blake2b(publicKeyED25519(txSignature)))
			)
		)
	)
)

// short form of lock a(<hex bytes>)
// $0 - ED25519 address, 32 byte blake2b hash of the public key
func a : addressED25519($0)
```
This structure enables efficient unlocking: if a previous input has the same lock, later inputs can reference it.
Note, that the siglock script assumes valid signature of the transaction.

## Chain constraint
The `chain` constraint is central to Proxima. It enables **mutable state**, NFTs, sequencing, delegation and other functions. Unlike standard UTXOs, chain-constrained outputs represent persistent, trackable assets.

Key properties:
* Each chain constraint encodes the _chain ID_ and **predecessor** info. 
* Chain origins are created with a zero chain ID, which is later replaced by the hash of the origin's output ID
* Each chain output must have exactly one **successor**, ensuring single-tip chains

This enforces a single UTXO per chain ID on the ledger—essentially a native NFT.

The `chain` constraint enforces a non-forkable chain of transactions on the ledger and always a single tip (UTXO) of that chain on the ledger state.

<p style="text-align:center;"><img src="../static/img/chain_succ_pred.png"></p>

The source of the chain constraint function in EasyFL we provide [here](ledgerdocs/chain.md):

### Chain lock
The `chainLock` (alias `c`) is an advanced locking mechanism. It allows tokens to be locked to a chain instead of a static address. Whoever controls the chain (via the appropriate private key) can unlock the tokens—even if the controlling key changes.

Chain locks are fundamental for:

* Tag-along mechanism
* Token custody with rotating keys
* Secure interaction with the sequencer chain (e.g. token withdrawal) 
* Trust-less interchain messaging

EasyFL source of the `chainLock` is provided [here](ledgerdocs/chain_lock.md).

## Sequencer constraint
The _sequencer constraint_ `sequencer`, adds additional conditions to the `chain` constraint. Sequencer chain is a special kind of chain. Its purpose is to support cooperative consensus among sequencers, by enabling branches, baseline and other.  

## Inflation
The inflation constraint ensures deterministic inflation based on:
* Ledger time (for general chains)
* Verifiable randomness (for branches)

At transaction level, the following invariant is enforced:
```
Total Consumed Amount + Inflation == Total Produced Amount
```
