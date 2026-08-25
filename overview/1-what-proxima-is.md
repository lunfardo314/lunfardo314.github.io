# What Proxima is

Proxima is a distributed ledger — what is usually called a blockchain, although it is
not built out of blocks.

What distinguishes it is *who keeps it running*. In most ledgers a separate class of
participants is paid to agree on the state of the ledger on everyone else's behalf:
miners in Bitcoin, validators or a committee in proof-of-stake systems. How
decentralized such a system really is depends on how decentralized that class is, and
its members have interests of their own, which are not the users' interests.

Proxima has no such class. The people who hold the tokens reach the agreement
themselves, as a side effect of spending them. This is called **cooperative
consensus**, and the rest of the design follows from it.

## No blocks, no mempool

A Proxima transaction is added directly to a *directed acyclic graph* of transactions
called the **tangle**. Each transaction refers to earlier ones — by spending their
outputs and by *endorsing* them — and immediately becomes one of the newest points of
the graph.

There is nothing in between. No block has to be assembled, no queue of pending
transactions waits to be selected from, and no participant has a turn. A transaction is
either valid under the ledger's rules or it is not; once issued and valid, it is part
of the graph.

Removing blocks removes the bottleneck that producing them creates, along with the race
to win it.

## Consensus by cooperation

Because anyone may add a transaction at any moment, the tangle holds many versions of
the ledger at once — one for every transaction, each being the result of applying that
transaction's entire history to the ledger. Some of those versions contradict each
other. Consensus means converging on one.

Token holders converge by following a single rule, the **biggest ledger coverage rule**:
each participant builds on the version of the ledger that covers the most tokens.
"Coverage" is a measurement of how much of the token supply a transaction's history
accounts for. Building on the broadest version is also the most profitable thing a
participant can do, so it is what a self-interested holder does without being asked.

This is the same shape of argument as Bitcoin's longest chain rule. Miners follow the
longest chain because deviating costs them money; Proxima's token holders follow the
biggest coverage for the same reason. Neither rule is enforced by an authority. Both
hold because breaking them is expensive.

Consensus of this kind is **probabilistic**: you cannot prove a transaction will never
be abandoned, only become steadily more certain that it will not be. Bitcoin users wait
for six blocks for exactly this reason.

Much of this cooperation is carried out by **sequencers** — token holders who take an
active part, issuing transactions continuously and folding other people's transactions
into their own ledger version as they go. Running one is a role you can choose, not a
privileged position granted to anyone.

The full argument, with the definition of coverage and how sequencers and branches
work, is in [Cooperative consensus](overview/consensus.md).

## How it compares

Against **proof of work**: Proxima is permissionless in the same sense — anyone may
join, and nothing needs anyone's approval. But it spends no energy on mining races, and
its costs per transaction are low and bounded. How a system with no mining can still be
bootstrapped from nothing is treated in
[Being permissionless. Bootstrap](overview/permissionless.md).

Against **proof of stake**: Proxima resists Sybil attacks the same way, by weighing
tokens on the ledger rather than identities. What differs is *what casts the vote*.

We often call the principle Proxima is built on **Nakamoto-PoS**: consensus carried by
**fungible token votes**, where what counts is the tokens themselves and not who holds
them. Committee-based proof of stake instead counts **weighted identity votes** — a
known set of validators, each with a stake bound to its identity, voting as themselves.

Because a fungible token has no identity to register, Nakamoto-PoS needs no committee to
form, no quorum to assemble and no leader schedule. That removes a set of trust
assumptions along with a great deal of machinery.
[Safety and liveness](overview/safety_liveness.md) sets out what the design guarantees
and what it does not.

Proxima is therefore neither a proof-of-work system nor a BFT-based proof-of-stake one.
It is a [Nakamoto consensus](https://medium.com/@lunfardo/on-definition-of-nakamoto-consensus-be8f4b84c899)
that does not use proof of work: probabilistic, and with many leaders rather than one.

## The vision

The philosophy of Proxima is **social agreement**, **equity** and **cooperation** among
those who hold a stake in the ledger.

Following Bitcoin's example, we see Proxima as **peer-to-peer gold**: a verifiable,
trustless and fully decentralized platform for *digital scarcity*. The aim is to be the
enabling layer beneath derived ideas such as money, cash, payments — or even jewelry —
rather than to be all of those things itself.

Those derived concepts are better built as layer-2 systems that maintain a trustless,
provable equivalence with the base asset, using it as universal collateral.

## Where to go next

This page is the first of the overview. It is meant to be read on its own; everything
below is optional and can be taken in any order.

- [Tokens and supply](overview/2-tokens-and-supply.md) — where PROX comes from, and what
  holding it earns.
- [Taking part](overview/3-participate.md) — delegating, sequencing and the other ways in:
  what each costs and returns.
- [UTXO ledger](overview/utxo_ledger.md) — how transactions, conflicts and the tangle
  actually fit together.
- [Cooperative consensus](overview/consensus.md) — the full argument sketched above.
- [Incentives](overview/incentives.md) — where tokens come from and what makes the
  rules profitable to follow.
- [Delegation and liveness](overview/delegation.md) — putting tokens to work without
  running anything yourself.
- [Join and contribute](participate/participate.md) — the practical guides: running a
  node, delegating, mining, using the wallet.
- [Transaction model](txdocs/intro.md) — the technical treatment of transactions and
  the scripting that constrains them.

Further reading and community:

- [Proxima technical whitepaper](https://arxiv.org/abs/2411.16456) — the detailed
  description of the concept.
- [Proxima GitHub repository](https://github.com/lunfardo314/proxima) — node code,
  tutorials, videos and other resources.
- [Video introduction to the cooperative consensus](https://youtu.be/XT6GBSLCbZo)
- [Bitcoin forum topic](https://bitcointalk.org/index.php?topic=5499359.0)
- [Discord server](https://discord.com/invite/UfFcFDy38j)
