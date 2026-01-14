# Low Level Design

## Primary Objects

- Organization (tenant)
- Client
- EndClient (optional, for IP scoping)
- User
- Agent (type, capabilities, version)
- AgentCluster (composition, routing rules)
- ProductionRecipe (steps, tools allowed, guardrails)
- Template (schema, required sections, formatting rules)
- ContextAsset (brand kit, rules, examples, attachments)
- Request (structured fields, priority, due date)
- Deliverable (schema-based output + versions)
- Review (comments, checklist results, approvals)
- Export (format, destination, permissions)
- AuditEvent (who/what accessed which context and when)

## Execution Flow

Request submitted → validate → assign to Agent Owner/Cluster → retrieve scoped context → run recipe steps → produce deliverable + packet → human review → revisions if needed → approve → export/share → archive.

## Security and Governance Mechanics

- Retrieval must be tenant-scoped and client-scoped by default
- End-client context requires explicit permission gates
- Every retrieval and export creates an audit event
- Admin controls define allowable tools, allowable data sources, and restricted outputs
