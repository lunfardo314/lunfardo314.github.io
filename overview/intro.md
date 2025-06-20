Introduction
===

Proxima presents a novel architecture for a distributed ledger, commonly referred to as a *blockchain*.

- Proxima is as decentralized and permissionless as Bitcoin (*proof-of-work*, PoW).
- Proxima is similar to *proof-of stake* (PoS) due to its approach to the Sybil-resistance with tokens, its cost-and-energy-efficiency and high throughput.

Yet it is neither PoW, nor a PBFT-based PoS system. It is based on **cooperative consensus**, which is _probabilistic_ and _multi-leader_. 
It uses _transaction DAG_ (a _directed acyclic graph_) also known as the _tangle_. In contrast to blockchains and blockDAGs, **Proxima has no blocks**. We see the _cooperative consensus_ as a _Nakamoto consensus_ without PoW (see motivation in [On definition of Nakamoto consensus](https://medium.com/@lunfardo/on-definition-of-nakamoto-consensus-be8f4b84c899)).

In short, the *cooperative consensus* is a convergent profit-seeking behavior among token holders, issuing valid transactions while seeking inflation rewards and fees collected from peers. Similarly to the *longest chain rule* of PoW blockchains, in Proxima token holders follows rule, called **biggest ledger coverage** rule. The latter is an optimal profit-seeking strategy for them in the game-theoretical sense. It leads to Nash equilibrium among token holders, just like the *longest chain rule* is optimal for Bitcoin miners.

in general, token holders are the only category of participants that has genuine and vested interest in any distributed ledger. In blockchains, a special category of participants, 3rd parties such as miners or validators, must be incentivized to maintain consensus of the ledger state on behalf of the users. The extent of decentralization and security of the blockchain strictly depends on how decentralized its miners or validators are.

Proxima takes a different approach: the end-users -- token holders -- themselves maintain consensus on the ledger state by cooperating permissionless-ly with each other, only driven by self-interest in the environment defined by the ledger validity constraints. It removes the need for special incentivized categories of participants with their specific interests and behaviors. 

Tokens holders are free to choose the most profitable strategy of participation for them - given amount of their on-ledger capital and specific needs - as long as they satisfy purposefully designed ledger validity rules. The rest is market-driven.

The philosophy of Proxima is **social consensus**, **equity** and **cooperation** among stakeholders of the distributed ledger.

Proxima positions itself as a **peer-to-peer gold**: a possible platform for a _digital gold_. 
We envision Proxima a fundamental enabling layer of scarce, secure, cost-efficient and scalable resource for derived concepts such as _money_, _cash_, _payments_ or even _jewelry_. For Scalability and other reasons, those derived concepts can be implemented as layer 2 solutions, while establishing trust-less, (zk)-proven equivalence with the base asset, the trust-less and fully decentralized _digital gold_. 

---

This document gives a general overview of the Proxima design. It omits most of technical details and aims to explain main concepts in simple, general terms.

Links for the further information:
- [Proxima technical whitepaper](https://arxiv.org/abs/2411.16456) (detailed description of the concept).
- [Proxima GitHub repository](https://github.com/lunfardo314/proxima) (code of the Proxima node, readme, tutorials, links to video and other resources)
- [Bitcoin forum topic](https://bitcointalk.org/index.php?topic=5499359.0)
- [Discord server invite link](https://discord.com/invite/UfFcFDy38j)
