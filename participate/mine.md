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

## Library upgrade 6: what changes for miners

Library upgrade 6 changes the rules of mining at **slot 196000**, on Tuesday 2026-11-10
at about 12:03 UTC. It ships in release **v1.6.0** of `proxima` and `proxi`. In short:

* **Update before the slot.** From the slot, the ID of every transaction includes the key
  that signs it. Every wallet, the miner and every tool that signs transactions must be
  the v1.6.0 build or later; an older `proxi` and the old miner stop working at the slot.
  The new release mines by today's rules until then, so update now.
* **Mining pauses for 1,000 slots**, from slot 196000 to slot **197000** (about 14:54 UTC
  the same day). No transit is valid in between; the miner says so and waits.
* **The work becomes plain hashing**, described next, and graphics cards (GPUs) now
  outpace processors (CPUs) by far. A GPU seeker is published with the release.
* **Your profile keeps working unchanged.** One optional key is new,
  `mine.payout_address`, described below.
* **Run [the wallet consolidator](participate/consolidate.md) on every mining wallet.**
  It was optional before. Now it is not: see [below](participate/mine.md?id=run-the-consolidator-beside-the-miner).

What changes for everybody, not only miners, is on
[What changes with upgrade 6](participate/upgrade6.md). How mining works and why it is
built this way is on [How mining works](participate/mining_architecture.md).

## The proof of work

To produce a valid transit you must find a **nonce**, a number you choose, such that a
value derived from it has at least _K_ trailing zero bits. That much is familiar.

From upgrade 6 the value is the transit's own **transaction ID**: a BLAKE2b hash of the
whole transaction, with the nonce in it. The ID covers who signs the transaction and
every output it pays, so a solution belongs to the key that signed it and to the reward
outputs it names: change either and the work is gone. Searching for a nonce needs no key
at all, only the bytes of the transaction, so the search can run on machines that never
see your key.

Hashing is work that graphics cards do very well. One NVIDIA RTX 5090 runs about 15.4
billion attempts per second with the reference GPU seeker; an 8-core CPU machine runs
about 100 million with the reference CPU seeker, under 1% of one such card. A CPU can
still mine, but expect to be outpaced by anyone who brings a GPU. Difficulty adapts to
whatever hashrate shows up.

Until slot 196000 the work is still the older one: the output of a verifiable random
function under your own key, which every attempt needed the key for. The rest of this
page describes the rules from upgrade 6.

## What you need

* A wallet — but **no tokens to start mining**. A transit's only input is the mine
  output itself, so mining needs nothing up front. See
  [The `proxi` wallet](participate/proxi.md) for creating the wallet. Use a **dedicated
  wallet** for mining: the mining key controls everything it mines.
* **A few PROX of the wallet's own** for [the consolidator](participate/consolidate.md),
  which every mining wallet must run. Mining itself does not need them; the consolidator
  pays small request fees out of them. See below for how to get them.
* Access to a node API — your own [access node](participate/run_access.md), or a public
  one.
* Something to search with. `proxi node mine` searches on the CPU by itself. For more
  speed, hand the search to a **nonce seeker**, a separate program for a GPU or a faster
  CPU search, while `proxi` keeps doing the rest; see
  [Pluggable nonce seekers](participate/nonce_seeker.md).

This is the point of mining in a fair launch: it is the one way into Proxima that does
not ask you to already hold tokens.

## Running the miner

One command on the wallet profile:

```bash
proxi node mine
```

It mines, and it puts every reward to work as it is minted, in consensus. From upgrade 6
every transit mints the full reward _A_, 95 PROX today, wherever it goes. The miner
chooses where before every round:

| The reward goes | What lands there | When the miner takes it |
|---|---|---|
| to **your own sequencer** | the full reward | with `consolidate.send_to_sequencer: own`, while that sequencer is active |
| into a **delegation you already have**, as a top-up | the full reward | the default: first the smallest delegation below `consolidate.target_delegation_prox` |
| into a **new delegation** | the reward less an inclusion fee | while you have fewer delegations than `consolidate.target_delegations` |
| to the **payout address** as a plain output | the reward less an inclusion fee | only when `mine.payout_address` is set |

A sequencer includes a transit by taking a payment addressed to it. A reward sent to a
sequencer or into a top-up is that payment already. A new delegation or a plain output is
not, so the transit also pays a small inclusion fee to a sequencer: the larger of
`tag_along.fee` in your profile and the minimum that sequencer asks.

The choice follows the `consolidate` section of the profile, the same settings
`proxi node consolidate` reads: with `send_to_sequencer: own` the full reward goes to your
sequencer while it is active; otherwise it tops up your smallest delegation under
`consolidate.target_delegation_prox`, opens a new one while you have fewer than
`consolidate.target_delegations`, drawn by rating at the cut the sequencer leaves, and
tops up the smallest after that. Each round's log line says which. If the sequencer you
named in `send_to_sequencer` or `autodelegate` is not active, the miner does not wait for
it: it delegates by the draw until it is back, and says so once. A sequencer that cannot
freeze delegations, because it holds less than the minimum balance of upgrade 6, gets no
rewards from the miner.

