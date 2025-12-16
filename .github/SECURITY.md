# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in THEOS, please report it responsibly.

### What to Report
- Vulnerabilities in the reference implementation
- Flaws in the formal specification that could lead to safety failures
- Attack vectors not covered by the threat model
- Exploitable edge cases in the Governor state machine

### How to Report
**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead:
1. Email frederick.stalnecker@theosresearch.org with subject line: **[SECURITY]**
2. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if you have one)

### What to Expect
- **Acknowledgment within 48 hours**
- **Initial assessment within 1 week**
- **Fix timeline** depends on severity (critical: days, high: weeks, medium: months)
- **Public disclosure** coordinated with you (if desired)

---

## Supported Versions

| Version | Supported |
|---------|-----------|
| v1.4.x  | ✅ Yes    |
| v1.3.x  | ✅ Yes    |
| v1.2.x  | ✅ Yes    |
| < v1.2  | ❌ No     |

---

## Security Considerations

### THEOS Is Not a Security System
THEOS is a **governance layer**, not a security boundary. It:
- ✅ Constrains reasoning depth and energy
- ✅ Enforces capability gating
- ✅ Provides audit trails
- ❌ Does NOT prevent model jailbreaks
- ❌ Does NOT prevent prompt injection
- ❌ Does NOT replace authentication/authorization

### Known Limitations
- **Adversarial prompts** may still elicit harmful outputs (THEOS limits *depth*, not *content*)
- **Model vulnerabilities** are not addressed by THEOS (use Constitutional AI, RLHF, etc.)
- **Side-channel attacks** on the Governor state are possible (mitigated by audit logging)

### Threat Model
See [`/governance/THEOS_Threat_Model_Overview.md`](../governance/THEOS_Threat_Model_Overview.md) for the complete threat model.

---

## Responsible Disclosure

We follow coordinated vulnerability disclosure:
1. **Report received** → Acknowledge within 48 hours
2. **Vulnerability confirmed** → Assess severity and impact
3. **Fix developed** → Test and validate
4. **Fix deployed** → Update reference implementation
5. **Public disclosure** → After fix is available (typically 90 days)

**Credit:** We will credit you in the security advisory (unless you prefer anonymity).

---

## Security Best Practices

### For Implementers
- **Use the latest version** of the reference implementation
- **Validate all inputs** to the Governor
- **Log all state transitions** for audit
- **Monitor for anomalies** in wisdom accumulation
- **Test with adversarial inputs** before deployment

### For Deployers
- **Use the correct deployment mode** (Sandbox, Restricted, Operational, High-Assurance)
- **Enforce safety envelopes** (do not modify hyperparameter bounds)
- **Enable audit logging** and review regularly
- **Have an incident response plan** for posture escalations

---

## Contact

**Security Contact:** frederick.stalnecker@theosresearch.org  
**PGP Key:** (Available upon request)

---

**For general questions, see [`/outreach/`](../outreach/).**
