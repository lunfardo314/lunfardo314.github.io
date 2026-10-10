# The wallet consolidator

> **Pre-launch notice.** The network is in its centralized pre-launch phase. The founder can
> stop or reset it at any time, without notice. Tokens mined or held on a pre-launch network
> confer no rights, will not be carried over, and cease to exist when the network is reset.
> Nothing is sold and nothing is promised; take part for the exercise. See
> [Please read before taking part](README.md).

Any wallet that receives tokens in many small pieces ends up with a pile of outputs: mine
rewards, incoming payments, fees returned by a sequencer that never took them. Each piece
is permanent state that every node carries, and tokens sitting in a pile earn nothing and
are slowly diluted (see [Put your tokens to work](participate/active_tokens.md)). You can tidy up by
hand: `proxi node compact` sweeps the outputs into one, and `proxi node delegate amount`
puts them to work. For a wallet that keeps receiving, that is not convenient. So there is
a process that does it for you, continuously, in the background. `proxi node mine` runs
it beside the miner by default, so a mining wallet already has it; for any other wallet,
or a miner that is not `proxi`, it is a command of its own:

```
proxi node consolidate
```

The consolidator is a general wallet utility. It only looks at the wallet account, never at
what fills it, so it serves a miner, a shop receiving payments, or anyone who wants a tidy
wallet whose surplus keeps earning. Miners are the common case, and it does not matter which
mining software they use, the official one from the Proxima repository, an optimized one of
their own, or a GPU miner.

**For a miner it is the part that is not optional.** The miner itself can be replaced by any
software that produces valid transits; the consolidator is what keeps the proceeds in
consensus, and it is highly recommended to run it with whatever mines for you. `proxi node
mine` does that on its own unless told not to (`mine.consolidate: false` or
`--disable_consolidation`), with the settings below and its lines prefixed `[consolidate]`
in the miner's output. Replacing it
with something else makes sense only if you know exactly what you are doing, and skipping
it makes sense only if you choose to [delegate by hand](participate/delegate.md) and keep
at it.

> `proxi node mine` only mines and leaves every payout where it lands. The consolidator,
> run beside it on the same wallet profile, is what puts the payouts to work; see
> [Mining](participate/mine.md).

## Running the consolidator

Run it on the wallet profile to keep tidy, and leave it running. Every 10 seconds it
reads the wallet account and, when there is enough to act on, builds one transaction and
submits it. It does not wait for the transaction to settle; the next check sees the
result. A quiet check prints nothing, so a wallet that is already tidy costs nothing.

**What it consumes.** Plain outputs of the wallet, which is what a mine reward or an
incoming payment is, and tag-along fee outputs the wallet once sent to a sequencer that
never took them. Nothing else is touched. It consumes the smallest outputs first, up to a cap per transaction, and
whatever does not fit is picked up on a later pass.

**When it acts.** Two settings decide it. The **threshold**, 300 PROX by default, is the
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
* **into a delegation**, the default: `autodelegate: random` draws an active sequencer on
  every action, `autodelegate: <sequencer ID>` always delegates to that one. How the draw
  and the delegations work is described below;
* **nowhere**: with `autodelegate: none` the tokens stay in the wallet, folded into a
  single output. Better than a pile, but still diluted.

Sending takes precedence over delegating. If the chosen destination cannot be used right
now, for example the target sequencer has not produced anything recently, the consolidator
says so and folds the outputs into one instead. It never silently turns a transfer into a
delegation.

## How it delegates

**A price taker.** A sequencer publishes the share of the inflation it keeps for itself.
The consolidator accepts that: every delegation it makes or renews requires exactly what
its target leaves. It does not read `delegate.minimum_cut`, and a delegation it made is
never refused by its target as unprofitable.

**A random draw biased by a rating.** With `autodelegate: random` the target is drawn
among the sequencers active in the last few slots. The draw is not uniform: the sequencers
are rated on several criteria and the better rated are drawn more often, though every
sequencer leaving delegators anything keeps a chance. The criteria are

* the share of the inflation it leaves delegators (more is better, counted twice);
* its own balance (more is better);
* the ratio of what is delegated to it over its own balance (less is better, so the
  crowded ones are drawn less).

`proxi node seq_rating` prints the current rating and each sequencer's draw chance.