The miner also checks that each reward it sent was actually taken. If a sequencer has not
taken one within 3 slots, the miner stops choosing it for a while and, once the reward
may be taken back, takes it back itself.

**`mine.payout_address`** is new and optional: a holder ID (32 bytes in hex, the form of
`wallet.holder_id`). When it is set, every reward goes to that holder as a plain output,
for example to a wallet whose key never leaves your own machine. A plain output earns no
inflation and is diluted (see [Put your tokens to work](participate/active_tokens.md)),
so leave it unset unless you want liquid tokens.

The miner follows the common pattern in Proxima: software that acts on behalf of a token
holder and earns that holder as much as it can. Since the ledger pays for taking part in
the cooperative consensus, earning the most for you and keeping the ledger secure are the
same thing.

**Stick to `proxi node mine`, and make it faster with a nonce seeker.** Mining speed is
all in the search for a nonce, and that search is handed to a separate program: the
reference CPU seeker, the reference GPU seeker, or another one. See
[Pluggable nonce seekers](participate/nonce_seeker.md). The rest of what
`proxi node mine` does costs next to nothing, so replacing it gains you no speed. But
that rest matters: it builds, checks and signs every transit, and puts every mined token
into consensus, where it secures the ledger.

The miner runs until you stop it, or until the chain is exhausted. Useful options:

| Flag | Meaning |
|------|---------|
| `--workers N` | Parallel search workers inside the miner. Defaults to the number of CPUs; 0 with `--seeker`. `--workers 0` leaves the whole search to seekers. |
| `--seeker` | Start the reference CPU seeker beside the miner, see [Pluggable nonce seekers](participate/nonce_seeker.md). |
| `--max-hashrate-khs X` | Upper limit on the speed of the miner's own workers, in thousands of attempts per second (KH/s). Fractions are allowed, e.g. `2.5`. Default 0 — no limit. Use it when the machine has other work to do. Seekers are not limited by it. |
| `--nonce-start N` | First nonce of every round. Default 0 — a fresh random start per round, so several processes mining under one key search different nonces instead of repeating each other. |
| `--count N` | Stop after N transits. Default 0 — keep going. |
| `--stream URL,…` | Additional node endpoints to receive mining transactions from, and to send each of your transits to as well. **Worth setting** — see below. |
| `--no-stream` | Do not subscribe to the stream at all. Slower, and you will usually lose. |
| `--refetch N` | No effect since v1.0.2. Still accepted, so older start scripts keep working. |

Where the reward goes has no flags of its own: it follows the `consolidate` section of
the profile and `mine.payout_address`.

## Run the consolidator beside the miner

**Every mining wallet must run [the wallet consolidator](participate/consolidate.md),
`proxi node consolidate`, all the time, beside `proxi node mine`.** That includes a
wallet mining with GPUs. Earlier versions of these pages called it optional for miners;
that no longer holds.

```bash
proxi node mine          # in one terminal or service
proxi node consolidate   # in another, on the same wallet profile
```

The miner places each new reward. The consolidator looks after what the rewards are
already in, and without it a miner's delegations slowly stop earning:

* It re-delegates a delegation whose sequencer stopped, or can no longer freeze it, to a
  sequencer that can. A delegation earns only while it is frozen.
* It folds small delegations together, and sweeps plain outputs into consensus.
* **It moves delegations off small sequencers.** From upgrade 6 a sequencer holding
  less than **10,000 PROX of its own** can no longer freeze delegations, produce
  branches or work in the last ticks of a slot. A delegation already frozen there would
  wait for its freeze to run out. The consolidator does not wait: it asks that sequencer
  to stop the delegation early, and then re-delegates it to a sequencer that can freeze
  it. Asking works only while the small sequencer is still running, so the consolidator
  has to be running now, not later.

It does all this without asking you. For the stop requests it needs a few PROX of the
wallet's own tokens on plain outputs, to pay the request fee. A wallet that has mined
since before upgrade 6 usually has them, from its first reward. A new mining wallet has
none, since every reward goes into consensus: send it a few PROX from another wallet, or
set `mine.payout_address` to the wallet's own holder ID for one reward and then remove
it again. The consolidator keeps `consolidate.minimum_balance_prox` (100 PROX by default)
on plain outputs and puts only what is above it to work.

## Keeping the miner current

The ledger names the miner version it expects, and every transit carries the version of
the miner that built it; a transit from any other version is invalid. Upgrade 6 raises it
to **6**. When a new version is required, an older `proxi node mine` stops with the
message "update proxi", at start or between two rounds, and the node's mining stream
refuses it with the same reason. Nothing is lost: the payouts already mined stay yours.
Update `proxi` and start it again. Rebuild the seekers with each release as well: from
upgrade 6 a seeker must speak the new job format, and an older build gets no jobs.

## Faster searching: nonce seekers

