# Library upgrade 6: what to do before 10 November

> **What and when**
>
> * **Release:** v1.6.0, out on Sunday 8 November 2026, about 17:00 UTC.
> * **The new rules start:** at slot 196000, Tuesday 10 November 2026, about 12:03 UTC.
> * **Mining pauses** from that slot for 1,000 slots and resumes at slot 197000, about 14:54 UTC.
> * **Who must act:** everyone. Every node, every wallet, every miner and every other program
>   that signs transactions must run v1.6.0 or later before the slot.
> * **Most urgent:** sequencers holding less than 10,000 PROX of their own, and the people
>   who delegate to them. See [Sequencers](participate/upgrade6.md?id=sequencers) and [Delegators](participate/upgrade6.md?id=delegators).

The rules every transaction must follow are written in the ledger itself, in a set of
definitions called the **library**. A **library upgrade** adds or replaces some of those
definitions from a set slot on (a slot is 10.24 seconds). The network keeps running
across it, and nothing already on the ledger changes; only transactions from the slot on
are checked against the new rules.

A library upgrade cannot be undone. A node on an older release does not know the new
rules, so it stops following the network at the slot. A transaction built by older
software is refused from the slot: nothing is lost, the tokens stay where they are, but
the transaction has to be made again with the new software.

Upgrade 6 changes four things: how a transaction's ID is computed, how mining works, how
often a sequencer may issue transactions, and how much a sequencer must hold of its own.

## What you must do

### Everyone: update before the slot

Update the node (`proxima`) and the wallet (`proxi`) to v1.6.0 or later before slot 196000.
This applies to access nodes, sequencer nodes, wallets used only for sending, and any
program of your own that builds and signs transactions: from the slot, the transaction ID
is computed differently (see [What changes](participate/upgrade6.md?id=what-changes)), and a transaction signed the
old way is refused.

If you build from source, rebuild both programs from the release, as described in
[The `proxi` wallet](participate/proxi.md) and
[Running an access node](participate/run_access.md).

### Miners

* **Update `proxi` before the slot.** The ledger now expects miner version 6. From the slot
  an older `proxi node mine` stops with "update proxi" (see
  [Keeping the miner current](participate/mine.md?id=keeping-the-miner-current)).
* **Update your seeker.** The work the miner searches for is new, so a nonce seeker must be
  the v1.6.0 build. An older seeker gets no work from the new miner.
* **Run the consolidator on every miner wallet.** Start `proxi node consolidate` beside
  `proxi node mine` with the same wallet profile. It moves your delegations away from
  sequencers that can no longer hold them frozen (see [Delegators](participate/upgrade6.md?id=delegators)) and keeps
  the wallet tidy. See [The wallet consolidator](participate/consolidate.md).
* **Nothing to do for the pause.** A v1.6.0 miner started before or during the pause waits
  until slot 197000 by itself.
* Your wallet profile works unchanged. One setting is new and optional, see
  [Mining](participate/upgrade6.md?id=mining) below.

### GPU operators

From the upgrade, mining is plain hashing, and graphics cards (GPUs) do it far faster than
processors. A reference GPU seeker for NVIDIA cards ships with the release, in
`proxi/node_cmd/mine/gpu_seeker/` of the repository, with instructions in its `README.md`.
It holds no key: the miner keeps the key, builds and checks every transaction, and the
seeker only searches. It can therefore run on another machine, reached through an SSH
tunnel. Build it and run its self-test before mining resumes. Seekers for AMD and Intel
cards are expected later. How the miner and seekers fit together is on
[Pluggable nonce seekers](participate/nonce_seeker.md).

### Sequencers

* **Update the node before the slot.** From the slot a sequencer must leave at least
  6 ticks between each of its transactions and the inputs it consumes, instead of 3 (a
  tick is 1/128 of a slot, 80 ms). The v1.6.0 sequencer follows the new rule by itself.
