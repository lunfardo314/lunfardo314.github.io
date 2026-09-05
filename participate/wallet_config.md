# Proxi wallet configuration (`proxi.yaml`)

This document describes the configuration profile read by the `proxi` CLI wallet
(`proxi.yaml`). Every tag below was verified against its `viper.Get*` read-site
in the code, so the defaults and semantics reflect the actual implementation.

`proxi` is a simple CLI front end for the Proxima network, intended mostly for
admin tasks and as a demo. Most commands build and sign transactions and talk to
a node over the HTTP API (configured by `api.node_url`). The exception is the
`proxi db …` family, which opens a local BadgerDB directly and does not use this
profile's API settings. The node itself is configured separately — see
[`node_config.md`](participate/node_config.md) for `proxima.yaml`.

## File location and profile selection

- `proxi` loads a profile named **`proxi.yaml`** from the current working
  directory by default.
- The `--config <name>` / `-c <name>` global flag selects a different profile:
  `proxi -c mywallet …` loads `./mywallet.yaml`. (Default name: `proxi`.)
- Environment variables are also read (viper `AutomaticEnv`), so any tag can be
  overridden by its upper-cased env var.
- A profile is created with `proxi config wallet` (see below).

> This file documents the **wallet profile** only. For node (`proxima.yaml`)
> configuration see [`node_config.md`](participate/node_config.md).

## Quick reference

| Tag | Type | Purpose                                                         |
|-----|------|-----------------------------------------------------------------|
| `default_sequencer_id` | hex chain ID | Fallback sequencer used when own / tag-along sequencer is unset |
| `wallet.key_file` | path | Keystore (`.key`) file holding the wallet's private key         |
| `wallet.holder_id` | hex | Optional consistency check against the key file                 |
| `wallet.sequencer_id` | hex chain ID | Sequencer controlled by this wallet (for `seq withdraw` etc)    |
| `api.node_url` | URL | Base URL of the node API `proxi` talks to (legacy name: `api.endpoint`) |
| `api.timeout_sec` | int | Optional HTTP client timeout (seconds)                          |
| `tag_along.fee` | uint64 | Preferred tag-along fee; the sequencer's declared minimum wins if larger |
| `tag_along.sequencer_id` | hex chain ID or `random` | Tag-along sequencer (`random` = pick an active one; falls back to default only when unset) |
| `delegate.minimum_cut` | uint (promille) | Delegator cut this wallet requires from a delegation target. Default `900` |

---

## `default_sequencer_id`

Top-level tag. A hex-encoded chain ID used as the fallback sequencer whenever a
more specific sequencer is not configured — both `wallet.sequencer_id` and
`tag_along.sequencer_id` fall back to it. Read by `GetDefaultSequencerID`
(`proxi/glb/profile.go`); an invalid value is treated as "unset".

`proxi config wallet` seeds this with the **bootstrap sequencer ID**
(`ledger.BoostrapSequencerIDHex`,
`50726f78696d612e626f6f7473747261702e636861696e2e`).

```yaml
default_sequencer_id: 50726f78696d612e626f6f7473747261702e636861696e2e
```

---

## `wallet.*`

The wallet account: its key file, an optional holder-ID check, and the
sequencer it controls.

| Tag | Type | Default | Description |
|-----|------|---------|-------------|
| `wallet.key_file` | path | `proxima.key` (when created via `proxi config wallet`) | Path to the JSON keystore (`.key`) file holding the wallet's ED25519 private key. Loaded (and decrypted if needed) by `GetPrivateKey`. Managed with `proxi util key` (below). |
| `wallet.holder_id` | hex | "" (no check) | If set, `proxi` asserts it matches the holder ID derived from the key file's public key, failing fast on a mismatched key/profile. Read by `GetWalletData`. |
| `wallet.sequencer_id` | hex chain ID | "" (→ `default_sequencer_id`) | The sequencer chain controlled by this wallet's key. Used e.g. by `proxi node seq withdraw` to pull tokens off the sequencer chain. If empty, falls back to `default_sequencer_id`. Written by `proxi node seq init_genesis` when it creates the chain; `proxi config wallet` leaves it commented out. Read by `GetOwnSequencerID`. |

The holder ID is `hex(blake2b(sigType || publicKey))` — the same value the
keystore stores as `holder_id`.

```yaml
wallet:
  key_file: proxima.key
  holder_id: 7d3142a5af76d4be9de683d8f492dce2110936d553415102be768cf4df8cacc1
  # sequencer_id: <own sequencer ID>
```

---

## `api`

How `proxi` reaches the node's REST API.

