# How mining works

> **Pre-launch notice.** The network is in its centralized pre-launch phase. The founder can
> stop or reset it at any time, without notice. Tokens mined or held on a pre-launch network
> confer no rights, will not be carried over, and cease to exist when the network is reset.
> Nothing is sold and nothing is promised; take part for the exercise. See
> [Please read before taking part](README.md).

This page explains how mining works from **library upgrade 6** on, and why it is built the
way it is. It is about the design, not about running the software: for that, see
[Mining](participate/mine.md), [Pluggable nonce seekers](participate/nonce_seeker.md) and
[The wallet consolidator](participate/consolidate.md). What changes at the upgrade, and when,
is on [Library upgrade 6](participate/upgrade6.md).

Mining in Proxima hands out new tokens and does nothing else. It takes no part in
consensus, which token holders reach by cooperating; see
[Cooperative consensus](overview/consensus.md). Why the supply is distributed this way is on
[The fair launch](overview/fair_launch.md).

## The pieces

### The mine chain

There is exactly one **mine chain** on the ledger. At any moment it is a single output, the
**mine output**, which carries three numbers:

- **the remaining reward**: how many tokens are still left to be mined;
- **the difficulty**: how hard the next step is, in bits;
- **a counter of full slots**: how many slots in a row have had a step, used to adjust the
  difficulty.

Nobody owns the mine output. Anyone who follows its rules may spend it.

### The transit

A **transit** is the transaction that moves the mine chain one step forward. It spends the
current mine output, creates the next one with updated numbers, and creates the **reward**,
_A_ tokens, out of nothing. There is at most one step per **slot**, the ledger's unit of
time of about 10 seconds, so miners compete for each step. The reward is 95 PROX at first
and rises later by a fixed schedule, see [Mining](participate/mine.md).

### The miner

The miner is `proxi node mine`, part of the `proxi` wallet. It:

- **watches the mine chain**: nodes stream every new transit to it as it arrives, and it
  checks each one itself from the raw transaction before building on it;
- **builds the transit**: a complete transaction, missing only the number that makes it
  valid, the **nonce**;
- **hands out the search** for that nonce to seekers, its own or external ones;
- **signs the winner**: when a seeker finds a nonce, the miner checks it, signs the
  transaction with your key and sends it to the network. It signs nothing else;
- **places the reward**: it decides before every attempt where the reward goes, by the
  same settings the consolidator reads, and checks afterwards that the sequencer it paid
  really took it.

### Seekers

A **seeker** does the actual work: it tries nonce after nonce until one makes the transit
valid. It knows nothing about Proxima. It receives a job, a string of bytes to hash and the
place where the nonce goes in it, and sends back nonces that solve it. Three are available:

| Seeker | Runs on | Measured speed |
|--------|---------|----------------|
| the miner's own workers (`--workers`) | the CPU, inside `proxi` | about 7.5 million attempts per second per core |
| the Rust seeker | the CPU, as a separate program | about 99 million per second on an 8-core machine |
| the GPU seeker | NVIDIA graphics cards (CUDA) | about 15 billion per second on one RTX 5090 |

The figures are single measurements on one machine each, given only for scale. A version
of the Rust seeker for AMD and Intel graphics cards is to follow.

Since upgrade 6 a seeker **needs no key**. Version 2 of the seeker protocol sends it the
bytes to hash and nothing else, so a seeker can run on a machine you would not trust with
your wallet. The key stays with the miner, which signs.

### Sequencers

**Sequencers** are the nodes that build the ledger state and reach consensus. A transit
enters the ledger when a sequencer **includes** it, which it does by consuming a
**tag-along** of the transit: an output addressed to that sequencer. Tag-alongs are how any
transaction gets included, see
[Getting a transaction included](overview/3-participate.md?id=getting-a-transaction-included-tagging-along).

Several miners usually find a valid transit for the same step. Sequencers do not take the
first one they see. They wait for the **settlement window**, a fixed moment late in each
slot, and then take the best one by a fixed order (see
[Who wins a step](participate/mining_architecture.md?id=who-wins-a-step) below). A sequencer that holds a worse transit than one
addressed to another active sequencer steps aside and leaves the step to that one.

### The consolidator

