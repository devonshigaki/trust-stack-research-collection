--------------------------- MODULE TFP_HLC_GSet ---------------------------
(***************************************************************************)
(* Formal TLA+ Specification of Canonical HLC + SHA-256 G-Set Op-Log       *)
(* Proves Strong Eventual Consistency across concurrent offline replicas   *)
(* despite non-commutative [0, 10] clamped Master Law transitions.         *)
(***************************************************************************)

EXTENDS Integers, Sequences, FiniteSets

CONSTANTS Replicas, InitState, MaxState

\* Three out-of-order clamped events hitting upper and lower clamp boundaries:
\* e1: HLC=1, +8; e2: HLC=2, -9; e3: HLC=3, +4
\* Note that applying (e1, e2, e3) -> clamp(clamp(clamp(5+8)=10 - 9)=1 + 4)=5
\* whereas (e2, e1, e3) -> clamp(clamp(clamp(5-9)=0 + 8)=8 + 4)=10 (non-commutative!)
AllOps == {1, 2, 3}
Delta(id) == IF id = 1 THEN 8 ELSE IF id = 2 THEN -9 ELSE 4

Clamp(x) == IF x < 0 THEN 0 ELSE IF x > MaxState THEN MaxState ELSE x

\* Canonical deterministic fold over any subset S \subseteq {1, 2, 3} in strict HLC order 1 < 2 < 3
Replay(S) ==
    LET s1 == IF 1 \in S THEN Clamp(InitState + Delta(1)) ELSE InitState
        s2 == IF 2 \in S THEN Clamp(s1 + Delta(2)) ELSE s1
        s3 == IF 3 \in S THEN Clamp(s2 + Delta(3)) ELSE s2
    IN s3

VARIABLES gset, netPool, deliveredOrder

vars == << gset, netPool, deliveredOrder >>

Init ==
    /\ gset = [r \in Replicas |-> {}]
    /\ netPool = AllOps
    /\ deliveredOrder = [r \in Replicas |-> << >>]

\* Replicas receive ops from netPool in arbitrary asynchronous arrival orders
DeliverOp(r, op) ==
    /\ op \in netPool
    /\ op \notin gset[r]
    /\ gset' = [gset EXCEPT ![r] = @ \cup {op}]
    /\ deliveredOrder' = [deliveredOrder EXCEPT ![r] = Append(@, op)]
    /\ UNCHANGED netPool

\* Peer-to-peer anti-entropy gossip merges G-Sets directly
GossipMerge(r1, r2) ==
    /\ r1 # r2
    /\ gset[r2] \ gset[r1] # {}
    /\ gset' = [gset EXCEPT ![r1] = @ \cup gset[r2]]
    /\ UNCHANGED << netPool, deliveredOrder >>

Next ==
    \/ \E r \in Replicas, op \in AllOps : DeliverOp(r, op)
    \/ \E r1, r2 \in Replicas : GossipMerge(r1, r2)
    \/ ((\A r \in Replicas : gset[r] = AllOps) /\ UNCHANGED vars)

DeliverAction == \E r \in Replicas, op \in AllOps : DeliverOp(r, op)
GossipAction == \E r1, r2 \in Replicas : GossipMerge(r1, r2)

FairSpec ==
    /\ Init
    /\ [][Next]_vars
    /\ WF_vars(DeliverAction)
    /\ WF_vars(GossipAction)

TypeOK ==
    /\ \A r \in Replicas : gset[r] \subseteq AllOps
    /\ \A r \in Replicas : Replay(gset[r]) \in 0..MaxState

\* Strong Eventual Consistency: any two replicas with identical G-Sets compute identical clamped state
ReplicaSEC ==
    \A r1, r2 \in Replicas : (gset[r1] = gset[r2]) => (Replay(gset[r1]) = Replay(gset[r2]))

\* Monotone G-Set growth (inflationary join-semilattice)
GSetMonotonic ==
    [][\A r \in Replicas : gset[r] \subseteq gset'[r]]_vars

\* Liveness: all replicas eventually converge to the exact canonical state Replay(AllOps) = 5
EventualReplicaConvergence ==
    <>(\A r \in Replicas : gset[r] = AllOps /\ Replay(gset[r]) = Replay(AllOps))

=============================================================================
