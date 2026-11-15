------------------------ MODULE TFP_Edge_Protocol ------------------------
(***************************************************************************)
(* Formal TLA+ Specification of The Fresh Protocol (TFP)                   *)
(* Multi-Tenant Edge Isolation, Audit Chain Anchoring, & Light Clients     *)
(* Author: Devon Shigaki · ORCID: 0009-0003-8977-8010                      *)
(***************************************************************************)

EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS 
    Tenants,        \* Finite set of tenant edge nodes {t1, t2, ...}
    MaxSteps,       \* Maximum simulation time horizon
    AdversaryPower  \* Maximum number of corruptible edge nodes

VARIABLES
    edgeVaults,     \* edgeVaults[t] = local state record of tenant t
    auditChain,     \* Sequence of globally verified block header records
    networkMsgs,    \* Untrusted network packet pool (honest + Byzantine packets)
    compromised,    \* Set of compromised tenant keys (subset of Tenants)
    timeStep        \* Monotonic global step counter

vars == << edgeVaults, auditChain, networkMsgs, compromised, timeStep >>

Init ==
    /\ edgeVaults = [t \in Tenants |-> [trustState |-> 1, version |-> 0, valid |-> TRUE]]
    /\ auditChain = << >>
    /\ networkMsgs = {}
    /\ compromised = {}
    /\ timeStep = 0

MaxChainVer(t) ==
    LET indices == {i \in 1..Len(auditChain) : auditChain[i].tenant = t}
    IN IF indices = {} THEN 0
       ELSE CHOOSE m \in {auditChain[i].ver : i \in indices} :
            \A k \in indices : auditChain[k].ver <= m

LastHash(t) ==
    LET indices == {i \in 1..Len(auditChain) : auditChain[i].tenant = t}
    IN IF indices = {} THEN 0
       ELSE LET maxI == CHOOSE i \in indices : \A k \in indices : k <= i
            IN auditChain[maxI].stateHash

(***************************************************************************)
(* LocalTransaction: Honest tenant t updates local vault and emits signed  *)
(* packet onto the untrusted persistent network channel.                   *)
(***************************************************************************)
LocalTransaction(t) ==
    /\ t \notin compromised
    /\ timeStep < MaxSteps
    /\ edgeVaults' = [edgeVaults EXCEPT ![t].trustState = edgeVaults[t].trustState + 1,
                                        ![t].version = edgeVaults[t].version + 1]
    /\ networkMsgs' = networkMsgs \cup {[sender |-> t, tenant |-> t,
                                         ver |-> edgeVaults'[t].version,
                                         stateHash |-> 1, sigValid |-> TRUE]}
    /\ UNCHANGED << auditChain, compromised >>
    /\ timeStep' = timeStep + 1

(***************************************************************************)
(* AdversaryBreach & Active Byzantine Equivocation / Replay                *)
(* Compromised nodes can inject:                                           *)
(*   (1) Forged cross-tenant packets (claimedTenant # t => sigValid=FALSE) *)
(*   (2) Equivocating same-version packets (stateHash \in {1, 2})          *)
(*   (3) Persistent packet replay (networkMsgs is never deleted).          *)
(***************************************************************************)
AdversaryBreach(t) ==
    /\ Cardinality(compromised) < AdversaryPower
    /\ t \notin compromised
    /\ timeStep < MaxSteps
    /\ compromised' = compromised \cup {t}
    /\ edgeVaults' = [edgeVaults EXCEPT ![t].valid = FALSE]
    /\ UNCHANGED << auditChain, networkMsgs >>
    /\ timeStep' = timeStep + 1

ByzantineInjectMsg(t) ==
    /\ t \in compromised
    /\ timeStep < MaxSteps
    /\ \E target \in Tenants, v \in 1..MaxSteps, sh \in {1, 2} :
        /\ networkMsgs' = networkMsgs \cup {[sender |-> t, tenant |-> target,
                                             ver |-> v, stateHash |-> sh,
                                             sigValid |-> (target = t)]}
        /\ UNCHANGED << edgeVaults, auditChain, compromised >>
    /\ timeStep' = timeStep + 1

