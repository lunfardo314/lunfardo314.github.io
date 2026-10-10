# Pluggable nonce seekers

> **Pre-launch notice.** The network is in its centralized pre-launch phase. The founder can
> stop or reset it at any time, without notice. Tokens mined or held on a pre-launch network
> confer no rights, will not be carried over, and cease to exist when the network is reset.
> Nothing is sold and nothing is promised; take part for the exercise. See
> [Please read before taking part](README.md).

[Mining](participate/mine.md) is a race to find a **nonce**: a number such that a value
derived from it under your key has enough trailing zero bits. Everything else the miner
does, following the mine chain, choosing the target, building, signing and submitting the
transaction, is bookkeeping. The search is the only part where speed matters, and the only
part worth writing in another language or running on other hardware.

So `proxi node mine` lets you take the search out. With one option in the wallet profile
the miner becomes a small server that hands out **jobs** and accepts **solutions** from
any number of external programs, called **nonce seekers**. A seeker can be the reference
one shipped with Proxima, written in Rust and about twice as fast per core as the miner's
own workers, or one you write yourself, for a GPU or anything else.

This page covers the short way, where the miner starts the reference seeker itself,
configuring the miner for seekers you run yourself, running the reference seeker by
hand, and what you need to know to write your own.

## The short way: let the miner start it

