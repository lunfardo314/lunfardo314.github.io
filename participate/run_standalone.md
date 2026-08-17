# Running a standalone developer node

These instructions are aimed at **frontend developers** (wallets, browser apps,
React UIs, the WASM transaction builder) who need a real Proxima node to develop
against without joining the testnet.

A **standalone node** is a single, self-contained, throwaway network: one node
running its own bootstrap sequencer, with a fresh genesis created on the spot. It
needs no peers, no snapshot download, and no tokens from anyone. It is enough to
exercise most frontend functionality end-to-end:

- query and display ledger state (balances, UTXOs, chains, the current ledger time);
- compose, sign and submit transactions;
- watch them get confirmed by the local bootstrap sequencer.

Because every `proxi config node --standalone` run builds a brand-new genesis,
the network is disposable: to reset, stop `proxima` and delete the working
directory's `proxima.yaml`, `proxi.yaml`, `proxima.key`, the `*.snapshot` file and
the database directory.

All commands below are run in a single working directory. Build the binaries
first (`go install -v` in `proxima/` and `proxima/proxi/`), then check `proxi -h`.

### 1. Create the wallet (key + profile)

```
proxi config wallet
```

This single command creates **both** the ED25519 key and the wallet profile. It
asks for some entropy, writes the key to `proxima.key` (a small JSON keystore),
and writes the profile to `proxi.yaml` (the default profile name is `proxi`).
The generated profile:

```yaml
# default sequencer ID is used when own or tag-along sequencer is not specified
default_sequencer_id: 50726f78696d612e626f6f7473747261702e636861696e2e

wallet:
    key_file: proxima.key
    holder_id: <your account holder ID>
    # the sequencer this wallet controls; 'proxi node seq withdraw' draws from it
    sequencer_id: 50726f78696d612e626f6f7473747261702e636861696e2e
api:
    endpoint: http://127.0.0.1:8000

tag_along:
    # preferred fee paid to a sequencer so the tx gets pulled; the sequencer's own
    # declared minimum wins if it is larger
    fee: 1
    # pick whichever sequencer is currently active
    sequencer_id: random
```

> On a standalone network the only sequencer is the bootstrap one, so `random`
> resolves to it as soon as it is producing milestones. If you prefer the wallet
> not to depend on that, set `sequencer_id` to the bootstrap sequencer ID above.

- `holder_id` is your account identifier: `blake2b(<sig type byte> || <public key>)`.
  It is what sigLock outputs are addressed to, and what the frontend passes to
  `get_outputs` / `HolderIDFromPrivateKeyED25519` in the WASM wallet.
- Both `default_sequencer_id` and `wallet.sequencer_id` are set to the **bootstrap
  sequencer ID**. This is a **predefined constant** (`ledger.BoostrapSequencerIDHex`
  = `50726f78696d612e626f6f7473747261702e636861696e2e`, the hex of the 24-byte
  ASCII string `Proxima.bootstrap.chain.`) — independent of the genesis output
  IDs, and the same for every ledger. In standalone mode the wallet key controls that
  bootstrap sequencer, which is why this wallet can withdraw from it (step 4).

### 2. Create the standalone node config + genesis

```
proxi config node --standalone
```

Run this **after** the wallet exists — it reads the wallet key to credit the
genesis account. It produces two things in the working directory:

- `proxima.yaml` with an **enabled bootstrap sequencer** (named `boot`,
  `standalone: true`). The `standalone` flag bypasses the peer-connectivity gate,
  so the lone sequencer issues milestones with no peers.
- a **genesis snapshot** (`*.snapshot`) for a fresh single-node ledger, timestamped
  now. On first start the node restores its database from it.

Genesis distribution:

- the **bootstrap sequencer chain owns the whole supply** (`initialSupply - 1`);
- **1 token sits in your ED25519 sigLock account** (the genesis "mote" output),
  enough to bootstrap the first transaction.

### 3. Run the node

```
proxima
```

Run it from the working directory (it needs `proxima.yaml` and the `*.snapshot`
there). The REST API the frontend uses comes up on `http://127.0.0.1:8000`
(`get_ledger_definition`, `get_ledger_time`, `get_outputs`, `submit_tx`, …).

### 4. Fund your account from the bootstrap sequencer

The genesis mote is only 1 token. Withdraw a working balance from the boot
sequencer into your sigLock account — you will need it for fees and for any chains
you create:

```
proxi node seq withdraw 500000000000
```

## Example commands

With the node running and the account funded, the typical frontend-testing loop:

Send tokens to your own address (creates another UTXO):

```
proxi node send 500000000
```

`send` without `-t` targets the wallet's own account by default.

Show the wallet balance:

```
proxi node balance
```

Compact all consumable wallet UTXOs back into a single sigLock output (e.g. merge
the two UTXOs the steps above produced into one):

```
proxi node compact
```

These same operations — fetch the library and UTXOs, compose + sign, submit with
validation — are exactly what a browser wallet performs against the node; see
[`ledger/txbuildercore/wasm/README.md`](https://github.com/lunfardo314/proxima/blob/develop/ledger/txbuildercore/wasm/README.md) for
the WASM/JS equivalent.