`proxi node consolidate` is a separate, permanent process of the wallet. The miner places
each new reward; the consolidator looks after everything already placed: it moves
delegations away from sequencers that stopped working for them, folds small delegations
together, and puts plain outputs to work. **Run it on every miner wallet.** A mined token
earns only while it takes part in consensus; why that matters is on
[Put your tokens to work](participate/active_tokens.md), how to run it on
[The wallet consolidator](participate/consolidate.md).

## The work

### The rule

A transit is valid only if **its own transaction ID ends in at least _K_ zero bits**.

A transaction ID is a **hash** of the transaction: a 32-byte fingerprint computed by the
standard function BLAKE2b. Any change to the transaction, however small, gives a completely
different ID, and nobody can tell in advance which change gives which ID. So the only way to
find a transaction whose ID ends in _K_ zero bits is to try: change the nonce, hash, look,
repeat. On average it takes 2 to the power _K_ attempts.

_K_ comes from the difficulty carried on the mine chain:

- **after an empty slot** the difficulty eases by one bit, so a stuck chain gets easier
  with every slot it waits;
- **after 8 full slots in a row** it hardens by one bit;
- it never falls **below 24 bits**, a second or two of work for one CPU core, and never rises
  above 56.

The two sides are unequal on purpose: the difficulty settles where about one slot in nine
is empty, and the chain moves on about once per slot, whatever hashrate shows up.

### Why the transaction ID

The ID is computed from the whole transaction, and that gives the work three properties
for free:

- **It is bound to the signer.** From upgrade 6 the ID includes the identity of the key
  that signs the transaction. Signed by another key, it is another transaction with another
  ID, and the work is lost. A solution cannot be taken over by anyone else.
- **It is bound to the payout.** The ID covers every output: every payee, every amount.
  Change who is paid and the work is gone. A solution cannot be redirected.
- **It cannot be prepared in advance.** The ID covers the mine output being spent, so no
  work can start before that output exists.

And checking the work costs nothing extra: every node computes every transaction's ID anyway.

### Why a plain hash

BLAKE2b is a widely used, well-studied hash function. Choosing it keeps the work simple to
explain and to check, and lets every computer and every graphics card take part. Nothing in
the work is specific to Proxima or to the miner's key: an attempt is one hash, the same for
everybody.

A plain hash also means that graphics cards are far faster than processors, by more than a
hundred times in the measurements above. Whoever had a fast graphics card program first,
and kept it to themselves, would take most rewards while everyone else ran processors. So a
**reference GPU seeker is published** before mining starts under the new rules, and nobody
starts with a private edge. Better programs may follow, as for any hash.

### Why not the shape of another chain's work

Mining chips exist for BLAKE2b, built for other chains. If Proxima's work had exactly the
shape of one of those chains, that whole fleet of chips could turn to Proxima at once, and a
small slice of it would outweigh every other miner. Proxima's work does not have that shape.
Those chips hash a fixed 80-byte header. Here the work is the whole transaction, about 600
bytes, with the nonce at its very end, and the zero bits are counted at the other end of the
hash. No such chip can do it.

## A transit is free in shape

From upgrade 6 the ledger fixes only what the mine chain itself needs:

- **one input**, the mine output, and nothing else;
- **the next mine output** as the transit's first output, with exactly the numbers the rules
  compute;
- **the full reward _A_** created, always;
- **not a sequencer transaction**: a transit is a transaction of its own, which every node
  sees and can rank before its slot is settled.

**Everything else is up to whoever builds the transit**: how many other outputs it has, of
what kind, and how the reward is split among them. The ledger checks them as it checks any
transaction. The ordinary rule that a transaction creates exactly what it spends plus what
it may mint fixes the total: the other outputs together receive exactly _A_.

Because the only input is the mine output, mining needs no tokens: a brand-new, empty wallet
can mine. Nodes accept a transit from a wallet they have never seen as long as it stays
within 32 outputs and 8 KB.

What the free shape allows, with the reward:

| Where the reward goes | How |
|---|---|
| to your own address | a plain output to an address of your choice, such as a cold address while a hot key signs; at least 9.25 PROX, the storage deposit of a plain output |
| into a new delegation | a delegation with you as its owner; see [Delegation](participate/delegate.md) |
| into a delegation you already have | a tag-along to its sequencer carrying a top-up request |
| to your own sequencer | a tag-along to it |
| to several holders | several outputs, each paying one of them |
| a fee to the sequencer that includes it | a tag-along to that sequencer, in any amount |

