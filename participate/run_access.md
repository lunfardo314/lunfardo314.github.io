# Running an access node

An **access node** is the simplest node configuration: it has no sequencer, needs
no tokens, and anyone can run one. It keeps a copy of the multi-ledger state in
sync with the network, gossips transactions, and serves the REST API used by the
`proxi` wallet and other programs.

## An access node is a full node

In blockchain terms, a **full node** is one that independently and trustlessly
validates transactions against the consensus rules and maintains its own copy of
the ledger state — it enforces the rules itself rather than trusting what peers
tell it. (A *light* / SPV client, by contrast, trusts full nodes and only checks
proofs.)

An access node is a full node in exactly this sense. It is not a sequencer, so it
does **not issue** transactions, but it does everything else a full node does:

- it **validates transactions against the consensus rules** as it incorporates
  them into the ledger state (signatures, all UTXO/EasyFL constraints,
  conflict / double-spend checks) — it never takes a peer's word that a
  transaction is valid;
- it **maintains the valid consensus ledger state** and computes the consensus
  view itself — the latest reliable branch (LRB) and its ledger coverage are
  derived locally, not fetched;
- it **relays** pre-validated transactions to peers — raw transactions whose
  structure is valid (gossip happens on this cheap structural check, before the
  full constraint validation done during attachment).

The one thing it trusts is the **initial snapshot** it starts from: the snapshot
is a checkpoint (the ledger state at one branch), and the node validates
everything trustlessly **from that point forward**. This is the same model as
snapshot / checkpoint sync in other systems (e.g. Ethereum snap sync, Bitcoin
`assumeutxo`).

This has one important consequence. The node is **blind to history before its
snapshot**, so the snapshot's branch must lie in the shared past of the healthy
ledger states (branches) the network is currently building on. If you start from
a snapshot that is *not* in that common history — for example an orphaned or stale
branch — the node cannot connect it to the live branches and **will not sync**.
Because Proxima uses probabilistic, Nakamoto-style cooperative consensus, the exact
set of competing healthy branches is never known with certainty, which is why you
should start from a **recent** snapshot (see *Configure state sources* below).

### Archival or not — the operator's choice

State validation does not need any history before the snapshot. But the node also
has a separate **transaction store** (`txstore` DB) that, in the current
implementation, accumulates **every raw transaction that reached the node during
its lifetime**, including orphaned ones. These pre-snapshot transactions are not
needed for operating or validating your own state — you may delete the `txstore`
DB before any restart and it will simply refill with newly arriving transactions.

**One caveat:** peers sync from each other. When a node catches up, it sends pull
requests to peers for the transactions it is missing and validates each one to
rebuild the state. A node answers those requests from its own `txstore`. So a node
that deletes its store **cannot help other peers sync**. For the health of the
network you are highly encouraged to keep the transaction store for at least a day
or a week.

The store is also what makes the ledger history auditable. So whether the node is
**archival** is the operator's choice: if the `txstore` DB is never deleted, it
holds a deterministic, fully auditable record of the ledger state's history.

Minimal tooling for this already exists:

```
proxi db txstore audit <slot from>|latest [<slot back to>] --output <new store>
```

It walks the past cones of every branch in the slot range and reports whether the
store is complete. With `--output` it writes just the transactions it visited into
a fresh txstore — so the copy holds the reachable history for that range and
leaves the orphans behind. Add `--validate` to re-validate every transaction on
the way (this needs the state DB), or `--file` to write portable `.txsave` chunks
instead of a database. Stop the node first: `proxi db` opens the database
directly.

> Future work: pruning history in place rather than by copying, and likely a
> long-term decentralized backing store such as IPFS.

These are step-by-step instructions to start an access node and sync it with the
network. For the full list of `proxima.yaml` config options see
[Node configuration reference](participate/node_config.md).

> Placeholders such as `<BOOTSTRAP_HOST>`, `<BOOTSTRAP_PORT>`,
> `<BOOTSTRAP_HOST_ID>` and `<BOOTSTRAP_API>` refer to a public node. Use the
> values published for the
> [launch phase network](participate/launch_network.md).

All commands below use a single working directory for the config and database.

## What the machine needs

There is no measured 100 TPS network yet, so the figures below are an **extrapolation**,
not a benchmark. 

