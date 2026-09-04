# Redeemer scripts

A UTXO's constraints are permanent state. Every unspent output sits in the ledger state
that every node keeps — so every byte of every constraint on it is a byte the whole network
carries for as long as the output lives. Conditions of any real complexity, written out
inside the output, would be paid for by everyone, forever.

The code that *checks* a spending condition, on the other hand, is only needed at the
moment of spending. It belongs in the transaction, which no node keeps in its state.

**Redeemer scripts** are that split. A constraint commits to a script by its hash; the
transaction that spends the output carries the script itself.

### The two halves

A transaction can carry a **local script** — a self-contained piece of EasyFL — in a
transaction-level constraint:

```
redeemScript(<script>)
```

This does not run the script. It hashes it, and records that hash in the transaction's set
of *redeemed scripts*.

The argument is usually the script binary written out inline, and that stays the fast path.
It may also be **any formula that can be evaluated without a transaction** — in practice, a
call to a function in the ledger definition library. Such a formula is evaluated in an
empty context, so one that reaches for the transaction, or for a parameter, simply fails.
What survives is exactly the expressions whose value follows from the library alone, which
is what keeps the committed binary reproducible from the transaction's own bytes.

This matters for size. A frequently used script can be carried by a library upgrade as an
ordinary function, and transactions then *name* it instead of repeating it. The difference
is not small: in the chess game described below, the two script binaries account for 8,253
bytes of an 8,887-byte move transaction, whereas a `redeemScript` constraint naming a
library-resident script is 3 bytes.

Any constraint on a UTXO invokes a function of a script by hash:

```
callRedeemer(<32-byte hash>, <function index>, <args…>)
```

The call succeeds only if the spending transaction declared a script with exactly that
hash. So the output says *which* code decides the question, without containing that code;
the spender supplies the code and cannot substitute different code, because the hash would
not match.

This is not limited to locks. `callRedeemer` may appear in any constraint of an output —
the lock is simply where a spending condition most often belongs, so it is the common
case.

### What a constraint ends up looking like

The order locks of the example decentralized exchange in `examples/dex/` are the whole
picture. A sell order's lock is:

```
callRedeemer(dexHash, sellOrderFnIdx, price, timeoutSlots)
```

A hash, a function index, and the two parameters specific to this order. All the logic —
what a valid fill looks like, how a timeout refund works — lives in the script, in the
transaction of whoever spends the order, not in the order itself.

That example is a **proof of concept, and no longer how the exchange is built.** Having
been demonstrated this way, the order locks were graduated into the ledger definition
library, where `sellOrder(price, timeoutSlots)` and `buyOrder(amount, price, timeoutSlots)`
are now native locks like any other — see [UTXO constraints](ledgerdocs/constraints.md).
Examples are not part of the library.

That progression is worth noticing, because it is the point of the mechanism. A redeemer
script lets an idea be built and used with no ledger change and no permission; if it then
proves broadly useful, it can be moved into the library by an upgrade, and the
transactions using it stop carrying the code. What could not have happened is the reverse
order — waiting for a hardfork before the idea could be tried at all.

### Why the hash must be a literal

The hash in `callRedeemer` must be written as an inline literal; a formula computing it is
rejected. This is **auditability of the call site**: a reader can tell which script a call
reaches by looking at the call, without evaluating anything. The argument of `redeemScript`
is deliberately not restricted in the same way, because the set of committed scripts stays
readable either way — as an inline binary, or as the library function named.

### Why scripts terminate

Scripts may call other scripts, so something has to rule out cycles. The guarantee is a
bound on **dispatch depth**: every `callRedeemer` dispatches into one of the scripts the
transaction has committed, so a chain of *distinct* scripts can never be deeper than that
commitment list. A run that goes deeper must have re-entered a script it already used —
that is a cycle, and it is refused. The bound is exact, rejecting cycles and nothing else,
and there is no tunable limit to set wrongly.

An earlier, structural argument was that a script cannot contain its own hash, since the
hash exists only once the script is finished. That reasoning holds only while every hash is
an inline literal, and it is not what the ledger relies on: the depth bound does not care
how a hash was written down.

### What this makes possible

Redeemer scripts are how Proxima gets programmability that was not decided when the ledger
was defined. Anyone can write a spending condition and use it, without a ledger upgrade
and without asking anyone, and the cost of doing so falls on the transactions that use it
rather than on every node's state.

The exchange order locks above are one example — and, having since graduated into the
library, an illustration of the whole path. Another is m-of-n multisignature: Proxima
deliberately does **not** make multisig a protocol primitive — every transaction carries
exactly one signature, which is what gives it an unambiguous holder (see
[Proxima transaction](txdocs/tx.md)) — but an m-of-n spending rule is straightforward as a
redeemer script.

The most complete demonstration is a **trustless chess game**, in `examples/chess_poc/`.
A game is a chained account and one transition is one half-move, with the rules of chess
enforced by the ledger itself: an illegal move is not a valid transaction, so no node will
record it. Two redeemer scripts compose to achieve this — a rule-pure move validator, and
a protocol layer above it handling whose turn it is, deadlines, resignation and the
bounty — the second calling the first by its hash. The output's own lock stays small,
because the rules live in the transactions that play the game rather than in the state.
Neither player has to trust the other and there is no referee.

Where a script's checks are evaluated, and how they fit into the rest of validation, is
covered in [Validation of transaction](txdocs/validation.md).
