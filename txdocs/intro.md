# Introduction

Proxima uses an advanced UTXO model akin to those used by Bitcoin, Cardano and Kaspa. Proxima builds it on top of just few foundational concepts, that includes programmability and serialization primitives.   

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

* **Programmability and covenants**: each individual output (UTXO), and the transaction as a whole, carries **validation scripts** — an immutable part of the data they sit in. A script defines an enforced logical relationship, a **constraint**, between parts of the transaction data.

  This is what is commonly called a **covenant**. The creator of an output fixes, at the moment of creation, the conditions under which it may ever be spent; whoever spends it later cannot escape them. A consumer can produce a valid transaction only if it satisfies the constraints the creator embedded. The covenant is not a promise enforced by an operator — it is a validity rule, checked identically by every node.

  Instead of imperative, stack-based scripting (like Bitcoin Script), Proxima uses formulas from a simple functional language, [EasyFL](txdocs/easyfl.md). Despite differences in syntax and structure, Proxima’s UTXO programmability is computationally equivalent to Bitcoin’s — intentionally non-Turing complete and effectively a finite automaton. It *validates*; it does not *execute*.

  Covenants reach their full form on a **chained account**, an identity that persists across many transactions while its state changes. There the constraints do not merely decide who may spend an output: they program **the state transition itself**, the predecessor prescribing what its successor is permitted to be. A covenant on a chain therefore governs an unbroken line of states rather than a one-off spending condition. Sequencers, delegations, token foundries and NFTs are all chained accounts, and each is defined by the covenant governing its transitions.

  A chained account is always controlled by its **lock**, and the lock is what decides whether and when the account may be discontinued. In the simplest case the lock is an ordinary signature lock, so continuing or ending the account is up to the holder; a more elaborate lock can forbid it, or allow it only under stated conditions.

  This is where Proxima differs from how covenants are usually understood. On Bitcoin or Kaspa a covenant is not generally assumed to have a single state — the same covenant logic may constrain several parallel states at once. In Proxima the covenant's **identity** is one **atomic, non-forkable chain**: at any moment the ledger holds exactly one output for a given chain ID, so there is never an ambiguity about which of two states is the real one. That single chain can in turn spawn secondary chained accounts running in parallel under the same logic. The architectural possibilities are open-ended.

Proxima’s UTXO model can also be compared to [EUTXO](https://docs.cardano.org/about-cardano/learn/eutxo-explainer), as introduced by Cardano; however, Proxima’s approach may offer a broader generalization in some respects. For instance, in Proxima, any transaction data (including _unlock data_) can function similarly to what EUTXO refers to as a _redeemer_ or _datum_.

That said, Proxima's view of UTXO programmability differs from Cardano’s. While Proxima supports programmability, it does not aim to enable smart contracts comparable to those in Ethereum, SUI, or other Turing-complete platforms.

A similar comparison can be drawn with the covenants Kaspa gained after Tocatta. There, as in Bitcoin and in EUTXO, a covenant is a condition on **spending**: it constrains the transaction that consumes the output.

That is the key difference. In Proxima a validation script is not only a spending constraint — it is evaluated in **both** roles: when the output is produced, and again when it is consumed later. A constraint can therefore enforce declared validity rules of the *producing* transaction itself, not merely of some future transaction that spends its outputs. A produced UTXO becomes a trustless witness to properties of the transaction that created it. This opens up richer programmability and stronger transaction primitives for interaction with L2 entities; the details are beyond this introduction.

You can find further rationale for these design choices in the [Proxima whitepaper](https://arxiv.org/abs/2411.16456).

