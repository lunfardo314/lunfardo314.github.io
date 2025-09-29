Introduction
===

Proxima presents a novel architecture for a distributed ledger, commonly referred to as a *blockchain*.

- by claim, Proxima is as decentralized and permissionless as *proof-of-work* (PoW) systems, including Bitcoin.
- Proxima is similar to *proof-of stake* (PoS) due to its approach to the Sybil-resistance with tokens, its cost-and-energy-efficiency and high throughput.

Yet it is neither PoW, nor a PBFT-based PoS system. It is based on **cooperative consensus**, which is **probabilistic** and **multi-leader** (or leader-less). 
It uses _transaction DAG_ (a _directed acyclic graph_) also known as the _tangle_. In contrast to blockchains and blockDAGs, Proxima has **no blocks** and has **no mempool**. 
We see the _cooperative consensus_ as a _Nakamoto consensus_ but its essential traits which does not use PoW (see motivation in [On definition of Nakamoto consensus](https://medium.com/@lunfardo/on-definition-of-nakamoto-consensus-be8f4b84c899)).

In short, the *cooperative consensus* is an emergent profit-seeking behavior among token holders, 
issuing valid transactions while seeking inflation rewards and fees collected from peers. Similarly to the *longest chain rule* of PoW blockchains, in Proxima token holders follows rule, called **biggest ledger coverage** rule. The latter is an optimal profit-seeking strategy for them in the game-theoretical sense. It leads to Nash equilibrium among token holders, just like the *longest chain rule* is optimal for Bitcoin miners.

Generally speaking, users, the token holders, are the only category of participants that has genuine and vested interest in any distributed ledger. In blockchains, a special category of participants, 3rd parties such as miners or validators, must be incentivized to maintain consensus of the ledger state on behalf of the users. The extent of decentralization and security of the blockchain strictly depends on how decentralized its miners or validators are.

Proxima takes a different approach: the end-users -- token holders -- themselves maintain consensus on the ledger state by cooperating permissionless-ly with each other, only driven by self-interest in the environment defined by the ledger validity constraints. I.e. all players participate in the system with their own skin-in-the-game. 
That removes the need for special incentivized categories of participants with their specific interests and behaviors. This also minimizes number of base concepts and trust assumptions in the protocol and, as a result, leads to a simpler architecture. 

Tokens holders are free to choose the most profitable strategy of participation for them - given amount of their on-ledger capital and specific needs - as long as they satisfy purposefully designed ledger and transaction validity rules. The rest is market-driven.

## Vision
The philosophy of Proxima is **social agreement**, **equity** and **cooperation** among stakeholders of the distributed ledger.

Following example of Bitcoin, we see Proxima as **peer-to-peer gold**. We envision it as a verifiable, trust-less and fully decentralized platform for a _digital scarcity_ or _digital gold_. 

The goal is to be fundamental enabling layer of scarce, secure, cost-efficient and scalable resource for derived digital concepts such as _money_, _cash_, _payments_ or even _jewelry_.

For scalability and other reasons, those derived concepts can be implemented as layer 2 solutions, that maintain trust-less and (zk)-proven equivalence with the base asset, as a universal collateral. 

* Cost-efficiency, low and bounded costs per asset and per transaction, is how Proxima differentiates itself from PoW protocols.
* Permissionlessness and architectural simplicity is how Proxima is different from PoS protocols

---

This document gives a general overview of the Proxima design. It omits most of technical details and aims to explain main concepts in simple, general terms.

Links for the further information:
- [Proxima technical whitepaper](https://arxiv.org/abs/2411.16456) (detailed description of the concept).
- [Proxima GitHub repository](https://github.com/lunfardo314/proxima) (code of the Proxima node, readme, tutorials, links to video and other resources)
- [Bitcoin forum topic](https://bitcointalk.org/index.php?topic=5499359.0)
- [Discord server invite link](https://discord.com/invite/UfFcFDy38j)
