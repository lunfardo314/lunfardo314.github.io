# Proxima transaction

## Tuple trees
When composing a transaction, we aim to operate with the most generic data structures possible:
* a *byte array* (or *byte string*). *Byte array* may be empty, i.e. of zero length. Byte array can have any length (not exceeding practical limits set by the protocol);
* a *tuple* $(e_0, \dots e_{n-1})$, where each $e_i$ is either a *byte array*, or a *tuple* again.

Nested *tuples* may represent a finite hierarchical data structure, a *tree*, which has byte arrays as terminal elements and tuples as interim vertices.

Proxima transactions are represented as such a tree of tuples. Let's say $T$ is such a tree. Every element in the tree has unique *path* $(i_0, \dots i_{m-1})$ which uniquely specifies place of that element in the whole structure. Empty path $()$ points to the tip of the tree, the top tuple itself. Every part of the transaction has its *path*, a unique "address" in the transaction.

For a tuple $T$, we will denote $T_i$ as it's i-th element. In the hierachical case, element with the path $(i_0, \dots i_{m-1})$ we will denote:
$$
T_{i_0,\dots i_{m-1}} = ((T_{i_0})_{i_1}\dots)_{i_{m-1}}
$$

By $len(T)$ we will denote number of elements in the tuple:
$$
T = (T_0, \dots T_{len(T)-1})
$$
Similarly, $len(b)$ is number if bytes in the byte array $b$.

## Serialization

Let's say $bytes(e)$ is a function which gives a serialized binary representation of the element $e$ as a byte array. The serialization rules are simplest possible:

Serialized form of the byte array $b$ is itself: $bytes(b)=b$

Serialized form of the tuple $T=(e_0, \dots e_{n-1})$ is $bytes(T) = header(n, l)||e'_0||\dots||e'_{n-1}$
where
* $||$ is concatenation
* $header(n,l)$ is 2 bytes which contain information about number of elements in the tuple $len(T)$ and $l$ is number of of bytes reserved for the size prefix of elements. Parameter $l$ is selected the way, that size of any element  would fit $l$ bytes (e.g. $l=1$ for a tuple with elements are no longer than  255 bytes, or, otherwise, $l=2$ if elements are no longer than $2^{16}-1$);
* $e'_{i} = sz^l_i||bytes(e_i)$, where $sz^l_i$ is $len(bytes(e_i))$ in the form of $l$ bytes (big-endian). In other words, $e'_{i}$ is $bytes(e_i)$ prefixed with few bytes of size information.

Tuple serialization rule is applied recursively down to the terminal byte arrays. The serialized transaction is a nested blob of bytes.

Note, that in the serialized form, the element of the tuple tree does not contain information if it is terminal or not: a byte array may or may not be interpreted as a serialized tuple. It means that serialization assumes only **finite** tuple trees, i.e. the ones which has known structure in advance and does not need recursion nor loops to traverse it.

This is intentional: the user of a serialized tuple tree must know if a certain path $(i_0, \dots i_{m-1})$ is a valid path or not. Attempt to access element with invalid path will lead to exception with immediate invalidation of the entire data structure. This trait enables *lazy deserialization*: we can delay deserialization of part of the tuple tree until we need them.

