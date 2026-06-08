# Ledger definition library

The Proxima ledger definition library is contained in a single file, the _ledger definitions_. This file is written in JSON and is used to initialize the genesis ledger state for the first node in the network.

The ledger definition library includes:

* A list of embedded (hardcoded) functions
* A list of functions defined as [EasyFL](txdocs/easyfl.md) formulas

The full ledger definitions file is generated when the genesis ledger state is created; its current hash can be inspected on a running node (for example with `proxi db info`).

The Proxima ledger definition extends the base EasyFL function library. It is crucial that all nodes in the network share the exact same version of the ledger definitions—identified by the hash of the library.

We classify all functions into two broad categories: general-purpose functions and ledger validity constraint functions.

**General-purpose functions** include all embedded functions and other utilities for manipulating byte arrays or accessing specific parts of a transaction.

**Ledger validity constraints** are functions used as constraints within UTXOs. These include various types of locks (e.g., signature locks, chain locks, time locks), as well as mechanisms for chain building, sequencer behavior, inflation, delegation, and more. You can think of these constraints as a core set of smart contracts that define fundamental concepts on the ledger.

In the following sections, we will walk through examples of functions defined in the Proxima ledger. We hope the rest are either self-explanatory or will be covered in separate documentation.

