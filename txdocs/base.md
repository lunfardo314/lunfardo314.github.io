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

This serialized ledger time is called a _timestamp_. Each transaction $T$ contains a timestamp as $T_5$. Bit 0 of the last byte in the timestamp is reserved and must be 0. This bit is used in the transaction ID prefix (see below).

## Transaction ID
Each transaction is uniquely identified by a 32-byte ID, deterministically formed from the transaction’s data. By design, transaction IDs never repeat. A transaction ID cryptographically commits to the transaction and also encodes its timestamp, the number of UTXOs it produces, and a flag indicating whether it is a sequencer transaction.

|Byte indices | Description                                                                                                                                   |
| -------- |-----------------------------------------------------------------------------------------------------------------------------------------------|
|0-4| *transaction ID prefix*, 5 bytes (see below)                                                                                                  |
|6| index of the last UTXO produced by the transaction.<br>1 byte $\leftarrow$ maximum index = 255 $\leftarrow$ max 256 outputs per transaction |
|5-31| The last 26 bytes of of $blake2b(essence(T))$                                                        |

The _transaction essence_ is a concatenation of all elements of the raw transaction, excluding the signature:
$$
essence(T) = \bigoplus_{i=0, i\ne 3}^{10} bytes(T_i)
$$
where $\bigoplus$ denotes concatenation.

### Transaction ID prefix
The 5-byte _transaction ID prefix_ includes:

|Byte indice(s) | Description|
| -------- | -------- |
|0-3|*slot* as big-endian `uint32`|
|4|compound value of *tick* and *sequencer transaction flag*:<ul><li>bits [0:6] is *ticks* of the transaction</li><li>bit 7 is *sequencer transaction flag*</li></ul> |

Thus, the transaction ID prefix is the timestamp with the sequencer flag set in bit 7 of the last byte.

The genesis transaction is a sequencer transaction; hence, its transaction ID prefix is `0x0000000001`.


### Human-Readable Transaction ID Prefix

The human-readable form is `[<slot>|<ticks><seq-flag>]`, where.
* `<slot>` decimal slot value
* `<tick>` decimal tick value (max 127)
* `<seq-flag>`:
    * empty, if not a sequencer transaction
    * `sq` for sequencer transactions with $tick\ne 0$
    * `br` for sequencer transactions with $tick = 0$. i.e. *branch transaction*

The genesis transaction is a branch transaction producing two UTXOs. Its transaction ID is:

* raw (hex): `0000000001010000000000000000000000000000000000000000000000000000`
* human-readable: `[0|0br]010000000000000000000000000000000000000000000000000000`

> Note: the genesis transaction does not technically exist. Instead, there are two genesis outputs: the **genesis sequencer output** and the **genesis stem output**.

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
|32| Index of the output within the transaction (must match the last UTXO index in the transaction ID prefix) |

The human-readable form appends [n] to the transaction ID, where n is the output index. For example:
- `0000000001010000000000000000000000000000000000000000000000000000` and `[0|0br]010000000000000000000000000000000000000000000000000000[0]` (human-readable) is ID of the genesis sequencer output
-  `0000000001010000000000000000000000000000000000000000000000000001` and `[0|0br]010000000000000000000000000000000000000000000000000000[1]` is ID of the genesis stem output

## Integers and token amounts
All amounts and integers are encoded as byte arrays of up to 8 bytes, interpreted as big-endian `uint64`.

Terminal data in the transaction’s tuple tree always includes a size prefix. This enables space optimization: leading zeros are trimmed. Any array shorter than 8 bytes is left-padded with zeros and interpreted as big-endian `uint64`.

Examples:
* empty byte array is interpreted as `uint64(0)`
* 2-byte array `[]byte{0x01, 0x02}` is interpreted as `uint64(18)`

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
fmt.Printf("source: %s\n", timelock.Source())
fmt.Printf("human-readable: %s\n", timelock.String())
fmt.Printf("bytecode: %s\n", hex.EncodeToString(timelock.Bytes())
```
Output:
```yaml
source: timelock(u32/1000)
human-readable: timelock(1000)
bytecode: 45bf84000003e8
```

### Defining UTXO
In Go, a UTXO wraps a tuple:

```go
type Output struct {
   *tuples.Tuple
}
```
Example: creating a new UTXO:
```go
utxo := ledger.NewOutput(func(o *ledger.OutputBuilder) {
	o.WithAmount(1337)
	o.WithLock(ledger.AddressED25519Random())
	o.MustPushConstraint(tl.Bytes())
})
println(utxo.String())
```
Output:
```yaml
0: amount(1337)
1: a(0x31608fbd1cc5c98325ea0daac88ed5f752b66603344dc3b071992b5515c0921d)
2: timelock(1000)
```

### Building a transaction
The `txbuilder.TransactionBuilder` type is used to incrementally construct a transaction: consuming and producing UTXOs, setting fields, signing with a private key, and finally producing a byte blob for persistence.
