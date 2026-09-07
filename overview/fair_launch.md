# The fair launch: design and plan

*This document describes a design and a set of projections. It will be revised during and
after the pre-launch. It is not an offer. Nothing here is sold and nothing here is
promised.*

Background: the [Proxima manifesto and documentation](https://lunfardo314.github.io/) and the
[technical whitepaper](https://arxiv.org/pdf/2411.16456).

**The founder** is whoever creates the genesis ledger state and puts the bootstrap capital to
work running that ledger under the cooperative consensus protocol. The word denotes that role
and nothing else: no office, no entity, no status conferred by the protocol, and no rights
beyond those any holder of the same tokens has. The role is defined by what it does, so it
lasts exactly as long as it is doing it — once the ledger advances without that capital, the
role has no content left.

---

## 1. Goal

Launch Proxima as a decentralized ledger and hand control of it to a permissionless community
of token holders.

Decentralization is the prerequisite for the security of the ledger and the criterion of the
project's success. It is the feature Proxima was designed for. Not reaching it is failure.

Proxima is a cooperative consensus: a DAG of UTXO transactions, also known as _the tangle_, where consensus on the ledger
state comes from token holders cooperating to form a transaction set covering the biggest
possible amount of their holdings. No miners voting, no validator committee, no block
producers, no staking contract — only token holders exchanging transactions, each following
economic constraints and playing a self-assigned role, incentivized to cooperate while seeking
their own benefit.

The consequence: **Proxima is as decentralized as its active token holdings are distributed.**
If one entity holds most of the tokens, one entity decides the ledger.

Token distribution is therefore not marketing attached to the protocol. It is the **security
mechanism**. Decentralization is the process of moving the supply into as many independent
participants in the consensus as possible, permissionlessly.

### Two things decentralize

- **holdings** — who owns the coverage. Mining moves this, permissionlessly, with nobody
  deciding anything;
- **sequencing** — who assembles transactions into the DAG and commits ledger states. Coverage
  counts only through a sequencer that puts it to work.

A sequencer is a token holder generating inflation from its own tokens on the ledger who, by
running, also carries other holders' tokens — earning them their inflation in exchange for a
cut of it. Delegated tokens never leave their holder: the sequencer never has the key, the lock
stays the holder's, and the holder can take them back. The sequencer holds nothing on anyone's
behalf. Somebody operates the server, but the protocol confers no role for it: no licence, no
registration, no admission. The tokens are the qualification.

In Phase 1 both are the founder's. Holdings decentralize by mining alone; sequencing only when
holders act. A token earns inflation only while it works in the consensus, and a holder has two
ways to make it work, each with its cost in a different place:

- **delegate to a sequencer.** The cost is on the ledger: the sequencer takes a cut of the
  inflation the delegated tokens generate. Nothing to run;
- **run a sequencer.** No cost on the ledger — the holder keeps the whole inflation on its own
  tokens and collects a cut on everyone else's — but a real-world one: a server, bandwidth,
  uptime.

Which of the two a holder picks is a market decision, settled by the spread between a
sequencer's cut and the price of running a server. Cuts too high pay holders to run their own;
too low and running one stops being worth it. Nothing sets that balance from above.

Distributed holdings with concentrated sequencing is the weaker outcome, and the protocol does
not forbid it. What works against it is that centralization of any kind is against the interest
of the token holders themselves: their security is their distribution.

---

## 2. The two phases

Proxima runs in two phases, marked by how much of the supply the founder holds. What separates
them is a band rather than a line.

**Phase 1 — centralized.** The founder holds enough of the supply to run the ledger alone: it
runs because the founder runs it, and it stops when the founder stops it. The ledger in this
phase is an exercise on the technology. It rests on trust in one entity, therefore it carries
no value, and it comes with no obligations, no guarantees and no commitments of any kind —
including no commitment to continue it. During this phase, it may be discarded and restarted
from a fresh genesis at any time, without prior notice, any number of times. In theory, this can
last forever. However, repeating that indefinitely would be the failure of the project, not its plan.

**Phase 2 — decentralized.** The founder no longer holds enough of the supply to control the
ledger. The system runs and is not reversible or stoppable by anybody, the founder included. In
this phase nobody is in a position to make grounded promises about it, because nobody controls
it. There is no way back either: control, once gone, cannot be rebuilt.

**Phase 1 leads to Phase 2 by itself.** Nobody has to act for the transition to happen. Mining
moves the supply out of the founder's hands transit by transit (sections 5 and 6), and unless
the founder stops the process, it ends Phase 1 on its own. Stopping it is the only alternative
to it running to completion, and the founder makes no commitment either way: the sole statement
here is the intention to let it run.

### The transition is a band, not a line

The boundary is not a clean cut. Two thresholds bound it, expressed as the founder's share of
the supply:

- **above 7/12** — the founder can commit healthy ledger states alone, so the founder alone
  decides whether the ledger advances. This is Phase 1 proper;
- **between 7/12 and 5/12** — the founder can no longer advance the ledger alone, and neither
  can the rest without the founder. Control is shared and the founder can still stall by
  withdrawing;
- **below 5/12** — the ledger advances without the founder's participation. The founder is an
  ordinary holder.

The gap between the two thresholds is 2/12 = 1/6 of the supply, the same margin that bounds
forking (section 7). Reading it as the transition band assumes that up to 1/6 in one entity's
hands is tolerable concentration. That assumption, and the thresholds derived from it, follow
from the ledger's constants and simple arithmetic under assumptions about how much capital
participates.

---

## 3. Starting from zero

Proxima today is a maximally centralized project. One person authored the concept, the
whitepaper, the docs and the code. There is no funding, no team, no company, no investors, no
ICO, no presale, no VC allocation, no treasury, no foundation. There is an MIT-licensed
repository and a technical whitepaper PDF. There is no sunk cost behind it or cost to be compensated.

Bitcoin started the same way and may be more centralized still: one pseudonymous author, one PDF, no
publicity, one node, and for a while one miner holding the entire supply and all the hashrate.
Bitcoin became decentralized by attracting participants.

The approach is the same in one further respect: **code first**. The project launches with an
existing code base implementing the concept, not with a promise to build one.

Every ledger takes this path — from fully centralized to fully decentralized — whatever its
consensus. Every one begins as code written by one entity that nobody else is running, and
decentralizes gradually or not at all. What can be engineered is not the absence of an initial
center, but how fast it dissolves, what dissolves it, and whether it can rebuild itself once
gone.

The grounds for any obligation follow the same curve, by construction:

- in Phase 1 there is nothing of value and nothing sold. What is normally sold at a launch is a
  *promise* — a roadmap, a treasury, a team, a product that does not exist yet. That is the
  standard model in crypto, and it is exactly what creates obligations to somebody. There is no
  promise here to sell, and nothing is taken from anybody;
- in Phase 2 the ledger is outside the founder's control, who can affect it no more than any
  other holder of the same tokens.

There is no point on that curve where the founder holds both control and something of market
value carrying other people's expectations. **Success means the control leaving the founder.**

---

## 4. Bootstrap capital

At genesis the ledger mints **60,000,000 PROX** (6×10¹³ motes), controlled by the founder —
six per cent of the one-billion target supply. That amount, and all inflation it generates,
is the **bootstrap capital**. Phase 1 lasts while it is large enough to run the ledger on its
own.

### Why it exists

A consensus weighted by token holdings cannot start from zero token holdings. Coverage is the
anti-Sybil substance of a cooperative consensus, exactly as hashrate is for proof of work, and
at slot zero somebody has to hold it. This is a direct consequence of not using proof of work
to secure the ledger.

It exists to be outgrown: 6 % of the target supply at genesis, 94 % minted by mining. The
smaller the genesis share, the larger the share reaching people through mining.

### No distribution

Nothing in the genesis supply is allocated to anybody except the founder — no investors, no
advisors, no foundation, no recipients of any kind. It sits in one place because at genesis
there is exactly one participant and the consensus requires the coverage base to be held from
slot zero. It is a structural consequence of how the consensus works, not a distribution
event.

Nobody was paid with it. A single entity cannot pay itself with tokens it created out of
nothing. Nothing in Phase 1 gives it value, and the founder assigns it none.

There are no insiders, only people who started following the project earlier than others. The
rules are the same for everybody; the outcomes are not, and section 10 says why.

### What it is for

To secure the ledger through Phase 1: to commit ledger states while there is nobody else
holding enough coverage to do it. As the system enters Phase 2 that need ends, the role
dissolves, and what remains is an ordinary token holding.

One owner, several sequencers: the founder splits the bootstrap capital among a number of
them, so that the ledger survives one of them going down. Through Phase 1 those
sequencers collect what any sequencer collects: the inflation on their own tokens, the cut on
tokens delegated to them, and the tag-along fees of the mining transactions they include. The
covenant caps the fee at 1 % of each reward; a cut is published by the sequencer that takes it
and paid only by those who choose to delegate to it. All of it counts as bootstrap capital
here, and all of it is on the ledger for anyone to read.

Nothing is held on anyone else's behalf and nothing is earmarked for release: no treasury, no
vesting contract, no lock, no distribution mechanism, no schedule, no undertaking of any kind.
Nobody should expect to receive any of it, and nobody should plan on the basis that it will or
will not move. A change of hands does not weaken the ledger — the incentive to put tokens to
work in the consensus is a property of holding them, not of who holds them — so no undertaking
to keep it is owed; and any reassurance about it, a lockup or a vesting schedule, would itself
create an obligation and invite reliance on it.

What matters is not what the founder promises about it but what the founder can still do with
it, and when that ends. That is section 7.

---

## 5. Decentralization capital

**940,000,000 PROX** (9.4×10¹⁴ motes) is held by nobody at genesis. It does not exist at
genesis. It is a ceiling written into the ledger, minted one transit at a time by whoever
produces a valid proof of work.

Call it the **decentralization capital**: it is the substance that takes the ledger out of the
founder's hands.

Nobody grants it. There is no faucet, no airdrop, no registration, no whitelist, no
application, no distribution act. Nobody — the founder included — can accelerate it, redirect
it, mint it to a different key, or take it back once minted.

For as long as the bootstrap capital can commit healthy ledger states alone, the founder can
slow the process or stop it. That is what makes Phase 1 centralized. It is a similar position a
founder with majority hashrate occupies at the start of any proof-of-work chain.
Section 7 gives its duration.

The rules are a covenant fixed in the ledger at genesis, written in EasyFL, running on every
node, readable by anyone: [`ledger/def/lock_mine.easyfl`](https://github.com/lunfardo314/proxima/blob/develop/ledger/def/lock_mine.easyfl). **The covenant is the authority; this
document only describes it.**

---

## 6. Mining

Everything below is enforced by the covenant. Where this text and the covenant disagree, the
covenant is right.

### The shape of it

The mine chain is a single chained UTXO, open to everybody — no signature unlocks it, only
compliance with its rules. Each transit is a transaction that:

- consumes the predecessor and produces the successor;
- mints the current reward out of thin air;
- pays **at least 99 %** of it to the key that signed the transaction;
- pays **at most 1 %** as a tag-along fee to a sequencer of the miner's choice;
- decrements the remaining-mintable counter by the amount minted;
- carries a proof of work.

About **804,000 transits** exhaust the mintable supply. The chain is then dead and no further
token can be minted this way.

### Flat reward, then rising

The reward starts at **500 PROX** per transit and stays there for the first **~46 days**.
After that it grows linearly, by a fixed small amount every slot, ending near 2000 PROX at the
last transit.

The flat phase is set to the projected length of Phase 1: the reward stays constant while the
bootstrap capital can still run the ledger alone, and starts growing once it cannot.

Emission advances only when somebody transits the chain, so a reward too small to attract
miners in the first weeks would stall it and thereby lengthen Phase 1. The rise afterwards
keeps a transit worth attempting as difficulty tracks hashrate, which carries the long tail to
exhaustion.

Reward per transit is therefore lower early and higher late; difficulty moves the other way,
tracking whatever hashrate shows up. A given amount of CPU wins a larger share of the transits
early and a smaller share late.

### The proof of work

`blake2b` of the **whole signed transaction** must end in at least `K` zero bits. The miner
varies a nonce in the input's unlock parameters, which changes the transaction id, the
signature, and the hash.

Every attempt requires a **fresh Ed25519 signature under the miner's own key**. Three
consequences:

- **Not outsourceable.** The private key sits inside the hot loop. Hand it to a pool and you
  hand over the reward: the covenant forces ≥ 99 % of every payout to the signing key. Mining
  pools — the largest source of concentration in every proof-of-work chain launched so far —
  have no foothold here.
- **ASIC-hostile.** The inner loop is a signature, not a bare hash. Special hardware can shave
  a constant off it; it cannot build the orders-of-magnitude moat a bare hash invites.
- **CPU-egalitarian.** Flat marginal cost per attempt, no economy of scale, no discount for
  size.

Call it **proof-of-signing-work**.

### Difficulty and competition

Difficulty is **adaptive**: the covenant raises and lowers it to hold the pace near its target
of **4 slots** per transit, whatever hashrate shows up. Transits land a little later than the
target, because the difficulty a transit must satisfy eases as the gap grows: about 4.5 slots,
some 46 seconds. That is the pace the projections of section 7 assume. The retarget rule is in
the covenant.

The rest follows from this being a proof-of-work race on a chain. Many miners work on the same
tip, one lands the transit, the rest move on. Competing transits for the same step are
double-spends of the mine-chain output and the ledger settles them like any other. Miners
build on the mine chain with the most work behind it.

Every node exposes a stream of mining transactions as they arrive and the reference miner
subscribes by default. Without it, the only way to learn that somebody won a height is to wait
for ledger confirmation, which takes longer than mining a transit — so whoever won once would
stay ahead. With it, that lead collapses to a gossip hop. A miner can subscribe to several
independent nodes at once, which makes withholding by a single node ineffective, and verifies
every transit from the raw bytes rather than trusting the relay.

The reference miner is `proxi node mine` ([Mining](participate/mine.md)). It is not privileged in any way. Write your own; the
only thing that decides anything is whether your transaction is valid.

### The work stops

Proxima does not burn energy to defend the ledger. The work here is spent once, to put tokens
into the hands of everyone who wants them — in a cooperative consensus, distributing the
tokens *is* securing the ledger. When the last transit lands, the energy cost of Proxima
becomes negligible and the ledger keeps running, secured by the distribution the mining
produced.

---

## 7. The transition

None of the numbers below is a promise. They follow from the covenant and from arithmetic,
under assumptions about how much capital participates, and they have not been checked against a
peer-reviewed model of this consensus. Treat them as the design's working estimates.

### The rule everything follows from

A branch — a committed ledger state — is accepted by a node as a healthy tip only if it carries
more than **7/12** of the coverage. The fraction deserves a caveat, because it is not a protocol
constant of the 51 % or 2/3 kind. The ledger rules do not enforce it: a branch carrying less is
still a valid transaction. It is a policy every node applies when it accepts a committed state,
and every sequencer when it decides to produce one — a confirmation threshold of the same nature
as a Bitcoin recipient's choice to wait for six blocks, only applied by sequencers. The value is
read from the ledger definitions so that all nodes agree on it, and it can be changed by a ledger
upgrade without invalidating anything already committed. A node could run with a different
value; it would then disagree with the rest of the network about which states are final, which
helps nobody, so in practice everybody uses the same one. A holder is likewise free to apply a
stricter criterion before treating a payment as final. What the node implements today is a depth
behind the latest reliable branch, a chosen compromise; nothing in the protocol prevents a
stricter one.

Everything here is a corollary of that policy:

- **Founder's side.** While the bootstrap capital holds more than 7/12, the founder can produce
  healthy branches alone and can stop the ledger by refusing to. When the decentralization
  capital passes **5/12**, that ends and does not come back: from there the founder cannot
  advance the ledger without the rest of the network. Withdrawing can still stall it, because
  the rest of the network cannot reach 7/12 without the founder either — that is the transition
  band of section 2.
- **Community's side.** When the decentralization capital passes **7/12**, the ledger advances
  without the bootstrap capital at all and the band closes. The founder becomes an ordinary
  holder — not by stepping aside, but because it no longer matters.
- **Attacker's side.** Two healthy forks would need 7/12 each and there is only 12/12 to go
  around, so an adversary needs the overlap — **2/12 = 1/6** of the supply — to keep two
  disconnected healthy forks alive at once. That 1/6 is the safety margin. The constant is a
  parameter of choice: raising it makes forking dearer and stalls more likely, lowering it does
  the reverse.

### Projections from genesis, at the pace transits actually land

| Milestone | Condition | Projection |
|---|---|---|
| Phase 1 ends, transition band opens: founder can no longer advance the ledger alone | decentralization capital > 5/12 | **~46 days** |
| Decentralization capital overtakes bootstrap capital | > 1/2 | **~63 days** |
| Band closes, Phase 2: ledger advances without the bootstrap capital at all | decentralization capital > 7/12 | **~84 days** |
| Emission complete | ~804,000 transits | **~14 months** |
| End state | decentralization capital share | **~94 %** |

The first line and the length of the flat reward phase are the same ~46 days by construction.
The band spans the two, and nothing marks its edges on the day they are crossed: the shares
move continuously and the effects appear as tendencies before they are arithmetically exact.

### Participation, not holding, is what counts

The thresholds measure coverage, and coverage is capped by holdings. A token that sits idle
contributes nothing to either side.

Every token that contributes to the consensus is paid new tokens, and the decision belongs to
its holder. Holdings that do not contribute are diluted by those that do. There is no class of
passive holders in Proxima; they are disincentivized by design. The incentive model is really a
disincentive for sitting still: the inflation a holder collects only protects the holding from
being diluted.

The systemic consequence: since a healthy branch needs more than 7/12 of the coverage, **more
than 7/12 of the supply has to be actively participating at any time, or branches stop being
produced.** A Proxima where most tokens sit still is not a slow Proxima; it is a stalled one.
The milestones above assume miners do what the incentives push them toward — running a
sequencer with mined tokens or delegating them, which is the sequencing half of section 1. How
reliably that happens is an open question; see section 10.

### Until then

While the bootstrap capital holds more than 7/12 of the coverage, the founder can halt the
network or refuse to include mining transactions. In Phase 1 the process described here runs
because the founder lets it run.

This is not peculiar to Proxima. A founder launching a proof-of-work chain with more hashrate
than anybody else, controlling access to the nodes, is in the same position for as long, and
every chain passed through that interval. It is what launching means.

What bounds it is not a promise but the fact that using it is self-defeating. Proxima makes one
claim: that a ledger can be Nakamoto-decentralized without proof of work securing it. A Proxima
that stays under its founder's control has refuted that claim, and is worth nothing — to the
founder first of all. Nor is it a quiet lever: withheld mining is visible on-chain to anyone
watching, and it does not work in moderation. The only way to keep control is to stop mining
altogether, publicly and indefinitely, which ends the project rather than saves it.

Note what this power is not. It is **negative only**. The founder can delay the process; the
founder cannot direct it. Nothing lets the founder choose who mines, mint to a key of its
choosing, or take back a token once minted — the covenant forbids all three, from slot zero,
permanently.

The bootstrap capital itself is a different matter. The covenant governs what is *minted*, not
what is already *held*, so nothing in the ledger constrains those tokens. Nothing outside it
puts them on offer either: they are not for sale, and section 11 applies to them as to every
other token.

---

## 8. Supply

60 M at genesis, 940 M mintable, and inflation on top of both.

Proxima's supply is not a deterministic curve of the Bitcoin kind. Inflation accrues only to
capital that participates in the consensus, from two sources: a chain inflation whose rate is a
decaying fraction of the participating amount, and a pseudo-random yet flatly capped per-slot
bonus to whoever produces the committed ledger state. The flat part is large relative to a small
supply and negligible relative to a large one, so observed supply growth is high at the beginning
and falls quickly. How much is realized depends on how much capital participates and on how mining goes. Every
supply figure in this document is an approximation; total supply will pass 1 billion PROX and
keep growing slowly thereafter.

This is closer to how an economy works than to a fixed emission schedule, and it is deliberate.
The alternative — rewarding capital for doing nothing — is the failure mode a coverage-based
consensus cannot afford.

---

## 9. Pre-launch and reset

Every network begins as a Phase 1 in the sense of section 2: it may be discarded and restarted
from a fresh genesis at any time, without notice, as many times as it takes. **No network can
be called the main one in advance.** Which network turns out to have been the launch is known
only afterwards, when one reaches Phase 2. Until then every network is a pre-launch, whatever
it is called while it runs.

The intention here is one pre-launch and then a reset that, probably, survives into the
decentralized mainnet. That is an intention: not a promise, not a guarantee, and not a count.

### Pre-launch

The protocol and node code are the ones intended to be carried through the reset. Mining is
open and permissionless. Goals:

- tune the constants against real hashrate and real participation;
- find bugs and attack vectors while nothing is at stake;
- reach the people who will run nodes, sequencers and miners afterwards.

Expected duration: a few months or less. It may be run again from a fresh genesis, and again,
until the founder is satisfied with what it shows. Restarting is not a contingency and not a
failure of the plan; it is what a pre-launch is for.

**A pre-launch ledger will be destroyed** while the founder still controls it: discarded and
genesis regenerated with fresh keys, at a moment chosen by the founder. **Tokens mined during a
pre-launch confer no rights, will not be honoured, will not be carried over, and will cease to
exist; nothing here gives them value.** Anyone mining on a pre-launch does so for the exercise.

### After the reset

Fresh genesis, fresh keys, the same protocol and mining covenant — or transparently modified
according to what the pre-launch teaches. From that point the covenant is fixed: nobody, the
founder included, can change the rules, the amounts, or the destination of a single mined
token, and section 7 describes how it is expected to run.

It starts as a Phase 1 like every network before it. Whether it becomes the mainnet is decided
by whether it reaches Phase 2, and the founder neither promises nor guarantees that it does.

Crossing into Phase 2 cannot be undone — that is what Phase 2 is. The intention stated in
section 2, to let the process run, is held against that fact: what precedes the crossing is
watching how the network actually behaves, and thinking twice.

---

## 10. Risks and open questions

Stated because they are real, not because they are resolved:

- **Phase 1 and the band.** Until the decentralization capital passes 5/12 the founder can stop
  the network or withhold mining, and can discard the ledger and start over. Through the band
  that follows, up to 7/12, the founder can no longer advance the ledger alone but can still
  stall it by withdrawing. Everything else on this list bites in the same period.
- **Where the band's edges are.** 7/12 and 5/12 come from one constant chosen by design and
  from arithmetic on shares that participate. Reading them as the start and end of the
  transition assumes up to 1/6 of the supply in one entity's hands is tolerable. Neither the
  constant nor that reading rests on a peer-reviewed model of this consensus.
- **The length of the runway.** The design turns on one number nobody has measured: how long it
  takes for enough capital to be mined *and put to work* that the network no longer needs the
  bootstrap capital. 46 days is a judgement. Too short and the ledger stalls instead of
  decentralizing; too long and Phase 1 outlasts its purpose. The pre-launch exists in large
  part to replace that judgement with a measurement.
- **Participation mechanics.** The milestones assume mined tokens are put to work — run in a
  sequencer the miner controls, or delegated. The reference miner delegates its payouts by
  default and can add to an existing delegation, but how a miner should behave across many
  sequencers over a long run is still being learned.
- **Scalability of participation.** Many holders delegating to many sequencers is a regime the
  network has not been run in. How many delegations a sequencer can carry, and how that behaves
  as holders and sequencers multiply, has been modelled and needs measuring.
- **Early concentration.** Whoever shows up first with CPU takes a large share of the first
  weeks' emission — expect the largest single actor somewhere around a third to a half of
  month-one emission. Non-outsourceability and the absence of an ASIC moat limit how large, the
  flat opening reward keeps the first weeks from being disproportionately valuable, and the
  ~14-month tail dilutes what remains. It will not be even. **Fair launch means equal rules,
  not equal outcomes.**
- **Reach.** Where a network is announced decides who mines first, and therefore what early
  concentration looks like. That is a practical problem rather than a protocol one, and it is
  unresolved. The pre-launch of section 9 mitigates it.
- **The rising reward** is a design choice, reasoned in section 6 and untested against a real
  launch.
- **Information asymmetry between miners.** Whoever produces a transit knows it first — left
  alone, fatal to fairness, since the lead outlasts the time to mine the next transit. Broadly
  similar to *selfish mining* in proof-of-work networks. Addressed and shipped: nodes stream
  mining transactions as they arrive, the reference miner subscribes by default and to several
  nodes if asked, verifies what it receives, and never prefers a transit for being its own.
  What remains is one gossip hop, which decides anything only if difficulty falls so low that
  solving is far faster than the pace. On the testnet it does not.
- **Difficulty tuning.** Adaptive difficulty on a chain with a miner-chosen pace is subtle and
  has been through several iterations. The current design holds a steady pace near its target
  on the testnet without the oscillation earlier ones showed, but has not been tested against
  hashrate in the amounts a real launch would bring.
- **Everything else.** New consensus, new tokenomics, unproven code. It may fail outright.

---

## 11. No offer, no promise, no expectation

- Nothing is offered or sold, at any price, to anybody. There is no sale, no subscription, no
  allocation, no fundraising, and no mechanism by which anyone can pay the founder for a token.
- Nothing in this document is an undertaking, guarantee, or commitment to anyone. Statements
  about the future describe how the software is designed to behave and the founder's present
  view, not obligations owed to any person.
- The founder does not undertake to start, continue, maintain, or restart any network, and may
  discontinue or reset one at any time without notice.
- PROX has no counterparty, no redemption, no backing, no support obligation, and no promise of
  value, liquidity, listing, or a market. Nobody sells it, backs it, or owes anything on it. The
  founder provides no service, holds nothing for anyone, and has no roadmap obligation to
  anyone.
- Tokens minted through the mine chain are created by the person who mints them, under rules
  fixed at genesis, out of nothing. They are not transferred, granted, distributed, or released
  by the founder, who cannot do any of those things.
- The software is published under the MIT licence and provided as is, without warranty of any
  kind. Running it is the choice and the responsibility of whoever runs it.
- Anyone who acquires or mints PROX does so entirely at their own risk and on their own
  judgement.

---

See also: [Tokens and supply](overview/2-tokens-and-supply.md) for the numbers,
[Mining](participate/mine.md) for running the miner, and
[Launch phase network](participate/launch_network.md) for the network as it runs today.
