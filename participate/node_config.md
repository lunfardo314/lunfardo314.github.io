# Proxima node configuration (`proxima.yaml`)

This document describes every YAML configuration tag read by the Proxima node
(`proxima` binary). It is extracted from the code that consumes the keys
(`viper.Get*` calls), so the defaults and semantics below reflect the actual
implementation.

## File location and format

- The node reads a single file named **`proxima.yaml`** from its **current
  working directory** (`viper.SetConfigName("proxima")`, type `yaml`,
  path `.`). The node must be started from the directory that contains it.
- A starting template can be generated with `proxi config node` (optionally with
  `--sequencer` or `--standalone`). The template lives at
  `proxi/config_cmd/node_config.template`.
- The companion `.snapshot` file (for first-start DB restore) is also looked up
  relative to the working directory (see `snapshot.directory`).

> This file documents the **node** config only. The `proxi` CLI wallet reads a
> separate `proxi.yaml` profile (`wallet.*`, `api.node_url`, `tag_along.*`, …),
> documented in [`wallet_config.md`](participate/wallet_config.md).

## Quick reference

| Section | Purpose | Required |
|---------|---------|----------|
| `peering` | libp2p host identity + static/dynamic peers | yes |
| `api` | REST/WebSocket API server (incl. `api.dag_streaming.*` and `api.mining_streaming.*` feeds) | no (enabled by default) |
| `sequencer` | optional sequencer process | no |
| `snapshot` | periodic state snapshot creation | no (disabled) |
| `snapshot_restore` | periodic self-restart + restore (state cleanup) | no (disabled) |
| `sources` | trusted node API endpoints, used by both forward-sync and snapshot download | no |
| `sync` | forward-sync tuning (activation is governed by `sources`) | no |
| `logger` | log output, verbosity, per-topic overrides | no |
| `metrics` | Prometheus metrics endpoint | no (disabled) |
| `pprof` | Go pprof HTTP server | no (disabled) |
| `txlogger` | per-transaction event logger | no (disabled) |
| `memory` | soft GC memory limit + watchdog | no (disabled) |
| `health_relief` | coordinated relaxation of the healthy-branch threshold | no |
| `trace_tags` | runtime trace tags for debugging | no |
| `transaction_pull` | missing-tx pull retry tuning | no |
| top-level flags | `disable_slicepool`, `disable_deadlock_catcher`, `suppress_coverage_contribution_lower_bound`, `workflow.*`, `debug.*` | no |

---

## `peering`

P2P networking via libp2p. See https://docs.libp2p.io/concepts/fundamentals/addressing/
for multiaddr syntax.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `peering.host.id_private_key` | hex string | (required) | 64-byte ed25519 host private key, hex-encoded. **Not** a token key — identifies the libp2p host only. |
| `peering.host.id` | string | (required) | libp2p peer ID derived from the host public key. Must match `id_private_key` or the node refuses to start. |
| `peering.host.port` | int | (required, non-zero) | UDP/QUIC port other peers connect to. |
| `peering.host.external_addresses` | list of IP | empty | Public IPs this node advertises itself at (on the peering port). Needed only behind NAT / port mapping, where the public IP is on no local interface and neither interface enumeration nor libp2p observed-address discovery can find it. Just the IPs — port and host ID are filled in automatically. |
| `peering.peers` | map `<name>: <multiaddr>` | empty | Statically pre-configured peers ("manual peering"), also used as Kademlia DHT bootstrap. Empty is valid only for (a) the first bootstrap node and (b) a single-node dev network with `sequencer.standalone: true`. |
| `peering.max_dynamic_peers` | int | 0 | Max peers reachable via autopeering. `> 0` enables automatic peer discovery; `<= 0` disables it. Negative values are clamped to 0. |
| `peering.allow_local_ips` | bool | false | Allow local/private IPs to be used for autopeering. |
| `peering.ignore_pull_requests` | bool | false | Ignore all incoming pull (transaction solicitation) requests. |
| `peering.pull_requests_from_static_peers_only` | bool | false | Only answer pull requests originating from statically configured peers. |
| `peering.disable_quicreuse` | bool | false | Disable libp2p QUIC connection reuse. |
| `peering.connectivity.disable` | bool | false | Opt out of the network-mapping overlay: each node otherwise gossips its peer round-trip-time view (keyed by masked names) so the whole adjacency can be downloaded from any node via `/api/v1/get_connectivity_map`. Analysis-only, never a consensus input. |

