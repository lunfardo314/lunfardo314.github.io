# Mining

> **Pre-launch notice.** The network is in its centralized pre-launch phase. The founder can
> stop or reset it at any time, without notice. Tokens mined or held on a pre-launch network
> confer no rights, will not be carried over, and cease to exist when the network is reset.
> Nothing is sold and nothing is promised; take part for the exercise. See
> [Please read before taking part](README.md).

Most of Proxima's tokens do not exist yet. At genesis only 6% of the final supply is
created; the other 94% is **mined**, one reward at a time, by anyone who cares to
compete for it. Mining is how a newcomer with no tokens gets tokens.

This page is about running the miner. Why the launch is arranged this way belongs to
[Tokens and supply](overview/2-tokens-and-supply.md) and [The fair launch](overview/fair_launch.md);
here we assume you have decided to take part.

**Proxima is not a proof-of-work network.** The work distributes the supply and nothing
else: it takes no part in the consensus, which is reached by token holders cooperating.
Mining is a temporary role — when the mintable supply runs out the mine chain is dead and
there is no mining in Proxima after that.

## What you are competing for

There is exactly one **mine chain** on the ledger: a single chained output that moves
forward in steps. Each step is a **transit** — a transaction that consumes the current
mine output, produces the next one, and pays a reward _A_ to whoever produced it.

Only one transit can follow any given mine output, so miners race for each step. Winning
a step gives you the reward and nothing else: no fees, no privileged position, no
influence over the next step.

The chain carries a counter of how much remains to be minted. It starts at 940,000,000
PROX and falls with every transit. When it reaches zero, mining is over and the supply is
complete at 1,000,000,000 PROX.

## Key-bound proof of work

To produce a valid transit you must find a **nonce** such that a value derived from it has at
least _K_ trailing zero bits. That much is familiar.

What is different is how the value is derived. It is not a plain hash but the output of a
**verifiable random function** under your own private key, computed over the mine output you
are extending, the target slot and the nonce. For a given key and message there is exactly one
such output, and only the key holder can produce it. So every attempt needs your key, and the
winning transaction carries a short proof that the covenant checks under the key that signed
it. That is what the design buys: the work cannot be pooled or delegated. A pool would have
to hold your key, and with it your reward.

It does not buy independence from hardware. Each attempt is an elliptic-curve computation
that a GPU runs in parallel several times faster than a CPU, and dedicated hardware could go
further. A general-purpose computer can mine, but expect to be outpaced by anyone who brings
a GPU. Difficulty adapts to whatever hashrate shows up.

## What you need

* A wallet — but **not a wallet with any tokens in it**. You can start mining from an
  empty one. A transit's only input is the mine output itself, and the **tag-along fee**
  paid to a sequencer comes out of the reward, not out of your balance: the ledger fixes
  it at exactly **1 PROX** per transit, the same for everybody, and the rest of the reward
  _A_ goes to you. Nothing is required up front. See [The `proxi` wallet](participate/proxi.md)
  for creating the wallet and naming a tag-along sequencer; a sequencer whose minimum fee
  is above 1 PROX never takes a transit, and the default minimum is 0.1 PROX.
* Access to a node API — your own [access node](participate/run_access.md), or a public
  one.
* CPU cores. The `proxi` miner runs on the CPU; a GPU miner is faster, and you are free
  to use one. The search for a nonce can also be handed to a separate program while
  `proxi` keeps doing the rest, see [Pluggable nonce seekers](participate/nonce_seeker.md).
  The miner is the replaceable part of the setup; the consolidator beside it is not, see
  below.

This is the point of mining in a fair launch: it is the one way into Proxima that does
not ask you to already hold tokens.

## Running the miner

One command on the wallet profile:

```bash
proxi node mine
```