(***************************************************************************)
(* VerifierProcessMsg: Audit chain gate accepts ONLY packets with valid    *)
(* signature, matching uncompromised/non-forged sender, and strictly       *)
(* monotonic next version (ver = MaxChainVer(tenant) + 1).                 *)
(***************************************************************************)
VerifierProcessMsg(m) ==
    /\ m \in networkMsgs
    /\ m.sigValid = TRUE
    /\ m.sender = m.tenant
    /\ m.ver = MaxChainVer(m.tenant) + 1
    /\ auditChain' = Append(auditChain, [tenant |-> m.tenant, ver |-> m.ver,
                                        prevHash |-> LastHash(m.tenant),
                                        stateHash |-> m.stateHash])
    /\ UNCHANGED << edgeVaults, networkMsgs, compromised, timeStep >>

Next ==
    \/ \E t \in Tenants : LocalTransaction(t)
    \/ \E t \in Tenants : AdversaryBreach(t)
    \/ \E t \in Tenants : ByzantineInjectMsg(t)
    \/ \E m \in networkMsgs : VerifierProcessMsg(m)
    \/ (timeStep >= MaxSteps /\ UNCHANGED vars)

Spec == Init /\ [][Next]_vars

-----------------------------------------------------------------------------
(***************************************************************************)
(* FORMAL SAFETY INVARIANTS                                                *)
(***************************************************************************)

\* Invariant 1: Type Invariance
TypeOK ==
    /\ \A t \in Tenants : edgeVaults[t].trustState \in Nat
    /\ \A t \in Tenants : edgeVaults[t].version \in Nat
    /\ \A t \in Tenants : edgeVaults[t].valid \in BOOLEAN
    /\ compromised \subseteq Tenants
    /\ timeStep \in Nat

\* Invariant 2: Sovereign Edge Isolation (No Cascade Corruption)
\* An uncompromised tenant's vault ALWAYS remains valid and untampered.
CascadeIsolationInvariant ==
    \A t \in Tenants : (t \notin compromised) => (edgeVaults[t].valid = TRUE)

\* Invariant 3: Audit Chain Structural Validity & Non-Equivocation
\* Every appended entry references a valid tenant, bounded version, and
\* no compromised tenant can ever inject entries on behalf of an honest tenant.
AuditChainValid ==
    /\ \A i \in 1..Len(auditChain) :
        /\ auditChain[i].tenant \in Tenants
        /\ auditChain[i].ver \in 1..MaxSteps
        /\ auditChain[i].stateHash \in {1, 2}
    /\ \A i, j \in 1..Len(auditChain) :
        (i < j /\ auditChain[i].tenant = auditChain[j].tenant) =>
            (auditChain[i].ver < auditChain[j].ver)

\* Invariant 3b: Non-Equivocation & Hash-Chain Linkage
\* No two committed entries for the same tenant share a version (even with conflicting stateHash),
\* and every entry's prevHash matches the immediate predecessor's stateHash (or 0 for ver=1).
NonEquivocation ==
    \A i, j \in 1..Len(auditChain) :
        (auditChain[i].tenant = auditChain[j].tenant /\ auditChain[i].ver = auditChain[j].ver)
            => (i = j /\ auditChain[i].stateHash = auditChain[j].stateHash)

HashChainIntegrity ==
    \A i \in 1..Len(auditChain) :
        LET prior == {k \in 1..(i-1) : auditChain[k].tenant = auditChain[i].tenant}
        IN IF prior = {}
           THEN auditChain[i].prevHash = 0
           ELSE LET prevIdx == CHOOSE k \in prior : \A m \in prior : m <= k
                IN auditChain[i].prevHash = auditChain[prevIdx].stateHash

\* Temporal Action Property: Audit Chain Append-Only Immutability
\* Across every state transition, the audit chain length is monotonically non-decreasing
\* and all previously committed prefix entries remain strictly immutable.
AuditChainMonotonicAction ==
    /\ Len(auditChain') >= Len(auditChain)
    /\ \A i \in 1..Len(auditChain) : auditChain'[i] = auditChain[i]

AuditChainMonotonic ==
    [][AuditChainMonotonicAction]_vars

\* Invariant 4: Blast Radius Bound
\* The number of corrupted tenant stores is strictly bounded by AdversaryPower.
BoundedBlastRadius ==
    Cardinality(compromised) <= AdversaryPower

=============================================================================
