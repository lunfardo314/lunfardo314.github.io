The site is dedicated to the [Proxima project](https://github.com/lunfardo314/proxima).

It also contains [blog](blog/blog.md) with articles on general topics which may or may not be related to Proxima.

Currently available sub-sites:

- [Overview of Proxima concepts](overview/intro.md)
- [Transaction model](txdocs/intro.md)
- [UTXO scripting](ledgerdocs/library.md)
- [Multi-state database](multistate/multistate.md) (WIP)

-------------------------------

# PROXIMA MANIFESTO

## Beliefs and Philosophy

We believe the core use case of crypto is **Nakamoto-decentralized digital scarcity — digital gold — and our first priority must be to implement it.**  
Other layers of the digital financial system — fast payments, stablecoins, tokenized real assets, DeFi, and similar applications — should be built on solid foundations, just as a sound financial system must be anchored in a Gold Standard. These layers either do not require Nakamoto-grade decentralization or are fundamentally at odds with both decentralization and scalability if placed at the base layer.

Money is a social construct. Value emerges from shared beliefs and collective agreement on ownership of assets, and these beliefs must be continuously coordinated among peers. A system for digital gold must therefore be shaped around cooperation rather than authority or industrial competition. Proxima’s **cooperative consensus** follows this principle.

Satoshi Nakamoto introduced an open, permissionless competition among block proposers. Over time this model evolved into specialized authority roles — miners, validators, proposers, builders — actors who gained discretionary power over ordering, inclusion, and control of the ledger.

Proxima exists to correct this drift.  
It asserts that **decentralization means write access: writers — those who can append valid transactions to the canonical ledger — hold the power.** In a truly decentralized system, every user must be a writer — not through representatives, but directly through the protocol’s rules.
True decentralization therefore requires returning this power to users, the only participants with a genuine and permanent interest in the ledger.
Decentralization is not a voting structure or a validator set — it is the unconditional ability of every participant to directly extend the canonical ledger.

Authority is fragility; **only universal write access and the elimination of discretionary roles provides lasting decentralization**.
Minimalism is essential because only simple systems can be proven correct. Formal verification replaces governance; correctness becomes a theorem, not a vote. Incentives must align without creating operator classes. Fairness must persist for decades, not merely at launch.

## Architectural Principles

Proxima is a **Nakamoto-style permissionless, multi-leader, block-less, governance-less UTXO-DAG–based distributed ledger** with PoS-style Sybil resistance.  
Its core innovation is **cooperative consensus**.

There are no blocks, no proposers, no validators, and no global mempool. Every token holder writes the ledger through globally known validity constraints. This restores write access as a universal right rather than a privilege gated by miners, committees, leader elections, or validator roles. The protocol is largely defined by transaction validity rules alone. Raw transaction is the only type of message exchanged between peers while seeking consensus. 

Consensus resolves conflicting ledger updates — double-spends. It arises through selfish yet cooperative DAG building, where users through nodes extend a shared UTXO graph and collectively gravitate toward the branch whose coverage dominates the DAG.  
Inflation incentives ensure continuous participation: every transaction generates new tokens proportional to the funds moved.

**Sequencers** are token holders with voluntary, permissionless responsibilities: endorsing transactions of peers with their transactions, issuing branch transactions representing interim ledger states, and participating in VRF-driven branch inflation bonuses. Their discretion is never exclusive — users may target multiple sequencers, and multiple sequencers may pull the same external transactions. Because past cones overlap heavily, no sequencer controls ordering.
Sequencers do not write on behalf of users; they assist propagation and cooperation. Users retain full write authority through their own transactions.

UTXO determinism eliminates MEV at the base layer.

Sybil resistance is built directly into the ledger. Influence emerges from token ownership rather than proof-of-cost or privileged roles. Total system cost remains bounded and independent of market cap. Fairness is driven by the permissionless liquidity of the token and by ongoing token-holder participation.

The protocol is verifiable: its properties can be formally proven (e.g., with TLA+) directly from the ledger’s immutable constraint layer, within clearly stated system-wide assumptions. Governance is not part of the protocol: only backward-compatible, formally proven refinements are allowed.

## Paradigm & Vision

Traditional blockchains rely on single-leader steps, authority roles, global mempools, and competitive races. They incur escalating costs, centralization pressures, and execution-heavy complexity. Proxima replaces all of this with cooperative consensus, multi-leader DAG structure, deterministic validity, and constraint-level simplicity. It is a fundamentally different architecture, not a refinement of existing ones.
At its core, **Proxima re-centers the ledger around writers rather than operators: every user extends the DAG directly.**

Built on this paradigm, Proxima becomes a possible foundation for a **global Digital Gold Standard** — a neutral, incorruptible reserve asset usable by centralized and decentralized entities, humans and AI agents alike.  
These participants operate on layer 2, can trustlessly transact over the base layer, and are synchronously and asynchronously composable into sophisticated dApps and full ecosystems.

Its aims are sustainable security cost, enduring fairness, deterministic ordering, no MEV, no operator classes, and universal write access.

**Code is law.  
Law is math.  
Constraints are consensus.  
Decentralization is write access.  
Digital gold needs nothing less.**
