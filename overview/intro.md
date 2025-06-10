Introduction
===

Proxima presents a novel architecture for a distributed ledger, commonly referred to as a *blockchain*.

- Proxima is as decentralized and permissionless as Bitcoin (*proof-of-work*, PoW).
- Proxima is similar to *proof-of stake* (PoS) due to its approach to the Sybil-protection with tokens, its cost-and-energy-efficiency and high throughput.

Yet it is neither PoW, nor a BFT-based PoS system. It is based on **cooperative consensus**, which is _probabilistic_ and _multi-leader_. 
It uses _transaction DAG_ (a _directed acyclic graph_) also known as the _tangle_. In contrast to blockchains and blockDAGs, **Proxima has no blocks**. We see the _cooperative consensus_ as a _Nakamoto consensus_ without PoW.

In short, the *cooperative consensus* is a convergent behavior among token holders, issuing valid transactions while seeking profit in a form of inflation rewards and fees collected from peers. Similarly to the *longest chain rule* of PoW blockchains, in Proxima token holders follows rule, called **biggest ledger coverage** rule. The latter is an optimal profit-seeking strategy for them in the game-theoretical sense. It leads to Nash equilibrium among token holders, just like the *longest chain rule* is optimal for Bitcoin miners.

Token holders are the only category of users which has genuine and vested interest in any distributed ledger. In blockchains, a special category of participants, 3rd parties such as miners or validators, must be incentivized to maintain consensus of the ledger state on behalf of the users. The extent of decentralization and security of the blockchain strictly depends on how decentralized its miners/validators are.

Proxima takes a different approach: the end-users -- token holders -- themselves maintain consensus on the ledger state by cooperating permissionless-ly with each other, only driven by self-interest in the environment defined by the ledger validity constraints. It removes the need for special incentivized categories of participants with their specific interests and behaviors. 

Tokens holders are free to choose the most profitable strategy of participation for them - given amount of their on-ledger capital and specific needs - as long as they satisfy purposefully designed ledger validity rules. The rest is market-driven.

jewelryThe philosophy of Proxima is **social consensus**, **equity** and **cooperation** among stakeholders of the distributed ledger.

Proxima positions itself as a possible platform for a _digital gold_, a fundamental enabling layer of scarce and secure resource for derived concepts such as _money_, _payments_ or even _jewelry_. 

---

This document gives a general overview of the Proxima design. It omits most of technical details and aims to explain main concepts in simple terms.

Links for further information:
- [Proxima technical whitepaper](https://arxiv.org/abs/2411.16456) (detailed description of the concept).
- [Proxima GitHub repository](https://github.com/lunfardo314/proxima) (code of the Proxima node, readme, tutorials, links to video and other resources)
- [Bitcoin forum topic](https://bitcointalk.org/index.php?topic=5499359.0)
- [Discord server invite link](https://discord.com/invite/UfFcFDy38j)
