# Classical UTXO

_UTXO_ is a widely recognized term in the crypto world. It stands for **U**nspent **T**ransa**X**tion **O**utput.

Throughout this document, we will use _UTXO_ and _output_ interchangeably. [UTXO](https://en.wikipedia.org/wiki/Unspent_transaction_output) also refers to the ledger model popularized by Bitcoin.

## UTXO transaction

The simple illustration of what later became known as a UTXO transaction—taken from the Bitcoin whitepaper:
<p style="text-align:center"><img src="../static/img/btc-utxo.png">
</p>

A UTXO transaction, among other elements, includes at least inputs and outputs, which we refer to as **consumed UTXOs** and **produced UTXOs**, respectively. It must satisfy a globally trusted set of validity rules, also known as **validity constraints** or **ledger constraints**. The most basic rule is that the total number of fungible tokens in the inputs must equal the total in the outputs.

UTXO transaction represents a deterministic update to the ledger state. It updates a bounded part of the ledger state, which is unbounded, in general.

Here is a more detailed diagram, which still conveys the same core concept:

<p style="text-align:center;"><img src="../static/img/utxo.png">
</p>

In Proxima, a transaction is a data structure that, at its core, is equivalent to a classical UTXO transaction. However, its role within Proxima goes far beyond a simple ledger update.

## Ledger state
Each UTXO has a unique **output ID**, which is assigned at the moment the output is created. Output IDs are guaranteed to be unique (though UTXOs themselves can be duplicated in structure).

The ledger state is a key-value database consisting of pairs _(output ID, output)_. UTXOs can be retrieved by referencing their _output IDs_.

The history of the ledger begins with a _genesis ledger state_, which initially contains two UTXOs (explained further below).

A transaction does not include the full consumed outputs. Instead, it contains _inputs_, which are simply the IDs of the consumed outputs.

If the current ledger state contains all the output IDs listed as inputs in a transaction, that transaction is said to be _applicable_ to the ledger state.

An applicable transaction updates the ledger state in the following way:
* **consumed outputs** are removed from the ledger state
* **produced outputs** are added to the ledger state

Any valid ledger state results from the incremental application of transactions, starting from the _genesis ledger state_.

A key property of the UTXO model is that the final **ledger state is independent of the order** in which transactions are applied—so long as each transaction is applicable when applied. (This is similar to assembling a jigsaw puzzle: no matter the order in which you place the pieces, the end result is the same.)

This property contrasts with account-based ledger models, where the final state **does depend** on the sequence in which transactions are applied.