It does two things. It mines, and beside the mining loop it runs
[the wallet consolidator](participate/consolidate.md), which sweeps the payouts and puts
them to work: by default it delegates them to a sequencer drawn by rating, and with
`send_to_sequencer: own` in the profile it sends them to your own sequencer instead. The
consolidator's lines appear in the miner's output prefixed `[consolidate]`. Its settings
are the `consolidate` section of the profile, the same ones `proxi node consolidate`
reads; `mine.consolidate: false` in the profile, or `--disable_consolidation` on the
command line, leaves the payouts where they land, for a wallet that runs
`proxi node consolidate` separately or tidies up by hand.

Why the sweep is built in: every transit leaves a separate payout output in your wallet.
Left there, the tokens sit outside consensus and are diluted, and every output is
permanent state that every node on the network carries. **Never leave payouts
unswept for long.**

The two parts are not equally replaceable. **The miner is optional.** `proxi node mine`
is the reference implementation and nothing about it is privileged: an optimized miner, a
GPU miner, or one you write yourself competes on exactly the same terms, since the only
thing that decides anything is whether the transaction is valid. **The consolidator is
not.** It is not a piece of mining software: it is the wallet process that keeps what you
mine in consensus, it works with any miner because it only looks at the wallet, and there
is no reason to replace it with anything else unless you know exactly what you are doing.
Whatever mines for you, if it is not `proxi node mine`, run `proxi node consolidate`
beside it. The one alternative is to [delegate by hand](participate/delegate.md) now and
then, and even then the consolidator earns its keep by folding the payout outputs into one.

The miner runs until you stop it, or until the chain is exhausted. Useful options:

| Flag | Meaning |
|------|---------|
| `--workers N` | Parallel mining workers. Defaults to the number of CPUs. |
| `--max-hashrate-khs X` | Upper limit on the mining speed of this process, all workers together, in thousands of attempts per second (KH/s). Fractions are allowed, e.g. `2.5`. Default 0 — no limit. Use it when the machine has other work to do: the workers pause between attempts, so the processor load drops with the limit. The miner prints its measured speed while it works, which tells you what your machine does without a limit. |
| `--nonce-start N` | First nonce of every round. Default 0 — a fresh random start per round, so several processes mining under one key search different nonces instead of repeating each other. |
| `--count N` | Stop after N transits. Default 0 — keep going. |
| `--stream URL,…` | Additional node endpoints to receive mining transactions from. **Worth setting** — see below. |
| `--no-stream` | Do not subscribe to the stream at all. Slower, and you will usually lose. |
| `--refetch N` | Seconds to mine one target before re-stamping it. Default 0 — adaptive to the measured hashrate. Whatever the window, a round ends when the sequencers start settling its slot, since a solution found later reaches none of them in time. |
| `--disable_consolidation` | Do not run the consolidator beside the miner. Same as `mine.consolidate: false` in the profile. |

The consolidator has no flags of its own on the miner: it is configured by the
`consolidate` section of the profile, exactly as `proxi node consolidate` is. If that
section cannot be used, for example because no tag-along sequencer is set, the miner says
so at start and mines without it.

## Keeping the miner current

The ledger names the miner version it expects, and every transit carries the version of
the miner that built it; a transit from any other version is invalid. When a new release
of the miner is required, that number is raised in the ledger at an announced slot, and
from then on an older `proxi node mine` stops with the message "update proxi", at start
or between two rounds, and the node's mining stream refuses it with the same reason.
Nothing is lost: the payouts already mined stay yours. Update `proxi` and start it again.
If you mine with your own software, read the version from the node's
`ledger_constants` and put it into the mine lock you build, as the reference miner does.

## Faster searching: nonce seekers

Of everything the miner does, only the search for the nonce is work; the rest is
bookkeeping around the mine chain. So the search can be moved out of `proxi` to
external **nonce seekers**: the miner hands them its current target, checks the nonces
they return, and does everything else as before. Proxima ships a reference seeker in
Rust, about twice as fast per core as the miner's own workers; with it built and on the
PATH, `proxi node mine --seeker` starts it beside the miner and wires everything up by
itself. The same interface serves a seeker on another machine, a GPU seeker or one you
write yourself. Configuration, running and the interface are on
[Pluggable nonce seekers](participate/nonce_seeker.md).

## A quiet start

