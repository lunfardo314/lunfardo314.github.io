# Proxima. Incentives

The only participants with a genuine interest in the security of any distributed ledger are its end-users, the token holders. The rest must be incentivized to participate.

In Proxima, the sole category of participant is the token holder, the system's end-user. Unlike in other distributed ledgers, Proxima doesn't need to incentivize third parties, such as miners or validators, to run consensus on behalf of the end-users and keep the ledger secure.

Proxima's ledger gives token holders the freedom to choose their own strategies within the bounds set by enforced constraints. To ensure predictable behavior, the ledger's constraints must provide the right incentives. Here we present the system of incentives on the Proxima ledger, their types, and how they work for different token holder strategies.

The philosophy behind Proxima's incentives for participants (token holders) is *equity*, *financial fairness*, and *active contribution to consensus and security*. Proxima treats all token holders equally while aiming to motivate contributions to the consensus and security of the ledger, disincentivizing "lazy" token holders who do not contribute to the ledger's consensus and

## Inflation on the chain asset

The main element of incentives in Proxima is inflation on the chain. Each token holder is entitled to build chains of transactions on the ledger and earn *inflation income* by creating tokens out of thin air proportionally to their holdings and time.

### Chain asset
The **chain** (also known as the *UTXO chain*) is a sequence of chain outputs (UTXOs) constrained by a special type of validation script attached to the output called a *chain constraint*. The chain constraint on the output, known as the *predecessor*, invalidates any transactions that do not produce the single next output in the chain, called the *successor*. This enforces chain building, preventing the chain from forking into multiple chains on the ledger.

Each chain output in the chain bears a unique ID called the *chain ID*. Thus, chain outputs form a non-forkable chain of transactions on the ledger, all marked with the same *chain ID*.

There is always exactly one chain output for a particular *chain ID* on the ledger state. One can always retrieve that chain output by its *chain ID* from the ledger state.

Each chain represents a permanent *non-fungible* asset on the ledger with a unique ID. The *chain asset* has a state consisting of fungible tokens on the output, known as *on-chain tokens* or the *on-chain balance*, plus any other data and/or constraints. The chain output is always locked by a mandatory lock constraint called the *chain controller*, which usually is ordinary ED25519 account or *delegation lock*. *Chan controller* defines who, how and when can consume the chain output.

The state of the chain asset evolves along the chain. It is updated by the *chain controller* when they create a transaction with the produced *successor* chain output.

