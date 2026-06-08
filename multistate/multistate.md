# Multi-state database
The _transaction DAG_, also known as _the tangle_, is a DAG with UTXO transactions as vertices, while the edges of the DAG are either consumption (spending) relations of UTXOs in other transactions, or endorsements.

Each UTXO transaction in the tangle — a vertex — has a deterministic past cone, a sub-DAG. In a consistent tangle each past cone does not contain conflicts (also known as double-spends), and therefore constitutes a consistent ledger of transactions and the corresponding ledger state. The ledger state defines a set of UTXO assets: a collection of key/value pairs (output ID, UTXO).

In other words, each UTXO transaction represents a consistent ledger state. If two transactions are conflicting, so are their two ledger states.

In Proxima, the node tracks many ledger states at once and checks them for consistency. However, it **persists** in the database only the ledger states that correspond to special transactions called _branch transactions_. Each branch transaction validated by the node has a corresponding persistent ledger state in the database.

So, by design, a Proxima node must be able to handle multiple ledger states in the same database efficiently. This is the job of the **multi-state database**.

## Trie. Merkle tree
A ledger state is stored as a **Merkle trie** — a key/value map whose entire contents are summarized by a single cryptographic **root commitment** (a Merkle root). Proxima uses the [`unitrie`](https://github.com/lunfardo314/unitrie) library for this.

The trie is **immutable and persistent** in the functional sense: updating it does not overwrite the old state but produces a new root that shares all unchanged nodes with the previous one. This is what lets many branch states coexist in one database cheaply — two states that differ only slightly share almost all of their trie nodes (overlapping Merkle trees). Each distinct ledger state is fully identified by its root commitment, and the root also enables compact Merkle proofs about the state.

## State
A ledger state is referenced by its trie **root** (`common.VCommitment`). The node opens a *read-only* view of a state at a given root (a `Readable`), or an *updatable* view (an `Updatable`); applying a branch's mutations to an updatable state yields a new root.

### Ledger state
The core content is the set of unspent outputs: the (output ID → UTXO) pairs. Consuming a transaction removes its inputs and adds its produced outputs, transforming one ledger state into the next.

### Ledger index
Besides the UTXOs themselves, the trie also stores **index entries** that let the node answer lookups without scanning the whole state — for example "all UTXOs controlled by this account" or "the current UTXO of this chain ID". These index entries are derived from the outputs' index-value tuples (see [Base data elements](txdocs/base.md)). Because the index is specific to a particular ledger state, it is kept **inside** the trie, so it is committed to by the root and shared between overlapping states just like the UTXOs.

## Key-value store. Partitions
All trie keys are namespaced by a 1-byte **partition** prefix:

| Partition | Label | Contents |
|-----------|-------|----------|
| Ledger state | `UTXO` | UTXOs (33-byte output IDs) **and** past transaction IDs (32-byte). They share one partition and are told apart by key length — an optimization, since a transaction ID and its output IDs share the same 32-byte prefix. |
| Controllers | `ACCN` | Index by controller / account: which outputs a given address or chain controls. |
| Chain ID | `CHID` | Index by chain ID → the single current chain output for that chain. |

Underneath the trie, the persistent key-value store is **BadgerDB**.

## Root and branch records
For every branch transaction's committed state, the database stores a **root record** keyed by the branch (transaction) ID. A `RootRecord` is small:

* `Root` — the trie root commitment of that branch's ledger state;
* `SequencerID` — the chain ID of the sequencer that produced the branch.

For convenience the node also assembles `BranchData`, which extends the root record with the branch's stem and sequencer outputs and a set of aggregates projected from the stem output — total supply, ledger coverage and coverage delta, frozen coverage and slot inflation. These records let the node enumerate the branches it knows, locate the latest reliable branch, and pick baselines for attaching new transactions.

## Snapshots
A **snapshot** is a portable file that captures the complete ledger state at a chosen branch, together with the root record and the upgrade libraries needed to interpret it. Snapshots are used to:

* recover a node when its database is missing or corrupted;
* compact the database periodically by restoring from a recent snapshot;
* bootstrap a new node without replaying the tangle from genesis;
* distribute the genesis state (genesis is itself a snapshot).

A snapshot is a binary file in the `unitrie` key/value-stream format and is named after its branch ID in dashed form. (The exact on-disk layout is documented with the node's `ledger/multistate` package.)