| Tag | Type | Default | Description |
|-----|------|---------|-------------|
| `api.node_url` | URL | (required) | Base URL of the node API, e.g. `http://127.0.0.1:8000`. Must point at the node's `api.port` (see [`node_config.md` § `api`](participate/node_config.md)). Overridable per-command via the `--api.node_url` flag on `node`/`snapshot` subcommands. |
| `api.endpoint` | URL | — | Legacy name of `api.node_url`, still read (and still accepted as `--api.endpoint`) so existing profiles keep working. `api.node_url` wins if both are set. |
| `api.timeout_sec` | int | (client default) | HTTP client timeout in seconds. Only applied when `> 0`; otherwise the client default is used. Not written by `proxi config wallet` — add it manually if needed. |

```yaml
api:
  node_url: http://127.0.0.1:8000
  # timeout_sec: 30
```

> Cross-reference: `api.node_url`'s port must equal the node's `api.port`
> (`proxima.yaml`). On the launch phase network, sequencer nodes serve the API on
> `:8000` and access nodes on `:8001`.

---

## `tag_along`

Outgoing transactions reach a sequencer's backlog via a small **tag-along**
output (fee). Only one tag-along sequencer is supported at a time.

| Tag | Type | Default | Description |
|-----|------|---------|-------------|
| `tag_along.fee` | uint64 | `1` (template) | *Preferred* fee, not the price paid. See below. Read by `GetTagAlongFee`. |
| `tag_along.sequencer_id` | hex chain ID or `random` | `random` (template) | Sequencer that should pick up the transaction. `random` picks one that is currently active. Empty falls back to `default_sequencer_id`. Read by `GetTagAlongSequencerID`, which also validates (via the node) that an explicitly named ID is a live sequencer chain. |

```yaml
tag_along:
  fee: 1
  sequencer_id: random
```

### The fee is a floor, not the price

Every sequencer publishes a **minimum tag-along fee** in its on-chain sequencer
data. Its own operator sets it with `proxi node seq set-params --fee`; anyone can
read it with `proxi node delegate target_info <sequencer ID>`. A transaction
paying less than that minimum is refused by the target: it is dropped at the door
of the sequencer's backlog and never sequenced.

So the fee actually attached is:

```
fee paid = max(tag_along.fee, minimum fee declared by the target sequencer)
```

`tag_along.fee` is therefore only a *preference*, and it has an effect just when
it is the larger of the two. Raise it above the sequencer's minimum to outbid
other senders — a sequencer consumes its backlog biggest-fee-first — and leave
it alone otherwise. Every `proxi` command that builds a tag-along resolves the
figure this way, so no command can underpay a sequencer by relying on a stale
profile.

If the target sequencer cannot be read, the command fails rather than falling
back to `tag_along.fee`: a transaction built on a guessed fee would be ignored
by the sequencer and would look lost rather than rejected.

### `sequencer_id: random`

Instead of a chain ID, `tag_along.sequencer_id` accepts the literal string
`random`:

```yaml
tag_along:
  sequencer_id: random
```

This is a **complete specification of the target**, not an absent one — it never
falls back to `default_sequencer_id`. `proxi` picks uniformly among the
sequencers that are currently **active**, meaning their latest known milestone
is no more than one slot old, and fails with an error when none is:

```
no sequencer has been active in the last 1 slot(s): cannot pick a tag-along target at random
```

That is the point of the setting: naming a fixed sequencer that has since gone
quiet gets your transactions silently ignored, whereas `random` either finds a
live target or tells you the network has none.

Notes:

- Activity is judged in **ledger time** (the slot of the sequencer's latest
  milestone against the current slot), not by how recently the node happened to
  hear from it.
- The choice is made **once per `proxi` run** and reused for the whole command,
  so a command that prices the fee and then builds the output cannot end up
  addressing two different sequencers. Consecutive commands may well pick
  different sequencers.
- The candidate list comes from the node's own view of live sequencers
  (`/api/v1/last_known_milestones`), so `random` cannot be resolved offline.
  Display-only commands such as `proxi wallet` report the setting rather than
  resolving it.

---

## `delegate`

What this wallet requires of a sequencer it delegates to.

| Tag | Type | Default | Description |
|-----|------|---------|-------------|
| `delegate.minimum_cut` | uint, promille (0–1000) | `900` (`DefaultMinimumDelegatorCut`; the template writes it explicitly) | The share of a delegation's inflation that must go to the delegator, the rest being the target sequencer's own cut. Read by `GetMinimumDelegatorCut`; a value above 1000 is an error. |

```yaml
delegate:
  minimum_cut: 900
```

It is the default of the `--cut` / `--minimum_cut` flags of `proxi node dlg`, and
the floor `proxi node mine` applies when it picks a delegation target on its own.
A sequencer whose own cut would leave the delegator less than this refuses the
delegation, so setting it too high can leave the miner with no eligible target —
in which case automatic delegation stops and the miner reports the widest cut the
network currently offers. See [Mining](participate/mine.md).