Each entry under `peers` is `<name>: <multiaddr>`, where `<name>` is a local
mnemonic and `<multiaddr>` has the form
`/ip4/<ip-or-host>/udp/<port>/quic-v1/p2p/<hostID>`.

```yaml
peering:
  host:
    id_private_key: da3a99f3a43bdcfa10da986d548e2de1ecf285c8a093849924a41cf72513be5797d3142a5af76d4be9de683d8f492dce2110936d553415102be768cf4df8cacc
    id: 12D3KooWL32QkXc8ZuraMJkLaoZjRXBkJVjRz7sxGWYwmzBFig3M
    port: 4000
  peers:
    hloc0: /ip4/65.21.170.230/udp/4001/quic-v1/p2p/12D3KooWG8zty1Yfbxw4mpiLW6Eoh6wTpPNdqn2B3f22XqArLsnT
    oseq1: /ip4/79.137.70.25/udp/4001/quic-v1/p2p/12D3KooWPG5KW9JuunvpU5kBm51HZKYv7taYbtx1ThdjXPN533u8
  max_dynamic_peers: 10
  allow_local_ips: false
```

---

## `api`

REST and WebSocket API server.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `api.port` | int | — | Port the API server listens on. |
| `api.disable` | bool | false | Disable the API server entirely (it is **enabled** by default). |

```yaml
api:
  port: 8000
```

### `api.dag_streaming` (WebSocket DAG visualizer)

WebSocket feed for the DAG visualizer, nested under `api`. The older spelling
`api.streaming.*` is still accepted as a synonym.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `api.dag_streaming.enable` | bool | false | Enable the WebSocket DAG vertex stream. |
| `api.dag_streaming.max_connections` | int | 5 | Max simultaneous WebSocket connections (oldest evicted at capacity). `<= 0` → default. |
| `api.dag_streaming.connection_ttl_minutes` | int | 5 | Connection rotation timeout in minutes. `<= 0` → default. |

```yaml
api:
  port: 8000
  dag_streaming:
    enable: true
    max_connections: 5
    connection_ttl_minutes: 5
```

### `api.mining_streaming` (WebSocket mining feed)

WebSocket feed miners subscribe to. Unlike the DAG visualizer stream it is
**enabled by default** — miners depend on it for fair launch, so a node opts out
rather than in.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `api.mining_streaming.disable` | bool | false | Disable the mining transaction stream on this node. |
| `api.mining_streaming.max_connections` | int | 50 | Max simultaneous connections. `<= 0` → default. |

---

## `sequencer`

Optional sequencer process. Read via `viper.Sub("sequencer")`; if the section
is absent **or** `enable: false`, no sequencer is started. The sequencer chain
origin is created beforehand (wallet-side) with `proxi node seq init_genesis`;
configuring the `sequencer:` section + controller key file in `proxima.yaml` is
a manual operator step.

