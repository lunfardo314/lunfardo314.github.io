# Ledger definition library

**The ledger definition library is contained in the ledger state itself**, not in the node's binary and not in a configuration file. It is written in JSON and held in the state's upgrade partition, keyed by the slot from which that version applies. A node **always loads the library from the ledger state** when it starts, rather than from the version its build was compiled against.

One qualification: not everything is data. A minority of the library's functions are **embedded** — the library names them and fixes their codes and arities, but their implementation is Go code inside the node binary, bound by name when the library is loaded. Their behaviour therefore travels with the software, not with the state, and the library hash does not move when that code changes. Changing an embedded function quietly, instead of through an upgrade every node adopts, makes nodes disagree about what is valid while still believing they run the same ledger — a split in the consensus rather than a rejected transaction. Everything defined as an EasyFL formula is data in the state and carries no such risk.

The genesis state is created once, from the code in this repository. The library written into it carries, as ordinary ledger constants, the **genesis timestamp** and the **public key of the creator** — so the identity of a particular ledger, and the moment it began, are part of its rules rather than metadata beside them. The genesis time and a description are also recorded in the *ledger identity* at the root of the state trie.

Afterwards the library changes only through the **ledger upgrade mechanism**, which is part of the node code. An upgrade defines a new version of the library to take effect from a given slot, and that version is stored in the state next to the ones before it. Every such change is a **hardfork**: the library hash changes with it, and a node that does not carry the upgrade cannot follow the ledger past that slot.

The ledger definition library includes:

* A list of embedded (hardcoded) functions
* A list of functions defined as [EasyFL](txdocs/easyfl.md) formulas

The full ledger definitions file is generated when the genesis ledger state is created; its current hash can be inspected on a running node (for example with `proxi db info`).

The Proxima ledger definition extends the base EasyFL function library. It is crucial that all nodes in the network share the exact same version of the ledger definitions—identified by the hash of the library.

We classify all functions into two broad categories: general-purpose functions and ledger validity constraint functions.

**General-purpose functions** include all embedded functions and other utilities for manipulating byte arrays or accessing specific parts of a transaction.

**Ledger validity constraints** are functions used as constraints within UTXOs. These include various types of locks (e.g., signature locks, chain locks, time locks), as well as mechanisms for chain building, sequencer behavior, inflation, delegation, and more. You can think of these functions as a core set of covenants that define fundamental concepts on the ledger.

In the following sections, we will walk through examples of functions defined in the Proxima ledger. We hope the rest are either self-explanatory or will be covered in separate documentation.

