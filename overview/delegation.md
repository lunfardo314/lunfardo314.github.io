# Delegation and liveness

The cooperative consensus needs a large majority of the token supply taking part at every
moment. In practice that means most tokens must be *moving* — a chain that stands still
contributes nothing to coverage and earns nothing.

That creates a problem no other ledger has to solve. If Proxima is to have millions of
accounts, and each of them must move its tokens every slot to count, the network would
drown in transactions that exist only to prove the capital is still there.

**Delegation** is the answer, and it rests on a second primitive, **frozen coverage**.
Both are covenants — ledger validity constraints — and both are built on chains.

## The idea

<p style="text-align:center;"><img src="../static/img/delegate.png">

A holder wraps tokens in a chain output — the **delegation output** — locked by the
**delegation lock**, naming a sequencer of their choosing. That sequencer may then
*freeze* the output for a bounded period.

While frozen, the tokens do not move and nobody but the target sequencer can touch the
output, and then only to unfreeze it. But the frozen amount still counts toward the
sequencer's ledger coverage in every slot. The capital participates continuously while
the UTXO is written once per freeze period rather than once per slot.

That is the whole trick, and it is what makes participation by millions of accounts
affordable. Coverage without movement.

## The freeze, and its limits

Three numbers govern the freeze, and all three are **ledger constants, identical for
every sequencer**. None of them is a dial a sequencer can set:

| | |
|---|---|
| A delegation **epoch** | 600 slots, about 1 hour 45 minutes |
| Longest permitted freeze | 60 epochs, about 4 days and 6 hours |
| **Safe revocation window** | 60 slots, about 10 minutes |

Within that ceiling the sequencer chooses how long to freeze each delegation, and
different delegations at the same sequencer will differ. It is not choosing arbitrarily:
it spreads its unfreezes across the epochs available to it, weighted by amount rather
than by count.

The reason is worth stating, because it is not obvious. What matters to a sequencer's
coverage is the *value* released when a freeze ends, not the number of delegations
ending. If a sequencer let its delegations bunch into the same epoch, a large part of the
capital it works with would come unfrozen at one moment — a cliff in its coverage, and a
moment of weakness for the consensus as a whole. Spreading by amount turns the cliff into
a smooth trickle. Epoch boundaries are also staggered between sequencers, so the network
does not release capital in lockstep either.

When a freeze ends, the **safe revocation window** opens: for 60 slots only the owner may
act on the output. The sequencer cannot immediately re-freeze it. That window is what
guarantees the delegator a genuine opportunity to take the funds back.

## The cut, and the advance

The split of the inflation is set by the **inflation cut** — the delegator's share, in
promille, so `1000` is 100%. Each sequencer advertises a **profit margin** it must keep,
and can accept a delegation only if the requested cut still leaves it that margin.
Delegators want a larger cut, sequencers want their margin, and the two settle against
each other in an open market. A delegator who finds a margin too high moves to another
sequencer.

What makes the arrangement attractive is that the sequencer does not pay at the end. It
pays at the **start**. The moment it freezes the delegation it deposits the delegator's
projected share of the whole period into the delegation output — the **advance**.

This inverts the risk you would expect. The delegator holds the return from the first
slot and keeps it whatever happens next: if the sequencer goes offline for the rest of
the period, or the network has a bad week, the money is already theirs. The sequencer
must then earn the advance back, plus its margin, out of the inflation the frozen capital
actually generates. If it earns less than it advanced, it absorbs the difference.

Two consequences follow. A sequencer must hold enough **free balance** to fund the
advances it offers, so one that cannot afford the advance for a given amount and cut
simply will not accept the delegation. And the profit margin is not rent — it is the
price of carrying that risk.

## Getting the tokens back

There are two paths, and they are not equivalent: one is normal and depends on the
sequencer, the other is guaranteed and does not.

### Asking the sequencer — the usual way

While frozen, the delegator can send a signed **stop request** asking the sequencer to
unfreeze early. An honest sequencer does so immediately, and this is how delegations are
ended in practice — nearly all of the time.