Chain constraints are used to build [sequencer chains](https://hackmd.io/@Evaldas/Syd4uSp8R), for delegation outputs, NFTs, and other ledger constructs that represent a single (sub)state of the ledger state.

A unique feature of the chain asset in Proxima is that by updating its state, a token holder **can create new tokens out of thin air** (inflation) proportionally to the on-chain tokens in the predecessor.

<p style="text-align:center;"><img src="//hackmd.io/_uploads/B19QDAjvA.png"  width="550">

### Ledger time

Each token holder can earn inflation income by building a chain of transactions. The underlying idea of this type of income is the common financial concept of ["time is money"](https://en.wikipedia.org/wiki/Time_value_of_money). In Proxima, this takes the form of *ledger time is money*. The *ledger time* is an ever-growing integer timestamp value of (time) *ticks* assigned to each transaction and each output. The ledger time of genesis outputs is $0$ ticks. $100$ ticks make a slot. The transaction timestamp is enforced to be strictly greater than the timestamps of its inputs. When $100$ divides the timestamp with a residual 0, the transaction is on the *slot boundary*.

Timestamps of outputs and transactions are subject to *pace constraints*, such as a minimum number of ticks between successor and predecessor transactions. For example, if an output has a timestamp of $1000$ ticks, the consuming transaction must have a timestamp of at least $1005$.

### Inflation
Let's say chain with ID *chainID* is represented by chain output $A$. It has an *on-chain balance* of $amount(A)$ of tokens on it. This balance is controlled by the chain, which, in turn, is controlled by the private key of the chain controller.

Let's say *successor* of output $A$ is output $A'$. According to the chain constraint, the token holder can create up to $I$ new tokens on the successor output, representing the inflation on the chain.

The amount $I$ is proportional to the $amount(A)$ and to the ledger time in ticks between outputs $A$ and $A'$. Let's denote the ledger time duration in ticks between transactions as $\Delta T$.

With some simplifications, the inflation amount for one step of the chain is:
$$
I = amount(A) \cdot \Delta T \cdot R
$$

Here $R$ is the **inflation rate**, an immutable constant on the ledger.

This way, every token holder can inflate their holdings by building chains. There is no other way to create new tokens in Proxima.

<p style="text-align:center;"><img src="//hackmd.io/_uploads/SJ32KCiDR.png"  width="500">

Note that the maximum amount of inflation generated on the ledger per year is capped at $totalSupply \cdot R_{annual}$. Here, $R_{annual}$ is the annual inflation rate, while $totalSupply$ represents the total number of tokens on the ledger at the beginning of the year.

Token holders who do not build chains will incur an opportunity cost equivalent to the "lost" tokens they could have otherwise created. This serves as a strong incentive to build chains.

To further incentivize continuous chain building, ledger constraints include an **inflation opportunity window** constant (spanning several or dozens of slots), which sets the upper bound for $\Delta T$, after which inflation $I$ will be zero. This forces token holders to issue chain outputs at least once every few slots. Lazy or slow token holders will miss the opportunity to generate income.

In addition to the inflation $I$, a random branch inflation bonus is added at each slot boundary. This incentivizes the issuance of *branch transactions* on the chain, which are necessary for the cooperative consensus. More details on this can be found in the whitepaper and [Selecting a branch](https://hackmd.io/@Evaldas/Syd4uSp8R).

The intentions behind these incentives are:

- To incentivize token holders to contribute to the security of the ledger through chain building (*sequencing* and *delegation*). See [cooperative consensus](https://hackmd.io/@Evaldas/Syd4uSp8R).
- To ensure *equity* and *financial fairness*. Each active token holder can expect a fair, proportional, and predictable return on their *skin-in-the-game* on the ledger.

It is reasonable to expect that some token holders will keep a certain amount of their holdings in passive wallet addresses, similar to how we keep some cash in our wallets or stash it under the mattress. This is their right. However, those funds won't be return-generating capital, resulting in a financial cost for the owner. This, however, makes sense as a limited cash (liquidity) reserve on the ledger.

The intended behavior for the majority of funds on the Proxima ledger is to contribute to the security of the ledger by building chains for the cooperative consensus.

### Inflation on transaction

The inflation $I$ represents maximum inflation on an output. For convenience, the inflation constraint is enforced at the transaction level. Let's denote $S$ as the sum of input amounts and $S'$ as the sum of output amounts.

For a transaction to be valid, it must satisfy the following condition:
$$
S' \le S + I_{sum}
$$    
where $I_{sum}$ is sum of the upper inflation bounds $I$ of all chain outputs produced by the transaction.

This condition allows for the distribution of newly created tokens among multiple outputs produced by the transaction.

## Sequencers
*Sequencers* are "professional" token holders who consistently build *sequencer chains* to earn inflation. By design, only sequencer chains can consolidate multiple ledger states, thus contributing to the consensus. Additionally, only sequencers are eligible to win the *branch inflation bonus*.

Becoming a sequencer is a voluntary decision for each token holder and represents one of several possible strategies for participating in the ledger.

The only requirement to become a sequencer is maintaining a minimum amount of tokens on a chain output. This requirement is a ledger constant intended to prevent the proliferation of small sequencers. A reasonable value for this minimum amount might be, for example, $1/1000$ of the total supply, which would cap the maximum number of sequencers at 1000.

### Deposits and custody
What are *sequencers* beyond being token holders with significant assets?

In general, sequencers will predominantly be large **custodians**, such as **crypto exchanges** or **L2 chains** enshrined on the Proxima ledger, whether trusted or zk-proven.

By taking tokens into custody on its chain on behalf of other token holders, a custodian can generate inflation from these deposits. Consequently, it is reasonable for the original token holder to expect interest on their deposited holdings from the sequencer.

The sequencer/custodian will pay interest on the deposit, potentially retaining a margin from the generated inflation. The specific charges and rates will be determined by competition in the custody market, similar to practices in the banking sector.

<p style="text-align:center;"><img src="//hackmd.io/_uploads/SJz8Zknv0.png"  width="500">

Depositing funds with a sequencer is one of several strategies for ordinary (non-sequencer) token holders to protect their holdings from the diluting effects of on-ledger inflation.

By depositing funds with a sequencer, token holders also contribute to the security of the cooperative consensus and the overall ledger.

However, custody involves **counterparty risk** and the need for **additional trust**: a crypto exchange or L2 chain must be trusted, much like banks. Depositing tokens off-ledger will always require additional trust assumptions, meaning it is **not trustless**.

On the other hand, the sequencer may also be a decentralized or zk-proven system itself, thereby mitigating these risks.

### Delegation
A **trustless** alternative to depositing funds with a sequencer is **delegation**, which does not require additional trust. Token holders can delegate their funds to a sequencer to generate inflation on their behalf without giving the sequencer control over their tokens.

To delegate, a token holder places a certain amount of tokens into a chain output. The special **delegation lock** grants the chosen sequencer the right to consume the delegated output in the sequencer transaction by producing a chain successor in the same transaction *without the ability to remove tokens from the delegated chain*. Thus, the sequencer can generate inflation from the delegated tokens but cannot "steal" those tokens.

The **revocation prescription** provided in the delegation output allows the delegating party to take back the delegated output according to the prescribed rules. The revocation prescription is based on ledger time sharing and offers various options: delegation may have a deadline, it may be returnable every fifth slot, or similar conditions. When the revocation condition is met, the token holder can consume the output and override the delegation conditions, for example, by delegating the tokens to another sequencer. Race conditions and potential double-spends do not occur, as either the delegating party or the sequencer can consume the output at a particular time, but never both.

The sequencer will use the delegated funds in its sequencer transactions to generate inflation. Whether the sequencer takes a *delegation margin* from the generated inflation is a matter of competition among sequencers in the market.

<p style="text-align:center;"><img src="//hackmd.io/_uploads/BJv6GJ2w0.png"  width="500">

### Branches
Branches in the Proxima ledger refer to sequencer transactions occurring precisely on slot boundaries. Each branch transaction competes for inclusion in the consensus ledger state, adhering to the principle that only one branch per slot can be accepted into the ledger. This mechanism ensures the convergence of the distributed ledger system towards a global consensus.

In a branch transaction, a **verifiably random inflation bonus** amount $B$ is enforced uniformly over a specific interval, distinct from the regular inflation rules described earlier. This random inflation bonus is crucial for determining which branch will be included in the consensus ledger state according to the biggest ledger coverage rule (refer to [Cooperative consensus](https://hackmd.io/@Evaldas/Syd4uSp8R) and the Proxima whitepaper for detailed explanations). Sequencers participate in a fair lottery for this branch inflation bonus on every slot boundary.

Therefore, in each slot, a sequencer earns inflation of at least
$$
I=amount(T) \cdot R_{slot}
$$
or, if fortunate enough
$$
I=amount(T) \cdot R_{slot} + B
$$

The branch inflation bonus serves as a significant incentive for token holders to operate as sequencers, as only sequencers have the opportunity to win this bonus.

## Tag-along mechanism

*Tagging-along* is a strategy used by token holders to incentivize a chosen sequencer to include their transaction in the sequencer's ledger state.

*Tagging-along* does not require any special mechanism. The producer of the transaction simply includes an output that sends a specified amount to the chosen sequencer. This output, known as the **tag-along output**, contains the **tag-along fee**.

The sequencer is naturally motivated to include this tag-along output in their ledger state. Consequently, the entire transaction, along with any chain transitions and associated inflation, becomes part of the cooperative consensus on the ledger state. Non-sequencer user essentially "bribes" the chosen sequencer to include the transaction in their ledger state.

There is a risk if the tagged-along sequencer is inactive or does not consume the tag-along output for any reason. In such cases, the transaction could be orphaned. To mitigate this risk, the transaction can include several tag-along outputs targeting different sequencers.

In summary, tagging-along leverages the tag-along output to persuade sequencers to include transactions in their ledger state, thereby participating in the cooperative consensus and potentially earning inflation without being a sequencer themselves.

## Motivation to run a sequencer

Sequencers, such as crypto exchanges or L2 smart contract chains, have their own compelling reasons to operate as sequencers and maintain their respective chains.

These entities derive income from various sources, including:

* inflation from own on-chain capital
* margin from inflation on deposited capital (trust-based)
* margin from inflation on delegated capital (trustless)
* tag-along service fees

The specific margins and fees charged by sequencers are determined by market dynamics and competition. Depending on market conditions, these fees and margins can vary, even to the extent of being offered at no cost in competitive environments.

In essence, running a sequencer on Proxima provides various financial incentives to entities willing to participate in maintaining the ledger state, catering to both token holders seeking security and income opportunities, as well as sequencers aiming to leverage their operational capabilities in the blockchain ecosystem.  