The data structures described above are low level binary bytes. Serilaization uses only very basic primitives, are platform-independent and have no dependencies on language-specific data types, nor on particular mechanisms such as Protobuf. Go implementation of it can be found in [github.com/lunfardo314/easyfl/tree/develop/tuples](https://github.com/lunfardo314/easyfl/tree/develop/tuples).

## Raw transaction

We distinguish two forms of the same Proxima transaction:
* *raw transaction*, aka *canonical transaction* or *transferable transaction*. It is the transaction which is persisted, exchanged between nodes and stored in the transaction store;
* *transaction context*. It is the *raw transaction*, extended with the fragment of the ledger state it updates. This form is transient and is only used for transaction validation, never persisted.

The *raw transaction* is a tuple, consisting of 11 data elements listed below. The following are the top level tuple elements of the raw transaction:

| Index | Name | Description |
| -------- | -------- | -------- |
|0|Inputs|Non-empty tuple of up to 256 output IDs of consumed UTXOs (not the consumed UTXOs themselves)|
| 1     | Unlock data     | a tuple of *unlock parameters*. 1-to-1 correspondence with the tuple of inputs|
|2|Produced outputs|Non-empty tuple of up to 256 produced outputs|
|3|Signature| a terminal. It is ED25519-signed *transaction ID* with the public key|
|4|Sequencer and stem output indices| a terminal. 2 bytes with sequencer-related indices of produced outputs|
|5|Timestamp|a terminal. 5 bytes of transaction [ledger time](#ledger-time) value|
|6|Total produced amount|a terminal. `uint64` sum of token amounts of the produced outputs as [zero-trimmed big-endian bytes](#integers-and-token-amounts)|
|7|Input commitment|a terminal. Hash of concatenated all consumed outputs (which are not part of the transaction): $hash(consumed(T))$ (see below)|
|8|Endorsements|a tuple of up to 8 transaction IDs|
|9|Explicit baseline|a terminal. Optional explicit transaction ID of a branch transaction|
|10|Local libraries|a tuple. Uninterpreted in the version 1, usually empty|

For example, for a transaction $T$, element $T_0$ will be a tuple of inputs while $T_6$ will be total produced amount. The *i-th* produced output is $T_{2,i}$

<p style="text-align:center;"><img src="txdocs/utxo-tx.png" width="500">
</p>

## Transaction context

Let'denote $utxo(id)$ is the UTXO loaded from the ledger state by its ID $id$.

Let's say $T=(T_0, \dots T_{10})$ is a raw transaction. Then
$$
consumed(T) = (utxo(T_{0,0}), utxo(T_{0,1}) \dots utxo(T_{0,len(T_0)-1}))
$$
is a tuple of consumed outputs of the transaction $T$.
By the *transaction context* $T^{ctx}$, we define the tuple:
$$
T^{ctx}=(T, (consumed(T)))
$$

**The transaction context $T^{ctx}$ contains all the information needed for the validation of the transaction $T$**. It is the transaction itself plus all consumed outputs, loaded from the ledger state, in one data structure with all elemebts uniforml accecssible with their paths.

It is always true that $T^{ctx}_0 = T$ and $T_{path}=T^{ctx}_{0,path}$
Path to the *i-th* input in the *transaction context* $T^{ctx}$ is $(0,0,i)$.

From the path of the input, we can easily find all other data elements corresponding to it:
* the ID of a consumed output is $T^{ctx}_{0,0,i}$
* the coresponding consumed output is $T^{ctx}_{1,0,i}$
* the coresponding unlock parameters is $T^{ctx}_{0,1,i}$

<p style="text-align:center;"><img src="txdocs/utxo-tx-context.png" width="500">
</p>

## Outputs (UTXOs). Validation scripts/formulas
The node is using globally trusted rules to determine if transaction $T$ is valid or not. Invalid transaction is rejected immediately.

Transaction validity rules are applied to the *transaction context* $T^{ctx}$.

Ultimately, globaly trusted transaction validity rules are hardcoded in the node's software. However, in order to increase flexibility, UTXO transaction models usually implement some kind of programmability, such as Bitcoin Script. In that case, node has interpreter of the scripts hardcoded in its software, and is only responsible for running it on scripts, provided with the transaction.

For example, instead of using hardcoded types of unlock conditions of UTXOs, producer of the transaction can compose a script and embed it into the UTXO. When run in the context of the consuming transaction, checks if transaction meets certain unlock criteria.

In Proxima, we adopt this approach too. Each UTXO is treated as tuple of terminal elements $(c_0, \dots c_{k-1})$ where each $c_i$ is interpreted as a bytecode of a script.

**In Proxima, each UTXO is a tuple of validation scripts**. All the data, such as amounts or addresses, are wrapped into those scripts. The scripts can access and define **logical relations between any data elements of the transaction context**: inside one UTXO, between several of them, between inputs and outputs and so on.

Further we will describe a simple functional language *EasyFL* which is used for the scripting. Here, the main point is that **each script is a closed formula, which represents a composition of function calls and data**, serialized as a bytecode.

The formula plays two roles: as a validation script and as serialization primitive for the UTXO data.

Formula is a **validity constraint imposed on the transaction data elements**, specified by their paths in the $T^{ctx}$. For a transaction $T$ to be valid, all of its scripts must return *true* when evaluated in the context of $T^{ctx}$. The producer of the transaction, by placing those scripts into a UTXO, impose validity constraints on the transaction: both on the producing, and, later, on the consuming one;

The **bytecode of the formula also serves as a data type descriptor** for the serialized form of data in UTXOs.

Some examples:

* the formula `amount(100)` not only invokes library-defined function `amount` with data `100` (which must return `true`), but also wraps `100` with the descriptor `amount`. Bytecode (compiled form) of such formula can be recognized as `amount` and the wrapped data (`100` in this case) can be parsed-out by other scripts/formulas and by the node. Otherwise, the function `amount`, when evaluated, checks if the provided amount meets the minimum requirement for the particular UTXO;
* the formula  `addressED25519(0x370563b1f08fcc06fa250c59034acfd4ab5a29b60640f751d644e9c3b84004d0)` invokes library-defined function `addressED25519` which verifies if the signature at $T_3$ is a valid signature of the transaction ID and if the hash of the public key is equal to the data `0x370563b1f08fcc06fa250c59034acfd4ab5a29b60640f751d644e9c3b84004d0` provided as the parameter of the call. It is a siglock script.
  From the other side, another script or user, can parse the bytecode and check if the script is indeed the `addressED215519` function and, say, check if the parameter is the public key it expects.

All participants share a globally trusted **library of validation function definitions**. The most primitive of those functions are hardcoded (embedded), akin **opcodes** in other UTXO models. Majority of it is defined as open *EasyFL* formulas with parameters.

Due to the fundamental reasons, we assume definitions of those functions composed in validation script formulas do not use loops nor recursion, i.e. do not form a Turing-complete set. 