| Key | Type | Default | Description                                                                                                                                                                                      |
|-----|------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `sequencer.enable` | bool | false | Start the sequencer. If false, the whole section is skipped.                                                                                                                                     |
| `sequencer.name` | string | "" | Optional sequencer name, 1–6 chars (truncated to 6). Stored on-chain. An on-chain name set via `proxi node seq set-params --name` takes priority.                                                |
| `sequencer.chain_id` | hex string | (required) | Chain ID of the sequencer chain.                                                                                                                                                                 |
| `sequencer.controller_key_file` | path | (required) | Path to the controller key file (JSON keystore, from `proxi util key generate`). Must exist at startup.                                                                                          |
| `sequencer.pace` | int | ledger minimum | Distance in ticks between two consecutive sequencer transactions. Clamped up to the ledger-defined minimum sequencer pace (cannot be smaller).                                                   |
| `sequencer.max_tag_along_inputs` | int | 15 | Max tag-along inputs consumed per milestone (batch size). `0` = the sequencer accepts no tag-along inputs; an absent key keeps the default 15.                                    |
| `sequencer.tag_along_drain_rate` | int | 100 | Target tag-alongs to drain per slot (~10 TPS/sequencer: 100 ÷ 10.24 s slot). With `max_tag_along_inputs`, controls drain milestones per slot. Values `< 1` ignored.                   |
| `sequencer.max_frozen_delegations` | int | 300 | Approximate per-epoch cap on the number of delegations the sequencer freezes. A freeze into a reachable epoch already holding this many is refused (the delegation stays unfrozen, retried later). `0` = the sequencer freezes no delegations; an absent key keeps the default 300. |
| `sequencer.logging` | bool | false | Write a separate sequencer log file.                                                                                                                                                             |
| `sequencer.global_logging` | bool | false | If `logging` is true, also duplicate those messages into the node's main log.                                                                                                                    |
| `sequencer.force_activity` | bool | false | Always issue a branch + milestone regardless of throttle pressure. Use for bootstrap sequencers that must maintain liveness.                                                                     |
| `sequencer.disable_throttle` | bool | false | Disable tag-along budget throttling entirely (budget stays at full 2/3 of consensus). Debugging only.                                                                                            |
| `sequencer.produce_branches` | bool | false | Issue branch transactions and compete for the branch inflation bonus. **Default false: the sequencer never branches.** A non-branching sequencer still captures chain inflation, services tag-along + delegation freezing, and gets its milestones into the ledger state via other sequencers' branches; it stops raising its coverage once its own milestone reaches healthy coverage. Branching is opt-in because only a few branches per slot are needed — every extra branching sequencer adds load and bonus competition without adding security — and it costs CPU and latency headroom. The bootstrap sequencer always branches regardless of this flag. |
| `sequencer.standalone` | bool | false | Bypass the libp2p connectivity check before submitting milestones. **ONLY** for single-node dev networks. Never enable on a networked sequencer — it permits one-sided forks during a partition. |
| `sequencer.do_not_wait_for_sync_at_start` | bool | false | Start producing without waiting for the node to be synced. Default false, so the sequencer never builds milestones on a stale or abandoned lineage (which manufactures forks). It **must** be set for a genesis/bootstrap sequencer on an empty network, which can never become "synced" because it is the one creating the chain. Implied by `force_activity` and `standalone`. |
| `sequencer.max_branches` | int | unlimited | Max branches to produce (testing). Values `>= 1` only.                                                                                                                                           |
| `sequencer.backlog_tag_along_ttl_slots` | int | 10 | TTL (slots) for tag-along outputs in the backlog. Clamped up to the minimum (10).                                                                                                                |
| `sequencer.backlog_delegation_ttl_slots` | int | 20 | TTL (slots) for delegation outputs in the backlog. Clamped up to the minimum (20).                                                                                                               |
| `sequencer.milestones_ttl_slots` | int | 24 | TTL (slots) for own milestones in the tippool. Clamped up to the minimum (24).                                                                                                                   |

```yaml
sequencer:
  name: boot
  enable: true
  chain_id: af7bedde1fea222230b82d63d5b665ac75afbe4ad3f75999bb3386cf994a6963
  controller_key_file: bootstrap.keystore
  pace: 12
  max_tag_along_inputs: 15
  tag_along_drain_rate: 100
  max_frozen_delegations: 300
  logging: false
  global_logging: false
  # standalone: true   # single-node dev network only
```

---

## `snapshot`

