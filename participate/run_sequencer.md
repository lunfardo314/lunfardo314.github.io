# Running a sequencer node

A **sequencer** is an optional process that runs *inside* a node. It actively
builds a **sequencer chain** by endorsing/consolidating other sequencers' chains,
by consuming the **tag-along** outputs that users attach to their transactions,
and by consuming **delegated** outputs and freezing them (the frozen amount counts
toward the sequencer's coverage). Pulling those transactions in is how ordinary
transactions reach the ledger, and the tag-along fees plus token inflation are the
sequencer's reward.

Sequencers are profit-seeking, but a sequencer only profits when it **cooperates**
with the others — converging on the ledger state with the biggest coverage. That
emergent cooperation *is* Proxima's decentralized consensus: **sequencers make the
consensus**.

Sequencers are also what keep the network **live**. By proactively issuing
transactions every slot they push the tangle — and the consensus — forward; access
nodes only validate and relay, so without sequencers the ledger would not advance.

- A node that runs a sequencer is a **sequencer node**.
- A node that does not is an **access node** ([Running an access node](participate/run_access.md)).

The node core supports multiple sequencers, but the current version allows **one
sequencer per node**.

> A sequencer is a token holder that puts **its own tokens** to work: its balance is
> its **equity capital** — the owner's own investment in the business, which is both
> what lets it operate and what makes it worth trusting. Nothing is staked, locked up
> or handed to anyone: the tokens stay yours, on your own chain.
>
> The equity is what pays the **delegation advance**: a sequencer advances a
> delegator's share of the inflation up front, so it can only take on as much
> delegated capital as its own balance can afford.
>
> A bigger balance does not by itself make a sequencer more competitive. What
> decides that is how close it sits to the network's *centre of mass*, where mass
> is balance plus frozen coverage and distance is round-trip time — beyond the
> scope of this page. What the balance does show is how much equity the operator has
> committed to providing sequencing services to other token holders — skin in the
> game — which is why delegators and users tend to prefer heavier sequencers.

## Prerequisites

A sequencer runs as part of a normal node, so first get an **access node running
and synced** following [Running an access node](participate/run_access.md). You also need a funded
wallet ([Wallet configuration](participate/wallet_config.md)) — the key that creates the
sequencer chain is the key that controls it.

## Create the sequencer chain origin

This is a **wallet-side** step. From the wallet that holds your tokens:

```
proxi node seq init_genesis <amount> --name <1-6 chars>
```

(`seq` is an alias for `sequencer`.) This builds and submits a normal wallet
transaction whose output is a fresh **sequencer chain origin** holding `<amount>`
tokens, and records the new chain ID in your `proxi.yaml` as
`wallet.sequencer_id`. It does **not** touch `proxima.yaml` — node-side
configuration is a separate, manual step (below).

Leave enough tokens in your wallet, say 100 PROX, for ongoing fees and spending —
don't put your entire balance into the chain. Optional flags seed the chain's initial sequencer
parameters (all default to library values if omitted): `--fee`, `--margin`,
`--greedy`, `--pace`, plus the immutable delegation params `--epoch-slots` and
`--max-frozen-epochs`. These mutable parameters can be changed later on-chain with
`proxi node seq set-params`.

Verify the new chain:

```
proxi node allchains            # list all chains
proxi node seq info <chain ID>  # details of one sequencer chain
```

Or look at it in the browser: every access node serves a **chain explorer** at
`/chain_explorer`, which lists the chained accounts in the latest reliable branch
and lets you filter for sequencers and open yours to see its current output. On
the initial access points that is
[alpha](http://65.21.170.230:8001/chain_explorer) or
[beta](http://79.137.70.25:8001/chain_explorer).

## Configure the sequencer section in `proxima.yaml`

On the node, add a `sequencer` section. The easiest way to get a correct template
is to (re)generate the node config with `proxi config node --sequencer`, which
writes a **disabled** sequencer section already pointing `controller_key_file` at
your wallet key file. Then edit it: set the real `chain_id` and flip `enable` to
`true`.

```yaml
sequencer:
  enable: true
  name: <sequencer name>      # 1-6 chars; shown in logs and on-chain
  chain_id: <chain ID hex>    # the sequencer ID created above (no 0x / $/ prefix)
  controller_key_file: proxima.key
  pace: 12
```

- **`controller_key_file`** must point to the key that controls the chain — the
  same wallet key that ran `init_genesis`. Copy, symlink or encrypt that file as
  you see fit; keep it `chmod 0600`. (`controller_key_file` is **required**; there
  is no inline-key option.)
- **`pace`** is the minimum number of ticks between two consecutive sequencer
  transactions. One tick is 80 ms, so the default/minimum `12` is ≈ 1 second. The
  node clamps any smaller value up to the ledger minimum.
- `enable: false` keeps the node a plain access node.

- **`produce_branches`** is `false` by default: the sequencer does not issue
  branch transactions and does not compete for the branch inflation bonus. It
  still captures chain inflation, services tag-along and delegation freezing, and
  its milestones reach committed state via other sequencers' branches. Opt in
  only if you intend to compete for the bonus and have the CPU and latency
  headroom — a handful of branching sequencers per slot is all the network needs.

The other sequencer options (`max_tag_along_inputs`, `tag_along_drain_rate`,
`max_frozen_delegations`, `logging`, `force_activity`,
`standalone`, …) are documented in
[Node configuration reference](participate/node_config.md).

## (Optional) Encrypt the controller key

For better security, encrypt the controller key file:

```
proxi util key encrypt --file proxima.key
```

This prompts for a passphrase and rewrites the file as an encrypted JSON keystore
(AES-256-GCM, Argon2id key derivation). At node startup the passphrase is read
from the `SEQUENCER_KEY_PASSPHRASE` environment variable; if it is unset, the node
prompts on stdin.

**The interactive prompt is only usable when you start the node by hand.** A node
run as a system service has no terminal to prompt on, so an encrypted key would
simply fail to unlock and the sequencer would not start — see *The controller key
when running as a service* below.

Inspect or verify a key file with:

```
proxi util key info --file proxima.key --verify
```

## Start the node

Start the node as usual:

```
proxima
```

The log shows the sequencer configuration on startup. It typically takes ~10–15
seconds (to fill its tip pool) before the sequencer begins issuing transactions
and earning inflation, including the branch inflation bonus when it wins a branch.

## Point your wallet at your own sequencer

`init_genesis` already set `wallet.sequencer_id` to your chain. With that in
place you can withdraw funds from the running sequencer chain **without stopping
it**:

```
proxi node seq withdraw <amount> [-t <target address>]
```

(The withdrawn amount has to cover the minimum storage deposit of the output it
creates — 9,250,000 motes for a plain address.) It is also smart to set your
wallet's tag-along sequencer to your **own** sequencer in `proxi.yaml`:

```yaml
tag_along:
  sequencer_id: <your sequencer ID>
```

Then the tag-along fees on your own transactions go back to you — making your
transactions effectively fee-less.

## The controller key when running as a service

For production you typically run the node under `systemd` (see
[Running as a systemd service](participate/run_access.md) in the access-node guide). One
caveat applies specifically to the sequencer's controller key:

**Do not encrypt the controller key when the node is controlled by `systemctl`.**
A service started by systemd has no interactive terminal, so the node cannot prompt
for a passphrase on stdin — an encrypted key would simply fail to unlock and the
sequencer would refuse to start. Use a **plaintext** key file, protected by
filesystem permissions (`chmod 0600`, owned by the service user) on a secured host.

If you nonetheless must keep the key encrypted, supply the passphrase
non-interactively in one of two ways:

- set the `SEQUENCER_KEY_PASSPHRASE` environment variable for the service, e.g. via
  a restricted `EnvironmentFile`:

  ```ini
  # in the [Service] section
  EnvironmentFile=/home/proxima/node/.seqpass   # 0600; contains SEQUENCER_KEY_PASSPHRASE=...
  ```

- or place a **passphrase file** named after the key's holder ID, containing the
  passphrase, in the node's working directory.

Note that either method stores the passphrase in plaintext next to the node, which
largely defeats the point of encrypting the key — so on a single dedicated host an
unencrypted, permission-locked key file is usually the simpler and equally
reasonable choice.

## Notes

- **Clock sync matters most here.** A sequencer issues timestamped transactions,
  so keep the node's clock tightly synced to real time (see the clock note in
  [Running an access node](participate/run_access.md)).
- **Logging.** Use the `logger` and `sequencer.logging` options to control how
  much sequencer activity is written, and to a separate file if desired (see
  [Node configuration reference](participate/node_config.md)).
- Everything from the access-node guide (snapshots, sync, browser tools, state
  cleanup, running as a service) applies unchanged — a sequencer node *is* a full
  node that additionally issues transactions.
