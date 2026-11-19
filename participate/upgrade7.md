# Library upgrade 7: what to do before 20 November

> **What and when**
>
> * **Release:** v1.7.0, out on Thursday 19 November 2026.
> * **The new rules start:** at slot 283000, Friday 20 November 2026, 19:31 UTC.
> * **Who must act:** every node operator, and above all **sequencer operators**: the branch
>   bonus becomes a market, and a sequencer needs more weight behind it to issue branches.
> * **Delegators and miners:** update `proxi`; the consolidator moves your delegations where
>   they are needed.

The rules every transaction must follow are written in the ledger itself, in a set of
definitions called the **library**. A **library upgrade** adds or replaces some of those
definitions from a set slot on (a slot is 10.24 seconds). The network keeps running across
it, and nothing already on the ledger changes. A node on an older release does not know the
new rules, so it stops following the network at the slot.

Upgrade 7 changes four things: who sets the branch bonus, which sequencers may issue
branches, when a slot's last sequencer transaction may be stamped, and who may add tokens to
a delegation.

## What you must do

### Everyone: update before the slot

Update the node (`proxima`) and the wallet (`proxi`) to v1.7.0 before slot 283000. No
configuration change is needed. If you run several sequencers, restart them one at a time,
waiting until each is producing again. A node configured with `sequencer.version: v2` now
runs `v3`, the only sequencer version left.

To start a new sequencer chain from the slot on, use `proxi` v1.7.0: a chain started with
an older `proxi` is refused.

### Sequencers

* **Choose your branch bonus.** From the slot, each sequencer chooses the bonus its branches
  earn, from 1 mote to 5 PROX (see [The bonus market](participate/upgrade7.md?id=the-bonus-market)).
  Set it in motes (1 PROX = 1,000,000 motes), for example 0.5 PROX:

  ```
  proxi node seq set-params --bonus 500000
  ```

  Without the setting your sequencer asks 5 PROX, the most allowed, and loses nearly every
  tie to a sequencer asking less. `proxi node seq info` shows the bonus your sequencer asks.

* **Check that your sequencer may still issue branches.** It needs either **20,000 PROX of
  its own** on its chain or **100,000 PROX of coverage**: its own balance plus the
  delegations frozen to it. `proxi node seq info` shows both and whether the sequencer
  qualifies (see [Who may issue branches](participate/upgrade7.md?id=who-may-issue-branches)).

* **Other sequencer software:** stop stamping sequencer transactions after tick 119 (a tick
  is 1/128 of a slot, 80 ms). From the slot such transactions are refused. The reference
  sequencer does this by itself.

**If your sequencer holds less than 20,000 PROX of its own and less than 100,000 of
coverage**, it keeps running: it issues milestones, takes tag-alongs and keeps its frozen
delegations until they expire. It no longer issues branches and no longer freezes new
delegations. To get back in, do one of:

1. **Top the chain up to 20,000 PROX** or more, as a tag-along to your own sequencer:

   ```
   proxi node send_to_chain <amount in motes> <your sequencer chain ID>
   ```

2. **Delegate to your own sequencer** from another wallet until its coverage reaches
   100,000 PROX. This keeps the tokens out of the sequencer's hot wallet: the server's key
   can freeze a delegation but cannot take it.

3. **Or merge several small sequencers into one**, winding the others down as described in
   [Shut down a sequencer](participate/run_sequencer.md?id=shut-down-a-sequencer).

### Delegators

* **Update `proxi` before the slot**, above all if you run the consolidator. Its target
  choice and `proxi node delegate` follow the new rules. An older consolidator does not know
  that a sequencer can qualify by coverage: it would ask your delegations at such a sequencer
  to stop, and move them elsewhere.
* Delegations frozen to a sequencer that no longer qualifies stay frozen until they expire
  and earn as before. That sequencer then does not freeze them again. If you run the
  [wallet consolidator](participate/consolidate.md), it moves them to a qualifying sequencer
  by itself.
* **Anyone can now top up your delegation**, for example a mining pool or an exchange paying
  straight into it. The tokens become yours, and nothing about your rights changes.

### Miners

Update `proxi` before the slot: the miner places rewards into delegations, and from the slot
it chooses only sequencers that may freeze them. Nothing else about mining changes.

## What changes

### The bonus market

Until the slot, the branch bonus is a random amount of up to 5 PROX per slot, drawn by the
ledger. From the slot, **each sequencer chooses its own bonus**, from 1 mote to 5 PROX.

When the best branches of a slot have the same coverage, which is the usual case, one of
them must be chosen. Each gets a **lottery number** between 0 and 10 PROX that nobody can
choose, and the bonus it asked for is subtracted from it. The highest result wins. The result
can be negative (a lottery number of 2 with a bonus of 4 gives -2): only the order counts. So:

* asking for **more** gives a bigger prize but a smaller chance to win;
* asking for **less** gives a smaller prize but a better chance.

**Bids are sealed.** Each sequencer commits to its bonus before the slot ends and reveals it
only in its branch, so nobody can wait to see the others' bids before choosing its own.

**Where the bonus settles.** With N sequencers competing, the bonus settles at about
10 / N PROX: about 0.36 PROX with 28 sequencers. More sequencers mean a smaller bonus for
each, so splitting one's capital into many sequencers stops paying. Sequencers start or stop
until the bonus income pays for running the machine. The bonus thus follows what running a
sequencer really costs and the price of the token, instead of a fixed schedule.

Example: a sequencer asking 0.30 PROX that draws 6.20 scores 5.90; one asking 0.05 that
draws 5.50 scores 5.45. The first wins, though it asks six times more.

### Who may issue branches

To **issue branches** and **freeze new delegations**, a sequencer needs either:

* **20,000 PROX of its own** on its chain, or
* **100,000 PROX of coverage**: its own balance plus the delegations frozen to it.

Below both, a sequencer keeps running as described above. Starting a new sequencer chain
still needs 10,000 PROX of its own, as before.

The two ways to qualify suit the usual split between a hot and a cold wallet. A sequencer's
key sits on a server that is always online, so it is sensible to keep there only what is
needed: at most 20,000 PROX, or as little as 10,000 with the rest delegated to the
sequencer from a cold wallet, whose key stays offline.

On 16 November 2026, 28 of the 166 active sequencers qualified. The others held 0.7% of all
frozen delegations, which move to qualifying sequencers as their freezes expire.

### A quiet end of the slot

A sequencer transaction other than a branch may be stamped at tick 119 at the latest. The
last eight ticks of a slot, about two thirds of a second, are left for branches to be built
and spread. Before, a sequencer stamping its last transaction at tick 127 could include
everyone else's, so its branch always covered slightly more and won whatever the lottery
said. With tick 119 the last allowed, the best branches tie, and the lottery of the bonus
market decides between them.

### Topping up anyone's delegation

Anyone can add tokens to any delegation, not only its owner:

```
proxi node delegate topup <amount in motes> --delegation <delegation ID>
```

The tokens become the delegation owner's. The delegation keeps its sequencer and its
terms, and the owner can still stop it and take it out as before. If the sequencer does not
take the request, the payer can take the tokens back after 30 slots. A sequencer accepts
top-ups from 90 PROX up, or from a higher minimum it sets.