| Resource | Suggested for ~100 TPS | Where it comes from |
|---|---|---|
| CPU | **4 cores**, 8 comfortable | Constraint validation costs 0.15–0.3 ms per transaction, so validation alone is a fraction of one core. The whole process measures 0.01–0.07 core at 1.7 TPS; sixty times that is under 4. |
| RAM | **16 GB** | An access node holds 0.7–0.9 GB today. What grows with load is the memDAG — the transactions in flight — so the figure is headroom for that, not a measured ceiling. |
| Disk | **NVMe SSD, 1 TB** | See below. Spinning disks are not suitable: the state is a trie and commits are random writes. |
| Network | **100 Mbit/s symmetric** | Every transaction is relayed to every peer, so traffic is roughly `TPS × peers × transaction size`. At 100 TPS, 10 peers and the measured 835-byte average that is about 0.8 MB/s — some 7 Mbit/s — **each way**. Upload is the side that matters: it scales with the number of peers. |

Disk is the resource that actually runs out. The transaction store keeps every raw
transaction that reaches the node, so at 100 TPS it grows by roughly **7 GB a day, or
some 200 GB a month**, and the state database grows on top of that. Plan for one of the
two remedies described above — periodic snapshot restore to keep the state compact, or
trimming the transaction store with `proxi db txstore audit` — rather than for a disk
large enough to never need them.

More peers cost bandwidth proportionally, and `max_dynamic_peers` is what you turn down
if upload is the constraint.

## Build

Clone the repository to `<your_dir>/proxima`, then from the repository root run:

```
go install -v ./...
```

This builds and installs both executables:

- `proxima` — the node
- `proxi` — the CLI wallet / admin tool

Check it works: `proxi -h`, `proxi config -h`, `proxi snapshot -h`.

## Create the node configuration

```
proxi config node
```

This writes `proxima.yaml` to the working directory and generates the node's
**libp2p host key and ID** from system entropy. That key only secures
peer-to-peer communication; it does **not** control any tokens.

The generated file contains sensible defaults: peering port `4000`, API port
`8000`, autopeering up to 10 dynamic peers, and an **empty** static-peers list.

> If you plan to add a sequencer to this node later, generate the config with
> `proxi config node --sequencer`. It adds a **disabled** sequencer section, so
> the node still runs as a plain access node until you enable it. See
> [Running a sequencer node](participate/run_sequencer.md).

### Add a bootstrap peer

A fresh node has no peers and cannot find the network on its own. Add at least
one known node as a **static peer** under `peering.peers` in
`proxima.yaml` — it is also used to bootstrap autopeering (Kademlia DHT):

```yaml
peering:
  peers:
    boot: /ip4/<BOOTSTRAP_HOST>/udp/<BOOTSTRAP_PORT>/quic-v1/p2p/<BOOTSTRAP_HOST_ID>
  max_dynamic_peers: 10
```

Adjust the `api.port` / `peering.host.port` if those ports are taken on your
machine. Other options are documented inline as comments and in
[Node configuration reference](participate/node_config.md).

## Configure state sources (automatic snapshot download)

A new node needs an initial ledger state to start from. You no longer download a
snapshot by hand — the node fetches one automatically. You only need to tell it
where to look, via the top-level `sources` list in `proxima.yaml`:

```yaml
sources:
  - "http://<BOOTSTRAP_API>"
  - "http://<ANOTHER_NODE_API>"
```

The node restores from a snapshot when the `proximadb` state database is absent or
corrupted — and also when the database is intact but has fallen too far behind the
network to catch up, which is treated exactly like corruption. In those cases it:

1. asks every source for its snapshot info, skipping itself and any source that
   declines to serve one;
2. prefers a snapshot that is **old enough** — so that a sequencer does not have to
   wait out its start guard — and takes the newest one within that preference. It is
   downloaded into `snapshot.directory` (default: the working directory), and a
   downloaded snapshot takes priority over whatever is already on disk;
3. restores the database from it, falling back to the newest **local** snapshot only
   if every download fails. If neither is available, the node refuses to start.

The same `sources` list is also used for ongoing branch-by-branch
forward-sync, so configuring it serves both purposes — in fact, an empty `sources`
is what disables forward-sync. The remote nodes must have
`snapshot.enable_download_api: true` to serve snapshots. A snapshot taken before a ledger
upgrade that has since activated is detected and discarded automatically.

