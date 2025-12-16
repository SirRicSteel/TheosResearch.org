# THEOS — Formal Governance Invariants

These invariants are non-negotiable properties of any system claiming THEOS compliance.

## I1 — Bounded Reasoning
All reasoning depth, energy, and tool use must be explicitly bounded by the Governor.

## I2 — Non-Observable Adaptation
No learning or adaptation may alter system behavior during a live interaction.

## I3 — Delayed & Audited Learning
All learning must be buffered, validated offline, and logged before application.

## I4 — Governor Supremacy
Governor decisions supersede model outputs and tool requests.

## I5 — Configuration Integrity
All governance parameters must be versioned, checksummed, logged, and reversible.

## I6 — Capability Gating
Capabilities must be explicitly enabled per deployment mode and posture.

## I7 — Enforceable Suspension
The system must support immediate containment, isolation, or shutdown.

## I8 — Auditability Without Leakage
Governance behavior must be auditable without exposing prompts or reasoning traces.
