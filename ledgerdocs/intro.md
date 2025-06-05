# Introduction

The Proxima ledger has two important aspects: the ledger validity rules and managing multiple ledger states efficiently.

The ledger validity rules defines what is a valid ledger state and how valid ledger state it can be updated to the next valid ledger state. This part we call **ledger definitions**. We will describe particular definitions of EasyFL constraints, which makes token holders produce transactions the way which leads to the cooperative consensus on the ledger state.

In Proxima, each transaction in the _transaction DAG_ (aka _the tangle)_ represents a separate ledger state. We will describe how the _multi-state_ database enables handling the tangle and multiple ledger states efficiently.