> Manual override (rarely needed): you may still drop a `*.snapshot` file into
> `snapshot.directory` yourself — it is used when no download succeeds.
> To pull one by hand: `wget --content-disposition http://<NODE_API>/api/v1/get_snapshot`.
> To check a local file is part of the network's latest reliable branch before
> using it: `proxi snapshot check --api.node_url <NODE_API>` (and `proxi snapshot
> info` prints a file's metadata offline).

## Run the node

**Keep your computer's clock synced to real time** (NTP). A single node can never
harm the network, but a node whose clock is off by even a few seconds will
struggle to keep up with the network consensus, so it is in the operator's own
interest to stay as close to global clock time as possible. This matters most for
**sequencer nodes** (which issue transactions) and for nodes that **serve wallets
over the API** (helping them build transactions) — there the tighter the sync,
the better.

Start the node from the working directory:

```
proxima
```

On first start, with no database yet, the node downloads and restores a snapshot
as described under *Configure state sources* — this can take several minutes. Interrupting it is safe:
on the next start the node detects the incomplete restore and starts over. The
node then syncs by pulling branches and their past cones along the heaviest chain
from its peers.

> You can also pre-build the database manually with `proxi snapshot restore -v`
> before the first `proxima` start, but it is not required.

Stop the node safely with `Ctrl-C`.

## Confirm it is synced

Watch the log for lines like:

```text
[sync] latest reliable branch is 1 slots behind from now, current slot: 75613, coverage: 1_702_419_177_591_708 (1.6ms)
```

The node is synced when the latest reliable branch (LRB) is only a few slots
(typically 1–3) behind the current slot and coverage is healthy. You can also
query the network's current LRB any time with:

```
proxi node lrb
```

## Browser tools

The node serves several read-only browser tools on its API port (default
`8000`). Open them at `http://<your-node>:8000/<path>`:

- **DAG explorer** — `/dag_explorer`. Interactive view of the transaction DAG
  read from the **txstore DB**: browse by slot, search a transaction, inspect a
  transaction's details and its past cone (scroll to zoom, drag to pan, click for
  details, double-click to explore). Available whenever the node uses the default
  BadgerDB txstore. You can also run it **offline** against a local database,
  without a running node — handy when debugging the node's core:

  ```
  proxi db txstore dag_explorer --port 8080
  ```

- **dagviz** (live MemDAG) — `/dagviz`. Real-time visualizer of the **in-memory**
  DAG as transactions arrive. It connects to the node's WebSocket vertex stream,
  so it requires streaming to be enabled in `proxima.yaml`
  (`api.dag_streaming.enable: true`; see [Node configuration reference](participate/node_config.md)).

- **Chain explorer** — `/chain_explorer`. Browser view of chained accounts
  (sequencers, delegations, foundries, …) in the latest reliable branch, with
  per-chain UTXOs.

- **Peer browser** — `/peers`. Auto-refreshing dashboard of the node's peers
  (static / dynamic, alive / dead, round-trip times). The same data is available
  as JSON at `/api/v1/peers_info`.

## Running as a systemd service

In production you typically run the node under `systemd` so it survives reboots
and is managed with `systemctl`. A minimal unit
(`/etc/systemd/system/proxima.service`):

```ini
[Unit]
Description=Proxima node
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=proxima
WorkingDirectory=/home/proxima/node      # must contain proxima.yaml + the snapshot
ExecStart=/home/proxima/go/bin/proxima
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start it, and follow the log with `journalctl`:

```
sudo systemctl enable --now proxima
journalctl -u proxima -f
```

> If you run a **sequencer** on this node, note the constraint on the controller
> key under systemd (no interactive passphrase prompt) — see
> [Running a sequencer node](participate/run_sequencer.md).

## Operational notes

- **Metrics.** To expose Prometheus metrics, enable the `metrics` section in
  `proxima.yaml`. All metric names start with the `proxima_` prefix.
- **State cleanup.** The state DB holds a **multi-root trie**: it keeps the trie
  roots of many branches (past ledger states) in overlapping tries. Only recent
  roots matter for consensus, so over time the older state just accumulates as
  garbage and the database grows. Two ways to reclaim it:
  - *Automatic:* enable the `snapshot_restore` section in `proxima.yaml` to
    periodically restart and restore from the latest snapshot, keeping the
    database compact (see [Node configuration reference](participate/node_config.md)).
  - *Manual:* stop the node, delete the state DB (`proximadb`) directory, and
    restart. The node downloads the latest snapshot, syncs, and continues from
    there — exactly the first-start flow of *Configure state sources* and *Run the node*.
    You can but normally do not delete `proximadb.txstore`. 
    It contains all transactions from which all history can be reconstructed and audited. 
- **Crash safety.** The database stays consistent across crashes; a restart
  continues from the last committed branch, or re-restores from a snapshot if the
  database was corrupted.