* **Check your own balance.** This is what the sequencer chain holds itself, not counting
  delegations. `proxi node seq info` shows it. Two minimums now apply, explained under
  [Minimum own balance of a sequencer](participate/upgrade6.md?id=minimum-own-balance-of-a-sequencer):
  * **10,000 PROX for every sequencer**, old ones included. Below it a sequencer keeps
    running but can no longer produce branches or freeze new delegations.
  * **5,000 PROX for a sequencer chain started from the slot on**, on its first output and
    on every later one. Chains started before the slot are not affected by this one.

**If your sequencer holds less than 10,000 PROX of its own, decide now.** On 7 November
2026, 59 of the 83 active sequencers were below it, with about 2.1 million PROX of
delegations frozen to them (about 3% of all frozen delegations). Each such operator should
do one of two things before the slot:

1. **Top the chain up above 10,000 PROX**, with some margin. Send the tokens as a
   tag-along to your own sequencer, which takes them into its chain:

   ```
   proxi node send_to_chain <amount in motes> <your sequencer chain ID>
   ```

   (1 PROX = 1,000,000 motes, so 10,000 PROX is 10000000000.)

2. **Or wind the sequencer down.** Stop it freezing new delegations:

   ```
   proxi node seq set-params --max_frozen 0
   ```

   and follow [Shut down a sequencer](participate/run_sequencer.md?id=shut-down-a-sequencer).

   **Keep the node running until your delegations have moved away.** A delegator can ask a
   frozen delegation to be released early, but only a running sequencer can act on the
   request. Once the sequencer stops, its frozen delegations stay frozen, earning nothing,
   until their freeze runs out, up to about 4.3 days later.

A sequencer below 10,000 PROX that keeps running regains everything as soon as its own
balance reaches 10,000 again.

### Delegators

A **delegation** lends your tokens to a sequencer, which **freezes** them for a period and
pays you a share of the inflation in advance (see [Delegation](participate/delegate.md)).
From the slot, a sequencer holding less than 10,000 PROX of its own cannot freeze a
delegation afresh. A delegation frozen at such a sequencer earns until its freeze ends, and
then sits idle unless it is moved.

* **If you run the consolidator** (`proxi node consolidate`), it handles this for you: it
  asks such a sequencer to release your frozen delegations early, and moves them to
  another sequencer once they are free. The request needs a small fee from the wallet's
  own tokens, so keep a little outside your delegations.
* **Otherwise**, check with `proxi node delegate status` where your delegations are, and
  ask for an early release yourself:

  ```
  proxi node delegate askstop <delegation ID>
  ```

  Then delegate the freed tokens again (see
  [Taking your tokens back](participate/delegate.md?id=taking-your-tokens-back)).
* **Do it soon.** An early release works only while the sequencer is still running.
* **New delegations** should go to sequencers holding at least 10,000 PROX. From the slot,
  `proxi node delegate` refuses a smaller one, and the wallet's random choice of a sequencer
  passes such sequencers over.

## What changes

### The transaction ID

Every transaction has an ID, computed from its contents, by which the ledger and everyone
else refers to it. From the slot, the ID commits to the signer and to every element of the
transaction: two transactions that differ in anything, including who signed them, always
have different IDs. This is why every program that signs transactions must be updated.

### Mining

Mining is how most of the supply is issued: there is a single **mine chain** on the
ledger, and each step of it, a **transit**, pays a reward to the miner who finds a valid
proof of work. How mining works, and why, is explained in
[How mining works](participate/mining_architecture.md). What the upgrade changes:

* **The work.** Until now the proof of work was a VRF, a calculation that needs the miner's
  private key. From the upgrade, the work is the mining transaction's own ID: a miner
  varies a number inside the transaction, its **nonce**, until the transaction's ID ends in
  enough zero bits. This is ordinary BLAKE2b hashing, which GPUs do best.
* **The full reward on every transit.** Every transit now mints the full reward (95 PROX
  today).
