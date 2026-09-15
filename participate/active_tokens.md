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

You can always tidy up by hand: `proxi node compact` sweeps the outputs into one, and
`proxi node delegate amount` puts them to work. For many miners that is not convenient.
So there is a command that does it for you, continuously, in the background:

```
proxi node consolidate
```

It does not matter which mining software you use, the official one from the Proxima
repository or an optimized one of your own. The consolidator never looks at the miner; it
only looks at the wallet, so it works either way.

> The official `proxi node mine` still tidies up its own payouts. Do not run the
> consolidator beside it on the same wallet until that built-in tidy-up has been retired,
> since two processes spending the same outputs get in each other's way.

## Running the consolidator

Run it on the same wallet profile as your miner, and leave it running. Every 10 seconds it
reads the wallet account and, when there is enough to act on, builds one transaction and
submits it. It does not wait for the transaction to settle; the next check sees the
result. A quiet check prints nothing, so a wallet that is already tidy costs nothing.

**What it consumes.** Plain outputs of the wallet, which is what a mine reward is, and
tag-along fee outputs the wallet once sent to a sequencer that never took them. Nothing
else is touched. It consumes the smallest outputs first, up to a cap per transaction, and
whatever does not fit is picked up on a later pass.

**When it acts.** Two settings decide it. The **threshold**, 1000 PROX by default, is the
balance worth acting on: the consolidator acts once the consumable outputs hold more than
that and there are at least two of them, since one large output is not scattered and is
left alone. Independently of the balance, it acts once a set number of outputs have piled
up, 10 by default, whatever they hold; in that case it only folds them into one output and
nothing leaves the wallet.

The **minimum balance**, 100 PROX by default, is the pocket change above: the wallet
always keeps that much on plain outputs, and only what is above it moves.

**Where the tokens go.** Everything above the minimum goes to one of three places,
chosen in the wallet profile:

* **to your own sequencer**, if you run one: `send_to_sequencer: own`. The tokens join the
  sequencer's capital and earn inflation without a cut. Before each transfer the
  consolidator checks that the sequencer is really controlled by this wallet and is
  currently active;
* **into a delegation**: `autodelegate: random` draws an active sequencer at random on
  every action, so your tokens spread across sequencers, and `autodelegate: <sequencer ID>`
  always delegates to that one. Up to `max_delegations` delegations are created; at the cap
  an existing one is topped up instead;
* **nowhere**: with both settings empty the tokens stay in the wallet, folded into a single
  output. Better than a pile, but still diluted, so set one of the two above.

Sending takes precedence over delegating. If the chosen destination cannot be used right
now, for example the target sequencer has not produced anything recently, the consolidator
says so and folds the outputs into one instead. It never silently turns a transfer into a
delegation.

**Configuration.** A section of the wallet profile, created by `proxi config wallet` with
all keys commented and both destinations empty. Every key has a command-line flag of the
same name that overrides it:

```yaml
consolidate:
    # act once the consumable balance exceeds this, in PROX
    threshold_prox: 1000
    # balance always kept in the wallet on plain outputs, in PROX
    minimum_balance_prox: 100
    # most outputs one consolidating transaction consumes
    max_inputs: 30
    # fold the outputs into one as soon as this many have piled up, even below the threshold
    compact_at: 10
    # 'own' sends everything above the minimum to wallet.sequencer_id;
    # a sequencer ID sends it to that sequencer; empty leaves it in the wallet
    send_to_sequencer:
    # applies only when send_to_sequencer is empty: 'random' or a sequencer ID
    autodelegate:
    # cap on your own delegations; at the cap an existing one is topped up
    max_delegations: 10
```

| Key | Flag | Default | Meaning |
|-----|------|---------|---------|
| `threshold_prox` | `--threshold-prox` | 1000 | Balance over at least two outputs that triggers a consolidation, in PROX. Must be at least the minimum. |
| `minimum_balance_prox` | `--minimum-balance-prox` | 100 | Balance kept in the wallet, in PROX. Must be at least the storage deposit of one output, about 9.25 PROX. |
| `max_inputs` | `--max-inputs` | 30 | Outputs one transaction consumes, 2 to 256. |
| `compact_at` | `--compact-at` | 10 | Fold the outputs into one once this many have piled up, even below the threshold. |
| `send_to_sequencer` | `--send-to-sequencer` | empty | `own`, a sequencer ID, or empty. |
| `autodelegate` | `--autodelegate` | empty | `random`, a sequencer ID, or empty. Ignored while `send_to_sequencer` is set. |
| `max_delegations` | `--max-delegations` | 10 | Cap on your own delegations. |

The tag-along fee and its target come from the `tag_along` section of the profile, and the
smallest cut a delegation target must leave you from `delegate.minimum_cut`, as for every
other wallet command. Both are read again before every transaction, so a sequencer changing
its fee or going quiet does not leave the consolidator building transactions nobody picks
up.

**What you see.** At startup a banner with the settings in force: the account, the
minimum, when it acts, the destination and the tag-along target. Then one line per event:
what was consumed, what moved and where, what was kept, and the transaction ID; or why an
action was deferred; or a node error, which is retried on the next pass. Run it with `-v`
to see every output classified and the retries.

**One transaction at a time.** The consolidator remembers the outputs it consumed and
stands still while any of them is still reported in the account. If they are still there
after 3 minutes the transaction is presumed lost and the next pass starts from a fresh
snapshot. This is what keeps it from spending the same outputs twice.
