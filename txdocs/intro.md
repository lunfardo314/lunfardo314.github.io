# Introduction

(*This is **version 1.0** of the document. The document and definitions presented in it will be modified in subsequent versions, while trying the best to preserve backwards compatibility with the core concepts*)

This document is "down-to-the-technical level". It's main purpose is knowledge transfer. The document aims to provide both, the general philosophy and the precise definitions of the Proxima core data structures. Its intended audience are core and other developers, as well as anybody who is interested in studying Proxima and bringing it forward.

We intend to provide links to the particular places of the implemented Go code, as well as descriptions of some core Go APIs and data structures. The document, however, is not a API documentation. The code links serves as examples and illustrations.

## Importance of transaction in Proxima

In Proxima, the **transaction is a central concept**. Everything else is derived from the model of the transaction and its validity rules. Including the consensus.

In other crypto ledgers, usually blockhains/blockDAGs, the concept of *transaction* is somehow secondary: transaction can be anything defined as such. One can pack whatever is defined as "a transaction" in blocks and then consensus is run on (a sequence) of blocks. Meanwhile, **we have no blocks in Proxima.**

Raw transaction, a canonical form of it, in Proxima is a *blob* of data, which is deserialized to the hierarchical(nested), finite and deterministic structure of tuples of binary data, which is validated according to the trusted rules. Invalid transactions are immediately rejected by the network.

Raw transaction is **the only type of message exchanged between participants** of the distributed ledger. From the other side, **anybody who is able to produce a valid transaction, is entitled to post it to the network of peers**, via the open gossip protocol.

The "anybody" is an owner of private keys, a **token holder**. Any token holder is entitled to send transactions to peers. It is the only category of participants in the Proxima distributed ledger: no miners, no chosen set of validators.

The above makes the system completely **permissionless** in a sense, that anybody who is able to buy tokens, automatically becomes a participant of the consensus because of their ability to exchange transactions with peers.

Each token holder produces transactions by maximising their profits, which is either inflating their holdings or collecting fees from fellow peers. The emerging behavior is a converging (probabilistic) consensus called **cooperative consensus**, which we consider a particular kind of a *Nakamoto consensus* due to its *permissionless-ness*.

**The cooperative behavior of peers is derived from the validity rules of the transaction**, that's why transaction is a central concept in Proxima.

By abstracting details, one can imagine a shared global structure, a *DAG*, with transactions as vertices, which is incrementally, independently yet deterministically constructed by the participants. The constructed data structure, called **the tangle** depends only on the set of transactions which reached the participant at particulat moment. It is independent on the order in which transactions arrived.

In the deterministic DAG of transactions, each vertex defines a deterministic and **totally ordered set of transactions** in its past cone, thus making **sequencing not necessary** (unlike in blockchains/blockDAGs).

All this makes Proxima a unique and unorthodox approach in the crypto space.
By our claim, Proxima is significantly simpler than other crypto ledgers (except, maybe, Bitcoin), because it is based on fewer underlying basic concepts.

## Transactions and the ledger
At its core, Proxima transaction model is a classical UTXO model, because. it retains all fundamental traits of the UTXO, as it was introduced in the Bitcoin whitepaper.

It is also is fundamentally similar to [EUTXO](https://docs.cardano.org/about-cardano/learn/eutxo-explainer), however Proxima takes somehow different direction from Cardano's models: the programmability of the former has no intention for *smart contracts* (at least not in the form it is known in Ethereum, SUI and similar Turing-complete designs).

The main trait of UTXO (and Proxima transaction model for that matter) is its **deterministic** transactions, which are **validation-oriented**. This is in contrast with *non-deterministic* or **execution-oriented** transactions, used in Ethereum (there are deep reasons and implications of this difference but this discussion is outside of the scope of this document). Each Proxima transaction is either *valid* according to globally trusted formal validity rules, or it is not treated as a transaction (i.e. it is *invalid*) and is immediately rejected by the system.

While remaining classical UTXO, the Proxima model enhances the former with the following features needed for the Proxima's *cooperative consensus*:
* **endorsement**. Each Proxima transaction can optionally *endorse* other transactions by pointing at them with immutable links, which are signed by the producer of the transactions, the token holder. Endosements and UTXO consumption links allows interpretation of the ledger as a *directed acyclic graph* (DAG). The trait of *endorsement* is needed for the consolidation of different non-conflicting ledger states into one.
* **progammability**. Proxima makes transaction and each individual output (UTXO) programmable via validation scripts which are an immutably part of it. The scripts specify enforced logical relations between different parts of the transaction data. Proxima uses formulas of a simple **functional language** [*EasyFL*](https://github.com/lunfardo314/EasyFL) (introduced in this document) instead of imperative scripts for the stack-based VM used in the [Bitcoin Script](https://en.bitcoin.it/wiki/Script) and many other crypto ledgers. Computationally, however, Proxima's approach to the UTXO programmability is equivalent to Bitcoin's: both are non-Turing complete by intention, i.e. equivalent to a *finite automaton*. The purpose of the validation scripts is to **enforce intended behavior** on the ledger. Consumers of the UTXOs can only produce valid transactions that satisfy immutable validity constraints embedded in those UTXOs by the producers of it. One can imagine a Proxima transaction as a programmable finite automaton.


More details on the rationale of the design choices can be found in the [Proxima whitepaper](https://arxiv.org/abs/2411.16456).

