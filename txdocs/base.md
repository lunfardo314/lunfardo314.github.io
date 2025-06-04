# Base data elements

Transaction is defined and validated at the byte level. Number of high level concepts, such as byte arrays interpreted as particular data types, is very limited. Certain data elements, however, have special meaning, and we will describe it here.

## Ledger time (timestamp)
*Ledger time* is similar to the _block height_, however it intentionally uses semantics of the timescale. 
The ledger time consists of values *slot* and *tick*. Each slot has 128 ticks.
At genesis, *slot = 0* and *tick=0*

Maximum possible *slot* value is $2^{32}-1$. Maximum enforced *tick* value is 127.

In Proxima, each transaction and each UTXO has the number of ticks from genesis:
$$
numberOfTicksSinceGenesis = slots \times 128 + tick
$$

In Go the ledger time is defined the following way:
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

The *ledger time* is serialized as 5 bytes-long byte array:

|Byte indices | Description|
| -------- | -------- |
|0-3|big-endian form of slots|
|4|`tick` value multiplied by 2|

Serialized ledger time is called *timestamp*. Each transaction contains *timestamp*. The bit 0 of the last byte in the timestamp is reserved and must be 0. It is used in the transaction ID prefix (see below).

## Transaction ID
Each transaction is uniquely identified by the 32 byte-long ID, deterministically formed from the the data of the transaction. By the assumption, transaction ID never repeats. The transaction ID (cryptographically) commits to the transaction and also bears information about timestamp of the transaction, number of UTXOs it produced and a flag indicating if it is a sequencer transaction:

|Byte indices | Description                                                                                                                                     |
| -------- |-------------------------------------------------------------------------------------------------------------------------------------------------|
|0-4| *transaction ID prefix*, 5 bytes (see below)                                                                                                    |
|6| index of the last UTXO produced by the transaction.<br>1 byte -> maximum index is 255 -> maximum number of outputs produced by a transaction is 256 |
|5-31| The last 26 bytes of the transaction ID are the last 26 bytes of the  $blake2b(essence(T))$                                                     |

The *transactions essence* is a concatenation of all elements of the raw transaction, except signature:
$$
essence(T) = \bigoplus_{i=0, i\ne 3}^{10} bytes(T_i)
$$
where $\bigoplus$ is concatenation.

The 5 bytes of the *transaction ID prefix* are:

|Byte indice(s) | Description|
| -------- | -------- |
|0-3|*slot* of the transaction as big-endian `uint32`|
|4|a compound value of *tick* and *sequencer transaction flag*:<ul><li>bits [0:6] is *ticks* of the transaction</li><li>bit 7 is *sequencer transaction flag*</li></ul> |

So, the *transaction ID prefix* is the timestamp of the transaction with the sequencer flag set in the bit 7 of the last byte.

Genesis transaction is a sequencer transaction, therefore prefix of the genesis transaction ID is `0x0000000001`.

Human readable form of the transaction prefix takes form `[<slot>|<ticks><seq-flag>]`.
* `<slot>` is decimal value of the slot
* `<tick>` is the decimal value of tick (max 127)
* `<seq-flag>` is one of the followingL:
    * empty, when it is not a sequencer transaction
    * `sq` if it is a sequencer transaction and $tick\ne0$
    * `br` if it is a sequencer transaction and $tick= 0$. i.e. it is a *branch transaction* (see below and in the whitepaper).

The genesis transaction is a branch transaction. It has 2 produced UTXOs, therefore its transaction ID is the following constant:
* raw form (hex-encoded): `0000000001010000000000000000000000000000000000000000000000000000`
* human-readable form: `[0|0br]010000000000000000000000000000000000000000000000000000`

(In fact, genesis transaction does not exist. Instead, there are 2 genesis outputs (UTXOs): one is **genesis sequencer output**, another is **genesis stem output**).

Most of the code of transaction and output ID can be found in the `proxima/ledger/base` package.

