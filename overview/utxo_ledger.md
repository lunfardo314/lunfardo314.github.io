UTXO ledger
---
Proxima uses UTXO (**U**nspent **T**ransa**X**tion **O**utput) as its ledger model. 

A classical UTXO transaction presents an update to the **ledger state**. A UTXO transaction:
1. **consumes** (**spends**) outputs on the ledger state,
2. deletes them from there, and
3. **produces** (creates)  new outputs on the next ledger state.

<p style="text-align:center;"><img src="../static/img/utxo.png">
</p>

More detailed description of the UTXO model can be found in [Proxima transaction model](https://lunfardo314.github.io/#/txdocs/intro). 

### Conflicts. DAG. Past cone

Two transactions that directly or indirectly consume (spend) the same output in the ledger state are considered *conflicts* or *double-spends*. A valid ledger cannot contain conflicting transactions. The set of UTXO transactions as vertices with the relation of consumption of outputs between them as edges naturally forms a *directed acyclic graph* (DAG).

The *past cone* of transaction $T$ consists of all transactions reachable along consumption links down to the baseline state. The past cone of the transaction cannot contain conflicting transactions: this is the definition of the consistency of the ledger. So, the past cone of transaction $T$ is a consistent ledger that transforms the baseline ledger state to the ledger state $S_T$. Each UTXO transaction $T$ represents a separate ledger state $S_T$.

### Endorsements

Proxima's UTXO model adds new element to the UTXO transaction: a link to another UTXO transaction called **endorsement**. Technically, the *endorsement* is the ID of another transaction. The link is part of the UTXO transaction, i.e., the endorsement is signed by the token holder who produces the transaction. Transaction can contain none or several endorsements of other transactions.

The concepts of DAG, *past cone* and *conflicts* naturally extend to the transaction model with endorsements. The past cone of the transaction (now including endorsement links) cannot contain conflicting transactions, i.e. each transaction represents a valid ledger state.

By putting endorsement into transactions, users enforce the consistency of the ledger states of consumed transactions with the endorsed ledger states. This way, the Proxima's transaction not only transforms some ledger state by consuming and producing outputs but also makes a statement on the ledger about consistency of the new transaction with other transactions. Proxima's cooperative consensus heavily relies on this feature.

### UTXO tangle

**UTXO tangle** is a DAG where UTXO transactions are vertices, and output consumption links and endorsements are edges. Each vertex (transaction) represents a consistent ledger state, i.e., its past cone cannot contain conflicts. However, two transactions on the UTXO tangle can be conflicting, meaning their corresponding ledger states cannot be consolidated into one by some transaction.

<p style="text-align:center;"><img src="../static/img/utxo_tangle.png"> </p>

The UTXO tangle is the main data structure of Proxima: a **transaction DAG**. It combines two elements of traditional blockchains in one: transactions and blocks. One may see UTXO transactions in the UTXO tangle as analogs of blocks in a blockchain. The difference is that here both "the transaction" and "the block" are the same thing and are produced (and signed) by the same entity: the holder of the tokens on transaction inputs.