A fresh network opens with the mine chain closed. The ledger carries a start slot, set at
genesis, before which the covenant accepts no transit whatever its proof of work; the
default is **slot 2000, about 5.7 hours** after genesis, time enough for the nodes and
sequencers to be up and settled before the first transit is contested. The miner reads
the start slot from the node, says how long it will wait, and starts its first round a
few slots before it, so that round targets the start slot itself. A standalone developer
ledger opens at slot 0.

Expect the first transit to be a crowd: its gap from genesis relieves the required
difficulty to the floor, so every miner solves it at once, and the one with the smallest
VRF output among those stamped at the start slot wins. It is one reward; from the second
transit on the race is the ordinary one described below.

## The reward, and how it changes

For the first **60 days** the reward _A_ is flat at **95 PROX** per transit. After slot
506,250 it grows by 134 motes per slot, so a transit mined later pays slightly more than
one mined earlier.

At the pace transits actually land, about 1.12 slots each, the whole mintable supply is
mined in about **3.3 million transits** over **roughly 443 days**, with the reward near
530 PROX by the end.

## Difficulty, and why waiting helps

The pace is **one transit per slot**. The chain carries its current difficulty _B_ in
bits, seeded at 24 and kept inside a band of 10 to 56. Every transit retargets it from
the single gap it sees: the chain **hardens by one bit after 8 full slots in a row**,
slots in which a transit landed, and **eases by one bit for every empty slot**. The two
sides are deliberately unequal. A full slot says only that at least one solution came in
time, never how many competed, so a symmetric rule would settle with half the slots
empty; the asymmetric one settles with about one slot in nine empty and a couple of
competing solutions in every full one.

The difficulty a particular transit must actually satisfy depends on how long it has been
since the last one:

> _K_ = max( _B_ − (_M_ − _P_), _E_ )

where _M_ is the gap in slots since the predecessor, _P_ is the minimum pace of 1 slot,
and _E_ is the floor of 10 bits. In words: **the longer the chain has been stuck, the
easier the next transit becomes.** This is what stops the chain from wedging if hashrate
disappears, and it means a lone miner on a quiet network can always make progress.

## Racing fairly

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
* When two transits compete for the same step, every miner and every sequencer rank
  them the same way: the one stamped at the **older slot** wins, because it had to meet
  the higher difficulty, and between equal slots the one with the **smaller VRF output**,
  a value fixed by the key and the message that nobody can choose. Sequencers hold the
  competing transits until a settlement window late in the slot before picking one, so a
  transit that arrives a little later is judged by the rule, not by who was seen first.
  At one transit per slot most contests are between equal slots, so once your miner has
  a solution it keeps grinding for a smaller VRF output while a competitor outranks it
  and the settlement is still ahead, and submits each improvement. Nothing is preferred
  merely for being yours, and your chance of winning a contested step is your share of
  the hashrate, as before.

Because the stream matters this much, pass `--stream` with a couple of independent node
endpoints. Subscribing to several means no single node can slow you down by withholding
what it has seen.

## What happens to what you mine

Every confirmed transit leaves a payout output in your wallet, and that is where the
miner's job ends. What the tokens do next is up to you, and doing nothing is the one
choice that costs you: tokens outside consensus earn no inflation and are diluted by
those that do, and a pile of small outputs is permanent state every node has to carry.
Why that is so is on [Put your tokens to work](participate/active_tokens.md).

Two ways to handle it:

* **Run the consolidator**, as shown above. It sweeps the payouts into delegations, or
  to your own sequencer, and keeps those delegations placed when a sequencer changes its
  price. This is the default and the recommended way; it works with any mining software,
  since it only looks at the wallet.
* **Delegate by hand** with `proxi node delegate amount`, and keep an eye on your
  delegations with `proxi node delegate status`, since a delegation is a standing offer
  at a fixed cut and a sequencer that raises its margin stops freezing it. Even then,
  run the consolidator with `autodelegate: none` so the payout outputs are at least
  folded into one.

Either way, the miner itself never touches a payout once it has landed.