Periodic creation of multi-state snapshot files. Snapshots are also what the
node restores from on first start / after DB corruption.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `snapshot.enable` | bool | false | Enable periodic snapshot creation. |
| `snapshot.directory` | string | "" (→ working dir / `snapshot`) | Single directory for snapshot files (creation and restore). On startup with a missing/corrupted DB, the node searches here for a snapshot to restore from and refuses to start if none is found. |
| `snapshot.period_in_slots` | int | 176 (~30 min) | Slots between snapshots. `<= 0` falls back to default. |
| `snapshot.keep_latest` | int | 3 (template sets 2) | Keep this many newest snapshots; older are purged. `<= 0` falls back to default. |
| `snapshot.safety_slots` | int | 20 | Snapshot the state this many slots behind the tip (safety margin). `0` falls back to default. |
| `snapshot.enable_download_api` | bool | false | Enable the snapshot-download API endpoint, independent of snapshot creation. |
| `snapshot.always_serve` | bool | false | Serve the latest snapshot over the API skipping the safety gate. With the default `false`, a snapshot is served only if the node is synced, the snapshot is at least 64 slots old (or within 64 slots of genesis), and its branch is in the past of the node's latest reliable branch; otherwise the API refuses with diagnostics. |

```yaml
snapshot:
  enable: true
  directory: ""
  period_in_slots: 176
  keep_latest: 2
  enable_download_api: true
```

Snapshots can be downloaded from a node exposing the API with:
`wget --content-disposition http://<host>:<api-port>/api/v1/get_snapshot`.

---

## `snapshot_restore`

Automatic state cleanup: periodically restart the node and restore from the
latest snapshot, discarding old historical state. Distinct from the first-start
restore (which always runs when the DB is missing).

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `snapshot_restore.enable` | bool | false | Enable the periodic restart-and-restore cycle. |
| `snapshot_restore.period_slots` | int | 8438 (~24 h) | Slots between restores. `0` falls back to default. |
| `snapshot_restore.window_slots` | int | 1406 (~4 h) | Randomization window to avoid mass simultaneous restarts. `0` falls back to default. |
| `snapshot_restore.ttl_minutes` | int | 10 | If a restore takes longer than this, it is assumed failed and reset. `0` falls back to default. |
| `snapshot_restore.snapshot_directory` | string | (uses `snapshot.directory`) | Override the snapshot source directory; can point at another node's shared snapshot directory. |
| `snapshot_restore.log_file` | string | "" | Optional separate log file for restore activity (stats, duration). |
| `snapshot_restore.max_state_age_slots` | int | half the branch-txID retention | How far the local state may lag the network before the node replaces it (from a fresher snapshot) rather than syncing forward. Always clamped strictly below the branch-txID retention: forward-building a state needs its branch baselines still in the trie, so this is a correctness bound, not a tuning knob. Unset = the default; it is always on. |

```yaml
snapshot_restore:
  enable: false
  period_slots: 8438
  window_slots: 1406
  ttl_minutes: 10
  # snapshot_directory: /path/to/other/node/snapshot
  # log_file: .snapshot_restore.log
```

---

## `sources`

Trusted node API endpoints the node fetches ledger data from. This is a
**top-level** list, shared by both forward-sync (requesting branch lists for
catch-up) and snapshot acquisition (downloading a snapshot when one is needed) —
it belongs to neither subsystem. Self URLs (`localhost` with the node's own
`api.port`) are skipped automatically. A source must be a synced node with a
reachable API; the node cycles to the next source on failure.

```yaml
sources:
  - "http://65.21.170.230:8001"
  - "http://79.137.70.25:8001"
  - "http://51.254.47.76:8001"
```

---

## `sync`

Tuning for sequential branch-by-branch forward sync (catch-up). **Activation is
governed entirely by `sources` above** — with at least one source, forward-sync
runs (catch-up + fork detection); with none it is disabled and the node relies on
recursive solidification alone. There is no on/off flag and no gap thresholds:
forward-sync runs exactly while at least one attacher is stalled at the recursion
depth cap (roughly, the node is more than ~50 branches behind).

A node with no `sources` logs a loud warning at startup, and if its local state is
farther behind than recursion can bridge, an attacher hitting the depth cap
gracefully shuts the node down instead of wedging — configure `sources` or restore
from a fresher snapshot. Bootstrap and standalone nodes run with no `sources` by
design.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `sync.pull_ahead` | int | 5 | Pull the k-th branch ahead to parallelize past-cone solidification. `<= 0` → default. |
| `sync.commit_batch` | int | 10 | Max branches committed per sync tick before forcing GC. Lower reduces memory spikes during rapid catch-up at the cost of slower sync. `<= 0` → default. |
| `sync.max_slots_behind` | int | 8740 | Catch-up horizon: how many slots behind the target the node still attempts to sync forward. Beyond it the node refuses to sync and expects to be restored from a fresher snapshot. `<= 0` → default. |

