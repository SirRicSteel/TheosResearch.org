#!/bin/bash
# THEOS Document Renaming Script
# Purpose: Rename all documents with descriptive, professional filenames
# Date: 2025-12-17

cd /home/ubuntu/THEOS/docs/latest

# Documents already well-named (01-08, 55-56): Keep as-is

# Rename documents 09-54, 57 with descriptive titles based on content

# 09-20: Extended Architecture Layer
git mv 09_Interpretability.md 09_Interpretability_Audit_Replay.md
git mv 10_Governor_Authority.md 10_Governor_Authority_Control_Hierarchy.md
git mv 11_Engine_Disagreement.md 11_Engine_Disagreement_Anti_Collapse.md
git mv 12_Wisdom_Compression.md 12_Wisdom_Compression_Temporal_Memory.md
git mv 13_Governor_Selection.md 13_Governor_Selection_Cycle_Arbitration.md
git mv 14_Temporal_Consequence.md 14_Temporal_Consequence_Memory_Compression.md
git mv 15_Cycle_Execution.md 15_Cycle_Execution_Stop_Conditions.md
git mv 16_Auditability.md 16_Auditability_Trace_Preservation.md
git mv 17_Adversarial_Delay.md 17_Adversarial_Delay_Deception_Control.md
git mv 18_Outcome_Selection.md 18_Outcome_Selection_Post_Decision_Stabilization.md
git mv 19_Wisdom_Calibration.md 19_Wisdom_Calibration_Future_Cycle_Influence.md
git mv 20_Delay_Strategy.md 20_Delay_Strategy_Wisdom_Guided_Containment.md

# 21-30: Consistency & Integration Layer
git mv 21_Longitudinal_Memory.md 21_Formal_Consistency_Cross_Section_Coherence.md
git mv 23_document.md 23_Contradiction_Compression_Signal_Noise_Wisdom.md
git mv 24_document.md 24_Governor_Arbitration_Cycle_Termination.md
git mv 25_document.md 25_Wisdom_Accumulation_Memory_Encoding.md
git mv 26_document.md 26_Failure_Modes_Drift_Prevention_Anti_Dogmatism.md
git mv 27_document.md 27_Formal_Metrics_Auditability_Review_Readiness.md
git mv 28_document.md 28_Human_AI_Interface_Review_Alignment.md
git mv 29_document.md 29_Wisdom_Accumulation_Consequence_Encoding.md
git mv 30_document.md 30_End_to_End_Execution_Lifecycle.md

# 31-40: Formal Specifications Layer
git mv 31_document.md 31_Formal_Governor_Decision_Schema.md
git mv 32_document.md 32_Wisdom_Temporal_Consequence_Encoding.md
git mv 33_document.md 33_Contradiction_Detection_Measurement_Compression.md
git mv 34_document.md 34_Governor_Cycle_Count_Disengagement_Stop.md
git mv 35_document.md 35_Wisdom_Memory_Compression_Consequence.md
git mv 36_document.md 36_Adversarial_Engagement_Delay_Intelligence_Capture.md
git mv 38_document.md 38_Integrated_Consistency_System_Wide_Reconciliation.md
git mv 39_document.md 39_Canonical_Readiness_External_Presentation_Boundary.md
git mv 40_document.md 40_Final_Canonical_Index_Dependency_Map.md

# 42-54: Meta & Deployment Layer
git mv 42_document.md 42_Canonical_Readiness_Submission_Adoption_Protocol.md
git mv 43_document.md 43_Long_Horizon_Evolution_Future_Research_Boundary.md
git mv 44_document.md 44_Ethical_Non_Collapse_Guarantees.md
git mv 45_document.md 45_Human_AI_Co_Governance_Framework.md
git mv 46_document.md 46_Scientific_Medical_Acceleration_Boundaries.md
git mv 47_document.md 47_Adversarial_Deception_Boundaries_Strategic_Delay.md
git mv 48_document.md 48_Governor_Cycle_Control_Engine_Engagement.md
git mv 49_document.md 49_Invariant_Coherence_Cross_Section_Consistency.md
git mv 50_document.md 50_Canonical_Completion_Self_Audit_Anti_Omission.md
git mv 51_document.md 51_Institutional_Drift_Resistance_Anti_Dilution.md
git mv 52_document.md 52_Dual_Engine_Execution_Trace_Cycle_by_Cycle.md
git mv 53_document.md 53_Formal_Dual_Engine_State_Machine.md
git mv 54_document.md 54_Compute_Energy_Model_E_equals_AI_squared.md

# 57: Final Layer
git mv 57_document.md 57_Formal_Provenance_Auditability_PANRI.md

echo "All documents renamed with descriptive titles"