Of everything the miner does, only the search for the nonce is work; the rest is
bookkeeping around the mine chain. So the search can be moved out of `proxi` to
**nonce seekers**: the miner hands them the bytes of its next transit, checks the nonces
they return, and does everything else as before. From upgrade 6 a seeker needs no key.
There are three to choose from:

* the miner's own workers, `--workers N`, on the CPU;
* the reference CPU seeker, in Rust, somewhat faster per core; with it built and on the
  PATH, `proxi node mine --seeker` starts it beside the miner and wires everything up;
* the reference GPU seeker, for NVIDIA cards, about 15.4 billion attempts per second on
  one RTX 5090. A version for AMD and Intel cards is to follow.

Configuration, running a seeker on another machine, and the interface are on
[Pluggable nonce seekers](participate/nonce_seeker.md).

## A quiet start

**The pause of upgrade 6.** Mining stops at slot 196000 and resumes at slot 197000. The
miner reads this from the node and waits. The first transit after the pause has a gap of
1,000 slots behind it, so its difficulty is relieved to the floor of 24 bits (see
below): every miner solves it at once, and the smallest hash among those stamped at the
first open slot wins. From there the difficulty climbs one bit every 8 full slots until it
matches the hashrate, every slot paying one transit meanwhile.

**A fresh network** opens with the mine chain closed. The ledger carries a start slot, set at
genesis, before which the covenant accepts no transit whatever its proof of work; the
default is **slot 2000, about 5.7 hours** after genesis, time enough for the nodes and
sequencers to be up and settled before the first transit is contested. The miner reads
the start slot from the node, says how long it will wait, and starts its first round a
few slots before it, so that round targets the start slot itself. A standalone developer
ledger opens at slot 0.

Expect the first transit to be a crowd: its gap from genesis relieves the required
difficulty to the floor, so every miner solves it at once, and the one with the smallest
work value among those stamped at the start slot wins. It is one reward; from the second
transit on the race is the ordinary one described below.

## The reward, and how it changes

For the first **60 days** the reward _A_ is flat at **95 PROX** per transit. After slot
506,250 it grows by 134 motes per slot, so a transit mined later pays slightly more than
one mined earlier.

From upgrade 6 every transit mints exactly _A_, wherever its reward goes. Before it, a
reward paid into a new delegation or to a plain output minted less.

At the pace transits actually land, about 1.12 slots each, the whole mintable supply is
mined in about **3.3 million transits** over **roughly 443 days**, with the reward near
530 PROX by the end.

## Difficulty, and why waiting helps

The pace is **one transit per slot**. The chain carries its current difficulty _B_ in
bits, kept inside a band of 24 to 56 from upgrade 6 (10 to 56 before it). Every transit retargets it from
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
and _E_ is the floor of 24 bits (10 before upgrade 6). In words: **the longer the chain has been stuck, the
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
  the higher difficulty, and between equal slots the one with the **smaller work value**,
  the hash of the transaction itself, which nobody can choose. Sequencers hold the
  competing transits until a settlement window late in the slot before picking one, so a
  transit that arrives a little later is judged by the rule, not by who was seen first.
  At one transit per slot most contests are between equal slots. So your miner searches
  every slot until about 0.7 seconds before it is settled, not only until its first
  solution: it submits the first one at once, and after that each solution with a
  smaller work value than the best one known, its own or a competitor's. A miner that
  stopped at its first solution would make only a fraction of its draws. Nothing is
  preferred merely for being yours, and since every miner searches the whole slot, your
  chance of winning a contested step is your share of the hashrate.

Because the stream matters this much, pass `--stream` with a couple of independent node
endpoints. Subscribing to several means no single node can slow you down by withholding
what it has seen. Your miner also sends each transit to these nodes, not only to its
own: from a slow connection, a transit sent along one path can reach the sequencers
after the slot is settled.

## What happens to what you mine

Every confirmed transit has already placed its reward: into one of your delegations,
into a new one, or on your own sequencer, as described above. Your wallet holds a
handful of delegations, each frozen and topped up in place by its sequencer, and the few
PROX of its own that the consolidator needs. Why the ledger insists on keeping tokens in
consensus is on [Put your tokens to work](participate/active_tokens.md): tokens outside
consensus earn no inflation and are diluted by those that do, and a pile of small
outputs is permanent state every node has to carry.

A delegation stops earning when its sequencer raises its margin, goes quiet, or holds
too little of its own to freeze it. The miner then stops topping it up, and
[the consolidator](participate/consolidate.md), which runs beside the miner, moves it to
a sequencer that works. `proxi node delegate status` shows what you hold, and
`proxi node delegate askstop` takes a delegation back by hand.

**The mining key controls everything you have mined**: the delegations are owned by it.
Mine with a dedicated wallet, keep the key on a machine you control, and run seekers
anywhere else without it. To move what you have mined to a wallet whose key never leaves
your own machine, see [Keeping the key safe](participate/nonce_seeker.md?id=keeping-the-key-safe).
