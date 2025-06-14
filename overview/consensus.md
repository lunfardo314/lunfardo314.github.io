
# Cooperative consensus

## General

In Proxima, users seek consensus on each individual transaction, unlike blockchains, where consensus is reached on an entire block of transactions. Proxima ledger is organized as *directed acyclic graph* (DAG), also known as [UTXO tangle](overview/utxo_ledger.md).

UTXO tangle is a *transaction DAG*, unlike the block-DAGs used by Kaspa and IOTA (pre-Sui fork). The *UTXO tangle* is build by transaction producers (token holders) themselves rather than by block producers, who are third parties. The removal of third parties and related trust assumptions from the consensus is the whole point of the transaction DAG.

In the *UTXO tangle* each vertex is a plain UTXO transaction. Raw transaction bytes are the only message type participants exchange.

Each vertex $T$ of the UTXO tangle represents an individual ledger state $S_T$ (a set of outputs or UTXOs), which is the result of updating the genesis ledger state with the transactions from the past cone of $T$. The UTXO tangle keeps track of multiple versions of the ledger state in one data structure, one ledger state for each vertex. Some of them will be conflicting, while others not. The UTXO tangle is a *multi-ledger* data structure.

The whole point of consensus among participants is eventually agree on one single version of the ledger state, which is **will be present in the history of any possible future transactions**.

To reach this goal, Proxima uses a novel mechanism called **cooperative consensus**, which is optimized for the parallel nature of the transaction DAG.

Cooperative consensus does not need "marshaling" transactions into blocks therefore avoids related global bottlenecks. It also avoids mining races of PoW and is energy-efficient. It is completely permissionless and does not require any BFT committee setup or other complexities and tradeoffs with decentralization, unlike most PoS systems. The system's Sybil protection is ensured similarly to PoS: by tokens on the ledger.

The cooperative consensus provides efficient protocol for coordinating the common interest (social consensus) of multiple token holders in a **multi-leader** way on a shared ledger that records their assets.

