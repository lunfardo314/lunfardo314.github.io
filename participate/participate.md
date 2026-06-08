# Join Proxima

Proxima is **permissionless**: the only participants are token holders, and anyone holding tokens can write to the ledger and take part in the consensus. There is no separate class of miners or validators to apply to. This page summarizes the ways to participate; the operational guides for each are part of this section.

## Ways to participate

* **As a token holder.** Hold and move your tokens with the `proxi` command-line wallet. Moving tokens (building a chain) is what earns inflation and contributes to the security of the ledger — see [Incentives](overview/incentives.md).
* **By delegating.** Delegate your funds to a sequencer of your choice to earn inflation on your behalf, while keeping full, trustless control of your tokens. This is the recommended option for most holders — see [Delegation and liveness](overview/delegation.md).
* **By running an access node.** Run a full (non-sequencer) node to follow the tangle, serve the API, and relay transactions to peers. A good first step for developers and infrastructure operators.
* **By running a sequencer.** Run a sequencer to proactively build a sequencer chain, issue branches, and pull user transactions via the tag-along mechanism. Sequencers are the most active participants and are critical to the security of the ledger.

## Contribute

Proxima is open source. The node, the `proxi` wallet, the EasyFL language and the supporting libraries are developed in the open:

* Proxima node and tools — [github.com/lunfardo314/proxima](https://github.com/lunfardo314/proxima)
* EasyFL scripting language — [github.com/lunfardo314/easyfl](https://github.com/lunfardo314/easyfl)
* `unitrie` trie / Merkle-tree library — [github.com/lunfardo314/unitrie](https://github.com/lunfardo314/unitrie)

Issues, discussion and pull requests are welcome in those repositories.