It is worth being clear that this path is **not trustless**. A sequencer is a
self-interested party and could ignore the request. What stops it is economics rather
than the ledger: refusing gains a little for a few days and costs it income and
reputation with every delegator watching.

Because the advance was paid up front, releasing early — before the frozen capital has
generated the inflation that repays it — would leave the sequencer out of pocket. So the
stop request carries a calculated **compensation** back to the sequencer, which is what
makes early release fair rather than a way to extract the advance and leave.

The delegator does not need to hold that compensation in their wallet. Whatever their own
tokens do not cover is authorised by a signed **allowance** and comes out of the
delegated balance itself. Early release is therefore always available, whatever the
wallet holds; the wallet need only cover the request's tag-along fee.

### The safe revocation window — the guarantee

The fallback needs no cooperation at all. When the freeze period ends the delegation
unlocks by itself, and for the following 60 slots **only the owner** may act on the
output — the sequencer cannot re-freeze it, and cannot do anything else with it either.

This is the path that matters when a sequencer is offline, unresponsive or hostile. It is
expected to be rare, precisely because the ordinary path works and refusing costs the
sequencer more than it gains. But it is what makes delegation safe *without* trusting
anyone: the worst case is not losing the tokens, it is waiting until the freeze expires.

And waiting is all it costs, because **the return has already been paid**. A sequencer
that goes down, or that ignores a stop request, cannot claw back the advance: it is
sitting in the delegation output, it belongs to the delegator, and no cooperation is
needed to keep it. The delegator waits out the freeze and walks away with the tokens and
the inflation both.

The sequencer, meanwhile, has paid for a period it then failed to earn from. **The whole
risk of being unavailable sits with the sequencer** — which is the point of paying in
advance rather than at the end, and another part of what its margin is charging for.

Underneath both paths sits the covenant. **The sequencer cannot take the tokens** — not
because it would be caught, but because a transaction moving the funds anywhere except
forward along the same chain is not a transaction honest nodes decline. It is not a valid
transaction anywhere, and no arrangement between sequencers could make it one.

## Delegations are permanent state

One consequence deserves stating plainly, because it shapes how delegation should be
used. A delegation is a chain, and a chain persists: its output sits in the ledger state
for as long as the delegation exists, and **every node on the network carries it**.

A delegation output is on the order of half a kilobyte. A few thousand are nothing. A
million of them is over a gigabyte of permanent state on every node, forever.

The cost does not depend on the amount delegated. One delegation holding ten times the
tokens costs the network exactly what a small one does; ten separate delegations cost ten
times as much. So the way to add capital is to **top up a delegation you already have**
rather than to open another. Nothing prevents opening many — it is a matter of not
imposing an avoidable cost on everybody else.

Topping up is not a separate ledger primitive. It is the two mechanisms above run back to
back: if the delegation is frozen it is stopped first, exactly as an early release would
be, and then re-delegated in the same breath with the additional tokens folded in. The
delegator sees one operation; underneath it is an unwind and a fresh delegation on the
same chain, which is why it costs only fees and why the topped-up amount is subject to
the freeze like everything else on the chain.

That also makes topping up cheaper for the delegator than opening a second delegation —
one chain to manage instead of two, and no new chain to pay for.

## What this achieves

* A token holder can put capital to work by choosing a sequencer, and keeps **full
  liquidity** of the delegated funds — comparable to liquid staking in proof-of-stake
  systems, but without handing over control.
* A sequencer counts the coverage of frozen tokens in every slot without moving the UTXO,
  which gives the network **high liveness** and lets participation scale with the number
  of accounts rather than collapse under it.

## Where to go next

- [Taking part](overview/3-participate.md) — delegation set against the other ways in.
- [Tokens and supply](overview/2-tokens-and-supply.md) — what the inflation being shared
  actually is.
- [How transactions work](overview/4-transactions.md) — chains and covenants, the
  machinery underneath this page.
- [The delegation guide](participate/delegate.md) — the commands.
