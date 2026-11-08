# Put your tokens to work

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

The miner follows a pattern that runs through all of Proxima: **software that acts on
behalf of a token holder and works to earn that holder as much as it can.** A
sequencer does it with the holder's capital, and so does the miner. Because the ledger
pays for taking part in the cooperative consensus, earning the most for the holder and
keeping the ledger secure turn out to be the same thing. Nobody has to be asked to
cooperate, because cooperating is what pays.

For mining, the rules are set up to make this so. A token in consensus, in a delegation
or on your own sequencer, earns inflation every slot; a token idle in your wallet earns
nothing. Until library upgrade 6 the ledger also paid a mined reward in full only when it
landed in consensus, and only a fraction of it to a plain output. From the upgrade (slot
196000, see [Upgrade 6](participate/upgrade6.md)) every reward is paid in full wherever it
goes, and what it earns afterwards makes the difference.

`proxi node mine` acts on this for you. Before every round it picks where the next reward
goes, whichever pays you most: your own sequencer, a top-up of one of your delegations,
or a new delegation with one of the active sequencers. You end up with a handful of
delegations, each frozen and topped up in place by its sequencer.
Nothing piles up. How the miner decides, and how to steer it, is on
[Mining](participate/mine.md). To mine faster, keep `proxi node mine`
and plug in a faster nonce seeker of your own: that is where all the speed is, and the
miner keeps placing the rewards.

The miner only places new rewards. If a sequencer raises its margin, goes quiet, or
holds too little of its own to freeze delegations, your delegation with it is no longer
frozen and stops earning. So **every mining wallet must also run
[the wallet consolidator](participate/consolidate.md)**, `proxi node consolidate`, beside
the miner. It moves delegations that stopped working, asks small sequencers to release
the delegations they can no longer freeze, folds several delegations into one, and puts
plain outputs above a minimum you choose to work. Any other wallet can run it too, or be
tidied by hand: `proxi node delegate status` shows how your delegations are doing,
`proxi node delegate amount` puts tokens into a delegation and `proxi node compact`
sweeps plain outputs into one.