```yaml
sync:
  pull_ahead: 5
  commit_batch: 10
```

---

## `logger`

Log destinations and verbosity. Log level is always INFO; `verbosity` controls
the topic-aware `LogTopicf`/`WarnTopicf` calls.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `logger.directory` | string | "" (working dir) | Directory holding the live, rotated and crash logs. Several nodes on one machine may share one directory; distinct `output` basenames keep them apart, and the rotation purge only ever touches a node's own basename pattern. |
| `logger.output` | string | "" (stdout only) | Log file basename, resolved inside `logger.directory`. When set, stdout + this file are both used, and previous-file maintenance runs. |
| `logger.previous` | string | (append) | What to do with an existing log file: `erase` (delete) or `save` (rename with timestamp, keeping `keep_latest_logs`). Any other value / absent → append. |
| `logger.keep_latest_logs` | int | 0 | When `previous: save`, how many rotated log files to keep. |
| `logger.verbosity` | int | 0 | Global verbosity for all topics. `0` = essential, `1` = normal, `2` = verbose. |
| `logger.topics` | map `<topic>: <level>` | empty | Per-topic verbosity overrides. |

Known topics (default level in parentheses): `lifecycle` (0), `tag_along`
(0: failures, 1: additions/transient), `freeze_delegation` (1), `branch_attach`
(1), `seq_attach` (1), `branch_commit` (1), `poker` (2).

```yaml
logger:
  verbosity: 0
  output: proxima.log
  previous: save
  keep_latest_logs: 2
  topics:
    tag_along: 1
    branch_attach: 1
```

---

## `metrics`

Prometheus metrics endpoint (`/metrics`).

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `metrics.enable` | bool | false | Expose Prometheus metrics. |
| `metrics.port` | int | 14000 | HTTP port for the `/metrics` endpoint. `0` → default 14000. |

```yaml
metrics:
  enable: true
  port: 14000
```

---

## `pprof`

Go runtime profiling HTTP server (`net/http/pprof`). Enables mutex/block
profiling when on.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `pprof.enable` | bool | false | Start the pprof HTTP server. |
| `pprof.port` | int | 8080 | Port for pprof. `0` → default 8080. |
| `pprof.external_access_enabled` | bool | false | Bind to `0.0.0.0` instead of `localhost`. |

```yaml
pprof:
  enable: false
  port: 8080
  external_access_enabled: false
```

---

## `txlogger`

Per-transaction event logger (separate DB, TTL-pruned). Starts disabled; can be
auto-enabled or toggled via API.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `txlogger.enable_on_start` | bool | false | Auto-enable the logger at startup with `level`. |
| `txlogger.level` | string | "" | Log level: `off`, `branch`, `sequencer`, `non_sequencer`, `all`. With `enable_on_start: true`: `off` is contradictory (logger left disabled, warning); empty/unknown → defaults to `all` (warning). |
| `txlogger.ttl_hours` | int | 0 | Retention in hours. `> 0` sets the TTL; otherwise no TTL configured. |
| `txlogger.enable_on_off_api` | bool | false | Allow enabling/disabling the logger at runtime via the API. |

```yaml
txlogger:
  enable_on_start: false
  level: "all"
  ttl_hours: 1
  enable_on_off_api: true
```

---

## `memory`

Soft GC memory limit and a watchdog that triggers graceful shutdown at 100%
stress (allocated >= limit). Disabled when `limit_mb` is 0.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `memory.limit_mb` | int | 0 (disabled) | Soft memory limit in MB (`debug.SetMemoryLimit`). `> 0` also starts the watchdog. |
| `memory.gogc` | int | 50 | `GOGC` percentage when `limit_mb > 0` (Go default is 100). Lower = more frequent GC, less spike sensitivity. `<= 0` → 50. |

