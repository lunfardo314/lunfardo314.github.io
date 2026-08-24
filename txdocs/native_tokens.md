# Native tokens and foundries

PROX is not the only kind of token a Proxima UTXO can hold. Anyone can issue their own
**native token** — and the resulting tokens are not managed by a contract that must be
trusted or called. They are carried in ordinary UTXOs and their supply is checked by the
same validation every node performs on every transaction.

### The foundry

A native token is issued by a **foundry**: a chained account (see
[Proxima transaction](txdocs/tx.md)) whose output carries a `foundry` constraint alongside
its `chain` constraint.

The foundry's **tag** — the identity of the token it issues — is simply the ChainID of the
chain it lives on. There is no separate token identifier to register, reserve, or collide
over: a chain ID is derived from the output that started the chain, so every foundry
issues a token nobody else can issue.

The `foundry` constraint stores one number: the **circulating supply**, the amount of that
token currently in existence. It starts at zero.

```
proxi node foundry create
```

This produces the chain origin with `foundry(0)` on it. Your token's tag is known straight
away: a chain ID is derived from the output that started the chain, so it is fixed the
moment the foundry exists. What starts at zero is the supply, not the identity — the first
mint puts the first tokens into circulation.

### Holding tokens

A UTXO holds native tokens by carrying a `tokenAmount(tag, amount)` constraint. An output
can hold base tokens and native tokens at once; the base-token amount and the native-token
amount are separate things in the same UTXO.

Two rules are enforced locally, on the output itself: the amount must be greater than
zero, and the tag must be one the transaction has **declared**.

### Declaring a tag, and the balance rule

A transaction that touches native tokens must say so, at the transaction level, with a
`token(...)` declaration naming the tag. The declaration is what makes per-tag accounting
possible: each `tokenAmount` adds itself to the running consumed or produced total for its
tag, and at the end of validation the ledger checks the closing equation for every
declared tag.

The equation is what you would expect: **what goes in must come out, unless the foundry
says otherwise.** Tokens cannot appear in a transaction that does not mint them, and
cannot vanish from one that does not burn them.

A declaration comes in two forms.

* **Pure conservation** — no foundry is involved. The supply does not change, and the
  transaction is simply moving existing tokens around. Consumed and produced totals for
  that tag must be equal.
* **Foundry transit** — the declaration also names the produced foundry output. The
  foundry's supply changes, and the difference is exactly the tokens minted into, or
  burned out of, the transaction.

This is why a foundry's supply cannot drift: it is only allowed to move inside a
transaction that declares the move and balances it against real token outputs.

### Minting and burning

```
proxi node foundry mint <chainID> <amount>
proxi node foundry burn <chainID> <amount>
```

`mint` consumes the foundry output and produces the foundry with its supply increased, an
output carrying `tokenAmount(<chainID>, <amount>)` locked to the target (your own wallet
by default), a tag-along output, and any base-token remainder back to you.

`burn` is the reverse: it consumes token-holding outputs and produces the foundry with its
supply decreased by the same amount.

Both require your wallet to control the foundry.

### Policies: issuance is programmable

By default a foundry can mint without limit and can be discontinued at will by whoever
controls it. That default is only the starting point. A foundry output can carry a
**policy** — EasyFL constraints, the same language the rest of the ledger is written in —
and the policy, together with the lock on the foundry output, decides what issuing this
particular token means.

That covers a wide range:

* **Centralized.** No policy, an ordinary signature lock: the controller mints, burns and
  retires at will. Appropriate when the token represents something the issuer is
  answerable for anyway — a stablecoin backed by deposits, a claim on a real-world asset.
* **Constrained, including against the issuer.** A policy fixing a supply cap, or refusing
  to let the foundry disappear while tokens are still outstanding. Because a policy locks
  its own bytecode across every transit, these bind the controller too: they are promises
  that cannot be withdrawn later.
* **Openly issuable.** Nothing requires the foundry to be controlled by one party. A lock
  anyone can satisfy, together with a policy stating the conditions under which minting is
  valid, gives a token anybody may issue by meeting those conditions rather than by being
  the owner.

This is what native tokens were designed for: **tokenized fungible assets** — stablecoins,
claims on real-world assets, and anything else where the interesting question is not "can I
make a token" but "what exactly is the issuer able to do to holders afterwards". On Proxima
that question has a precise answer, readable off the foundry itself.

### The policies `proxi` offers

The wallet exposes two simple predefined policies. Anything beyond them means writing the
constraint yourself and building the transaction directly — the ledger has no fixed menu.

```
proxi node foundry create --max-supply <N>
proxi node foundry create --non-destructible
```

* `foundryMaxSupply(N)` rejects any transit that would take the supply above `N`. A hard
  cap, checked on every mint.
* `foundryNonDestructible` refuses to let the foundry chain be discontinued while its
  supply is above zero — every token must be burned back before the foundry can go away.

The important part is that a policy **locks itself in**. Each predefined policy requires
its own bytecode to be identical in the successor output on every transit, so the foundry
owner cannot quietly swap a cap for a larger one, or drop it altogether, later on. A
holder of your token can check the policy once and rely on it.

These two are mutually exclusive in `proxi` — at most one of the flags. Policies are opt-in
and chosen at creation, because they are promises the issuer makes and cannot take back.

### Retiring a foundry

```
proxi node foundry retire <chainID>
```

This consumes the foundry output and produces no successor, ending the chain. The
foundry's base-token balance returns to your wallet. If the foundry carries
`foundryNonDestructible`, this is rejected unless the supply is already zero.
