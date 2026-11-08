# Pluggable nonce seekers

> **Pre-launch notice.** The network is in its centralized pre-launch phase. The founder can
> stop or reset it at any time, without notice. Tokens mined or held on a pre-launch network
> confer no rights, will not be carried over, and cease to exist when the network is reset.
> Nothing is sold and nothing is promised; take part for the exercise. See
> [Please read before taking part](README.md).

[Mining](participate/mine.md) is a race to find a **nonce**: a number such that the
transaction it goes into has a hash with enough trailing zero bits. The search is the
only part where speed matters, and the only part worth running on other hardware.
Everything else the miner does costs next to nothing: following the mine chain, choosing
the target, building, checking, signing and submitting the transaction, and deciding
where each reward goes. That last part matters for the network: it puts every mined token
into consensus, where it secures the ledger.
See [Put your tokens to work](participate/active_tokens.md).

**So the recommended way to mine faster is to keep `proxi node mine` and replace only the
search, with a nonce seeker.** With one option in the wallet profile the miner becomes a
small server that hands out **jobs** and accepts **solutions** from any number of
external programs, called **nonce seekers**. Proxima ships two reference seekers:

| Seeker | Runs on | Speed, measured |
|---|---|---|
| the miner's own workers, `--workers N` | any CPU | about 7.5 million attempts per second per core |
| the reference CPU seeker, `nonce_seeker`, in Rust | any CPU | about 100 million per second on an 8-core machine |
| the reference GPU seeker, `gpu_seeker` | NVIDIA cards | about 15.4 billion per second on one RTX 5090 |

A CPU is under 1% of one such card. A GPU version for AMD and Intel cards is to follow.

**From library upgrade 6, slot 196000, a seeker needs no key.** A job carries the bytes of
the transaction to hash, not a key, so a seeker can run on a machine you do not trust
with your key. Every seeker must be the build of release v1.6.0 or later: an older build
gets no jobs after the slot. Until the slot, mining uses the older work: the GPU seeker
does not do it, and the CPU seeker does it only with the key. See
[What changes with upgrade 6](participate/upgrade6.md) and
[How mining works](participate/mining_architecture.md).

Whatever seekers you run, keep [the wallet consolidator](participate/consolidate.md)
running on the mining wallet as well: every mining wallet needs it, see
[Mining](participate/mine.md?id=run-the-consolidator-beside-the-miner).

## The short way: let the miner start the CPU seeker

On the machine that mines, with the reference CPU seeker built once (see
[The reference CPU seeker](participate/nonce_seeker.md?id=the-reference-cpu-seeker) for
the build) and placed on the PATH or next to `proxi`:

```bash
proxi node mine --seeker
```

That is the whole setup. The miner opens its job server on a free loopback port, makes up
a token for it, starts the seeker with the port, the token, the key file and the number
of threads filled in, and hands it the passphrase it unlocked the key with, so an
encrypted key is asked for once. The seeker's lines appear in the miner's output marked
`[seeker]`; if it exits, the miner starts it again; when the miner stops, the seeker
stops with it. The miner's own workers are off in this mode, since the seeker is faster;
`--workers N` adds some back.

The same, in the wallet profile, so that a plain `proxi node mine` does it every time:

```yaml
mine:
    seeker:
        spawn: true
        # the binary to start; empty means 'nonce_seeker' on the PATH or beside proxi
        binary:
        # search threads; 0 means every core
        threads: 0
```

Leave a few cores free with `threads` when the machine also runs a node. Seekers on
other machines, a GPU seeker for example, can still connect to the same miner: set
`listen` and `token` as described next, and the spawned one and the others share the
work.

## How it fits together

| | `proxi node mine` | nonce seeker |
|---|---|---|
| follows the mine chain and picks the target | yes | no |
| holds your private key | yes | no, from upgrade 6 |
| searches nonces | its own workers, optional | yes |
| checks a solution | always | no |
| builds, signs and submits the transaction | yes | no |
| decides where the reward goes | yes | no |

The miner builds the transit, leaving only the nonce open, and gives the seeker those
bytes. The seeker returns a nonce; the miner computes the hash itself, checks it against
the job, and only then signs and submits the transaction. A buggy seeker therefore cannot
produce an invalid transaction; the worst it can do is waste the miner's time. And since
the reward outputs are part of the hashed bytes, a seeker cannot change where the reward
goes.

The seeker is the client. It dials the miner, asks for the current job, and posts
solutions and progress reports. That direction is chosen on purpose: a seeker on a rented
machine or inside a container can usually reach out but cannot be reached, and either
side can restart while the other just waits.

Several seekers can work for one miner at once, on the same machine or on different
ones, without any coordination between them: each starts at a random nonce, so they
almost never repeat each other's work.

## Configuring the miner

In the wallet profile, `proxi.yaml`:

```yaml
mine:
    seeker:
        # address the miner serves jobs on; empty means no seekers
        listen: 127.0.0.1:8100
        # shared secret the seekers must present; empty means none
        token: choose-something-long
```

