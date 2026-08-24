# Mining

Most of Proxima's tokens do not exist yet. At genesis only 5% of the final supply is
created; the other 95% is **mined**, one reward at a time, by anyone who cares to
compete for it. Mining is how a newcomer with no tokens gets tokens.

This page is about running the miner. Why the launch is arranged this way belongs to the
overview of the token supply; here we assume you have decided to take part.

### What you are competing for

There is exactly one **mine chain** on the ledger: a single chained output that moves
forward in steps. Each step is a **transit** — a transaction that consumes the current
mine output, produces the next one, and pays a reward _A_ to whoever produced it.

Only one transit can follow any given mine output, so miners race for each step. Winning
a step gives you the reward and nothing else: no fees, no privileged position, no
influence over the next step.

The chain carries a counter of how much remains to be minted. It starts at 950,000,000
PROX and falls with every transit. When it reaches zero, mining is over and the supply is
complete at 1,000,000,000 PROX.

### Proof of signing work

To produce a valid transit you must find a **nonce** that makes the finished transaction
hash to a value with at least _K_ trailing zero bits. That much is familiar.

What is different is that the hash covers the **signature**. Changing the nonce changes
the signature, so every single attempt costs one ed25519 signing operation. You cannot
grind hashes cheaply, and there is no shortcut for specialised hardware — the work is
deliberately CPU-bound and roughly equal per core on ordinary machines. A general-purpose
computer is competitive.

This also makes pooling unattractive: the work cannot be split into shares that a pool
operator can verify cheaply, because each attempt requires the miner's own key.

### What you need

* A wallet — but **not a wallet with any tokens in it**. You can start mining from an
  empty one. A transit's only input is the mine output itself, and the **tag-along fee**
  paid to a sequencer comes out of the reward, not out of your balance: of the reward _A_,
  the fee goes to the sequencer and the rest to you. Nothing is required up front. See
  [The `proxi` wallet](participate/proxi.md) for creating the wallet and naming a
  tag-along sequencer.
* Access to a node API — your own [access node](participate/run_access.md), or a public
  one.
* CPU cores. That is the whole of the hardware story.

This is the point of mining in a fair launch: it is the one way into Proxima that does
not ask you to already hold tokens.

### Running the miner

```bash
proxi node mine
```

It runs until you stop it, or until the chain is exhausted. Useful options:

| Flag | Meaning |
|------|---------|
| `--workers N` | Parallel mining workers. Defaults to the number of CPUs. |
| `--count N` | Stop after N transits. Default 0 — keep going. |
| `--fee M` | Tag-along fee in motes, taken out of the reward. Default 0 uses the sequencer minimum; the miner caps it at 1% of the reward. |
| `--stream URL,…` | Additional node endpoints to receive mining transactions from. **Worth setting** — see below. |
| `--no-stream` | Do not subscribe to the stream at all. Slower, and you will usually lose. |
| `--delegate=false` | Only mine and tidy up; do not put the rewards to work. |
| `--compact-at P` | Sweep accumulated payout outputs into one once P have piled up. Default 10. |

### The reward, and how it changes

For roughly the first 45 days the reward _A_ is flat at **375 PROX** per transit. After
slot 379,688 it grows by 462 motes per slot, so a transit mined later is worth slightly
more than one mined earlier.

The ramp is about **how long emission takes**, not about hashrate. However much hashrate
arrives, the retarget holds the chain at its target pace, so transits keep arriving at
roughly the same rate — and at a flat 375 PROX that rate would take more than three years
to mint the remaining supply. The reward grows so that the whole of it is mined in
**roughly fifteen to seventeen months** instead.

### Difficulty, and why waiting helps

The chain carries its current difficulty _B_ in bits. It is seeded at 24 and retargets by
**one bit per transit**, aiming at a target pace of **4 slots** between transits. It
cannot move faster than one bit at a time, so it settles at the target instead of
oscillating around it. It stays inside a band of 10 to 40 bits.

The difficulty a particular transit must actually satisfy depends on how long it has been
since the last one:

> _K_ = max( _B_ − (_M_ − _P_), _E_ )

where _M_ is the gap in slots since the predecessor, _P_ is the minimum pace of 3 slots,
and _E_ is the floor of 10 bits. In words: **the longer the chain has been stuck, the
easier the next transit becomes.** This is what stops the chain from wedging if hashrate
disappears, and it means a lone miner on a quiet network can always make progress.

### Racing fairly

A transit takes many slots to be confirmed, but only about one pace to mine. A miner who
waited for confirmation before starting the next attempt would waste most of its time, so
the miner does not wait — it builds on the best transit it knows about immediately, its
own or someone else's.

That creates a fairness problem. If the only way to learn that a competitor won a step
were to wait for confirmation, then whoever won once would be ahead for longer than it
takes to mine a step — and would keep winning. Proxima closes that gap two ways:

* Nodes **stream mining transactions** to miners as they arrive, so a competitor's win
  reaches you in a gossip hop rather than in a confirmation. Your miner verifies every
  transit it receives from its raw bytes before building on it.
* When two transits compete for the same step, the tie-break is **the most proof of
  work** — never whichever was seen first. Nothing is preferred merely for being yours.

Because the stream matters this much, pass `--stream` with a couple of independent node
endpoints. Subscribing to several means no single node can slow you down by withholding
what it has seen.

### What happens to what you mine

Every confirmed transit leaves a payout output in your wallet. Left alone these
accumulate, and every output is permanent state that every node on the network carries.
So the miner cleans up after itself:

* **Compaction** runs unconditionally: once enough payout outputs have accumulated, they
  are swept into one.
* **Delegation** runs unless you turn it off. Rather than sitting idle, mined tokens are
  delegated to sequencers, where they earn inflation and contribute to consensus. See
  [Delegation](participate/delegate.md).

Both run on their own, and neither slows the mining loop. If you would rather manage the
proceeds yourself, use `--delegate=false`; compaction still runs, because leaving hundreds
of outputs behind imposes a cost on everyone else.