**Two numbers shape the delegation set:** how many delegations to have, and how large
one should be. The defaults are **5 delegations of 10,000 PROX**. The consolidator grows
one delegation to that size before starting the next, up to that number; from then on
it tops up the smallest one. How the tokens are added depends on the delegation's state.
One the wallet can spend right now, because it is not frozen or its freeze has run out,
is re-delegated by the wallet with the added amount, for the tag-along fee. A frozen one
is topped up **through its target**: the consolidator sends the amount to the target
sequencer as a top-up request, and the sequencer adds it to the delegation in place,
within a tick, with the freeze and the share unchanged and your advance on the added
tokens paid up front. A top-up request pays no fee, and a sequencer takes one only from
a minimum amount, 100 PROX unless it set more. If the delegation the rule picks cannot be
reached this pass, because its target is quiet, the amount is under the target's
minimum, or the target now keeps more than the delegation leaves it, the consolidator
falls through to the next delegation in the order, then to a new one, so the payouts
never wait on one delegation.

**It tidies what is already there.** Before sweeping anything, every pass looks at the
delegations the wallet can spend right now and does one of two things, paying the fee
out of the delegation itself:

* with more delegations than the target number, the smallest one is folded into the
  largest one, which is delegated again with the combined balance;
* a delegation whose target has gone quiet, or now keeps more than the delegation
  leaves it (its target refuses to renew it), or is not the sequencer you configured,
  or has sat unfrozen for longer than an epoch, is delegated again to a fresh target;
  one too small to be delegated again on its own is folded into the largest delegation
  the wallet can spend, or, when there is none, ended and its balance returned to the
  wallet, where the next sweep picks it up.

Delegations made by an earlier version of the consolidator, by `proxi node mine`, or by
hand are treated the same way, so a wallet with a pile of small or stalled delegations is
brought to the target count and put back to work without any action on your part.
Frozen delegations are never touched: they are earning, and they belong to their target
until they thaw.

**Configuration.** A section of the wallet profile, created by `proxi config wallet` with
all keys commented and both destinations empty. Every key has a command-line flag of the
same name that overrides it:

```yaml
consolidate:
    # act once the consumable balance exceeds this, in PROX
    threshold_prox: 300
    # balance always kept in the wallet on plain outputs, in PROX
    minimum_balance_prox: 100
    # most outputs one consolidating transaction consumes
    max_inputs: 30
    # fold the outputs into one as soon as this many have piled up, even below the threshold
    compact_at: 10
    # 'own' sends everything above the minimum to wallet.sequencer_id;
    # a sequencer ID sends it to that sequencer; empty leaves it in the wallet
    send_to_sequencer:
    # applies only when send_to_sequencer is empty: 'random' (the default),
    # a sequencer ID, or 'none' to only fold the outputs
    autodelegate: random
    # number of delegations to build up to
    target_delegations: 5
    # size a delegation is grown to before the next one is started, in PROX
    target_delegation_prox: 10000
```

| Key | Flag | Default | Meaning |
|-----|------|---------|---------|
| `threshold_prox` | `--threshold-prox` | 300 | Balance over at least two outputs that triggers a consolidation, in PROX. Must be at least the minimum, and with delegation on, the threshold less the minimum should be at least the 100 PROX a top-up request must carry, or frozen delegations are never topped up; the consolidator warns at startup otherwise. |
| `minimum_balance_prox` | `--minimum-balance-prox` | 100 | Balance kept in the wallet, in PROX. Must be at least the storage deposit of one output, about 9.25 PROX. |
| `max_inputs` | `--max-inputs` | 30 | Outputs one transaction consumes, 2 to 256. |
| `compact_at` | `--compact-at` | 10 | Fold the outputs into one once this many have piled up, even below the threshold. |
| `send_to_sequencer` | `--send-to-sequencer` | empty | `own`, a sequencer ID, or empty. |
| `autodelegate` | `--autodelegate` | `random` | `random`, a sequencer ID, or `none`. Empty reads as `random`. Ignored while `send_to_sequencer` is set. |
| `target_delegations` | `--target-delegations` | 5 | Number of delegations to build up to; beyond it existing ones are topped up, extra ones are folded together. The older name `max_delegations` is still read when this key is absent. |
| `target_delegation_prox` | `--target-delegation-prox` | 10000 | Size a delegation is grown to before the next one is started, in PROX. |

The tag-along fee and its target come from the `tag_along` section of the profile, as for
every other wallet command, and are read again before every transaction, so a sequencer
changing its fee or going quiet does not leave the consolidator building transactions
nobody picks up. `delegate.minimum_cut` is not read: the consolidator takes the cut each
sequencer offers.

**What you see.** At startup a banner with the settings in force: the account, the
minimum, when it acts, the destination and the tag-along target. Then one line per event:
what was consumed, what moved and where, what was kept, and the transaction ID; or why an
action was deferred; or a node error, which is retried on the next pass. Run it with `-v`
to see every output classified and the retries.

**One transaction at a time.** The consolidator remembers the outputs it consumed and
stands still while any of them is still reported in the account. If they are still there
after 3 minutes the transaction is presumed lost and the next pass starts from a fresh
snapshot. This is what keeps it from spending the same outputs twice.