The watchdog warns at >=80% stress and gracefully shuts the node down at 100%.

```yaml
memory:
  limit_mb: 4096
  gogc: 50
```

---

## `health_relief`

Coordinated, time-bounded relaxation of the healthy-branch threshold. Branch
healthiness (coverage delta vs total supply) is **not** enforced on the immutable
ledger; it is enforced in Go — the attacher rejects unhealthy branches, a
sequencer refuses to issue them, and LRB selection ignores them. Within slots
`[from_slot, to_slot]` the fraction below is used at all those sites instead of
the ledger fraction.

It exists for a coordinated restart of a network from an old snapshot, where
expired frozen coverage can otherwise make a healthy branch impossible to
reconstruct (a deadlock). Relief is a network-wide convention: **every
participating node must configure exactly the same window and the same
fraction**, or nodes disagree on which branches are acceptable. An absent section
means the ledger fraction everywhere.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `health_relief.from_slot` | int | — | First slot of the relief window. |
| `health_relief.to_slot` | int | — | Last slot of the relief window. Must be `>= from_slot`. |
| `health_relief.numerator` | int | — | Numerator of the relaxed healthy-branch fraction. |
| `health_relief.denominator` | int | — | Denominator; must be non-zero and greater than the numerator. |

A branch which passes only because of the window is logged with both fractions,
so the evidence is per branch rather than per startup. The boolean
`suppress_health_enforcement` this replaced is gone: a config still carrying it
makes the node **refuse to start**.

```yaml
health_relief:
  from_slot: 8740
  to_slot: 8800
  numerator: 4
  denominator: 12
```

---

## `trace_tags`

List of trace tags to enable at startup. Very verbose — for debugging only.
Search the code for `TraceTag` constants for available tags (e.g.
`autopeering`, `pull_server`, `txinput`, `txStore`, `gossip`, `global`).

```yaml
trace_tags:
  - txinput
  - pull_server
```

---

## `transaction_pull`

Tuning for re-requesting (pulling) missing transactions from peers.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `transaction_pull.repeat_after_sec` | int | 2 | Seconds between pull retries for a still-missing transaction. Only applied when `> 0`. |
| `transaction_pull.max_attempts` | int | 30 | Max pull attempts before giving up. Only applied when `> 0`. |

```yaml
transaction_pull:
  repeat_after_sec: 2
  max_attempts: 30
```

---

## Top-level flags

These keys live at the root of the YAML (no section).

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `disable_slicepool` | bool | false | Disable the optimized EasyFL slice-pool allocator (falls back to plain `make`). |
| `disable_deadlock_catcher` | bool | false | Disable deadlock detection in the attacher. |
| `suppress_coverage_contribution_lower_bound` | bool | false | Disable enforcement of the per-sequencer coverage lower bound on this node: the attacher stops rejecting branches below it, and a local sequencer will issue them. The bound **constant** stays on the ledger; only the Go-side enforcement is suppressed, for the same coordinated snapshot-restart scenario as `health_relief` (expired frozen coverage). The upper bound is a ledger constraint and is unaffected. Read by both the workflow attacher and the sequencer. |
| `workflow.do_not_start_pruner` | bool | false | Disable the memDAG garbage collector (pruner). Debugging only — memory will grow. |
| `workflow.max_concurrent_attachers` | int | auto: `max(20, 10 × GOMAXPROCS)` | Cap on concurrent sequencer-attacher goroutines. Gates unsolicited gossip; forward-sync and pulled attachers are exempt. `0` or unset keeps the automatic value. |
| `debug.memdag_port` | int | 0 (disabled) | Port for the read-only memDAG debug API. It exposes internal node state, so it binds loopback only — reach it over an SSH tunnel. |

```yaml
disable_slicepool: false
disable_deadlock_catcher: false
# suppress_coverage_contribution_lower_bound: false
workflow:
  do_not_start_pruner: false
  # max_concurrent_attachers: 0
```

---

## Generating a starting config: `proxi config node`

