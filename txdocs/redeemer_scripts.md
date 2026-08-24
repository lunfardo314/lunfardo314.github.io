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
redeemScript(<script binary>)
```

This does not run the script. It hashes it, and records that hash in the transaction's set
of *redeemed scripts*.

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

The order locks used by the example decentralized exchange are the whole picture. A sell
order's lock is:

```
callRedeemer(dexHash, sellOrderFnIdx, price, timeoutSlots)
```

A hash, a function index, and the two parameters specific to this order. All the logic —
what a valid fill looks like, how a timeout refund works — lives in the script, in the
transaction of whoever spends the order, not in the order itself.

### Why both arguments must be literals

The script binary in `redeemScript` and the hash in `callRedeemer` must both be written as
inline literals; a formula that computes them is rejected.

For `redeemScript` this is **auditability**: the set of scripts a transaction commits to
can be read straight out of the transaction's bytecode, without evaluating anything.

For `callRedeemer` it is **termination**. A 32-byte hash literal can only be written down
once the script it identifies is finished, so a script cannot contain its own hash and
cannot call itself. Scripts can call other scripts, but only ones that already existed
when they were written — which makes recursion impossible by construction rather than by
checking for it.

### What this makes possible

Redeemer scripts are how Proxima gets programmability that was not decided when the ledger
was defined. Anyone can write a spending condition and use it, without a ledger upgrade
and without asking anyone, and the cost of doing so falls on the transactions that use it
rather than on every node's state.

The exchange order locks above are one example. Another is m-of-n multisignature: Proxima
deliberately does **not** make multisig a protocol primitive — every transaction carries
exactly one signature, which is what gives it an unambiguous holder (see
[Proxima transaction](txdocs/tx.md)) — but an m-of-n spending rule is straightforward as a
redeemer script.

Where a script's checks are evaluated, and how they fit into the rest of validation, is
covered in [Validation of transaction](txdocs/validation.md).
