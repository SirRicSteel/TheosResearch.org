# THEOS Diagrams & Visual Documentation

This folder contains visual representations of THEOS architecture, flows, and threat models.

---

## Purpose

Diagrams serve multiple audiences:
- **Engineers** need flow diagrams to understand implementation
- **Executives** need architecture diagrams to understand value
- **Researchers** need state machine diagrams to understand formal properties
- **Regulators** need threat surface maps to understand safety

---

## Diagram Formats

All diagrams are provided in multiple formats:
- **Markdown** (Mermaid syntax) — Viewable on GitHub
- **PNG** — For presentations and documents
- **SVG** — For high-resolution printing

---

## Diagrams in This Folder

### THEOS Governor Flow (Coming Soon)
```
User Query → Governor → Model → Tools → Governor → Response
              ↓                              ↓
         Allocate Depth              Update Wisdom
         Check Posture               Log Audit Trail
```

Shows the complete request/response cycle with governance checkpoints.

### Wisdom Accumulation Flow (Coming Soon)
```
Event → Risk Assessment → Wisdom Buffer → Offline Validation → Audit Ledger
                                ↓
                         Delayed Update (W_u)
                         Temporal Decay (λ)
```

Shows how consequence-based wisdom is accumulated without observable adaptation.

### Threat Surface Map (Coming Soon)
```
[Adversarial Probing] → [Depth Throttling] → Contained
[Gradient Extraction] → [Non-Observable Learning] → Blocked
[Capability Outpacing] → [Posture Escalation] → Degraded
[Silent Drift] → [Wisdom Accumulation] → Detected
```

Shows how THEOS addresses known AI safety threats.

### Posture State Machine (Coming Soon)
```
NOM → PEM → CM → ISO
 ↓     ↓    ↓    ↓
[D=10][D=8][D=6][D=2]
[V=2] [V=1][V=0][V=0]
[T=Y] [T=Y][T=N][T=N]
```

Shows posture transitions and their effects on depth (D), verbosity (V), and tool access (T).

### Deployment Modes (Coming Soon)
```
Sandbox → Restricted → Operational → High-Assurance
  ↓          ↓            ↓              ↓
[Loose]  [Moderate]   [Standard]    [Strict]
```

Shows the four deployment modes and their safety profiles.

---

## How to Use These Diagrams

### In Presentations
1. Use PNG or SVG exports
2. Include the diagram title and source attribution
3. Link to this repository for full context

### In Documentation
1. Embed Markdown (Mermaid) directly in GitHub
2. Reference the diagram file path
3. Provide a brief caption

### In Academic Papers
1. Use SVG for high-resolution figures
2. Cite the THEOS repository
3. Include the diagram in supplementary materials

---

## Creating New Diagrams

To contribute a new diagram:
1. Create the diagram in Mermaid syntax (Markdown)
2. Export to PNG and SVG
3. Add to this folder with descriptive filename
4. Update this README with diagram description

**Mermaid Documentation:** https://mermaid.js.org/

---

## Status

**Governor Flow:** Planned  
**Wisdom Accumulation Flow:** Planned  
**Threat Surface Map:** Planned  
**Posture State Machine:** Planned  
**Deployment Modes:** Planned  

**Contributions welcome!**

---

**For governance materials, see [`/governance/`](../governance/).**  
**For technical specifications, see [`/governor/`](../governor/).**
