# Ledger definition library
Proxima ledger definition library is contained in the ledger definition file, also known as the _ledger ID_, which is usually YAML. It is used to create a database with genesis ledger state for the first node in the network.

The ledger definition library contains a list of embedded (hardcoded) functions as well as a list of functions, defined as EasyFL formulas. We introduced EasyFL [here](txdocs/easyfl.md).

Here we provide the entire [proxima.genesis.id](ledgerdocs/genesis.id.md) file as an example of ledger definition library.

The Proxima ledger definitions is an extension of the base EasyFL library of functions. It is crucial, that all nodes in the network share the ledger definitions with exactly the same hash of the library.

All functions we divide in two broad categories: general-purpose functions and validity constraint functions. 

General purpose functions are all embedded functions and other functions for manipulation of byte arrays and accessing particular parts of the transaction. 

Ledger validity constraints are functions, which are used as constraints in the UTXOs, such as different lock functions (siglock, chain lock, time lock etc), chain constraints, sequencer, inflation, delegation and many other. One may think about ledger validity constraints as core set of smart contracts, that defines core concepts on the ledger.

We will go through examples of functions, defined in the Proxima ledger, hoping that the rest are self explanatory or deserves separate documentation. 