With `listen` set, `proxi node mine` starts the job server before its first round and
prints the address in its banner. Everything else about the miner stays as it was:

* The miner's own workers keep running next to the seekers. Start it with
  `--workers 0` to leave the whole search to the seekers, which is what you want with a
  GPU; the miner then only waits for their solutions. Without any seeker configured,
  `--workers 0` is refused with a message, so a miner that was meant to hand the search
  away never quietly mines on one core instead.
* `--max-hashrate-khs` and `--nonce-start` apply to the local workers only. Seekers pace
  themselves.
* Where each reward goes is the miner's decision, as before. Seekers change nothing
  about it.

The token stops strangers from feeding the result endpoint, since each posted result
costs the miner one check. Keep the listener on the loopback address, `127.0.0.1`, and
reach it from other machines through an SSH tunnel, as shown for the GPU seeker below.
If you must listen on an address other machines can reach (`0.0.0.0:8100` for all
interfaces), set a token, and open that port in the firewall for those machines only.

## The reference CPU seeker

It lives in the Proxima repository under `proxi/node_cmd/mine/nonce_seeker`. It needs a
Rust toolchain, which [rustup](https://rustup.rs) installs in a minute. Build it once:

```bash
cd proxi/node_cmd/mine/nonce_seeker
cargo build --release
```

The binary is `target/release/nonce_seeker`. For the short way above, put it on the
PATH, for example with `sudo install -m 755 target/release/nonce_seeker /usr/local/bin/`,
or next to `proxi`. Adding `RUSTFLAGS="-C target-cpu=native"` before `cargo build` lets
it use the vector instructions of the machine it is built on, for a few percent more.

To run it by hand, on the same machine or another one, start it against a miner that has
`listen` set:

```bash
nonce_seeker --proxi http://127.0.0.1:8100 --token choose-something-long
```

| Flag | Meaning |
|------|---------|
| `--proxi URL` | The address `proxi node mine` serves jobs on. Required. |
| `--token T` | The profile's `mine.seeker.token`. Omit when the miner has none. |
| `--key-file FILE` | The wallet key file. Default `proxima.key` in the working directory. Needed only before upgrade 6. |
| `--threads N` | Search threads. Default: all cores. |
| `--name NAME` | How this seeker appears in the miner's statistics. Default `seeker-<pid>`. |

**Without a key.** From upgrade 6 the seeker needs no key: started where there is no key
file, it says so and takes only the new jobs. Run it that way on any machine you do not
fully control. It reads a key only if it finds one: the file `proxima.key` in its working
directory, the file named by `--key-file`, or the environment variable
`NONCE_SEEKER_SEED`.

**With a key**, before upgrade 6: the key file is the same one `proxi` uses, and an
encrypted one is unlocked the same way: the seeker looks for a passphrase file in its
working directory named exactly as the keystore's holder ID, then for the environment
variable `PROXIMA_KEY_PASSPHRASE`, and otherwise asks on the terminal.

It runs until you stop it: a miner that is down or restarting is retried with backoff,
and a job that has expired is dropped without fuss.

## The reference GPU seeker

It lives in the Proxima repository under `proxi/node_cmd/mine/gpu_seeker`: a small
Python program that talks to the miner, and a CUDA program that runs the search on the
card. It runs on **NVIDIA cards only** for now, and only for the work of upgrade 6. It
needs no key.

**What you need** on the GPU machine: an NVIDIA card and its driver; the CUDA toolkit,
for the `nvcc` compiler (version 12.8 or later for RTX 50 cards); Python 3.8 or later,
with nothing else installed.

**Build** it once, in that directory, naming the generation of your card: `sm_120` for
RTX 50, `sm_89` for RTX 40, `sm_86` for RTX 30:

```bash
cd proxi/node_cmd/mine/gpu_seeker
nvcc -O3 -arch=sm_120 -Xcompiler -fPIC -shared -o libb2s.so blake2b_search.cu
```

The built `libb2s.so` must stay next to `gpu_seeker.py`.

**Check and measure** before mining:

```bash
python3 gpu_seeker.py selftest     # the card's results must equal a plain CPU search
python3 gpu_seeker.py bench 10     # attempts per second, for 10 seconds
```

The self-test must pass. If it fails, do not mine with that build.

**Run.** In the miner's wallet profile:

```yaml
mine:
    seeker:
        listen: 127.0.0.1:18555
        token: choose-something-long
```

Then start the miner, leaving the whole search to the card, and the seeker:

```bash
proxi node mine --workers 0
python3 gpu_seeker.py run http://127.0.0.1:18555 choose-something-long
```

**A GPU on another machine**, such as a rented one: keep the listener on the loopback,
and from the miner's machine open an SSH tunnel to the GPU machine:

```bash
ssh -N -R 18555:127.0.0.1:18555 gpu-box
```

This makes port 18555 on the GPU machine lead back to the miner. Run the seeker there
with the same `run http://127.0.0.1:18555 <token>` command. The GPU machine then needs
neither your key nor an open port: the miner's machine dials out to it.

## Keeping the key safe

From upgrade 6 the key stays with `proxi node mine` alone, which needs it to sign. Keep
the miner on a machine you control, and run the seekers wherever the hardware is,
without a key.

Know what the key is worth. `proxi node mine` puts every reward into a delegation whose
owner is the mining key, or onto a sequencer the same key controls, so the key controls
everything it has mined so far. Whoever copies it can take back those delegations.
So:

* mine with a **dedicated wallet** that holds nothing else;
* keep the miner, and any seeker that holds the key, on machines you control;
* run seekers on machines you do not control only without a key;
* from time to time, move what the mining wallet holds to a wallet whose key never
  leaves your own machine: release its delegations with
  `proxi node delegate askstop`, then end them with
  `proxi node endchain <delegation ID> ... -t a/<holder ID>`, which sends the tokens straight
  to that wallet (see [Delegation](participate/delegate.md)). What a stolen key can take is
  then at most what was mined since the last move, and you switch to a new mining key.
  Alternatively, `mine.payout_address` sends every reward to such a wallet as a plain
  output, which earns nothing until you put it to work (see [Mining](participate/mine.md)).

## What you see

* A seeker logs each job it takes, with the target slot, the difficulty and the time
  left, every solution it submits and whether the miner accepted it, and its own speed
  every ten seconds.
* The miner's progress line counts the seekers' attempts together with its own, and its
  totals line, printed after each confirmed transit, lists every seeker by name with its
  speed and when it last reported.

A seeker that stops reporting makes the miner believe it is slower than it is, and the
miner then gives up waiting for a confirmation of its transits sooner than it should.
The reference seekers report about once a second.

## Writing another seeker

Proxima's reference seekers cover CPUs and NVIDIA cards. If you want to port the search
to other hardware, the interface is three HTTP calls with JSON bodies, and the work is
one well-defined computation. The complete specification, with every field and status
code, is
[`kb/external_nonce_seeker.md`](https://github.com/lunfardo314/proxima/blob/develop/kb/external_nonce_seeker.md)
in the repository; what follows is the shape of it for upgrade 6, version 2 of the
protocol.

**The calls.** `GET /seeker/job` returns the current job, and with `?after=<id>&wait=<ms>`
it holds the request until the job changes, so a seeker learns about a new target within
one round trip. `POST /seeker/result` delivers a nonce. `POST /seeker/report` delivers the
number of attempts made since the last report, about once a second. With a token
configured, every call carries `Authorization: Bearer <token>`.

**The job** carries `version: 2`, an id (`0` means there is nothing to mine right now),
the bytes of the transaction without the nonce (`message`), where the 8-byte nonce goes
(`nonce_offset`, the end of the message), the required number of trailing zero bits
(`k`), how many milliseconds the job is still worth working on (`ttl_ms`), and, once a
solution for the target is known, yours or a competitor's, the value to beat (`beat`).

**The work.** An attempt is the BLAKE2b-256 hash of `message` followed by the nonce, as 8
bytes, big-endian; plain BLAKE2b, unkeyed, with a 32-byte result. It solves the job when
the last 8 bytes of the hash, read as a big-endian number, end in at least `k` zero bits.
Its **work value** is those 8 bytes followed by bytes 6 to 23 of the hash, 26 bytes; it
beats `beat` when it is smaller, compared byte by byte. Since the nonce comes last, hash
`message` once per job and finish a copy of that state per attempt.

**How long a job lasts.** A job covers one slot and lasts until shortly before the slot is
settled, which is what `ttl_ms` counts down to. A solution does not end it. The slot goes
to the smallest work value the sequencers hold when they settle it, so after each
accepted solution keep searching the same job for a smaller one. The `beat` goes down as
better solutions come in; the job id stays the same, so a seeker that works in long
batches, a GPU, loses nothing in flight.

**The answer.** `200` comes with `accepted` and `beat`. `accepted: true` means the miner
took your solution; `accepted: false` means it is valid but no longer below the job's
`beat`. Either way the job is still open: take the `beat` from the answer and keep
searching. `409` means the job has ended; poll for the next one. `422` means the nonce
does not solve the job as the miner sees it, which is a bug in the seeker, and the reply
says why. Send your hash in the result as `beta`: the miner compares it with its own,
which is the fastest way to find a mistake.

Check two things first: that your hash equals the miner's for the same bytes (the
repository has shared test vectors, used by both the Go miner and the Rust seeker), and
that you count the zero bits from the **end** of the hash, not the front.

Whatever you build, the miner stays the one that checks, signs and submits. Keep it that
way: a seeker that tried to build transactions itself would have to track the mine chain,
the settlement timing and the rule that ranks competing transits, all of which change
with the ledger and are easy to get subtly wrong.
