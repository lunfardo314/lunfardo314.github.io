# Reset rules for the centralized phase of a take
_What the founder will look at, and what the community can do about it_

> **Draft, open for discussion.** Nothing here is final. The rules, the numbers and the
> wording are up for debate, and the founder wants to hear objections before any of it is
> settled. Comment on Discord.

A network started from a fresh genesis is a _take_. Each take launches in two phases. In
the centralized phase the founder holds enough of the supply to run the ledger alone, and
can stop it or reset it at any time. In the decentralized phase nobody can, the founder
included. Mining moves the network from the first phase to the second on its own, unless
the founder stops it.

Reset or let it go is the only lever the founder has. This document says how it will
likely be used, so that the community has measurable goals and knows what to expect.

It is not a promise of any kind. A centralized network can be reset at any moment, for
the reasons below or for others. Meeting the rules does not mean the take continues;
failing them means it very likely does not.

## Why a reset may be needed

The goal is Proxima running decentralized and unstoppable. That is not where the network
will be when the centralized phase ends, and nobody should count on it: the phase ends
with a small part of the supply mined, and the network decentralizes, or does not, while
the rest is mined. What the phase has to deliver is **healthy trends**: not decentralized
yet, but moving that way, with no known reason it cannot get there. Once the phase ends
there is no way back, so this is what gets checked before it ends, on three sides:

- **technical**: no known bugs or obstacles that would need a breaking change;
- **structural**: capital and sequencing are spreading, not gathering in fewer or less
  visible hands than the founder's;
- **community**: enough knowledge and activity around to maintain the network and drive
  it ahead.

The rest is up to the community and the market. Proxima positions itself, and wants to be
seen, this way:

> More decentralization means more value, more centralization means less.

Every holder can act on that: delegate where the terms are fair, move when they are not,
run a sequencer when it pays. Sequencers have to mind the same market with their
settings, the profit cut and the fees first of all.

> Proxima cannot tell holders what to do with their tokens. It only gives incentives for
> the cooperative behavior that leads to the most value for everybody. That also means
> that if a significant amount of capital does not respond to the incentives, the free
> riders, the security of the ledger may be compromised.

With the current setup, the ledger halts when more than 5/12
of the supply stops taking part in the consensus. During the centralized phase the founder
holds well over half of it on the five bootstrap sequencers, so stopping three of them
halts the network, four towards the end of the phase. That is what the centralized phase
means; how much sits on those sequencers or is delegated to them changes nothing. What the
measures have to show is whether the mined capital, the sequencers it sits on and the
people behind them are becoming a network of their own.

## What a reset means

The network goes back to genesis. Tokens on it cease to exist. The ledger rules may change
with the reset, mining included: there is no guarantee that mining stays the same in the
next take.

## When the rules are assessed

The founder's option ends with mining: once mined capital passes 5/12 of the supply the
founder can no longer advance the ledger alone, and past 7/12 cannot even stall it. So the
trends and the numbers below will be looked at several times while mined capital is still
below 5/12, and the reading published each time. After that the founder's options are
gone, and everybody knows it.

All numbers are read from the ledger. Anyone can compute them. The terms used below are
defined in the glossary at the end.

## The rules

The lines below are not formal thresholds. They say what the founder looks at and where
the line roughly is; the trend matters as much as the level, and a number moving the
wrong way is a bad sign even above its line.

The network will likely be reset if any of the following happens:

1. **Idle mined capital share above 10%.** Almost all newly mined tokens are expected to
   join the cooperative consensus and secure the ledger. This is the one rule every holder
   can act on alone: delegate, or run a sequencer.
2. **Fewer than 15 active community sequencers.** A sequencer carrying more than ten
   times its own capital in delegations does not count.
3. **One sequencer carries 1/8 or more of the supply**, own and delegated together. 1/6
   is the share that lets one party keep two forks alive at once; 1/8 leaves a margin.
