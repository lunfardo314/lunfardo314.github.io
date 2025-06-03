# Validation of the transaction
Nodes exchange serialized raw transactions. It is the only type of messages they exchange. Each node, before updating its ledger state, checks validity of each transaction.

There are two steps of validation of transaction $T$:
1. validation of the raw transaction $T$: checking all properties of the received data blob, both syntax and semantics, which are possible with the data of $T$ only;
2. validation of transaction context $T^{ctx}$, which also involves fragment of the ledger state consumed by the transaction.

Note 1. Step 2 requires certainty that $T$ is validated against the consistent ledger state, i.e. past cone of $T$ is **conflict-free**. This aspect is beyond the strict scope of the transaction validation.

Note 2. $T^{ctx}$ contains **all** the information to determine if the transaction is a valid ledger state update. It means, validation of mutiple transactions is isolated from each other, and it can be run in **parallel** on multiple cores on the multi-core systems. The UTXO ledger is naturally parallelizable, unlike to the account-based systems and VMs.

## Validation of the raw transaction
Validation of the raw transaction $T$ does not require full context and can be performed in isolation from the ledger state and other transactions.

It goes through the following steps:
1. The blob is parsed as a tuple with 11 elements;
2. Transaction timestamp $T_5$ is parsed;
3. Sequencer and stem output indices $T_4$ are checked. It determines if $T$ is a sequencer transaction
4. `blake2b-256` hash of the $essence(T)$ is calculated
5. The *transaction ID* is composed from the data parsed in the steps 1-3

Steps 1-5 is a fast base validation. **Only syntactically well formed tuple can have transaction ID**, otherwise the data blob is not considered a transaction and is rejected.

6. for sequencer transactions, consistency of sequencer and stem indices are checked: they must point to the corresponding UTXOs
7. syntactical correctness of other elements is checked (explicit baseline, input commitment, number of elements, etc).
8. signature of the *transaction ID* is verified
9. the produced UTXOs are scanned, total produced amount ($A^{out}$) and total inflation $I$ is calculated. It is enforced $A^{out}=uint64(T_6)$
10. time pace constraints are enforced: timestamps of all inputs (IDs of the consumed outputs) must be before the timestamp of the transaction ($T_5$) by a number of ticks set by a ledger constant. This step also enforces consistency of the timestamps with the causal order of the transaction DAG.

## Validation of the transaction context

Validation of the transaction context follows the validation of the raw transaction, i.e. we assume $T$ is valid as a raw transaction.

Steps of the validation of the transaction context:

1. all consumed UTXOs of $T$ are loaded from the ledger state by their IDs provided in the $T_0$ of the *raw transaction*. This gives $consumed(T)$. If ledger state does not contain a corresponding UTXO, validation fails (for the particular ledger state, if such exist at all);
3. the *transaction context* $T^{ctx}=(T, (consumed(T))$ is created
4. for each **consumed** UTXO $(c_0, \dots c_{k-1})$  in $T^{ctx}_{1,0}$, each of its validation script $c_i$ is **evaluated** in the context of $T^{ctx}$. Failure of any of it means invalid transaction
5. for each **produced** UTXO $(c_0, \dots c_{k-1})$, each of its validation script $c_i$ is **evaluated** in the context of $T^{ctx}$. Failure of any of it means invalid transaction
6. Total sum of consumed amounts $A^{in}$ is calculated;
7. It is enforced that $A^{in}+I=uint64(T_6)$, where $uint64(T_6)$ is total produced amount and $I$ is total inflation calculated before;
8. It is enforced that $blake2b(T^{ctx}_{1,0})=T^{ctx}_{0,7}$, i.e. input commitment must be equal to the `blake2b-256` hash of $consumed(T)$. If it is not, it means loaded consumed outputs are tampered with (not equal to those which were used to create the transaction).

