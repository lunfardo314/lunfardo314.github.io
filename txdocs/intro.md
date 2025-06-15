# Introduction

(_This is **version 1.0** of the transaction model. The content and definitions presented here may be revised in future versions, with a strong effort to maintain backward compatibility with the core concepts._)

This document delves into the technical details of Proxima. Its primary purpose is knowledge transfer. It aims to convey both the overarching philosophy and the precise definitions of Proxima’s core data structures. The intended audience includes core developers, other contributors, and anyone interested in studying Proxima and contributing to its evolution.

We provide links to specific parts of the implemented Go code, along with descriptions of key Go APIs and data structures. However, this is not API documentation. The code links are meant to serve as illustrative examples.

## The importance of transactions in Proxima

In Proxima, the transaction is a foundational concept. Everything else, including consensus, derives from the transaction model and its associated validity rules.

In many other crypto ledgers—typically blockchains or blockDAGs—the concept of a transaction is secondary: a transaction is simply whatever is defined as such, and these are packed into blocks on which consensus is run. **Proxima, by contrast, has no blocks**.

A **raw transaction** in Proxima is a *blob* of data that is deserialized into a hierarchical (nested), finite, and deterministic structure of tuples of binary data. This structure is validated against trusted rules. Invalid transactions are immediately rejected by the network.

The raw transaction is **the only** type of message exchanged between participants in the distributed ledger. Anyone who can produce a valid transaction may submit it to the peer network via an open gossip protocol.

"Anyone," in this context, refers to private key-holders — **token holders**. Any token holder can submit transactions to peers. This is the only category of participants in the Proxima network: there are no miners or designated validators.

This setup makes Proxima **completely permissionless**. Anyone who acquires tokens can participate in the consensus process by exchanging transactions with peers.

Each token holder produces transactions to maximize their own benefit — either by inflating their holdings or collecting fees from peers. The resulting system behavior leads to a probabilistic yet convergent consensus mechanism we call **cooperative consensus**. We consider this a specific form of Nakamoto consensus, owing to its permissionless nature.

The cooperative behavior of peers emerges from the transaction validity rules — hence, the central role of the transaction in Proxima.

At a higher level of abstraction, one can imagine a shared global data structure: a **DAG** (directed acyclic graph) with transactions as vertices. This structure, called **the tangle**, is constructed incrementally, independently, and deterministically by each participant. The tangle depends only on the set of transactions a participant has seen at a given moment, not on their arrival order.

In this deterministic DAG, each vertex defines a fully ordered set of transactions in its past cone. As a result, explicit sequencing (as used in blockchains or blockDAGs) is not required.

This makes Proxima a unique and unorthodox entry in the crypto space. We claim that Proxima is significantly simpler than most other crypto ledgers (with the possible exception of Bitcoin), as it is built upon a smaller set of foundational concepts.

## Transactions and the ledger
At its core, Proxima’s transaction model follows the classical UTXO paradigm, retaining all the essential characteristics described in the original Bitcoin whitepaper.

The hallmark of the UTXO model (and thus Proxima’s model) is that transactions are **deterministic** and **validation-oriented**. This contrasts with the **non-deterministic**, **execution-oriented** transactions of platforms like Ethereum (EVM) or SUI (MoveVM). (_The deeper implications of this distinction are outside the scope of this document._) 

In Proxima, a transaction is either valid—according to globally trusted formal rules—or it is invalid and immediately rejected.

While preserving the classical UTXO model, Proxima introduces two key enhancements to support its _cooperative consensus_ mechanism:

* **Endorsements**: Each Proxima transaction can optionally endorse other transactions by referencing them with immutable links, signed by the transaction’s producer (the token holder). These endorsements, along with UTXO consumption links, allow the ledger to be interpreted as a DAG. Endorsements help consolidate different non-conflicting ledger states into a unified view.

* **Programmability**: In Proxima, each transaction and individual output (UTXO) can be made programmable using validation scripts, which are an immutable part of the transaction. These scripts define enforced logical relationships between different parts of the transaction data. Instead of imperative, stack-based scripting (like Bitcoin Script), Proxima uses formulas from a simple functional language called [EasyFL](ledgerdocs/easfl.md). Despite differences in syntax and structure, Proxima’s UTXO programmability is computationally equivalent to Bitcoin’s — intentionally non-Turing complete and effectively a finite automaton. The purpose of these scripts is to enforce intended behavior on the ledger. A consumer of a UTXO can only create a valid transaction if it satisfies the immutably embedded validity constraints imposed by the UTXO’s creator.

Proxima’s UTXO model can also be compared to [EUTXO](https://docs.cardano.org/about-cardano/learn/eutxo-explainer), as introduced by Cardano; however, Proxima’s approach may offer a broader generalization in some respects. For instance, in Proxima, any transaction data (including _unlock data_) can function similarly to what EUTXO refers to as a _redeemer_ or _datum_.

That said, Proxima's view of UTXO programmability differs from Cardano’s. While Proxima supports programmability, it does not aim to enable smart contracts comparable to those in Ethereum, SUI, or other Turing-complete platforms.

You can find further rationale for these design choices in the [Proxima whitepaper](https://arxiv.org/abs/2411.16456).

