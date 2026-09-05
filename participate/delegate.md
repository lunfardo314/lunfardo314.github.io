# Delegation

_Delegation_ is a way to take part in Proxima's _cooperative consensus_ and earn
inflation on your tokens **without running a sequencer yourself**.

You hand your tokens to a _sequencer_ of your choice. It uses them to generate inflation
and shares that inflation with you; you keep ownership throughout.

**Your tokens cannot be stolen.** A delegation is a **covenant**: the tokens sit in a
chained account carrying constraints that spell out what each side may do with them, and
every node checks those constraints before accepting a transaction. A transaction that let
the sequencer walk off with your tokens is not one an honest node rejects — it is not a
valid transaction at all, anywhere.

Throughout this page, commands are shown as `proxi node delegate ...`. You can shorten
`delegate` to `dlg`.

## Why delegation exists

Proxima's consensus measures agreement in **ledger coverage** — the token value that has
taken part in building the current state. What it wants is every token participating in
every slot, which literally means moving every token every slot. With a million holders,
a million wallets cannot do that.

Delegation is the answer, and the whole covenant is designed around it, without giving up
anything on security. Delegated tokens are **frozen** for a period, and while frozen they
work as one consolidated balance behind the sequencer, which moves its own chain every slot
and so generates coverage — and inflation — on all of it at once. One sequencer transaction
per slot does the work that would otherwise take a transaction from every holder.

So it is the delegation's **coverage** that takes part in the consensus, slot after slot,
while the tokens themselves are moved only once per freeze period — in practice once every
three or four days. They are not shut away in the meantime: an `askstop` request can be
sent at any moment, and an honest sequencer unfreezes the delegation immediately.

The cost of that consolidation is precise, and worth stating plainly: while the tokens are
frozen, **only the sequencer can unfreeze them**. That single step is the trusted part of
delegation; everything else is enforced by the covenant. Two mechanisms bound it:

* the **inflation advance** pays your share up front, the moment the freeze starts, so a
  sequencer that goes quiet has already paid you;
* the **safe revocation window** after each freeze gives you an interval in which only you
  can act, so tokens cannot be re-frozen out from under you.

What remains is delegation that is trustless as to ownership, with a bounded, temporary
limit on liquidity if a sequencer misbehaves — bounded because the ledger caps how long a
freeze may last.

## How delegated tokens are held

When you delegate, your tokens are placed into a special chained output (a UTXO)
controlled by a **delegation lock**. This output is a _chained account_ that passes back
and forth between you and the sequencer, and the delegation lock is the covenant governing
it.

Concretely, the covenant fixes who may unlock the output and what they may do with it in
each state, that the tokens must stay in the chain when the sequencer touches it, how the
inflation is split, how long a freeze may last, and that the output returns to your sole
control when the freeze ends. The sequencer can generate inflation with your tokens; it
cannot move them anywhere except forward along the same chain.

At any moment a delegation is in one of these states:

* **unlockable by the owner** — you can spend or withdraw it freely.
* **frozen** — the sequencer is currently using it to generate inflation. While frozen,
  only the target sequencer can touch the output, and only to unfreeze it.
* **on hold** — the freeze has ended (or the sequencer released it on request). The
  tokens are yours again; you can end the delegation or continue it.

Behind all of this sits the assumption the cooperative consensus itself rests on: that a
majority of token holders behave rationally. Given that, every transaction is a proof that
the token holders in its past cone acted honestly — a transaction built on dishonest
behaviour does not become part of a state anyone extends. When the assumption fails, the
consensus does not settle on a wrong ledger state; it stalls. Proxima calls this **fair
liveness**, and it is the reason a covenant needs to guard only against theft, not against
every way a sequencer might behave badly.

## Looking at delegations

* `proxi node balance` (or `proxi node balance -v`) shows your holdings and, for each,
  the form it takes — an ordinary output, a delegation output, or a plain chain output —
  together with its current state (`frozen`, `unlockable by the owner`, `on hold`).
* `proxi node allchains -q` lists all sequencers in the network — your possible
  delegation targets.
* `proxi node allchains -l` lists all active delegations in the network.
* `proxi node allchains -o` (add `-v` for detail) lists delegation owners and their
  delegations.
* `proxi node delegate status` lists all delegations controlled by your wallet.
  `proxi node delegate status <delegation ID>` (add `-v` for detail) shows one
  delegation.

To browse rather than query, any node serves a **chain explorer** in the browser at
`/chain_explorer` — for example `http://<node address>:8001/chain_explorer`. It lists the
chained accounts in the latest reliable state and lets you filter by kind, so you can look
at every delegation on the network, or every sequencer, or every token foundry, and open
any one of them to see its current output. Delegations are chained accounts like any
other, which is why they show up there alongside the rest.

## Sharing the inflation: the inflation cut

A delegation produces inflation, and that inflation is split between you and the
sequencer. The split is set by the **inflation cut** — the share that goes to **you**,
the owner.

