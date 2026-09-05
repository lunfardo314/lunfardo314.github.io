# Launch phase network

The launch phase network is at least four or five sequencers and several public access
nodes, run by the founder and by whoever joins during the launch phase. How the launch is
phased, and what has to be true before Proxima can be called decentralized, is described in
[The fair launch](overview/fair_launch.md).

Note that the network can be stopped and reset at any time while it is still in its
**centralized pre-launch phase**, without notice and as many times as it takes. The point
of the exercise is to survive the centralized phase and come out of it decentralized.
Until that happens, treat everything on the network as temporary — tokens included.

## Initial public access points

* alpha — `http://65.21.170.230:8001`
* beta — `http://79.137.70.25:8001`

Either can be used to reach the network from your wallet, and either can be listed as a
trusted source for bootstrapping a new node, in the node's configuration.

## Other public access points

A couple of access points is a starting point, not a network. A handful of entry points that
everyone depends on is exactly the shape the launch phase exists to grow out of, and it is
the easiest thing for a newcomer to fix.

**Run your own [access node](participate/run_access.md) and publish its address.** An
access node needs no tokens, costs little to run, and every one of them makes the network
harder to disrupt and easier for the next person to join. Publish the address wherever
other participants will see it, and use your own node from your wallet instead of someone
else's.

### Web tools

Each public access node also serves a few read-only browser tools on its API port:

* **Launch phase monitor** — a high-level view of where the ledger and the network stand:
  supply and distribution, fair-launch mining progress, and decentralization. Aggregates
  only; per-chain and per-transaction browsing is in the explorers below.
  Open it on [alpha](http://65.21.170.230:8001/monitor) or
  [beta](http://79.137.70.25:8001/monitor).
* **Chain explorer** — the _chained accounts_ (sequencers, delegations, foundries) in the
  latest reliable branch, with the UTXOs of each chain. A good starting point to see which
  sequencers are running and what delegations exist.
  Open it on [alpha](http://65.21.170.230:8001/chain_explorer) or
  [beta](http://79.137.70.25:8001/chain_explorer).
* **DAG explorer** — an interactive view of the transaction DAG read from the node's
  transaction store: browse by slot, search for a transaction, and inspect a transaction
  together with its past cone.
  Open it on [alpha](http://65.21.170.230:8001/dag_explorer) or
  [beta](http://79.137.70.25:8001/dag_explorer).
* **DAG visualizer** — a real-time visualizer of the **tangle**, the transaction DAG being
  built by the node as transactions arrive. It needs transaction streaming to be enabled on
  that node, so it may not be available on every access point.
  Open it on [alpha](http://65.21.170.230:8001/dagviz) or
  [beta](http://79.137.70.25:8001/dagviz).
* **Peers** — an auto-refreshing dashboard of the node's peers: static or dynamic, alive or
  dead, with round-trip times.
  Open it on [alpha](http://65.21.170.230:8001/peers) or
  [beta](http://79.137.70.25:8001/peers).

The same paths work on any access node, including your own.

## How to get tokens

By **mining**. During the launch phase this is the way in, and it is open to everyone: you
do not need tokens to start, and nobody hands any out.

```bash
proxi node mine
```

You need a wallet, which may be empty; access to a node API — one of the access points
above, or your own; and CPU cores. The tag-along fee a transit pays to a sequencer comes
out of the reward rather than out of your balance, so nothing is required up front. The
full guide, including the flags worth setting and what the miner does with the proceeds,
is [Mining](participate/mine.md).

There is no faucet.

## What can you do with your tokens?

### Transfer tokens between accounts

Use `proxi node send` to send tokens between accounts (see the
[`proxi` wallet](participate/proxi.md)). For this, `proxi.yaml` must be configured
properly — in particular the _tag-along sequencer_ and the _tag-along fee_. List the
available sequencers with `proxi node allchains -q` and pick one as your tag-along.

### Earn inflation by delegation

Please read [delegation](participate/delegate.md). It is **strongly encouraged** to
delegate all but a small reserve (say 100 or 1000 PROX) of your tokens as soon as you
receive them. List the sequencers available as delegation targets with
`proxi node allchains -q`.

Delegated tokens contribute to the security of the network and, in return, earn you
inflation. Tokens left idle in an ordinary account (an address of the form `a/<hex>`) earn
nothing.

If you are mining, this happens by itself. By default `proxi node mine` delegates what it
earns, each time to a sequencer drawn **at random** from those currently alive that leave
you enough of the inflation cut. The draw is repeated for every delegation, so a miner
spreads its tokens across the sequencers instead of piling them on one — which is exactly
what the launch phase is trying to achieve. Use `--delegate=false` if you would rather
place your tokens yourself.

### Earn inflation by running a sequencer

To run a sequencer you need two things:

1. **An access node.** An ordinary full node that keeps a valid copy of the ledger but does
   not run a sequencer. It is easy to run and needs no tokens. It does not add to the
   consensus security, but it does add to decentralization by keeping a replica of the
   ledger — the whole network can be recovered from a single node, plus the private keys
   controlling the token accounts. See [Running an access node](participate/run_access.md).
2. **A sequencer** configured on that access node, which then makes it a _sequencer node_.
   Running a sequencer requires tokens. See
   [Running a node with a sequencer](participate/run_sequencer.md).

Sequencers generate inflation and so contribute to the network's security on behalf of the
token holder. In addition to the usual inflation, a sequencer may receive a _branch
inflation bonus_.

## Disclaimer

We will do our best to help on the
[Proxima Discord](https://discord.com/invite/UfFcFDy38j), but please note our resources are
very limited — we count on a growing community that helps each other.