The `proxi config node` command writes a fresh `proxima.yaml` (and, with
`--standalone`, the companion genesis snapshot) from the template at
`proxi/config_cmd/node_config.template`. It refuses to overwrite an existing
`proxima.yaml` — except the edit mode below.

It prompts for at least 10 random seed characters to derive the peering host
key/ID. Fixed defaults baked into the generated file: peering `port: 4000`,
`api.port: 8000`, `max_dynamic_peers: 10`, `allow_local_ips: false`.

### Flags

| Flag | Effect |
|------|--------|
| (none) | Base node config: `peering`, `api`, `snapshot`, `snapshot_restore`, `logger`, `metrics`, plus commented-out `workflow`, `health_relief`, `sources`, `sync` and `memory` blocks. No sequencer section. |
| `--sequencer` | Add a **disabled** sequencer section with a placeholder `chain_id` (`<sequencer id hex encoded>`) and `enable: false`. If `proxima.yaml` already exists, this is **edit mode**: only the `sequencer:` section is added/replaced, the rest of the file is untouched. |
| `--standalone` | Fresh single-node dev network: an **enabled** bootstrap sequencer (`name: boot`, `enable: true`, `chain_id` = the fixed bootstrap sequencer ID `50726f78696d61…636861696e2e`, `standalone: true`), plus an enabled `txlogger` section and an enabled `api.dag_streaming` block (the DAG visualizer is the main way to watch a single node, so its connection TTL is set long). Also reads the wallet key and writes a **genesis snapshot** into the current directory. Cannot be combined with the existing-file edit mode. |
| `--trace` | Also include the `trace_tags` block and an enabled `txlogger` section. |
| `--name <1-6 chars>` | Sequencer name, used with `--sequencer`/`--standalone` (defaults to `boot` under `--standalone`). |

The generated `controller_key_file` is the wallet key file — `wallet.key_file`
from `proxi.yaml` if set, otherwise the default `proxima.key`.

---

## Full annotated example (access node)

Typical hand-edited access node (no sequencer): static peer to a bootstrap node,
metrics on.

```yaml
peering:
  host:
    id_private_key: <64-byte ed25519 hex>
    id: 12D3KooW...
    port: 4000
  peers:
    hloc0: /ip4/65.21.170.230/udp/4001/quic-v1/p2p/12D3KooW...
  max_dynamic_peers: 10
  allow_local_ips: false

api:
  port: 8001

snapshot:
  enable: false
  directory: ""
  period_in_slots: 176
  keep_latest: 2
  enable_download_api: false

snapshot_restore:
  enable: false
  period_slots: 8438
  window_slots: 1406
  ttl_minutes: 10

logger:
  verbosity: 0
  output: proxima.log
  previous: save
  keep_latest_logs: 2

metrics:
  enable: true
  port: 14001

# trace_tags:
#   - txinput
```

## Full annotated example (single-node dev / standalone)

Approximation of what `proxi config node --standalone` generates: an enabled
bootstrap sequencer with no peers (`max_dynamic_peers` is still written as `10`,
but autopeering finds nothing in a single-node network).

```yaml
peering:
  host:
    id_private_key: <hex>
    id: 12D3KooW...
    port: 4000
  peers:                 # empty: standalone bypasses the peer-connectivity gate
  max_dynamic_peers: 10
  allow_local_ips: false

api:
  port: 8000

snapshot:
  enable: false
  directory: ""
  period_in_slots: 176
  keep_latest: 2
  enable_download_api: false

snapshot_restore:
  enable: false
  period_slots: 8438
  window_slots: 1406
  ttl_minutes: 10

logger:
  verbosity: 0
  output: proxima.log
  previous: save
  keep_latest_logs: 2

metrics:
  enable: false
  port: 14000

txlogger:
  enable_on_start: true
  level: "all"
  ttl_hours: 1
  enable_on_off_api: true

sequencer:
  name: boot
  enable: true
  chain_id: 50726f78696d612e626f6f7473747261702e636861696e2e
  controller_key_file: proxima.key
  pace: 12
  max_tag_along_inputs: 15
  tag_along_drain_rate: 100
  max_frozen_delegations: 300
  standalone: true       # single-node only — never on a networked sequencer
```
