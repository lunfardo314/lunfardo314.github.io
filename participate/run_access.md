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

One more thing the machine needs is a **clock synced to real time**; see
*Keep the clock synced* below.

## Where the node sits in the network

Bandwidth is not the whole story. In Proxima the consensus runs on a clock, so
**how far your node is from the other nodes, in round-trip time, decides how well
it takes part.** Some numbers to keep in mind:

* a slot lasts about ten seconds, and the sequencers issue transactions
  continuously, many per slot;
* a sequencer endorses the transactions of other sequencers **within the same
  slot**, and the slot ends with a branch that commits the state;
* the chain the network settles on is the one with the biggest **ledger coverage**,
  which in practice means the one most of the token mass has built on.

Picture the sequencers weighted by the tokens behind them, their own balance plus
what is frozen in delegations to them, and the links between them weighted by
round-trip time. Somewhere in that picture is the network's **centre of mass**: the
place where the heaviest branches are built and seen first. A node near it sees
the winning branch early and learns which transactions are settled within the
slot. A node far from it hears everything late: by the time it has seen a branch,
the rest of the network is already building on the next one.

What that costs depends on what the node does:

* **An access node** that only follows the ledger loses little; it syncs a little
  behind the others and that is all.
* **An access node that serves wallets** hands the transactions it receives to
  the network. A transaction that reaches the sequencers late is picked up a slot
  later, and under load it competes with fresher ones. The wallet sees slower
  confirmation, nothing worse.
* **A sequencer** is where distance really costs. Its transactions must reach the
  other sequencers in time to be endorsed in the same slot, and its branches must
  arrive before the others have committed to a competitor. A sequencer that is far
  from the centre of mass is endorsed less, loses most of the branches it
  proposes, and therefore earns less: fewer endorsements, less coverage, fewer
  branch bonuses. Being big does not help if you are far away.

So, in practical terms:

* **Host the node in a data centre with low round-trip time to the active
  sequencers**, not on a home connection. A residential or mobile link behind NAT
  adds latency, drops packets, and changes address; the network sees such a node
  as a peer that keeps disappearing. At the time of writing the active sequencers
  sit in Europe.
* **Peer with the sequencers directly.** Autopeering finds nodes, but it does not
  know which ones matter. Put several of the active sequencer nodes, or the
  public nodes closest to them, under `peering.peers` as static peers, so your
  transactions and theirs travel one hop.
* **Check the distance.** Every node serves a peers page in the browser at
  `/peers`, for example `http://<node address>:8001/peers`, with the round-trip
  time to each peer. Tens of milliseconds to the sequencers is good; hundreds
  means your node is on the wrong continent for a sequencer, though fine for an
  access node.
* **Keep the UDP port open.** Peering runs over QUIC on the configured UDP port.
  A firewall or NAT that lets you dial out but blocks inbound connections halves
  your connectivity: nobody can reach you, you reach everybody.

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

The file is written without its explanatory comments, so it stays short. Add
`-v` to get the fully commented version, with every option explained in place:

```
proxi config node -v
```

Both forms produce the same settings; `-v` only keeps the comments. Options
that are off by default appear in both as commented-out lines, ready to
uncomment.

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

## Keep the clock synced

**Before starting the node, make sure the computer's clock is synced to real time
with NTP.** This is not a nicety: in Proxima, ledger time *is* real time.

There are no blocks and no block producers to agree on what time it is. Genesis is
pinned to a real instant, every transaction carries a timestamp in ticks of
80 milliseconds, and every node measures those timestamps against its own clock.
A node that does not know the real time cannot take part in the consensus, and
the only practical way to know it is to sync the clock to a global reference.

What goes wrong when the clock is off:

- **Every node** accepts a transaction only once its own clock has reached the
  transaction's timestamp, and rejects one stamped more than six slots (about a
  minute) ahead. With a slow clock, everything the network sends you is "from the
  future": you hold it and fall behind. With a fast clock, everything you issue is
  held by everyone else.
- **A node that serves wallets** over the API stamps the transactions it helps
  build: wallets take the timestamp from the node, not from their own clock. A
  wrong clock here means every transaction the wallet submits is held or rejected
  by the network.
- **A sequencer** issues timestamped transactions continuously at its own clock
  time. Running ahead, its transactions are held by its peers and miss the
  endorsements that give it coverage. Running behind, it builds on tips the
  network has already moved past. Either way it earns less, and a clock a few
  slots off takes it out of the consensus altogether while the rest of the network
  runs fine.

**How accurate:** well under one tick, that is under 80 milliseconds. Ordinary NTP
keeps a server within a few milliseconds of the reference, which is enough. An
unsynced clock drifts by seconds per day, so "set once by hand" is not enough.

**How to do it:**

- *Linux.* Ubuntu and Debian ship `systemd-timesyncd` enabled. Check with
  `timedatectl`: it must show `System clock synchronized: yes` and
  `NTP service: active`. If it does not, run `sudo timedatectl set-ntp true`.
  For a sequencer, `chrony` is the better choice, since it corrects drift
  continuously and converges faster after a reboot: `sudo apt install chrony`
  (it replaces timesyncd), then `chronyc tracking` shows the current offset from
  NTP time in milliseconds.
- *Windows.* Settings → Time & language → Date & time → *Set time automatically*
  on. `w32tm /query /status` shows the last sync.
- *macOS.* System Settings → General → Date & Time → *Set time and date
  automatically* on.
