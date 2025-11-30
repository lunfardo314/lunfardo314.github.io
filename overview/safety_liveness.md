# Safety and liveness

Cooperative consensus is a [Nakamoto consensus](https://medium.com/@lunfardo/on-definition-of-nakamoto-consensus-be8f4b84c899). 
That is, it is permissionless and probabilistic by its nature.

In Nakamoto consensus, the full set of participants is undetermined and remains unknown to the protocol and any individual participant--a defining characteristic of this approach. Unlike PBFT protocols where consensus involves communication and voting within a defined committee until agreement is reached, Nakamoto consensus participants individually follow optimal strategies (as per Nash equilibrium), driven by local data and oblivious to the history, and without direct consideration of other participants' states. This process leads to *convergence* towards global consensus over time, rather than a deterministic *reaching* of consensus.

Proof-of-Stake (PoS) systems, typically classified under PBFT, exhibit *conditional decentralization* based on factors such as committee formation and other protocol-specific criteria.

In contrast, Nakamoto consensus systems, including Proxima's cooperative consensus, retain the decentralization and permissionless characteristics seen in Bitcoin and other Proof-of-Work (PoW) systems, despite not relying on PoW itself.

## Network partitions. Forks
When part of miners (in PoW), validators (PoS, PBFT) and token holders (cooperative consensus) can't communicate to the rest of the network, we have situation of dividing (partitioning) the network into several parts. It can happen due to communication failure or even due to intention _eclipse attack_.
Analyzing how the system behaves in such situations reveals differences between approaches towards fault-tolerance the decentralization. 
It may also be a convenient way to reason about majority attacks (such as 51% in PoW), because network split immediately changes the majority. 

We will roughly compare how distributed ledgers behave in each of the three principles described above. 
Note, that these are only thought experiments, while in the practical reality the picture may be much more complicated.

### PBFT, PoS
In PBFT (and most of PoS) systems, committees will continue operating as long as the largest partition of the network contains at least $\lfloor 2/3 \rfloor + 1$ of the validators. If this condition is not met, the system stops producing blocks -- a liveness issue. However, the system remains secure in the sense that transactions included in the ledger are considered valid and irreversible. This property is known as *deterministic consensus*.

*PBFT-based systems are said to prioritize safety over liveness.*

### PoW, Bitcoin, etc.
In PoW systems like Bitcoin, the response to the network split is different. If miners are isolated into separate partitions, each partition will continue producing blocks at a reduced rate (due to less hashrate in the partition) until the PoW difficulty adjusts accordingly. Consequently, each partition will maintain its own version or fork of the ledger. 
Due to the decentralization of the hashrate itself, generally speaking, there's no objective way to determine neither the fact of network split nor how much hashrate there is in the partition. Thus, this situation can persist unnoticed until the network reunites. 

It is said, *Nakamoto systems prioritize liveness over safety*. Users risk having their transactions included in a partition that might later be reverted.

After network reunites, forks are merged according to the _longest chain_ rule. This demonstrates automatic self-healing capabilities of Nakamoto PoW systems. This also demonstrates how the partition (perhaps a big mining pool) with more hash rate (>51% of the total) takes over the consensus after reunification. 

## Safety and liveness in Proxima
In Proxima's cooperative consensus, the behavior during network partitioning - specifically among token holders - is akin to that observed in PoW systems.

When isolated into partitions, each partition in Proxima continues to follow the biggest ledger coverage rule, maintaining its own chain of branches at the pre-split pace. This results in each partition representing its own **fork** of the ledger state.

Upon reconnecting the network partitions and resuming transaction exchange, nodes will synchronize their UTXO tangles. The biggest ledger coverage rule dictates that sequencers in partitions with smaller ledger coverage must revert their chains and start anew from the baseline state of the branch with the highest ledger coverage. Forks with lesser coverage will be orphaned, illustrating a form of "self-healing."

Thus, the cooperative consensus in Proxima exhibits behavior similar to PoW consensus systems, *prioritizing liveness over safety*, which is characteristic of Nakamoto consensus.

However, there are crucial safety-related distinctions between the two approaches.

In PoW systems like Bitcoin, users typically employ a "6 block rule" to ensure transaction safety, assuming the transaction is secure once buried under six blocks. This indirectly relies on the assumption that the user's chain is part of the partition with at least 51% of the global hashrate — a presumption lacking objective verification, because total hashrate has no bounds.

In Proxima's cooperative consensus, token holders may adopt a similar rule: waiting until all branches with ledger coverage exceeding 51% of the total token supply include their transaction $T$. Unlike PoW hashrate, maximum coverage is bounded by a constant: the total supply of tokens. 
Because of this, Proxima users know the partition's weight. It allows them to withhold admitting confirmation until a sufficient majority threshold is met. The sufficient majority is when it reaches $50\%+\theta>0$) of the total supply of tokens where $0<\theta<50\%$ is some parameter. The larger the $\theta$, the safer the transaction. By assuming small $\theta$, a token holder will risk her transaction to be reverted later. 

This perception of liveness in Proxima is tightly linked to safety assumptions. **Users consider the network non-operational until their transactions are deemed safe**.

Moreover, Proxima introduces considerations of malicious behavior among token holders. Security measures rely on economic incentives, where each token holder acts in their most profitable interest. This setup assumes legitimate behavior but necessitates precautions against economically motivated attacks.

For instance, during a network split where partitions are nearly equal, a token holder *Eve*, with a small stake, could attempt a *double-spending* or *long-range attack*. This scenario involves *Eve* being (secretly) able to communicate with both partitions and convincing the network to switch from a branch with *Alice*'s transaction $T$ to another branch without it. *Alice*, assuming her transaction is safe under the 51% token coverage assumption, risks financial loss.

In practice, executing such an attack profitably depends on factors like inflation opportunities and transaction values. *Alice* may assume larger security threshold, for example waiting until her transaction $T$ will be included into all branches with ledger coverage of $2/3$ of the total amount of tokens on the ledger.
In that case *Eve* would need to control $1/3$ of the total token supply to disrupt transactions on a large scale. This significant stake implies considerable financial risk for *Eve*, dissuading most attackers due to potential losses outweighing gains.

Analogous to why 2 or 3 dominant Bitcoin mining pools do not collude to alter rules like halving, Proxima's ledger security hinges on significant token holder commitment, emphasizing the importance of "skin-in-the-game" among stakeholders.

Our observation is that **security of any public permissionless ledger**, including PoW, ultimately depends on _skin-in-the-game_ of its dominant stakeholders, i.e. fundamentally rely on game-theoretical equilibrium. 

In summary, Proxima's cooperative consensus model merges aspects of PoW's robustness with novel mechanisms for managing safety and liveness during network partitions, incorporating economic incentives to maintain network integrity.
