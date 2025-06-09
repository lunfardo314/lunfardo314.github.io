# Validation of the transaction
The raw transaction is the only type of message exchanged between nodes. Before updating their ledger state, each node must validate each transaction it receives.

Validation of a transaction $T$ occurs in two stages:

1. **validation of the raw transaction** $T$:  Checks the syntax and semantics of the data blob that can be verified using only the contents of $T$ itself.
2. **validation of the transaction context** $T^{ctx}$. Checks the ledger state fragment consumed by the transaction, in conjunction with $T$.

Note 1.  Step 2 requires certainty that $T$ is validated against a consistent ledger state — specifically, that the past cone of $T$ is conflict-free. Ensuring this is beyond the strict scope of transaction validation.

Note 2: The context $T^{ctx}$ contains all information necessary to determine whether the transaction represents a valid ledger state update. This means the validation of multiple transactions is mutually isolated and can be performed in parallel on a multicore system. The UTXO-based ledger model is inherently parallelizable — unlike account-based systems and their corresponding virtual machines.

## Validation of the raw transaction
Validation of the raw transaction $T$ uses only the data contained in the received transaction blob. The steps are as follows:


1. The received blob is parsed as a tuple with 11 elements.
2. The transaction timestamp $T_5$ is parsed.
3. The sequencer and stem output indices $T_4$ are checked to determine if $T$ is a sequencer transaction.
4. The `blake2b-256` hash of the $essence(T)$ (i.e., all elements except the signature) is computed;
5. The *transaction ID* is composed based on the data parsed in steps 1-4

Steps 1-5 is a fast base validation.  Only syntactically well-formed tuples can be identified as transactions; otherwise, the data blob is rejected.

6. For sequencer transactions, the consistency of the sequencer and stem indices is verified—they must reference the corresponding UTXOs.
7. The syntactical correctness of other elements is checked (explicit baseline, input commitment, number of elements, etc.).
8. The signature of the *transaction ID* is verified;
9. The produced UTXOs are scanned. The total produced amount ($A^{out}$) and total inflation $I$ is calculated. It is enforced that $A^{out}=uint64(T_6)$.
10. Time pace constraints are enforced: the timestamps of all inputs (i.e., IDs of the consumed outputs) must precede the transaction's timestamp $T_5$ by a number of ticks defined by a ledger constant. This step also ensures consistency of timestamps with the causal order of the transaction DAG.

## Validation of the transaction context
Transaction context validation assumes that $T$ has already passed raw transaction validation.

Steps for validating the transaction context:

1. All consumed UTXOs of $T$ are loaded from the ledger state using their IDs provided in $T_0$. This yields $consumed(T)$.
   If the ledger state does not contain any of the referenced UTXOs, validation fails (for that particular ledger state, if it exists at all).
2. The transaction context $T^{ctx}=(T, (consumed(T))$ is constructed.
3. For each **consumed** UTXO $(c_0, \dots c_{k-1})$ in $T^{ctx}_{1,0}$, each of its validation script $c_i$ is **evaluated** in the context of $T^{ctx}$.  Failure of any script results in an invalid transaction.
4. For each **produced** UTXO $(c_0, \dots c_{k-1})$ in $T^{ctx}_{0,2}$, each of its validation script $c_i$ is **evaluated** in the context of $T^{ctx}$.  Failure of any script results in an invalid transaction.
5. Total sum of consumed amounts $A^{in}$ is calculated;
6. It is enforced that $A^{in}+I=uint64(T_6)$, where $uint64(T_6)$ is total produced amount and $I$ is total inflation calculated before;
7. It is enforced that $blake2b(T^{ctx}_{1,0})=T^{ctx}_{0,7}$, i.e. input commitment must equal the `blake2b-256` hash of $consumed(T)$. If it is not, it means loaded consumed outputs are tampered with (not equal to those which were used to create the transaction).
