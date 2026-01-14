# High Level Design

## Core Modules
- **Request Intake:** Forms + chat intake → normalized structured request
- **Agent Control Plane:** Agent registry (Design Agent, Marketing Agent, etc.), routing rules to agent owners or clusters, production recipes and policy enforcement
- **Context Vault:** Company context (voice, offers, rules), client context (brand kit, history, campaigns), end-client IP context (restricted and scoped), retrieval layer with strict boundary enforcement
- **Deliverable Factory:** Template library + structured output schemas, draft generation, validation, versioning, variant generation and selection
- **Human Review and Packaging:** Editor, QA checklist, approvals, deliverable packet creation
- **Export and Sharing:** Controlled exports, access-limited links, watermarking options later
- **Analytics:** Volume, cycle time, revision rates, approval times, deliverable mix