The cut is given in _promille_ (parts per thousand): `1000` means 100%, `900` means 90%,
and so on. You choose it with the `--cut` flag; the default is `900` (90% to you, the
rest to the sequencer).

Each sequencer advertises a **profit margin**, also in promille — the minimum it wants
to keep for itself. A sequencer can only accept a delegation whose cut leaves it at least
its margin. In other words, the largest cut a sequencer will grant is
`1000 − profit margin`. Ask for more than that and the sequencer rejects the delegation.

### What you actually get: the market dynamics

What you ask for is not always what you are paid. Besides its margin, a sequencer carries
a **`greedy`** flag, off by default, and it decides how the sequencer treats a request for
less than it could give:

* **not greedy** — it pays out everything above its own margin, `1000 − margin`, whatever
  you asked for. Ask for less and you are paid more than you asked.
* **greedy** — it pays exactly what you asked and keeps the rest.

Either way a request above `1000 − margin` is refused as loss-making. So the two
parameters interact like this:

| Sequencer margin | Your `--cut` | `greedy` | Outcome |
|---|---|---|---|
| 100 | 900 | no  | Accepted, you get **900** — the most this sequencer can give. |
| 100 | 900 | yes | Accepted, you get **900**. At the limit the flag changes nothing. |
| 100 | 500 | no  | Accepted, you get **900** — more than you asked for. |
| 100 | 500 | yes | Accepted, you get **500**; the sequencer keeps 500. |
| 100 | 950 | either | **Rejected** — above `1000 − 100`, so it would be loss-making. |
| 0   | 900 | no  | Accepted, you get **1000**: all of the inflation. |
| 0   | 900 | yes | Accepted, you get **900**. |
| 1000 | 0  | either | Accepted, and you get **0**. Any cut above `0` is rejected. |

Two things follow from the table. Asking for a low cut never earns you more, and against a
greedy sequencer it earns you less. And the flag only matters below the limit: ask for
exactly `1000 − margin` and greedy and non-greedy sequencers pay you the same.

Check both numbers before you commit: `proxi node delegate target_info <sequencer ID>`
prints the sequencer's profit margin and its `Greedy` setting.

#### Where the price settles

Nobody sets these numbers from above. A delegator asking a large cut is refused by every
sequencer whose margin cannot cover it; a sequencer holding out for a large margin is
passed over by delegators who do better elsewhere. **The more either side asks, the fewer
counterparties it has** — the same pressure, pointing in opposite directions.

Where it comes to rest depends on how many there are of each. Many delegators competing
for few sequencers lets margins rise; many sequencers competing for the delegations that
exist pushes margins down towards what it actually costs to run one. Asking for a low cut
buys nothing in inflation, but it does widen the field of sequencers that can accept you —
which is what `proxi node delegate amount` trades on when it picks a target for you.

The conclusion is worth stating on its own: **the more decentralized the network becomes,
the less delegation costs the delegator.** More independent sequencers means more
competition for your tokens and a larger share of the inflation left with you. The cheapest
delegation market is the one Proxima is trying to reach anyway.

## The advance: the sequencer pays you up front

To make delegation attractive, the sequencer does not wait until the end to pay your
share. The moment it freezes your tokens, it adds your projected share of the inflation
to the delegation output straight away. This prepayment is called the **delegation
advance** — the sequencer's own investment in your delegation.

So the sequencer carries the risk: if it or the network goes down during the freeze, you
already hold your cut. Its profit margin reflects that risk and its running costs.

The sequencer then earns that money back (plus its margin) from the real inflation the
frozen tokens generate over the freeze period. For this to work the sequencer must
actually hold enough free balance to pay the advance. A sequencer that cannot afford the
advance for the amount and cut you asked for will not take the delegation.

This advance is also why taking your tokens back _early_ may cost you — see "Taking your
tokens back" below.

**Delegation economics is entirely market-driven: delegators want as big cut as possible,
sequencers want their profit, both compete with their peers in the permissionless free market.**

## Checking a sequencer before you delegate

You do not need to delegate blindly. Two commands inspect a target first, and neither
needs your private key:

* `proxi node delegate target_info <sequencer ID>` shows everything about a target: its
  balances and how much it has available for advances, its parameters (profit margin,
  minimum fee), and the current delegation epoch and its boundaries.
* `proxi node delegate estimate <sequencer ID> <amount>` estimates whether that sequencer
  can afford the advance for a given amount and cut. Add `--cut <promille>` to test a
  different cut, or pass amount `0` to ask for the largest delegation the sequencer can
  currently accept.

## Delegating

The simplest form picks a good target for you automatically:

```
proxi node delegate amount <amount>
```

This selects a sequencer at random, weighted so that less-loaded sequencers are more
likely — the preferred default, as it spreads delegations across the network.

To choose the target and terms yourself:

