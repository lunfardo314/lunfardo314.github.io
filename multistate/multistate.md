# Multi-state database
The _transaction DAG_ also known as _the tangle_, is a DAG with UTXO transactions and vertices, while edges of the DAG are either consumption (spending) relations of UTXOs in other transactions, or endorsements.

Each UTXO transaction in the tangle - a vertex - has a deterministic past cone, a sub-DAG. In a consistent tangle each past cone does not contain conflicts (also known as double-spends), and therefore constitutes a consistent ledger of transactions and the corresponding ledger state. Ledger state defines list of UTXO assets and is a collection of key/value pairs (output ID, UTXO).

In other words, each UTXO transaction represents a consistent ledger state. If two transactions are conflicting, so are two ledger states.

In Proxima, we track all ledger states, for their consistency. However, we persist in the database only ledger states, that correspond to special transactions, called _branch transactions_. **Each branch transactions, which was validated by the node, have a corresponding persistent ledger state in the database.

So, by our requirements, the Proxima node must be able to handle multiple ledger states in the same  database efficiently.

## Trie. Merkle tree

## State

### Ledger state

### Ledger index

## Key-value store. Partitions

## Root and branch records

## Snapshots

