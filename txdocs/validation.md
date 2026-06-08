# Validation of the transaction
The raw transaction is the only type of message exchanged between nodes: _cooperative consensus_ is reached by exchanging UTXO transactions. Before updating its ledger state, each node must validate every transaction it receives.

Validation of a transaction $T$ happens in **three stages**, each requiring strictly more information than the one before:

1. **Pre-validation** (identification): uses only the raw bytes of $T$. Establishes that the blob is a well-formed transaction and computes its ID.
2. **Partial-context validation**: uses the raw transaction $T$ alone, *without* the consumed UTXOs. Checks everything that does not depend on the ledger state.
3. **Full-context validation**: uses the transaction together with the ledger-state fragment it spends — the transaction context $T^{ctx}$.

A transaction must pass all three, in order. The earlier stages are cheap filters: a node runs pre-validation before gossiping the transaction to peers, and partial-context validation before attaching it to the UTXO DAG.

> The context $T^{ctx}$ contains all information necessary to decide whether the transaction is a valid ledger-state update. Validation of different transactions is therefore mutually isolated and can run in parallel on a multicore system. The UTXO ledger model is inherently parallelizable — unlike account-based systems and their virtual machines.

## Stage 1. Pre-validation (identification)
This stage uses only the received data blob.

1. The blob size is checked against a maximum (64 KiB).
2. The blob is parsed as a tuple; it must have exactly **11 elements** (indices 0–10, see [Transaction](tx.md)).
3. The version $T_0$ is checked against the node's ledger-definitions upgrade index for the transaction's slot. A node running an outdated library rejects the transaction and goes out of sync with the rest of the network.
4. The timestamp $T_1$ is parsed and the sequencer flag is read.
5. The `blake2b-256` hash of $essence(T)$ (all elements except the signature $T_3$) is computed. Together with the timestamp, the produced-output count and the sequencer flag it forms the 32-byte **transaction ID**.

If a transaction ID cannot be formed, the blob is not a transaction and is discarded. Only blobs that are identifiable as transactions are gossiped to peers.

## Stage 2. Partial-context validation
This stage checks everything that can be verified from $T$ alone, without loading the consumed UTXOs. It has two parts: a structural scan and an integrity script.

**Structural scan** of the variable-length parts:

* **Sequencer data $T_2$.** For a sequencer transaction, the sequencer output index (and, for a branch transaction, the stem output index) must reference valid produced outputs of the expected kind.
* **Inputs $T_6$.** Each consumed-output ID is parsed. The **time-pace** constraint is enforced: every input's timestamp must precede the transaction's timestamp $T_1$ by at least a ledger-constant number of ticks (a stricter pace applies to sequencer transactions). This also keeps timestamps consistent with the causal order of the DAG. The unlock-params block of each input is size-limited.
* **Endorsements $T_9$.** Each endorsed transaction ID is parsed; endorsements may not cross slot boundaries.
* **Produced outputs $T_8$.** The outputs are scanned and the total produced amount $A^{out}$ and total inflation $I$ are computed. (There is no stored total-amount field — token amounts live in each output's amounts vector.)

**Integrity script (partial context).** A single built-in EasyFL script enforces the constraints that need only $T$:

* there is at least one input, and exactly one unlock-params block per input;
* inputs contain no duplicates;
* the signature $T_3$ is a valid signature of the transaction ID (this is where the holder/spender is authenticated);
* endorsements are well-formed: only a sequencer transaction may endorse, the count is within the maximum, and there are no duplicates;
* the explicit baseline $T_5$ is either empty or — only on a sequencer transaction — a 32-byte branch transaction ID in a past slot.

A transaction that fails any of these is rejected before it is attached to the DAG.

## Stage 3. Full-context validation
This stage assumes stages 1 and 2 have passed, and additionally requires the consumed UTXOs.

1. All consumed UTXOs of $T$ are loaded from the baseline ledger state or are picked from the live _tangle_ (_memDAG_) using their IDs in $T_6$, yielding $consumed(T)$. If the at least one of them cannot be loaded for any reason, the transaction attachment and whole validation fails.
2. The transaction context $T^{ctx}=(T,\,(consumed(T)))$ is constructed, so that $T^{ctx}_0 = T$ and the consumed outputs are reachable at $T^{ctx}_{1,0}$.

> Stage 3 assumes $T$ is validated against a *consistent* ledger state — i.e. that the past cone of $T$ is conflict-free. Establishing that, as well as some other global constraints, is the job of the _attacher_, beyond the strict scope of transaction validation.

The following checks are then run over $T^{ctx}$:

1. **Input commitment.** An integrity script enforces that the input commitment $T^{ctx}_{0,4}$ equals `blake2b-256` of the consumed outputs $T^{ctx}_{1,0}$. If not, the loaded consumed outputs are not the ones used to build the transaction (tampering), and validation fails.
2. **Transaction-level scripts $T_{10}$.** Each element of the transaction-level constraints tuple is a script evaluated over $T^{ctx}$; all must succeed. These enforce rules that span the whole transaction rather than a single UTXO. Examples:
    * `redeemScript` / `callRedeemer` — the transaction redeems a *local script* whose hash it committed to, supplying the script and its arguments at the transaction level.
    * `token(tag, …)` — closes the **native-token** balance equation (a mint or burn) for a token across the whole transaction.
3. **Amount conservation (ledger invariant).** The total produced token balance must equal the total consumed balance plus total inflation: $A^{in} + I = A^{out}$.
4. **UTXO constraint scripts.** Every validation script of every **consumed** UTXO and every **produced** UTXO is evaluated over $T^{ctx}$; all must return true. In addition, every produced output must meet a minimum **storage deposit** (with the stem and tag-along outputs exempt). The per-token sub-totals accumulated by each `tokenAmount(tag, amount)` constraint as it fires are reconciled against the transaction-level `token(...)` declarations.

If any check fails, the transaction is rejected.

### Constraints are evaluated in their local context
Every constraint is a script evaluated together with its **path** in $T^{ctx}$. The path tells the script exactly where it sits, so the same script can act differently depending on context:

* a path under the consumed branch ($T^{ctx}_{1,0,i,\dots}$) means the UTXO is being **spent** — the script enforces *how* it may be spent (a signature lock, for instance, checks the unlock signature);
* a path under the produced outputs ($T^{ctx}_{0,8,i,\dots}$) means the UTXO is being **produced** — the script enforces properties of the producing transaction;
* a path under the transaction-level constraints ($T^{ctx}_{0,10,i}$) means a transaction-wide script.

Built-ins such as `selfIsConsumedOutput` and `selfIsProducedOutput` read this path. This is why a UTXO's script is written once but evaluated in two roles — once when the UTXO is produced and again when it is consumed. (Positions 0 and 1 of a UTXO — the amounts vector and the index-values — are pure data and are never evaluated.)

Because a script is also evaluated at production time, a produced UTXO is a trustless witness to properties of its producing transaction. This is valuable for L1↔L2 interaction: the UTXO alone attests to a fact about the transaction, relaxing data-availability requirements.
