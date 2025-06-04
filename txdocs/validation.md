# Validation of the transaction
The raw transaction is the only type of messages exchanged by nodes. Each node, before updating its ledger state, checks validity of each transaction.

There are two steps of validation of the transaction $T$:
1. **validation of the raw transaction** $T$: checking the part of the received data blob, both syntax and semantics, that are possible with the data of $T$ only;
2. **validation of the transaction context** $T^{ctx}$. The transaction context also involves fragment of the ledger state consumed by the transaction.

Note 1. Step 2 requires certainty that $T$ is validated against the consistent ledger state, i.e. that the past cone of $T$ is **conflict-free**. This aspect is beyond the strict scope of the transaction validation.

Note 2. $T^{ctx}$ contains **all** the information which is necessary to determine if the transaction is a valid ledger state update. It means, validation of multiple transactions are isolated from each other. It  can be run in **parallel** on multiple cores on a multicore system. The UTXO ledger is naturally parallelizable (unlike to the account-based systems and respective VMs).

## Validation of the raw transaction
Validation of the raw transaction $T$ only requires the data contained in the raw transaction, received by the node. It goes through the following steps:
1. The received blob is parsed as a tuple with 11 elements;
2. Transaction timestamp $T_5$ is parsed;
3. Sequencer and stem output indices $T_4$ are checked. It determines if $T$ is a sequencer transaction
4. `blake2b-256` hash of the $essence(T)$ (all elements except the signature) is calculated;
5. The *transaction ID* is composed based on the data parsed in the steps 1-4

Steps 1-5 is a fast base validation. **Only syntactically well-formed tuple can be identified as a have transaction**, otherwise the data blob is not considered a transaction and is rejected.

6. for sequencer transactions, consistency of the sequencer and stem indices are checked: they must point to the corresponding UTXOs;
7. syntactical correctness of other elements is checked (explicit baseline, input commitment, number of elements, etc);
8. signature of the *transaction ID* is verified;
9. the produced UTXOs are scanned, total produced amount ($A^{out}$) and total inflation $I$ is calculated. It is enforced that $A^{out}=uint64(T_6)$
10. time pace constraints are enforced: timestamps of all inputs (IDs of the consumed outputs) must be before the timestamp of the transaction ($T_5$) by a number of ticks set by a ledger constant. This step also enforces consistency of the timestamps with the causal order of the transaction DAG.

## Validation of the transaction context

Validation of the transaction context follows the validation of the raw transaction, i.e. here we assume $T$ is valid as a raw transaction.

Steps of the validation of the transaction context:

1. all consumed UTXOs of $T$ are loaded from the ledger state by their IDs provided in the $T_0$. This gives $consumed(T)$. If ledger state does not contain any of corresponding UTXOs, validation fails (for that particular ledger state, if such exist at all);
3. the *transaction context* $T^{ctx}=(T, (consumed(T))$ is created
4. for each **consumed** UTXO $(c_0, \dots c_{k-1})$  in $T^{ctx}_{1,0}$, each of its validation script $c_i$ is **evaluated** in the context of $T^{ctx}$. Failure of it means invalid transaction
5. for each **produced** UTXO $(c_0, \dots c_{k-1})$, each of its validation script $c_i$ is **evaluated** in the context of $T^{ctx}$. Failure of it means invalid transaction
6. Total sum of consumed amounts $A^{in}$ is calculated;
7. It is enforced that $A^{in}+I=uint64(T_6)$, where $uint64(T_6)$ is total produced amount and $I$ is total inflation calculated before;
8. It is enforced that $blake2b(T^{ctx}_{1,0})=T^{ctx}_{0,7}$, i.e. input commitment must be equal to the `blake2b-256` hash of $consumed(T)$. If it is not, it means loaded consumed outputs are tampered with (not equal to those which were used to create the transaction).