4. **Own share of the community sequencers below 1/10.** At least a tenth of the newly
   mined capital is expected to go into sequencing itself, not only into delegations.
5. **Bootstrap share above 1/3.** Capital delegated to the bootstrap sequencers stops when
   they stop; it is not part of the network that has to outlive them. Sequencing has to
   move to the community before the founder's option expires, not after.
6. **A critical bug that needs breaking changes**, or the system cannot run stably at 30
   TPS with 20 sequencers, the five bootstrap ones included. A reset for this reason is
   not a verdict on the community.

Rule 6 is the technical side, 1 to 5 the structural side. The community side is next.

One more number is published with the rules, with no line attached: _fault tolerance_,
how many sequencers must stop to halt the network. The bootstrap sequencers alone keep
it at 3 or 4 for the whole phase, so it says little now; it is there so that everybody
sees where it starts from and can watch it once the founder's option is gone.

## Commitment from the community

One more condition, and it cannot be read from the ledger: serious intentions on the
community's side. The founder will likely reset a take with no sign of people teaming up to
support the project and carry on the research and development of the protocol. The
founder has no intention of supporting the project alone after decentralization; it would
make no practical sense either.

The ledger sees accounts and assets, not people. Whether the capital that runs the network
belongs to a handful of anonymous holders or to participants who stand behind it is the
part of the decision no number can replace. It stays subjective, and it is honest to say
so.

## What is expected

What the community can do so that a take is worth not resetting:

1. Put everything you mine to work: delegate, or run a sequencer. Keep pocket change only.
2. If you hold a lot, run a sequencer and keep it up.
3. If you run a sequencer, put your own capital into it. A sequencer running on
   delegations alone has nothing at stake.
4. Keep your sequencer close to the network's centre of mass, as `/netviz` shows it. A
   well-connected sequencer takes a fuller part in the cooperative consensus and earns
   steadier inflation.
5. Price your sequencer for the market: a profit cut and fees that delegators and users
   accept and that keep it running. Adjust when the market moves.
6. Spread delegations. Watch the sequencer ratings, or make your own. Do not pile onto the
   bootstrap sequencers; prefer sequencers whose operators have their own capital in them,
   and move when the terms stop being fair. `proxi node consolidate` does this for you.
7. If you run a sequencer or public infrastructure, announce it and say who you are. A
   stable pseudonym is enough.
8. Run an access node others can sync from.
9. Take part in upgrades.
10. Learn the protocol well enough to explain it to the next person.
11. Research, develop, innovate, discuss.

None of this is rewarded by the founder, and none of it is required. It is what makes the
difference between a rehearsal and a network.

## Glossary

_Active sequencer_: a sequencer that keeps producing and whose transactions keep getting
into the committed ledger state.

_Own capital_ of a sequencer: the balance of its sequencer chain, put there by the
operator. It is what the operator has at stake.

_Delegated capital_ of a sequencer: the total frozen in delegations to it. It belongs to
the delegators.

_Capital at work_: own plus delegated capital over the active sequencers. _Idle capital_
is the rest of the supply. Approximate: capital delegated to an offline sequencer, for
example, is counted as at work.

_Idle mined capital share_: idle capital as a percentage of all mined tokens. Total mined
capital is estimated from the mining pace.

_Bootstrap sequencers_: the founder's five, at work from genesis. _Community sequencers_:
all the others. Their own capital is mined, and so is everything delegated to any
sequencer.

_Own share_ of the community sequencers: their own capital as a percentage of all they
carry, own and delegated. How much of the sequencing is done by people with their own
capital at stake, and how much by operators carrying other people's tokens.

_Bootstrap share_: the part of the mined capital at work that is delegated to the
bootstrap sequencers. When they stop, it stops with them.

_Fault tolerance_: how many sequencers must stop to halt the network, i.e. the size of the
smallest set carrying together more than 5/12 of the supply, over all sequencers. It
counts chains, not who controls them, so one operator with several sequencers looks
better than it is.
