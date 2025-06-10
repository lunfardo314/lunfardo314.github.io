UTXO ledger
---
Proxima uses UTXO (**U**nspent **T**ransa**X**tion **O**utput) as its ledger model. The UTXO ledger is a broad topic, so we will introduce here only the main concepts of Proxima's UTXO ledger. More detailed definitions can be found in the [Proxima whitepaper](https://github.com/lunfardo314/proxima/blob/master/docs/Proxima_WP.pdf) and also more general disucussion on the matter in the [Medium series on the constraint-based UTXO model](https://medium.com/@lunfardo/a-constraint-based-utxo-model-1-4-a61df1b0c724).

Fundamentally, the Proxima's UTXO model is not very different from well known models used in Bitcoin, Cardano and IOTA (pre-pivot). In all of them transactions are deterministic ledger updates. It is a defining feature of UTXO. However, there are differences:
- on Proxima, in addition *consuming* the output of another transaction, as usual, a transaction can also *endorse* another transaction;
- Each output of the UTXO transaction is a vector of *validations scripts*. Each validation script is an executable bytecode of [*EasyFL*](https://github.com/lunfardo314/easyfl), a platform-independent pure functional language which plays the same role as Bitcoin Script in Bitcoin.

### Classical UTXO
A classical UTXO transaction presents an update to the **ledger state**. A UTXO transaction:
1. **consumes** (**spends**) outputs on the ledger state,
2. deletes them from there, and
3. **produces** (creates)  new outputs on the next ledger state.

<p style="text-align:center;"><img src="//hackmd.io/_uploads/HJjHApkPC.png"  width="250">
</p>

The **ledger state** is a collection of outputs, also known as UTXOs. The ledger starts from the *genesis ledger state* and evolves by updating it with UTXO transactions. The **ledger** itself is a collection of transactions that constructs the current ledger state starting from the genesis ledger state (or any other *baseline ledger state*).

Outputs (UTXOs) on the ledger state efectively are *non-fungible assets*, each with unique ID. In the classical UTXO, UTXOs are one-time, transient assets, because the consuming transaction always destroys its inputs to create new ones.

Each output contains certain amount of tokens. These are *fungible assets* that exists only as amounts in outputs.

Transaction validity constraints (also known as ledger constraints) are enforced on each transaction. The simplest and most common example of the ledger constraint is: total number of fungible tokens in consumed outputs must equal to the total number of fungible tokens in produced outputs. Validity constraints ensure transactions, when applied to the ledger state, preserve important invariants of the ledger, such as the constant total supply of tokens.

More advanced validity constraints are usually expressed as the validation scripts embedded in the output on the ledger. In Bitcoin they are written in *Bitcoin Script*, in Proxima they are *EasyFL* formulas.

The example of a validation script is *signature lock*, a script which checks the transaction's signature and invalidates any transaction with an invalid signature. Once embedded into the output, it makes it impossible to spend tokens on it without knowing the private key which unlocks the output.

Embedding validation scripts in outputs makes the ledger **programmable**.

### Conflicts. DAG. Past cone

Two transactions that directly or indirectly consume (spend) the same output in the ledger state are considered *conflicts* or *double-spends*. A valid ledger cannot contain conflicting transactions. The set of UTXO transactions as vertices with the relation of consumption of outputs between them as edges naturally forms a *directed acyclic graph* (DAG).

The *past cone* of transaction $T$ consists of all transactions reachable along consumption links down to the baseline state. The past cone of the transaction cannot contain conflicting transactions: this is the definition of the consistency of the ledger. So, the past cone of transaction $T$ is a consistent ledger that transforms the baseline ledger state to the ledger state $S_T$. Each UTXO transaction $T$ represents a separate ledger state $S_T$.

### Endorsements

Proxima's UTXO model adds new element to the UTXO transaction: a link to another UTXO transaction called **endorsement**. Technically, the *endorsement* is the ID of another transaction. The link is part of the UTXO transaction, i.e., the endorsement is signed by the token holder who produces the transaction. Transaction can contain none or several endorsements of other transactions.

The concepts of DAG, *past cone* and *conflicts* naturally extend to the transaction model with endorsements. The past cone of the transaction (now including endorsement links) cannot contain conflicting transactions, i.e. each transaction represents a valid ledger state.

By putting endorsement into transactions, users enforce the consistency of the ledger states of consumed transactions with the endorsed ledger states. This way, the Proxima's transaction not only transforms some ledger state by consuming and producing outputs but also makes a statement on the ledger about consistency of the new transaction with other transactions. Proxima's cooperative consensus heavily relies on this feature.

### UTXO tangle

**UTXO tangle** is a DAG where UTXO transactions are vertices, and output consumption links and endorsements are edges. Each vertex (transaction) represents a consistent ledger state, i.e., its past cone cannot contain conflicts. However, two transactions on the UTXO tangle can be conflicting, meaning their corresponding ledger states cannot be consolidated into one by some transaction.

<p style="text-align:center;"><img src="//hackmd.io/_uploads/rJGEExlD0.png"  width="500">
</p>

The UTXO tangle is the main data structure of Proxima: a **transaction DAG**. It combines two elements of traditional blockchains in one: transactions and blocks. One may see UTXO transactions in the UTXO tangle as analogs of blocks in a blockchain. The difference is that here both "the transaction" and "the block" are the same thing and are produced (and signed) by the same entity: the holder of the tokens on transaction inputs.

