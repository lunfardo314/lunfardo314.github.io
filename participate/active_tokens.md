# Active tokens

> **Pre-launch notice.** The network is in its centralized pre-launch phase. The founder can
> stop or reset it at any time, without notice. Tokens mined or held on a pre-launch network
> confer no rights, will not be carried over, and cease to exist when the network is reset.
> Nothing is sold and nothing is promised; take part for the exercise. See
> [Please read before taking part](README.md).

Proxima's fair launch hands out the supply through a proof-of-work competition. That part
is well understood, and honestly one of the simplest parts of the whole undertaking. This
page is about what comes after: what to do with tokens once you have them, and why doing
nothing is the one choice that costs you.

## Why passive holding is discouraged

The blockchain stereotype is: you acquire tokens, for example by mining them, and then you
hold them in a wallet.

In Proxima that is allowed too. But it is discouraged, and the mechanism is simple.
PROX tokens earn inflation, but not for doing nothing. They earn it by taking part in the
_cooperative consensus_, which is what keeps the ledger secure. There are two plain ways
to do that:

* [Delegate to a sequencer](participate/delegate.md). Your tokens work for a sequencer,
  which shares the inflation with you. You keep ownership throughout.
* [Run a sequencer](participate/run_sequencer.md). Your tokens contribute to consensus
  directly and earn the full inflation, with no margin paid to anyone.

So rational behaviour means putting your PROX to work. This is no different from the
general rule of finance: keep assets as return-generating capital, not as cash under the
mattress.

**Tokens that do not earn inflation are diluted by those that do.** That is the whole
disincentive. The rate starts at roughly 10% a year and declines slowly and permanently
after that; see [Tokens and supply](overview/2-tokens-and-supply.md).

Like any economic activity, putting tokens to work carries the risk of earning less than
you hoped: a sequencer can underperform or take a larger cut than another. What it does
not carry, by design, is ownership risk. The ledger rules do not let a sequencer take
delegated tokens, and you can take them back, though a delegation may be tied up for a
while before it is released; the [delegation page](participate/delegate.md) explains when.

Proxima assumes that the overwhelming majority of holders respond to this incentive and
contribute to consensus. The undertaking is cooperative: keeping the ledger safe is in
everyone's interest. Free riders exist, but they are a minority, and they pay for it in
dilution.

None of this removes competition. Every participant is a profit-seeking party, so the
prices and the cuts are set by the market. In practice it makes sense to keep only a small
amount in the wallet as pocket change, say 100 PROX, for transaction fees and other running
costs. The rest is better off as working capital.

## What to do with mined tokens

Every mined transaction pays its reward into a separate output in your wallet. If you do
nothing, those outputs pile up: the tokens sit outside consensus and are slowly diluted,
and every output is permanent state that every node on the network has to carry. Mining
without tidying up costs you and costs everyone else.

You can tidy up by hand with `proxi node compact` and `proxi node delegate amount`, or
leave it to `proxi node consolidate`, a background process that sweeps the wallet and
sends what is above a kept minimum to your own sequencer or into delegations. It works
with any mining software, since it only looks at the wallet. How to run and configure it
is on its own page: [The wallet consolidator](participate/consolidate.md).
