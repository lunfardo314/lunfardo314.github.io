# Join Proxima

Proxima is entering its **launch phase** — the stretch in which the ledger passes from one founder running it alone to a community of independent token holders running it together.

The launch is a **fair launch**. There is no presale, no allocation, no investor round, no treasury. Six per cent of the supply is minted at genesis, as the bootstrap capital that gets the ledger moving. The other **94 % is mined**, with proof of work, by whoever competes for it: nobody hands those tokens out, a miner mints them by satisfying rules fixed at genesis. **Proxima is not a proof-of-work network.** The work distributes the supply and nothing else: it takes no part in the consensus, which is reached by token holders cooperating, and it ends for good once the mintable supply is exhausted. See [The fair launch](overview/fair_launch.md).

Taking part is the point of it. Proxima is **permissionless**: the only participants are token holders, and anyone holding tokens can write to the ledger and take part in the consensus. There is no separate class of miners or validators to apply to. And Proxima is only as decentralized as its tokens are spread among independent holders who put them to work — so distribution is not a slogan beside the protocol, it is what makes the ledger secure. The aim of everything below is to decentralize Proxima and make it a community effort.

This page summarizes the ways to take part; the operational guides for each are part of this section.

## Your self-assigned roles

* **Miner, a temporary role.** [Mine](participate/mine.md) for the 94 % of the supply that is not created at genesis — the way a newcomer with no tokens gets tokens. There is exactly one mine chain on the ledger and it is open to everybody: no signature unlocks it, only a proof of work. Each step pays its reward to whoever wins the race for it.
* **Token holder.** Hold and move your tokens with the [`proxi`](participate/proxi.md) command-line wallet (or any other). Moving tokens (building a chain) is what earns inflation and contributes to the security of the ledger — see [Tokens and supply](overview/2-tokens-and-supply.md).
* **Delegator.** [Delegate](participate/delegate.md) your funds to a sequencer of your choice to earn inflation on your behalf, while keeping full, trustless control of your tokens. This is the recommended option for most holders — see [Delegation and liveness](overview/delegation.md).
* **Access node operator.** [Run a full (non-sequencer) node](participate/run_access.md) to follow the tangle, serve the API, and relay transactions to peers, thus contributing to the network. A good first step for developers and infrastructure operators.
* **Sequencer.** [Run a sequencer](participate/run_sequencer.md) to proactively build a sequencer chain. A sequencer keeps the whole inflation on its own tokens instead of giving a cut to another sequencer, takes a cut of the inflation on the tokens others delegate to it, collects tag-along fees from the user transactions it pulls in, and earns the branch inflation bonus for committing ledger states. Sequencers are the most active participants and are critical to the security of the ledger — and the earnings above are the incentive to be one.

Frontend and wallet developers who want a private node to build against can spin up a [standalone developer node](participate/run_standalone.md).

## Guides in this section

* [The `proxi` wallet](participate/proxi.md) — the command-line wallet and node-management tool.
* [Wallet configuration](participate/wallet_config.md) — the `proxi.yaml` wallet profile.
* [Mining](participate/mine.md) — acquiring tokens during the launch phase.
* [Delegation](participate/delegate.md) — delegate funds to a sequencer to earn inflation trustlessly.
* [Running an access node](participate/run_access.md) — join and sync a full node with the launch phase network.
* [Running a sequencer node](participate/run_sequencer.md) — run a sequencer chain.
* [Running a standalone developer node](participate/run_standalone.md) — a throwaway single-node network for frontend/wallet development.
* [Node configuration reference](participate/node_config.md) — every `proxima.yaml` tag.

## Contribute

Proxima is open source. The node, the `proxi` wallet, the EasyFL language and the supporting libraries are developed in the open:

* Proxima node and tools — [github.com/lunfardo314/proxima](https://github.com/lunfardo314/proxima)
* EasyFL scripting language — [github.com/lunfardo314/easyfl](https://github.com/lunfardo314/easyfl)
* `unitrie` trie / Merkle-tree library — [github.com/lunfardo314/unitrie](https://github.com/lunfardo314/unitrie)

Issues, discussion and pull requests are welcome in those repositories.