## Consensus on the transaction DAG
The main principle of the cooperative consensus was proposed in the original paper about [the tangle](https://assets.ctfassets.net/r1dr6vzfxhev/2t4uxvsIqk0EUau6g2sw0g/45eae33637ca92f85dd9f4a3a218e1ec/iota1_4_3.pdf). Cooperative consensus employs the main principle of the tangle - "each transaction approves two others" - in the UTXO tangle and develops the concept even further.

The UTXO tangle grows by adding (attaching) new transactions to it, driven by the decisions and preferences of the end-user of the system, the token holder. Each new transaction references other transactions, already existing on the UTXO tangle by consuming their outputs and *endorsing* them. Each new transaction $T$, once attached to the UTXO tangle, immediately becomes a **tip** of the DAG. At any moment, the UTXO tangle has a set of tips, which is constantly change as new tips arrive.

Participants exchange transactions, each maintaining own copy of the UTXO tangle, therefore perception of the tip set will always differ for each participant due to communication latency.

Consensus on a particular transaction $T$ (and the corresponding ledger state $S_T$) is reached when there is a substantial guarantee for every participant in the network that transaction $T$ will be included in the past cone (history) of any future tip on the UTXO tangle. If transaction $T$ has no chance of making it to future tips, it is considered **orphaned**.

The producer of the transaction $T$, by analyzing UTXO tangle and **assuming the behavior of other token holders**, must convince herself, that the UTXO tangle won't develop in a way that would orphan transaction $T$. That would mean the network has consensus on the inclusion of the transaction $T$ into the ledger. Consensus on transaction $T$ is "reached" when chances of it to be orphaned become negligible.

The consensus criterion above is probabilistic by its very nature (i.e., no 100% guarantees), because user can only estimate he *chances* of how exactly UTXO tangle will develop in the future. Similarly, in the PoW blockchain, user estimates if the block with their transaction won't be orphaned by checking if it is deep enough in the longest known chain, based on the assumption the miners will follow the longest chain.

In the cooperative consensus, it is assumed that all token holders follow the **biggest ledger coverage rule** as the optimal strategy for all profit-seeking token holders. It is the **behavioral assumption** of the cooperative consensus.

In game theory, *optimal strategy* means, that, by deviating from it, participant will incur significant costs compared to sticking to it. (An everyday example of this kind of strategy -- Nash equilibrium -- is driving the right (or left) side of the road. We are quite comfortable when passing a car on the other side of the road because we know that for the other driver not to drive on the correct side may cost then their life)

In Proxima, we can assume that the absolute majority of the token holders will follow the biggest ledger coverage rule because it is the most profitable strategy, as per enforced validity constraints and [incentives](overview/incentives.md) on the ledger. So, new *tips* of the UTXO tangle will be appearing according to that rule with very high probability.

After sufficient amount of time, a user can be overwhelmingly convinced that once their transaction $T$ is included into the past cone of every tip of the UTXO tangle, it will remain that way in the future. That will be the moment when user will start considering their transaction *confirmed*.

Token holder produces their transaction $T$ by consolidating chosen non-conflicting ledger states proposed by other users in their transactions. This way, each transaction consolidates past cones of $T$'s' inputs into an even "broader" ledger. This also acts as a cooperation mechanism, helping other transactions to be included in the bigger ledger state of $T$.

Next, token holders will be looking for the "broadest" coverage of the past ledger by some transaction and will build upon $T$ if it happens to cover the most. Therefore, each token holder will want their transaction $T$  to represent the "broadest" ledger state. Ultimately, the ever-enlarging ledger coverage through cooperation among token holders will make it a stable strategy favorable for everyone.

<p style="text-align:center;"><img src="../static/img/blc.png">

The past cone of each transaction cannot contain conflicts as per ledger consistency requirements. It means transaction which conflicts with the "broadest" ledger will be *orphaned* (abandoned).

## Biggest ledger coverage

The intuitive concept of the "broadest" ledger needs to be quantified.

The **ledger coverage** of transaction $T$, denoted as $coverage(T)$, is the metric which tells how "broadly" the transaction $T$ covers outputs in the chosen past ledger state called the *baseline state*. It is calculated as a sum of amounts of all outputs consumed by the past cone of $T$ in the baseline state. The following picture illustrates this:

<p style="text-align:center;"><img src="../static/img/blc1.png">
</p>

Each token holder produces their transaction with the biggest ledger coverage possible in the constantly changing DAG at any given moment. This is the **biggest ledger coverage** rule.

The *biggest ledger coverage rule* is analogous to the *longest chain rule* in Bitcoin and other PoW blockchains. In Proxima, each token holder produces transaction that covers the maximum tokens in the baseline ledger state with their past cone.

However, the *ledger coverage* as defined above cannot grow forever: it will stop growing when it covers all outputs on the baseline state. So, the vanilla DAG does not suite the *biggest ledger coverage rule*. To overcome this and other problems, Proxima enforces additional constrains and incentives which make the *biggest ledger coverage rule* an optimal strategy on the UTXO tangle.

*Chains*, *sequencers* and *branches* are the main ledger constraints in the UTXO tangle, guiding participants towards eventual consensus.

## Sequencers
*Sequencers* build chains of transactions called *sequencer transactions*. By design, only sequencer transactions are allowed to consolidate several ledger states by endorsing other sequencer transactions. For more about chains and sequencers, see the [incentives](overview/incentives.md).

The above makes the cooperative consensus in Proxima a cooperation among sequencers. Each sequencer issues its transaction with as big a ledger coverage as possible in the dynamic context. Note that "consolidation" of the ledger states means consuming and endorsing other non-conflicting transactions in the past cone. By endorsing other sequencer chain transactions, the sequencer transaction can achieve bigger ledger coverage than the predecessor in the chain. This way, the sequencer chain is always advancing by growing its ledger coverage. This is only possible when sequencers cooperate by consolidating others into their own ledger state.

<p style="text-align:center;"><img src="../static/img/sequencers.png">
</p>

### Conflict resolution
Ledger cannot contain conflicting transactions of double-spends of any output. This rule is enforced by the node whenever it adds a new transaction to the UTXO tangle, ensuring that the past cone of every vertex in the UTXO tangle DAG remains conflict-free.

However, transactions on the UTXO tangle can conflict for various reasons. Sequencer transactions that conflict cannot be integrated into the past cone of new transactions, which is a common occurrence on the UTXO tangle.

Double-spending effectively forks the ledger into incompatible versions.

How does the *biggest ledger coverage rule* handles these situations? We cannot allow situations where a sequencer **Blue** cannot proceed with increased ledger coverage simply because both **Blue** and another sequencer, **Green**, accidentally spent the same output in their past cones. This scenario would make the system vulnerable to attacks.

<p style="text-align:center;"><img src="../static/img/conflict1.png">
</p>

The smart strategy for the token holder **Blue** is not to limit its options for the next chain transaction solely to the latest one. **Blue** can consider legitimate alternative fork points in the chain's past as long as they guarantee an increase in the current ledger coverage of the chain.

Sequencer **Blue** will revert its chain state to a point where it does not conflict with the latest state of another sequencer **Green**, which has the larger ledger coverage.

There is always a guaranteed *revert point* in the **Blue** chain that meets these criteria. Each sequencer transaction represents a ledger state, and we identify the output with the **Blue** chain's chain ID in the ledger state of **Green**. This transaction, denoted as $R_{Blue}$, serves as the basis for the next **Blue** transaction that can endorse **Green** without conflict.

<p style="text-align:center;"><img src="../static/img/conflict2.png">
</p>

This demonstrates how sequencers avoid conflicts and construct chains with growing ledger coverage.

The above diagram presents somehow simplified process, of course. Sequencers expand their coverage not only by endorsing transactions on other sequencers but also by consuming *tag-along* and *delegation* outputs. When reverting their state, sequencers may lose the latest transactions in their state, necessitating their "re-consumption" in the new chain fork, provided they do not conflict.

Moreover, conflicts are common on the UTXO tangle, turning the selection of the next transaction with the largest ledger coverage into an optimization problem for sequencer **Blue**. **Blue** must traverse all possible endorsement targets on the **Green** chain ($G_1, \dots, G_n$) and all potential revert points $R_{Blue}$ to identify the transaction with the maximum coverage.

Each sequencer chain can advance with growing ledger coverage through mutual cooperation. As sequencers endorse each other, conflicting transactions are naturally orphaned from the main stream of chain transactions.

The above would be some kind of competition between sequencers on who  is the best in cooperation. If sequencer does not cooperate by endorsing others, its transactions will likely be orphaned.

## Branches

The ledger coverage of any chain cannot expand indefinitely; it stops growing when its past cone encompasses the entire baseline ledger state. The total number of tokens on the ledger imposes a cap on ledger coverage. Consequently, the biggest ledger coverage rule will ultimately converge to an equal maximum value for all sequencer chains.

To address this issue, we introduce **branch transactions**, also known as **branches**, which periodically "reset" ledger coverage at each slot boundary.

A *branch* is simply a sequencer transaction occurring at a slot boundary. We divide the ledger's timeline into slots and impose specific constraints when a sequencer chain transitions from one slot to the next with a branch transaction. While not mandatory, sequencer chains are incentivized to include a branch transaction at each slot boundary.

Slot boundaries and branches serve several crucial functions:

1. Each branch's ledger state is automatically stored in the database as a distinct ledger state. When a node verifies a valid branch transaction, it persists the corresponding ledger state in the multi-ledger database for access by other components. This branch's ledger state then becomes a potential baseline for transactions in the subsequent slot.
2. Branches occurring at the boundary of the same slot are intentionally conflicting ledger states. They are designed to consume outputs from the previous branch, referred to as the stem, effectively resulting in double-spends. A transaction cannot include two branches from the same slot in its past cone. Consequently, each transaction on the UTXO tangle will have a singular chain of branches in its past cone.
3. Sequencer transactions can endorse other sequencer transactions only within the boundaries of the same slot. Cross-boundary endorsements are forbidden on the ledger according to validity constraints.
4. If a sequencer chain lacks a branch at a specific slot boundary, it must endorse another sequencer transaction that does have a branch, either directly or indirectly.

Constraints 3 and 4 compel each sequencer transaction to explicitly determine to which baseline ledger state (branch) it belongs. Therefore, **each sequencer transaction is tied to a deterministic baseline state** that is universally recognized by all nodes. Sequencer transactions can endorse each other only if their baseline states do not conflict.

Constraint 2 ensures a single chain of branches, making the biggest ledger coverage rule a consensus rule. By adhering to this rule, the group of cooperating sequencers achieves consensus on a unified chain of branches, representing the singular historical evolution of the ledger state. Any branches not included in this chain are orphaned.

In essence, history is shaped by the most successful participants—those who cooperate effectively, often with a measure of good fortune.

<p style="text-align:center;"><img src="../static/img/big_picture.png">
</p>

### Selecting a branch
All branches on the same slot boundary are intentionally conflicting. Let's explore how the biggest ledger coverage rule manages conflict resolution among branches.

It's important to note that we adhere strictly to the same ledger coverage rule, keeping it as straightforward as possible: each sequencer aims to produce a valid next transaction in the chain with the maximum ledger coverage achievable within a given time period. We do not introduce any special transaction types or outputs beyond the requirement that transactions must satisfy immutable global ledger constraints.

Sequencers are incentivized to include branch transactions in their chains because only branch transactions can potentially include a random **branch inflation bonus**.

However, only one of several conflicting branch transactions will be incorporated into the future consensus ledger state. The determination of which branch survives is left to the biggest ledger coverage rule. This process resembles a kind of lottery among branches, with the outcome dictated by the rule favoring the transaction with the highest ledger coverage. Our goal is to ensure this lottery remains unbiased and fair.

Sequencer chains whose branches do not achieve the highest coverage (due to factors including the random branch inflation bonus) must revert back to the chain transaction from the previous slot and resume their chain from there. While they lose out on the branch inflation bonus lottery, they retain the ability to continue their chains uninterrupted.

<p style="text-align:center;"><img src="../static/img/branch_cooperation.png">
</p>

Several questions still remain unanswered. Here are concise answers based on the Proxima whitepaper:

*What to do with ever-growing ledger coverage?*

The solution involves adjusting the calculation of ledger coverage by considering individual baseline states for each slot along the winning chain of branches. This is achieved by taking a weighted sum of ledger coverages for each baseline state, with weights exponentially decreasing as slots move further into the past.

*How to avoid bias of the *branch inflation bonus* lottery in favour of "richer" sequencers, i.e., those with more tokens?*

This kind of bias would be highly undesirable because it would mean the network will quickly centralize around the richest sequencers.

Proxima addresses this issue with a provably random branch inflation bonus. Using a verifiable random function (VRF), similar to Algorand's approach, sequencers are required to provide a pseudo-random yet deterministic (non-manipulable) value for new inflated tokens on each branch. The biggest ledger coverage rule then favors the branch with the highest branch inflation bonus for endorsement by other sequencers, irrespective of the token amount on the chain output. This approach ensures that the branch with the largest branch inflation bonus becomes the (random) winner of the branch lottery at the slot boundary, promoting fairness and equal opportunity among sequencers.

For more detailed analysis, please refer to the Proxima whitepaper.

