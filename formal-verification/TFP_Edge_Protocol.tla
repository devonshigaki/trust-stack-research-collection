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
    auditChain,     \* Sequence of globally verified block header hashes
    compromised,    \* Set of compromised tenant keys (subset of Tenants)
    timeStep        \* Monotonic global step counter

vars == << edgeVaults, auditChain, compromised, timeStep >>

(***************************************************************************)
(* Initial State: Every tenant holds a sovereign edge database (libSQL)    *)
(* with baseline trust state S0, empty audit chain, no initial compromise. *)
(***************************************************************************)
Init ==
    /\ edgeVaults = [t \in Tenants |-> [trustState |-> 1, version |-> 0, valid |-> TRUE]]
    /\ auditChain = << >>
    /\ compromised = {}
    /\ timeStep = 0

(***************************************************************************)
(* LocalTransaction: Tenant t executes a valid local private contract.    *)
(* Under TFP architecture, the update is written exclusively to t's vault   *)
(* and an attestation hash is prepared for the audit chain.                *)
(***************************************************************************)
LocalTransaction(t) ==
    /\ t \notin compromised
    /\ timeStep < MaxSteps
    /\ edgeVaults' = [edgeVaults EXCEPT ![t].trustState = edgeVaults[t].trustState + 1,
                                        ![t].version = edgeVaults[t].version + 1]
    /\ auditChain' = Append(auditChain, [tenant |-> t, ver |-> edgeVaults'[t].version])
    /\ UNCHANGED << compromised >>
    /\ timeStep' = timeStep + 1

(***************************************************************************)
(* AdversaryBreach: Adversary gains unauthorized physical/key access to t. *)
(* Crucially, the adversary only corrupts t's local storage.               *)
(***************************************************************************)
AdversaryBreach(t) ==
    /\ Cardinality(compromised) < AdversaryPower
    /\ t \notin compromised
    /\ timeStep < MaxSteps
    /\ compromised' = compromised \cup {t}
    /\ edgeVaults' = [edgeVaults EXCEPT ![t].valid = FALSE]
    /\ UNCHANGED << auditChain >>
    /\ timeStep' = timeStep + 1

(***************************************************************************)
(* Next State Transition Relation                                          *)
(***************************************************************************)
Next ==
    \/ \E t \in Tenants : LocalTransaction(t)
    \/ \E t \in Tenants : AdversaryBreach(t)
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

\* Invariant 3: Audit Chain Immutability
\* The audit chain history is monotonic and append-only.
AuditChainMonotonic ==
    Len(auditChain') >= Len(auditChain)

\* Invariant 4: Blast Radius Bound
\* The number of corrupted tenant stores is strictly bounded by AdversaryPower.
BoundedBlastRadius ==
    Cardinality(compromised) <= AdversaryPower

=============================================================================