---

## Generating a wallet profile: `proxi config wallet`

```
proxi config wallet [<profile name>]      # default name: proxi → proxi.yaml
```

Writes a new `<name>.yaml` profile (refuses to overwrite an existing one) and
ensures a key file exists:

1. **Key file** — if `proxima.key` already exists, offers to reuse it; otherwise
   generates an ED25519 key from system entropy and optionally encrypts it with
   a passphrase.
2. **Profile** — renders the template (`proxi/config_cmd/wallet_profile.template`)
   with:
   - `wallet.key_file: proxima.key`
   - `wallet.holder_id:` derived from the generated/loaded key
   - `default_sequencer_id:` set to the bootstrap sequencer ID, and
     `wallet.sequencer_id:` left commented out
   - `api.node_url: http://127.0.0.1:8000`, plus the public nodes as commented hints
   - `tag_along.fee: 1` and `tag_along.sequencer_id: random`
   - `delegate.minimum_cut: 900`

The file is written with `0600` permissions. Explanatory comments are included
only when the command is run verbosely (`-v`).

### Generated profile example

```yaml
# Proxi wallet profile

default_sequencer_id: 50726f78696d612e626f6f7473747261702e636861696e2e

wallet:
    key_file: proxima.key
    holder_id: <derived holder ID hex>
    # sequencer_id: <own sequencer ID>
api:
    node_url: http://127.0.0.1:8000
    # hloc0: http://65.21.170.230:8001
    # oseq1: http://79.137.70.25:8001

tag_along:
    fee: 1
    sequencer_id: random

delegate:
    minimum_cut: 900
```

The commented API endpoints are the public access points a wallet is pointed at.
A node can be a static peer and a sync source without being one of them, so
`proxima.yaml` may list more nodes than this.

Out of the box the profile therefore tags along to whichever sequencer is
active, at whatever fee that sequencer requires. Replace `random` with a chain
ID to always use the same sequencer.

> Cross-reference: when you run `proxi config node --standalone`/`--sequencer`,
> the node's `sequencer.controller_key_file` is filled from this profile's
> `wallet.key_file` (or the default `proxima.key`). See
> [`node_config.md` § Generating a starting config](participate/node_config.md).

---

## Key management: `proxi util key`

The key file referenced by `wallet.key_file` is a JSON keystore holding an
ED25519 key (optionally encrypted with Argon2id + AES-256-GCM). Subcommands:

| Command | Purpose | Key flags |
|---------|---------|-----------|
| `proxi util key generate` | Generate a new ED25519 key pair into a `.key` file (from system entropy). | `--output`/`-o` (default `proxima.key`), `--encrypt`, `--hint` |
| `proxi util key encrypt` | Encrypt an existing unencrypted `.key` file with a passphrase. | `--file` (default `proxima.key`), `--hint` |
| `proxi util key decrypt` | Decrypt an encrypted `.key` file back to plaintext. | `--file` (default `proxima.key`) |
| `proxi util key info` | Print key-file metadata (version, type, encrypted, holder ID); `--verify` checks the private key matches the public key. | `--file` (default `proxima.key`), `--verify` |

Keystore fields: `version`, `key_type` (0 = ED25519), `public_key`, `holder_id`
(`hex(blake2b(sigType || publicKey))`), `private_key`, and — when encrypted —
the KDF/cipher parameters plus an optional `hint`.

### Passphrase for encrypted keys

When a command needs the private key from an encrypted file, `proxi` looks for
the passphrase in this order:
1. `PROXIMA_KEY_PASSPHRASE` environment variable;
2. interactive stdin prompt.

The decrypted key is cached for the lifetime of the (short-lived) `proxi`
process, so each command prompts at most once.

> Cross-reference: on a **node**, the sequencer's controller key is loaded from
> `sequencer.controller_key_file` and uses the `SEQUENCER_KEY_PASSPHRASE` env
> var instead. See [`node_config.md` § `sequencer`](participate/node_config.md).

---

## Related global flags

These are command-line flags, not profile tags, but they affect how `proxi`
uses the profile:

| Flag | Effect |
|------|--------|
| `--config <name>` / `-c` | Load profile `<name>.yaml` instead of `proxi.yaml`. |
| `--target <lock>` / `-t` | Override the destination lock (EasyFL source); defaults to the wallet's own account. |
| `--force` / `-f` | Bypass yes/no confirmation prompts. |
| `--nowait` / `-n` | (node subcommands) Submit without waiting for ledger inclusion. |
| `--verbose` / `-v`, `--v2` / `-2` | Verbosity level 1 / 2. |

A couple of subcommands take a YAML/flag input that is *not* part of the wallet
profile: `proxi node fund --targets <file>` (default `distribute.yaml`) reads a
list of `{target, amount}` entries for a multi-output send.
