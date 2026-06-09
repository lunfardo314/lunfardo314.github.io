# Join Proxima

Proxima is **permissionless**: the only participants are token holders, and anyone holding tokens can write to the ledger and take part in the consensus. There is no separate class of miners or validators to apply to. This page summarizes the ways to participate; the operational guides for each are part of this section.

## Ways to participate

* **As a token holder.** Hold and move your tokens with the [`proxi`](participate/proxi.md) command-line wallet. Moving tokens (building a chain) is what earns inflation and contributes to the security of the ledger — see [Incentives](overview/incentives.md).
* **By delegating.** [Delegate](participate/delegate.md) your funds to a sequencer of your choice to earn inflation on your behalf, while keeping full, trustless control of your tokens. This is the recommended option for most holders — see [Delegation and liveness](overview/delegation.md).
* **By running an access node.** [Run a full (non-sequencer) node](participate/run_access.md) to follow the tangle, serve the API, and relay transactions to peers. A good first step for developers and infrastructure operators.
* **By running a sequencer.** [Run a sequencer](participate/run_sequencer.md) to proactively build a sequencer chain, issue branches, and pull user transactions via the tag-along mechanism. Sequencers are the most active participants and are critical to the security of the ledger.

The quickest way to get hands-on is the [open testnet](participate/testnet.md). Frontend and wallet developers who want a private node to build against can spin up a [standalone developer node](participate/run_standalone.md).

## Guides in this section

* [Participating in the open testnet](participate/testnet.md) — get tokens and start moving them on the live testnet.
* [The `proxi` wallet](participate/proxi.md) — the command-line wallet and node-management tool.
* [Wallet configuration](participate/wallet_config.md) — the `proxi.yaml` wallet profile.
* [Delegation](participate/delegate.md) — delegate funds to a sequencer to earn inflation trustlessly.
* [Running an access node](participate/run_access.md) — join and sync a full node with the testnet.
* [Running a sequencer node](participate/run_sequencer.md) — run a sequencer chain.
* [Running a standalone developer node](participate/run_standalone.md) — a throwaway single-node network for frontend/wallet development.
* [Node configuration reference](participate/node_config.md) — every `proxima.yaml` tag.

## Contribute

Proxima is open source. The node, the `proxi` wallet, the EasyFL language and the supporting libraries are developed in the open:

* Proxima node and tools — [github.com/lunfardo314/proxima](https://github.com/lunfardo314/proxima)
* EasyFL scripting language — [github.com/lunfardo314/easyfl](https://github.com/lunfardo314/easyfl)
* `unitrie` trie / Merkle-tree library — [github.com/lunfardo314/unitrie](https://github.com/lunfardo314/unitrie)

Issues, discussion and pull requests are welcome in those repositories.