On the machine that mines, with the reference seeker built once (see
[Running the reference seeker](#running-the-reference-seeker) for the build) and placed
on the PATH or next to `proxi`:

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
other machines can still connect to the same miner: set `listen` and `token` as
described next, and the spawned one and the remote ones share the work.

## How it fits together

| | `proxi node mine` | nonce seeker |
|---|---|---|
| follows the mine chain and picks the target | yes | no |
| holds your private key | yes | yes |
| searches nonces | its own workers, optional | yes |
| checks a solution | always | no |
| builds, signs and submits the transaction | yes | no |

A seeker holds the key because every attempt needs it: the value it searches for is a
verifiable random function of the key and the message. It never produces the proof that
goes into the transaction. It returns the nonce; the miner recomputes the value for that
nonce, checks it against the job, and only then completes the proof and builds the
transaction. A buggy seeker therefore cannot produce an invalid transaction; the worst it
can do is waste the miner's time.

The seeker is the client. It dials the miner, asks for the current job, and posts
solutions and progress reports. That direction is chosen on purpose: a seeker on a rented
machine or inside a container can usually reach out but cannot be reached, and either
side can restart while the other just waits.

Several seekers can work for one miner at once, on the same machine or on different
ones, without any coordination between them: each starts at a random nonce, and since
the same nonce under the same key is the same attempt everywhere, they almost never repeat
each other's work.

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
  `--workers 0` to leave the whole search to the seekers; the miner then only waits for
  their solutions. Without any seeker configured, `--workers 0` is refused with a
  message, so a miner that was meant to hand the search away never quietly mines on
  one core instead.
* `--max-hashrate-khs` and `--nonce-start` apply to the local workers only. Seekers pace
  themselves.
* The consolidator runs beside the miner exactly as before. Seekers change nothing
  about what happens to the payouts.

The token is not a secret worth protecting: jobs are public data. It exists so that
strangers cannot feed the result endpoint, since each posted result costs the miner one
verification. If you leave it empty, keep the listener on the loopback address. When
seekers run on other machines, listen on an address they can reach (`0.0.0.0:8100` for
all interfaces), set a token, and open that port in the firewall for those machines
only.

## Running the reference seeker

The reference seeker lives in the Proxima repository under
`proxi/node_cmd/mine/nonce_seeker`. It needs a Rust toolchain, which
[rustup](https://rustup.rs) installs in a minute. Build it once:

```bash
cd proxi/node_cmd/mine/nonce_seeker
cargo build --release
```

The binary is `target/release/nonce_seeker`. For the short way above, put it on the
PATH, for example with `sudo install -m 755 target/release/nonce_seeker /usr/local/bin/`,
or next to `proxi`. Adding `RUSTFLAGS="-C target-cpu=native"` before `cargo build` lets
it use the vector instructions of the machine it is built on, for a few percent more.

To run it by hand, on the same machine or another one, copy it to wherever it should
run, together with the wallet's key file, and start it against a miner that has
`listen` set:

```bash
nonce_seeker --proxi http://127.0.0.1:8100 --token choose-something-long --key-file proxima.key
```

| Flag | Meaning |
|------|---------|
| `--proxi URL` | The address `proxi node mine` serves jobs on. Required. |
| `--token T` | The profile's `mine.seeker.token`. Omit when the miner has none. |
| `--key-file FILE` | The wallet key file, encrypted or not. Default `proxima.key` in the working directory. |
| `--threads N` | Search threads. Default: all cores. |
| `--name NAME` | How this seeker appears in the miner's statistics. Default `seeker-<pid>`. |

The key file is the same one `proxi` uses, and an encrypted one is unlocked the same
way: the seeker looks for a passphrase file in its working directory named exactly as
the keystore's holder ID, then for the environment variable `PROXIMA_KEY_PASSPHRASE`,
and otherwise asks on the terminal. A service or a container has no terminal, so give it
the file or the variable. For images that carry no key file at all, the environment
variable `NONCE_SEEKER_SEED` with the 32-byte seed in hex is accepted instead.

The seeker refuses a job that names a key other than the one it holds, and says so in
its log. It runs until you stop it: a miner that is down or restarting is retried with
backoff, and a job that has expired is dropped without fuss.

What you see:

* The seeker logs each job it takes, with the target slot, the difficulty and the time
  left, every solution it submits and whether the miner accepted it, and its own speed
  every ten seconds.
* The miner's progress line counts the seekers' attempts together with its own, and its
  totals line, printed after each confirmed transit, lists every seeker by name with its
  speed and when it last reported.

A seeker that stops reporting makes the miner believe it is slower than it is, and the
miner then searches each target for a shorter time than it should. The reference seeker
reports once a second; so should any seeker you write.

## Keeping the key safe

A seeker needs the private key wherever it runs. Encrypting the key file protects it on
disk and in backups, not from the machine it runs on: once unlocked, the key sits in the
seeker's memory for as long as it mines, and whoever controls a rented machine can read
that memory.

The exposure is bounded, though. The key's only value is the payouts it has received and
not yet moved, so:

* mine with a **dedicated wallet** that holds nothing else, and
* run [the consolidator](participate/consolidate.md) on it, which sweeps every payout
  away as soon as it confirms.

Then a stolen mining key loses you at most the last few payouts, and you can simply
switch to a new key.

## Writing your own seeker

The protocol is three HTTP calls with JSON bodies, and the work is one well-defined
computation. The complete specification, with every field and status code, is
[`kb/external_nonce_seeker.md`](https://github.com/lunfardo314/proxima/blob/develop/kb/external_nonce_seeker.md)
in the repository; what follows is the shape of it.

**The calls.** `GET /seeker/job` returns the current job, and with `?after=<id>&wait=<ms>`
it holds the request until the job changes, so a seeker learns about a new target within
one round trip. `POST /seeker/result` delivers a nonce. `POST /seeker/report` delivers the
number of attempts made since the last report, about once a second. With a token
configured, every call carries `Authorization: Bearer <token>`.

**The job** carries an opaque id (`0` means there is nothing to mine right now), the fixed
part of the message to hash (`alpha_prefix`), the required number of trailing zero bits
(`k`), how many milliseconds the job is still worth working on (`ttl_ms`), the public key
the solution must be found under (`pubkey`), and, while the miner is fighting over a
contested step, a 64-byte value (`beat`) the output must be smaller than.

**The work.** For an 8-byte nonce of your choice, the message is `alpha_prefix || nonce`,
and the value is the output of ECVRF-EDWARDS25519-SHA512-TAI (RFC 9381) under the key for
that message: hash the message to a curve point with the try-and-increment method, multiply
it by the secret scalar, and hash the result. The nonce solves the job when the output has
at least `k` zero bits at its least significant end, counting from the last byte, and is
below `beat` when one is given.

**The answer.** `200` means accepted and the job is over; `409` means the job had already
ended, nothing to fix; `422` means the nonce does not solve the job as the miner sees it,
which is a bug in the seeker, and the reply says why. Send your own output in the result
as `beta`: the miner compares it with its own computation, and a mismatch is the fastest
way to find out that your hash-to-curve or your scalar multiplication differs.

Two mistakes account for most of the trouble, so check them first:

1. **Byte equality with the standard.** Your output for a given key and message must equal
   the miner's. The RFC 9381 test vectors for the TAI suite are the first check; they are in
   the repository's Go package `util/vrf` and in its Rust twin `util/vrf/rust`, which you can
   build on directly, or use as the reference to test against. The `beta` field is the second
   check.
2. **Trailing, not leading.** The zero bits are counted from the end of the output. A
   seeker counting from the front finds solutions that the miner refuses.

For the key file, the Rust library `util/keystore/rust` reads the same format `proxi`
writes, encrypted or not, and is kept equivalent to the Go code by the repository's tests.

If you are writing for a GPU, one property is worth knowing: the secret scalar is the
same for every attempt, so every thread executes the same sequence of point doublings and
additions, with no divergence to manage. What varies per attempt is the hash-to-curve,
which costs one square root, the multiplication of a different point, and the compression
of the result, which costs one inversion that can be shared across a batch of threads.

Whatever you build, the miner stays the one that verifies, proves and submits. Keep it
that way: a seeker that tried to build transactions itself would have to track the mine
chain, the settlement timing and the rule that ranks competing transits, all of which
change with the ledger and are easy to get subtly wrong.
