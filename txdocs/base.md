# Base data elements

A transaction is defined and validated at the byte level. The number of high-level concepts—such as byte arrays interpreted as particular data types—is very limited. However, certain data elements have special meaning, which we describe here.

## Ledger time (timestamp)
_Ledger time_ is similar to _block height_, but it intentionally uses the semantics of a time scale.
Ledger time consists of two values: _slot_ and _tick_. Each slot contains 128 ticks.
At genesis: _slot = 0_ and _tick = 0_.

* Maximum possible *slot* value is $2^{32}-1$
* Maximum enforced *tick* value is 127.

In Proxima, each transaction and each UTXO has a number of ticks since genesis:
$$
numberOfTicksSinceGenesis = slots \times 128 + tick
$$



In Go, the ledger time is defined as:
```go
type (
   Slot       uint32
   Tick       uint8
   LedgerTime struct {
     Slot
     Tick
   }
)
```
Ledger time is serialized as a 5-byte array:

|Byte indices | Description|
| -------- | -------- |
|0-3|Big-endian encoding of the slot value|
|4|`tick` value multiplied by 2|

This serialized ledger time is called a _timestamp_. Each transaction $T$ contains a timestamp as $T_1$. Bit 0 of the last byte in the timestamp is reserved and must be 0. This bit is used in the transaction ID prefix (see below).

## Transaction ID
Each transaction is uniquely identified by a 32-byte ID, deterministically formed from the transaction’s data. By design, transaction IDs never repeat. A transaction ID cryptographically commits to the transaction and also encodes its timestamp, the number of UTXOs it produces, and a flag indicating whether it is a sequencer transaction.

|Byte indices | Description                                                                                                                                   |
| -------- |-----------------------------------------------------------------------------------------------------------------------------------------------|
|0-4| *transaction ID prefix*, 5 bytes (see below)                                                                                                  |
|5| index of the last UTXO produced by the transaction.<br>1 byte $\leftarrow$ maximum index = 255 $\leftarrow$ max 256 outputs per transaction |
|6-31| the last 26 bytes of $blake2b(essence(T))$                                                        |

The _transaction essence_ is a concatenation of all elements of the raw transaction, excluding the signature (element $T_3$):
$$
essence(T) = \bigoplus_{i=0, i\ne 3}^{10} bytes(T_i)
$$
where $\bigoplus$ denotes concatenation. (The raw transaction is an 11-element tuple, indices 0–10; see [Transaction](tx.md).)

### Transaction ID prefix
The 5-byte _transaction ID prefix_ includes:

|Byte indice(s) | Description|
| -------- | -------- |
|0-3|*slot* as big-endian `uint32`|
|4|compound value of *tick* and *sequencer transaction flag*:<ul><li>bits [1:7] hold the *tick* (so the byte value is *tick* × 2)</li><li>bit 0 is the *sequencer transaction flag*</li></ul> |

Thus, the transaction ID prefix is the timestamp with the sequencer flag set in bit 0 of the last byte.

The genesis transaction is a sequencer transaction; hence, its transaction ID prefix is `0x0000000001` (slot 0, tick 0, sequencer flag set).


### Human-readable transaction ID

The default human-readable form is the *dashed* form `[s]<slot>-<tick>-<hash>`:
* a leading `s` means the transaction is a **sequencer transaction** (including branch transactions); ordinary transactions have no prefix.
* `<slot>` — decimal slot value.
* `<tick>` — decimal tick value (0–127).
* `<hash>` — hex of the rest of the ID (the output-count byte followed by the 26-byte hash).

A sequencer transaction with `<tick> = 0` sits exactly on a slot boundary and is a **branch transaction**.

The genesis transaction is a branch transaction producing three UTXOs. Its transaction ID is:

* raw (hex): `0000000001020000000000000000000000000000000000000000000000000000`
* human-readable: `s0-0-020000000000000000000000000000000000000000000000000000`