Format of the transaction ID is designed for:
- early and fast enforcement of the *transaction pace constraints*, which enforce that timestamps of the inputs must always be strictly before the timestamp of the transaction by a fixed constant;
- early and fast recognition if transaction ID represents a sequencer transaction;
- making sorting by transaction IDs equivalent to the topological sorting of the transaction DAG. This makes canonical (temporal) order of outputs on the ledger state consistent with the causal order of transactions on the DAG.

## Output ID (UTXO ID)
Each output (UTXO) in the ledger state has its unique *output ID* as its key in the key/value database. The *output ID* is a 33 byte-long byte array, which has ID of the produced transaction as prefix and 1-byte of the UTXO index in the transaction as suffix:

|Byte indice(s) | Description|
| -------- | -------- |
|0-31|transaction ID of the transaction, which produced the output|
|32|index of the produced output in the producing transaction.<br>Enforced to be consistent with the last UTXO index specified in the transaction ID prefix|

In the human readable form of the ouput ID we attach suffix `[n]` to the transaction ID, where `n` is index of the output. For example, the two genesis outputs are:
- `0000000001010000000000000000000000000000000000000000000000000000` and `[0|0br]010000000000000000000000000000000000000000000000000000[0]` (human-readable) is ID of the genesis sequencer output
-  `0000000001010000000000000000000000000000000000000000000000000001` and `[0|0br]010000000000000000000000000000000000000000000000000000[1]` is ID of the genesis stem output

## Integers and token amounts
All amounts and integers in the transaction are byte arrays, with the size of up to 8 bytes. They are always interpreted as `uint64` integers serialized as **big-endian**.

Terminal data in the transaction tuple tree always bears size prefix. We use this property to optimize space occupied by the integer data: all leading zero bytes are usually trimmed. I.e. any byte array of size less than `8` is padded with the prefix of zero bytes up to 8 bytes and treated as *big-endian* `uint64`.
For example:
* empty byte array (zero size) is interpreted as `uint64(0)`
* 2-byte array `[]byte{0x01, 0x02}` is interpreted as `uint64(18)`

## Language bindings
Here we will only provide examples of how low level transaction concepts are mapped into high-level programming language concepts.

Transaction and its validation is self describing and platform-independent. In theory, it can be composed and validated at the byte level. However, it is practical and convenient to provide higher level language-specific bindings for low level concepts. The Go language bindings for Proxima ledger are implemented in `proxima/ledger` package.

The specific constraints implemented as functions in the shared ledger library, takes for of Go object, used in the composition of the UTXO in the Go program. Those objects implements interface:
```go
type Constraint interface {
  Name() string   // EasyFL function name in the ledger library
  Bytes() []byte  // bytecode, compiled from EasyFL source
  Source() string // EasyFL source
  String() string // Human-readable
}
```

For example, *time lock* constraint, thet prevents UTXO from being consumed until slot `1000` can be created as a Go object, the following way:
```go
timeLock := ledger.NewTimeLock(1000)
fmt.Printf("source: %s\n", timelock.Source())
fmt.Printf("human-readable: %s\n", timelock.String())
fmt.Printf("bytecode: %s\n", hex.EncodeToString(timelock.Bytes())
```
will print:
```
source: timelock(u32/1000)
human-readable: timelock(1000)
bytecode: 45bf84000003e8
```

In Go, the UTXO is defined as type which wraps the tuple:
```go
type Output struct {
   *tuples.Tuple
}
```

The example of how we can create new UTXO:
```go
utxo := ledger.NewOutput(func(o *ledger.OutputBuilder) {
	o.WithAmount(1337)
	o.WithLock(ledger.AddressED25519Random())
	o.MustPushConstraint(tl.Bytes())
})
println(utxo.String())
```
The code above will compose the UTXO and will print it as a list of constraint scripts:
```json
0: amount(1337)
1: a(0x31608fbd1cc5c98325ea0daac88ed5f752b66603344dc3b071992b5515c0921d)
2: timelock(1000)
```

The `txbuilder.TransactionBuilder` type defines transaction builder object. It is used for the incremental building of a transaction, by consuming and producing UTXOs, setting other values and parts of it, and finally signing transaction with the private key and making final form of it, a blob of bytes which can be persisted. 