- *Virtual machines and containers* take the clock from the host. Make sure the
  host syncs, and in a VM run an NTP client in the guest as well.

## Run the node

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

- **Holders browser** — `/holders`. The capital per holder in the latest
  reliable branch, sorted by total or by idle holdings, where idle is neither in
  a sequencer chain nor frozen in a delegation. Off by default, since it walks the whole UTXO
  set: enable it with `api.get_holders.enable: true` (see
  [Node configuration reference](participate/node_config.md)).

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
- **Crash safety.** The database is designed to stay consistent across crashes; a
  restart continues from the last committed branch, or re-restores from a snapshot if
  the database was corrupted.
- **After a network reset.** A reset starts a new ledger with a new genesis, and the
  ledger a node runs is the one in its database, not in its binary. A node left running
  on the old ledger is not on the new network: the two speak different protocols, so no
  transaction crosses, and the new nodes cut it off. The first time such a node tries
  to talk, the other side closes the connection and ignores it for ten minutes; a node
  it is configured as a static peer of logs one warning, "is on another ledger", and
  keeps the connection closed. Nothing is harmed, but the old node contributes nothing
  until it is moved: stop it, delete the state DB (`proximadb`) and the transaction
  store (`proximadb.txstore`), and start it again against the new network's state
  sources, exactly as on first start. The same applies to a sequencer, whose chain
  does not exist on the new ledger, and to a miner, which the new nodes refuse.

## If the API is public: put a reverse proxy in front of it

The node's API has no rate limit and no authentication. A node whose port is
reachable from the internet, for example one listed as a public access point,
should not expose it directly: one client can keep it busy with state scans, and
a few endpoints describe the node's peers. The usual answer is nginx in front of
the node, with the node itself listening only on the loopback interface.

1. Move the node's API to loopback, on a port of its own, in `proxima.yaml`:

   ```yaml
   api:
     host: 127.0.0.1
     port: 18001
   ```

   `api.host` is empty by default, meaning all interfaces. Restart the node.

2. Install nginx and give it this configuration, for example as
   `/etc/nginx/conf.d/proxima.conf`. It serves the public port `8001`, forwards
   to the node on `18001`, blocks the endpoints that map the network, limits
   heavy calls to 10 per minute per client and everything else to 20 per second,
   and passes the two websocket streams through.

   ```nginx
   limit_req_zone  $binary_remote_addr zone=api:10m   rate=20r/s;
   limit_req_zone  $binary_remote_addr zone=heavy:10m rate=10r/m;
   limit_conn_zone $binary_remote_addr zone=conn:10m;
   limit_req_status  429;
   limit_conn_status 429;

   upstream proxima_api {
       server 127.0.0.1:18001;
       keepalive 16;
   }

   server {
       listen 8001;
       listen [::]:8001;
       server_name _;

       client_max_body_size  4m;
       proxy_connect_timeout 5s;
       proxy_send_timeout    30s;
       proxy_read_timeout    30s;
       proxy_buffering       off;
       proxy_http_version    1.1;
       proxy_set_header Host              $http_host;
       proxy_set_header X-Real-IP         $remote_addr;
       proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
       limit_conn conn 20;

       # endpoints that describe the network: not for strangers
       location = /api/v1/peers_info               { return 403; }
       location = /api/v1/get_connectivity_map     { return 403; }
       location = /api/v1/get_connectivity_matrix  { return 403; }
       location = /peers                           { return 403; }
       location = /netviz                          { return 403; }
       location ^~ /api/v1/txlog/                  { return 403; }

       # state scans, script evaluation, explorers, snapshot download
       location ~ ^/(api/v1/(eval|get_inactive|get_holders|get_all_chains|get_sequencers|get_cleanable_outputs|get_snapshot|get_branch_list|get_mainchain|dag_explorer/.*|chain_explorer/.*)|txapi/v1/compile_script)$ {
           limit_req zone=heavy burst=10 nodelay;
           proxy_pass http://proxima_api;
       }

       # websocket streams (the miner subscribes here)
       location /wsapi/ {
           limit_conn conn 3;
           # headers set here replace the ones above, and the node checks a
           # browser's Origin against Host, port included: repeat Host with $http_host
           proxy_set_header Host       $http_host;
           proxy_set_header Upgrade    $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_read_timeout 1h;
           proxy_send_timeout 1h;
           proxy_pass http://proxima_api;
       }

       location / {
           limit_req zone=api burst=40 nodelay;
           proxy_pass http://proxima_api;
       }
   }
   ```

   To exempt your own machines from the limits, add a `geo` block mapping their
   addresses to an empty key and use it in the zones; the nginx documentation
   covers it under `limit_req_zone`.

3. `sudo nginx -t`, then start nginx. Check from another machine:

   ```
   curl -s -o /dev/null -w "%{http_code}\n" http://<ip>:8001/api/v1/sync_info    # 200
   curl -s -o /dev/null -w "%{http_code}\n" http://<ip>:8001/api/v1/peers_info   # 403
   for i in $(seq 25); do curl -s -o /dev/null -w "%{http_code} " http://<ip>:8001/api/v1/get_inactive; done; echo
   ```

   The last line prints a run of `200` followed by `429`. Open `/dagviz` in a
   browser as well: a websocket that connects from `curl` but not from a browser
   means the `Host` header is not reaching the node with its port.

Anything on the machine that used `http://127.0.0.1:8001` keeps working through
nginx. This does not add HTTPS; that needs a domain name and a certificate, which
`certbot --nginx` sets up in one step once the name exists.