> Note: the genesis transaction does not technically exist. Instead, there are three genesis outputs: the **genesis sequencer output**, the **genesis stem output**, and the **genesis controller (dust) output**.

Most of the transaction and output ID logic is in the `proxima/ledger/base` package.

The transaction ID format is optimized for:

* Early and fast enforcement of transaction pace constraints (input timestamps must precede transaction timestamp by a constant)
* Quick recognition of sequencer transactions
* Lexical sorting of transaction IDs matching the DAG’s topological sorting, making the canonical ledger state order consistent with causal ordering

## Output ID (UTXO ID)

Each output (UTXO) has a unique output ID, which is used as a key in the key-value database. The output ID is a 33-byte array:

|Byte indice(s) | Description                                                                                              |
| -------- |----------------------------------------------------------------------------------------------------------|
|0-31| Transaction ID that produced the output                                                                  |
|32| Index of the output within the transaction (must not exceed the last UTXO index in the transaction ID prefix) |

The human-readable form appends `#n` to the transaction ID, where `n` is the output index. For example:
- `0000000001020000000000000000000000000000000000000000000000000000` → `s0-0-020000000000000000000000000000000000000000000000000000#0` is the ID of the genesis sequencer output
- `0000000001020000000000000000000000000000000000000000000000000001` → `s0-0-020000000000000000000000000000000000000000000000000000#1` is the ID of the genesis stem output

## Chain ID

A **chain ID** identifies a chained account (a sequencer, a foundry, a delegation, …). It is a 24-byte array, derived for a new chain as the first 24 bytes of `blake2b` of the chain origin's output ID. The human-readable form prefixes the hex with `$/`, for example `$/6393b6781206a652070e78d1391bc467e9d9704e9aa59ec7`.

## Integers and token amounts
All amounts and integers are encoded as byte arrays of up to 8 bytes, interpreted as big-endian `uint64`.

Terminal data in the transaction’s tuple tree always includes a size prefix. This enables space optimization: leading zeros are trimmed. Any array shorter than 8 bytes is left-padded with zeros and interpreted as big-endian `uint64`.

Examples:
* empty byte array is interpreted as `uint64(0)`
* 2-byte array `[]byte{0x01, 0x02}` is interpreted as `uint64(258)`

## Language bindings
Here are examples of how low-level transaction concepts map to high-level programming language structures.

Transactions are self-describing and platform-independent; they can be composed and validated at the byte level. However, higher-level bindings are practical and convenient. Go language bindings for the Proxima ledger are in the `proxima/ledger` package.

### Constraints in Go

Constraints are implemented as Go objects and follow this interface:

```go
type Constraint interface {
  Name() string   // EasyFL function name in the ledger library
  Bytes() []byte  // bytecode, compiled from EasyFL source
  Source() string // EasyFL source
  String() string // Human-readable
}
```

Example: a _time lock_ constraint preventing UTXO consumption before slot 1000:
```go
timeLock := ledger.NewTimeLock(1000)
fmt.Printf("source: %s\n", timeLock.Source())
fmt.Printf("human-readable: %s\n", timeLock.String())
```
```
source: timelock(u32/1000)
human-readable: timelock(1000)
```

### Defining a UTXO
In Go, a UTXO wraps a tuple of constraints:

```go
type Output struct {
   *tuples.Tuple
}
```

The constraints occupy fixed positions in the tuple:

| Index | Content |
|-------|---------|
| 0 | amounts vector (token balance, inflation, frozen coverage) |
| 1 | index-values (controller / target / sender hashes used for state indexing) |
| 2 | lock (the unlock-policy bytecode) |
| 3 | chain constraint (only for chain outputs) |
| 4+ | per-lock extras |

So, for a simple signature-locked output, the holder's address goes into the index-values at position 1 and the (argument-less) signature lock sits at position 2 — any additional constraints (such as a time lock) follow at positions 3 and up.

### Building a transaction
The transaction builder is used to incrementally construct a transaction: consuming and producing UTXOs, setting fields, signing with a private key, and finally producing a byte blob for persistence.