* **Where the reward goes.** The ledger no longer fixes
  the layouts a reward can take: the miner pays it out as it likes, within the usual rules
  for any transaction. The reference miner places it as before: into your own sequencer,
  as a top-up of one of your delegations, or as a new delegation. To receive the reward as
  plain tokens instead, set the new key `mine.payout_address` in the wallet profile to an
  address (a holder ID, 32 bytes in hex): every reward then goes there, less the fee paid
  to the sequencer that includes the transit.
* **Why the consolidator is now crucial.** This is the biggest practical change for a miner.
  Until now the ledger itself rewarded keeping mined tokens at work: a reward placed into a
  delegation or onto your own sequencer was paid in full, one paid as plain tokens to your
  wallet only a fraction of it. The miner alone was enough to keep rewards working, and the
  consolidator was an optional tidying tool. From the upgrade the ledger pays the full
  reward wherever it goes, so nothing in the rules keeps your tokens at work any more:
  that is now the job of your wallet's software, and the consolidator is the part that does
  it. Run `proxi node consolidate` beside `proxi node mine`, on every mining wallet:
  * it puts tokens that pile up in the wallet to work, into delegations or your own
    sequencer: for instance rewards paid as plain tokens when `mine.payout_address` is the
    wallet's own holder ID (paid to another holder, they are that holder's to put to work);
  * it moves a delegation whose sequencer stopped, now leaves less than the share the
    delegation requires, or can no longer freeze it, to a better one, and folds the
    smallest delegations together when there are more than you set;
  * it moves your delegations off sequencers under 10,000 PROX of their own (see
    [Delegators](participate/upgrade6.md?id=delegators)): it asks such a sequencer to
    release a frozen delegation early and re-delegates it, which works only while that
    sequencer still runs.

  A token left idle earns nothing, while one in a delegation or on a sequencer earns its
  share of the inflation every slot and adds to the weight that keeps the ledger secure.
  See [The wallet consolidator](participate/consolidate.md).
* **The pause.** No transit is accepted for 1,000 slots after the activation, from slot
  196000 to slot 197000, so that every miner and node has moved to the new rules before the
  first transit under them.
* **Difficulty.** The lowest difficulty the ledger allows rises from 10 to 24 bits. After
  the pause the difficulty starts at that floor and rises by one bit for every 8 slots in a
  row that have a transit, until it matches the hashing power of the network. Expect the
  first transits to come easily and the difficulty to climb over the following hour or so.
* **Miner version 6.** Only a miner of version 6 can build a valid transit.

### Sequencer pace

A sequencer must now leave at least 6 ticks, instead of 3, between each of its
transactions and every input it consumes. This means fewer sequencer transactions in the
busy moments right after a new branch. Transactions of ordinary wallets are not affected.

### Minimum own balance of a sequencer

A sequencer's **own balance** is what its chain holds itself, apart from the delegations
frozen to it. The upgrade sets two minimums. Each is a separate value in the ledger, which
a later upgrade may change.

* **5,000 PROX, for new sequencers.** A sequencer chain started at or after slot 196000
  must hold at least 5,000 PROX of its own when it starts and at every later step.
  Sequencers started before the slot are not affected by this minimum.
* **10,000 PROX, for every sequencer.** A sequencer holding less than this of its own:
  * cannot produce branches (a **branch** is the transaction that closes a slot and
    commits a ledger state);
  * cannot issue transactions in the last 25 ticks of a slot, the part reserved for
    building up to the next branch;
  * cannot freeze a delegation afresh.

  It can still issue transactions in the rest of the slot, pick up tag-alongs (outputs that
  users address to a sequencer, such as fees and requests), and top up delegations it
  already holds frozen. It regains everything as soon as its own balance reaches 10,000
  PROX.

## Dates and slots

| Event | Slot | Time (UTC) |
|-------|------|------------|
| Release v1.6.0 | | Sunday 8 November 2026, about 17:00 |
| Upgrade 6 activates; mining pauses | 196000 | Tuesday 10 November 2026, about 12:03 |
| Mining resumes | 197000 | Tuesday 10 November 2026, about 14:54 |
