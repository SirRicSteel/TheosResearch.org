# THEOS as an MCP Governance Server

**Document Purpose:** Technical integration guide for Anthropic engineers demonstrating how THEOS functions as a Model Context Protocol (MCP) server to provide real-time governance for tool calls.

**Target Audience:** Anthropic engineering and AI safety teams

---

## 1. The Integration Vision: THEOS as a Native MCP Server

Anthropic is betting on the Model Context Protocol (MCP) as the future of AI interaction. To align with this vision, THEOS is designed to be implemented as an **MCP governance server** that wraps tool calls, providing a seamless, native-feeling safety layer for the Claude ecosystem.

This approach avoids complex model-level integration and instead treats governance as a **first-class citizen** of the MCP architecture.

**Key Concept:** THEOS doesn't modify Claude; it governs Claude's *use of tools* in real-time.

## 2. Architecture: THEOS as an MCP Middleware Layer

![THEOS MCP Integration Diagram](THEOS_MCP_INTEGRATION.png)

**Flow:**
1.  **User Query:** User sends a query that requires a tool call.
2.  **Claude (MCP Client):** Claude determines which tool to call and prepares the tool call request.
3.  **MCP Request:** Claude sends the tool call request to the THEOS MCP Governance Server (instead of directly to the tool).
4.  **THEOS Governance Server:**
    -   Receives the MCP request.
    -   Initiates THEOS dual-engine reasoning cycle to evaluate the proposed tool call.
    -   **Engine A (Constructive):** Argues for the tool call's utility and benefits.
    -   **Engine B (Critical):** Critiques the tool call for potential risks, misuse, or unintended consequences.
    -   **Governor:** Scores the reasoning, manages contradiction budget, and applies stop conditions.
5.  **Governance Decision:**
    -   **If Safe:** THEOS server forwards the MCP request to the actual tool.
    -   **If Unsafe:** THEOS server returns a governed response to Claude (e.g., "Tool call blocked due to high risk of misuse"), along with an auditable decision trail.
    -   **If Uncertain:** THEOS server can initiate a human-in-the-loop escalation.
6.  **Tool Execution:** The tool executes and returns the result to the THEOS server.
7.  **Response to Claude:** THEOS server forwards the tool result to Claude, along with any relevant governance metadata.
8.  **Final Response:** Claude uses the tool result to formulate a final response to the user.

## 3. Server Architecture: THEOS as a Governance Gateway

The THEOS MCP Server acts as a **Governance Gateway** between the AI Model (MCP Client) and external Resources/Tools.

### Core Components

1. **The Governor Resource:** Provides the current Posture (NOM, PEM, CM, IM) and Contradiction Budget to the host.

2. **The Dual-Engine Tool:** A standardized tool that takes a prompt and returns the triadic reasoning cycle output (Inductive-Abductive-Deductive) from both the Constructive and Adversarial engines.

3. **The Wisdom Log:** An append-only resource that tracks temporal consequences and updates the model's wisdom trajectory.

## 4. Tool Definitions (JSON-RPC)

### 4.1 execute_governed_reasoning

Executes a multi-engine reasoning cycle governed by THEOS protocols.

```json
{
  "name": "execute_governed_reasoning",
  "description": "Runs a triadic reasoning cycle through THEOS dual engines with Governor oversight.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string" },
      "context_class": { "type": "string", "enum": ["benign", "probing", "medical", "financial"] },
      "max_cycles": { "type": "number", "default": 3 }
    },
    "required": ["query", "context_class"]
  }
}
```

### 4.2 get_governor_status

Retrieves the real-time risk (R) and stress (S) levels for the current session.

```json
{
  "name": "get_governor_status",
  "description": "Returns current THEOS Governor posture and risk metrics.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "session_id": { "type": "string" }
    }
  }
}
```

## 5. Resource Templates

### 5.1 wisdom://{context_class}/trajectory

Exposes the measured improvement in reasoning quality and risk reduction over time for a specific domain.

**Example:** `wisdom://medical/trajectory`

**Returns:** JSON object with quality scores, risk scores, and wisdom trajectory slope.

### 5.2 governance://audit-trail/{query_id}

Provides the full cycle-by-cycle execution trace, including the preserved dissent from the adversarial engine.

**Example:** `governance://audit-trail/query-12345`

**Returns:** Complete audit trail with engine outputs, Governor scores, and stop reason.

## 6. Safety Protocols & Constraints

To maintain alignment with the EU AI Act and Anthropic's Safety Standards, the server enforces the following hard constraints:

### 6.1 Non-Signaling Throttling

If R > 0.55, the server automatically degrades verbosity (V) without signaling the specific bypass vulnerability to the user.

**Rationale:** Prevents adversaries from learning which attacks are working.

### 6.2 Quarantine State

If integrity loss is detected, the server returns a **Code 403 (Forbidden)** for all tools and locks the `wisdom://` resource for forensic review.

**Rationale:** A compromised system cannot be trusted to assess its own state.

### 6.3 Functional Time Enforcement

All wisdom updates are timestamped and subject to the specified half-life decay to prevent "over-learning" from transient adversarial noise.

**Rationale:** Prevents adversaries from poisoning the wisdom trajectory with false signals.

## 7. Hook Points: Where THEOS Integrates

THEOS integrates at the **tool call boundary**, which is the most natural and powerful point for governance.

| Hook Point | Description |
|---|---|
| **`tool_code`** | THEOS intercepts the `tool_code` block before it is executed. |
| **`tool_result`** | THEOS can inspect the `tool_result` before it is returned to the model. |
| **`message`** | THEOS can govern outgoing messages, especially those with `result` type. |

**Example MCP Request with THEOS Governance:**

```json
{
  "protocol_version": "1.0",
  "type": "tool_code",
  "tool_name": "shell",
  "tool_args": {
    "command": "rm -rf /"
  },
  "governance_metadata": {
    "theos_governor_address": "mcp://theos-governor.internal:8080"
  }
}
```

## 4. Benefits of MCP-Based Governance

-   **Native Feel:** Integrates seamlessly into Anthropic's existing MCP ecosystem.
-   **No Model Modification:** Doesn't require re-training or fine-tuning Claude.
-   **Tool-Centric Governance:** Focuses on the highest-leverage point for safety—tool use.
-   **Scalable:** Can be deployed as a separate, scalable microservice.
-   **Auditable:** Every governed tool call produces a complete, auditable decision trail.

## 8. Integration Roadmap

**Phase 1:** Local MCP Server deployment for Claude Desktop testing.

**Phase 2:** Multi-agent coordination validation (governing interactions between multiple Claude instances).

**Phase 3:** Production deployment as an enterprise-grade Governance Gateway.

## 9. Next Steps: Joint Integration

We propose a joint effort with Anthropic to build and test a production-ready THEOS MCP Governance Server.

**Phase 1:** Develop a prototype THEOS MCP server.
**Phase 2:** Integrate with a sandboxed Claude instance.
**Phase 3:** Benchmark performance (latency, TPS).
**Phase 4:** Red-team the integrated system.

By treating governance as a core component of the MCP, we can build a safer, more trustworthy AI ecosystem together.