**A transit must still reach a sequencer.** Nothing in the ledger requires a tag-along,
but a sequencer includes a transit by consuming a tag-along addressed to it. A transit that
pays no active sequencer is unlikely to be included, and it does not hold back the transits
that do. A reward paid to your own sequencer, or as a top-up of your delegation, is itself
that tag-along. A reward paid elsewhere, to an address or into a new delegation, needs a
separate small tag-along as an inclusion fee.

**What the reference miner does.** `proxi node mine` pays the reward as one output, chosen
before every attempt from the profile: the full reward to your own sequencer, if you have
one configured and it is active; otherwise a top-up of one of your delegations, or a new
delegation while you have fewer than your target number; or, if you set a payout address,
a plain output to that address. A new delegation or a payout address adds a tag-along
inclusion fee, the larger of your wallet's tag-along fee and the minimum the sequencer asks.
A transit no longer pays a fixed fee to the sequencer: what a sequencer gets is what the
miner pays. If a sequencer has not taken a reward three slots after its transit, the miner
stops paying it for a while and takes the tag-along back itself once the ledger lets it, 30
slots on. The exact settings are on [Mining](participate/mine.md).

## Pooling

A **pool** lets many miners share the rewards of their combined search, so each is paid
small amounts often instead of a whole reward rarely. Proxima has no pool software, but the
design leaves room for one. **The reference software mines solo.** Everything in this
section is possible under the rules; none of it is built.

Two things make pooling straightforward:

- **The outputs are free and inside the ID.** A pool can build a transit paying its workers
  directly, with several outputs, and no worker can change them: that would change the ID
  and lose the work.
- **Seekers need no key.** A job of the seeker protocol is just bytes to hash, so a pool can
  hand the same kind of job to its workers' machines without giving them its key.

A worker proves how much it searched with **shares**: solutions to the same job at a lower
_K_, which turn up often. Now and then a share also meets the real _K_, and the pool sends it
as the transit.

Some ways a pool could be arranged:

| Arrangement | The reward | Who holds the tokens |
|---|---|---|
| a pool that runs a sequencer | one tag-along of _A_ to the pool's sequencer, which is also its inclusion payment | the pool, on its own chain, until it pays the workers |
| finder plus pool cut | most of it to the worker who found the solution, a tag-along of the cut to the pool | the finder is paid at once; the pool holds only its cut |
| direct payout | outputs to the pool and to the workers who sent shares recently | nobody holds the workers' tokens; a running tally decides who is paid in each transit |

The limits are plain:

- **One job, one set of payees.** Changing any output changes the transaction, so the
  payees of a job are fixed until the pool issues a new one.
- **The signer holds the key.** Whoever builds and signs the transit, usually the pool
  operator, keeps the key; the workers' machines only hash. A tag-along its sequencer does
  not take can be taken back only by the signer, from 30 slots on.
- **Small payments wait.** A plain output must hold at least 9.25 PROX, so a worker owed less
  is paid later, when the tally has grown. A tag-along can pay any amount, but only to a
  chain such as a sequencer or a delegation.
- **Size.** Paying many workers in one transit is bounded by the transaction size, and by
  the 32 outputs nodes accept from a wallet they do not know yet.

## Who wins a step

When several transits compete for the same step, every sequencer and every miner ranks them
the same way:

1. the one for the **older slot** wins: it had to meet a higher difficulty;
2. between transits for the same slot, the one with the **smaller work value** wins, the
   last 8 bytes of its ID read as a number;
3. if those are equal too, the rest of the ID decides.

Nobody can choose these values; they come out of the hash. Sequencers hold competing
transits until the settlement window and then take the best one, so a transit that arrived a
little later is judged by the rule, not by who was seen first or who is closer to a
sequencer. The miner keeps searching until shortly before the settlement window and sends
each solution that beats the best one it knows.

Each contest is therefore a draw that nobody can rig, and the more attempts you make, the
more tickets you hold: **the share of steps you win is your share of the hashrate.**

## Where to go next

- [Mining](participate/mine.md): running the miner.
- [Pluggable nonce seekers](participate/nonce_seeker.md): the Rust and GPU seekers, and the
  protocol for writing your own.
- [The wallet consolidator](participate/consolidate.md): keeping mined tokens at work.
- [Library upgrade 6](participate/upgrade6.md): what changes, and when.
- [Delegation](participate/delegate.md) and [Put your tokens to work](participate/active_tokens.md):
  where mined tokens earn.
