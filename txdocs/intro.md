# Introduction

Proxima uses an advanced UTXO model akin to those used by Bitcoin, Cardano and Kaspa. Proxima builds it on top of just few foundational concepts, that includes programmability and serialization primives.   

This document delves into the technical details of Proxima. It aims to convey both the overarching philosophy and the precise definitions of Proxima’s core data structures. The intended audience includes core developers, other contributors, and anyone interested in studying Proxima and contributing to its evolution.

We provide links to specific parts of the implemented Go code, along with descriptions of key Go APIs and data structures. However, this is not API documentation. The code links are meant to serve as illustrative examples.

## The importance of transactions in Proxima

In Proxima, the transaction is a foundational concept. Everything else, including consensus, derives from the transaction model and its associated validity rules.

In many other crypto ledgers - typically blockchains or blockDAGs - the concept of a transaction is secondary: a transaction is simply whatever is defined as such, and these are packed into blocks. Consensus is run on blocks. **Proxima, by contrast, has no blocks. Consensus is run on inclusion of each individual transaction into the ledger**.

A **raw or canonic transaction** in Proxima is a *blob* of data that is deserialized into deterministic structure using minimalistic primitives. This structure is validated against trusted rules. 

The raw transaction is **the only** type of message exchanged between participants in the distributed ledger. Anyone who can produce a valid transaction may submit it to the peer network via an open gossip protocol.

"Anyone," in this context, refers to private key-holders - **token holders** - the only category of participants in the Proxima network. 
Any token holder can submit transactions to peers. Each transaction defines a canonic and deterministic **write to the ledger**: the effect of the transaction on the ledger state is known in advance and is fully defined by the user.

This setup makes Proxima **completely permissionless**. Anyone who acquires tokens can write to the ledger and participate in consensus. 
Consensus resolves conflicting writes.

Each token holder produces transactions to maximize their own benefit — either by inflating their holdings or collecting fees from peers. The resulting system behavior leads to a probabilistic yet convergent consensus mechanism we call **cooperative consensus**. We consider this a specific form of Nakamoto consensus, owing to its permissionless nature.

**The cooperative behavior of peers emerges from the transaction validity rules — hence, the central role of the transaction in Proxima.**

At a higher level of abstraction, one can imagine a shared global data structure: a **DAG** (directed acyclic graph) with transactions as vertices. This structure, called **the tangle**, is constructed incrementally, independently, and deterministically by each participant. The tangle depends only on the set of transactions a participant has seen at a given moment, not on their arrival order.

In this deterministic DAG, each vertex defines a fully ordered set of transactions in its past cone. As a result, explicit sequencing (as used in blockchains or blockDAGs) is not required.

## Transactions and the ledger
At its core, Proxima’s transaction model follows the classical UTXO paradigm, retaining all the essential characteristics described in the original Bitcoin whitepaper.

The hallmark of the UTXO model (and thus Proxima’s model) is that transactions are **deterministic** and **validation-oriented**. This contrasts with the **non-deterministic**, **execution-oriented** transactions of platforms like Ethereum (EVM) or SUI (MoveVM). (_The deeper implications of this distinction are outside the scope of this document._) 

In Proxima, a transaction is either valid - according to globally trusted formal rules- or it is invalid and immediately rejected.

While preserving the classical UTXO model, Proxima introduces two key enhancements:

* **Endorsements**: Each Proxima transaction can optionally endorse other transactions by referencing them with immutable links, signed by the transaction’s producer (the token holder). These endorsements, along with UTXO consumption links, allow the ledger to be interpreted as a DAG. Endorsements help consolidate different non-conflicting ledger states into a unified view.

* **Programmability**: In Proxima, each transaction and individual output (UTXO) can be made programmable using validation scripts, which are an immutable part of the transaction. These scripts define enforced logical relationships (constraints) between different parts of the transaction data. Instead of imperative, stack-based scripting (like Bitcoin Script), Proxima uses formulas from a simple functional language called [EasyFL](txdocs/easyfl.md). Despite differences in syntax and structure, Proxima’s UTXO programmability is computationally equivalent to Bitcoin’s — intentionally non-Turing complete and effectively a finite automaton. The purpose of these scripts is to enforce intended behavior on the ledger. A consumer of a UTXO can only create a valid transaction if it satisfies the immutably embedded validity constraints imposed by the UTXO’s creator.

Proxima’s UTXO model can also be compared to [EUTXO](https://docs.cardano.org/about-cardano/learn/eutxo-explainer), as introduced by Cardano; however, Proxima’s approach may offer a broader generalization in some respects. For instance, in Proxima, any transaction data (including _unlock data_) can function similarly to what EUTXO refers to as a _redeemer_ or _datum_.

That said, Proxima's view of UTXO programmability differs from Cardano’s. While Proxima supports programmability, it does not aim to enable smart contracts comparable to those in Ethereum, SUI, or other Turing-complete platforms.

You can find further rationale for these design choices in the [Proxima whitepaper](https://arxiv.org/abs/2411.16456).

