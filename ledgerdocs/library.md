# Ledger definition library

The Proxima ledger definition library is contained in the ledger definition file, also known as the _ledger ID_. This file is typically written in YAML and is used to initialize the genesis ledger state for the first node in the network.

The ledger definition library includes:

* A list of embedded (hardcoded) functions
* A list of functions defined as [EasyFL](txdocs/easyfl.md) formulas

As an example, we provide the complete [proxima.genesis.id](ledgerdocs/genesis.id.md) file, which represents a full ledger definition library.

The Proxima ledger definition extends the base EasyFL function library. It is crucial that all nodes in the network share the exact same version of the ledger definitions—identified by the hash of the library.

We classify all functions into two broad categories: general-purpose functions and ledger validity constraint functions.

**General-purpose functions** include all embedded functions and other utilities for manipulating byte arrays or accessing specific parts of a transaction.

**Ledger validity constraints** are functions used as constraints within UTXOs. These include various types of locks (e.g., signature locks, chain locks, time locks), as well as mechanisms for chain building, sequencer behavior, inflation, delegation, and more. You can think of these constraints as a core set of smart contracts that define fundamental concepts on the ledger.

In the following sections, we will walk through examples of functions defined in the Proxima ledger. We hope the rest are either self-explanatory or will be covered in separate documentation.