```
proxi node delegate amount <amount> [-q <target sequencer ID>] [--cut <promille>]
```

* `-q` / `--delegation_target` — the sequencer to delegate to.
* `--cut` — your inflation cut in promille (default `900`).

The freeze length is not yours to choose. The sequencer decides how long to freeze each
delegation, within a ceiling fixed by the ledger (see below).

Before sending, `proxi` shows an affordability estimate. If your cut is too high for the
sequencer's margin, or the sequencer cannot afford the advance, it offers a workable
alternative (a lower cut, or a smaller amount) that you can accept or decline.

The command creates the delegation output with your tokens and the delegation lock. A few
slots later the sequencer consumes it, adds the advance, and freezes it.

## The freeze period

While frozen, your tokens work for the sequencer (you already have your cut in your
delegation output). The length of the freeze is measured in **delegation epochs**. Two
things are fixed by the ledger and identical for every sequencer:

* an epoch is **600 slots**, roughly 1 hour 45 minutes;
* a delegation may be frozen for at most **60 epochs**, roughly 4 days and 6 hours.

Within that ceiling, **each freeze is as long as the sequencer chooses**, and different
delegations at the same sequencer will differ. The sequencer is not picking arbitrarily:
it spreads unfreezes out, choosing the epoch that is carrying the least frozen value so
far, and preferring the longest freeze when several are equally light. Leaving all its
delegations to unfreeze in the same epoch would give it a moment where a large part of the
tokens it works with are simultaneously withdrawable, which is bad for the sequencer and
for the stability of the network's consensus.

So there is no per-sequencer freeze setting to compare when picking a target — only the
ledger-wide ceiling, and a scheduling decision the sequencer makes per delegation. Epoch
boundaries are also staggered per sequencer, so different targets freeze and release at
different moments.

## Taking your tokens back

**Whenever the delegation is not frozen** — for example during the 10-minute safe
revocation window that the delegation covenant enforces after every freeze — you can take
your tokens back at any time; the state is `unlockable by the owner`:

```
proxi node killchain <delegation ID>
```

This ends the delegation and returns the whole balance to an ordinary `sigLock` output in
your wallet.

**While it is frozen**, you can ask the sequencer to release it early:

```
proxi node delegate askstop <delegation ID>
```

This sends a securely authenticated stop request. An honest sequencer unfreezes the
delegation right away, moving it to `on hold`. (The shorter alias is
`proxi node delegate stop`.)

Because the sequencer already paid you the advance up front, releasing early before it has
earned that money back would leave it out of pocket. To make the request fair, `askstop`
includes a calculated **compensation** to the sequencer.

You do not need to hold that compensation in your wallet. Whatever your own tokens do not
cover is authorised as a signed **allowance** and comes out of the delegated balance
itself — so an early release is always available to you, whatever your wallet balance.
All your wallet must cover is the request's tag-along fee. `askstop` prints the split
before it sends anything.

A sequencer could ignore the request — this is the trusted step described above — but
doing so only delays its own inflation and costs it delegators.

In every case, the delegation **auto-unlocks the moment the freeze period ends**. Right
after that there is a **safe revocation window** of 60 slots (about 10 minutes) during
which only you, the owner, can act on the tokens — this prevents the sequencer from
immediately re-freezing them, guaranteeing you a chance to do as you wish.

## After unfreezing: end or continue

Whenever the delegation is not frozen (`unlockable by the owner` or `on hold`) you can:

* **End it** — `proxi node killchain <delegation ID>` returns all the funds to an ordinary
  address-locked output in your wallet.
* **Continue it** — `proxi node delegate chain <delegation ID> [--cut <promille>]
  [-q <sequencer ID>] [--add <amount>]` re-delegates the same chain to the same or a
  different sequencer, optionally moving more tokens in at the same time.

## Adding to a delegation you already have

If you have more tokens to delegate, you can put them into an existing delegation instead
of creating another one:

```
proxi node delegate topup [--delegation <delegation ID>]
```

Without `--delegation` it tops up the smallest delegation you can currently act on. The
same thing is available as `--add <amount>` on `delegate chain` when you are continuing a
delegation anyway.

**Prefer this to creating another delegation.** Every delegation is a chained output that
lives in the ledger state forever, and every node on the network carries that state for as
long as it exists. One delegation holding ten times the tokens costs the network the same
as one holding a tenth; ten separate delegations cost ten times as much. Nothing stops you
from creating many — it is a matter of not imposing an avoidable cost on everyone else,
and topping up is cheaper for you too, since it is one transaction rather than a new chain.

Topping up is a plain unwind-and-redelegate under the covers, so it costs only fees. Note
that freshly added tokens are subject to the freeze like the rest.

If you mine, the miner does this for you: it delegates its payouts automatically and, once
it is holding its configured number of delegations, tops up an existing one rather than
starting another. See [Mining](participate/mine.md).
