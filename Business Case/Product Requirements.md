# Product Requirements

## Users and Roles
- **Requestor (internal):** submits a request, provides context, reviews agent output.
- **Human Reviewer/Editor:** humanizes output, approves, packages for client delivery.
- **Admin/Governance Owner:** controls agent behaviors, templates, permissions, data boundaries.
- **AI Agent Owner / Agent Cluster:** executes production steps, generates deliverables, produces a handoff packet.

## MVP Deliverable Scope (Design + Marketing)
### Design Examples
- Social post concepts and copy blocks with design directions
- Brand kit components (logo usage rules draft, typography recommendations, color palette options)
- Creative brief drafts
- Ad creative variations and specs
- Simple landing page wireframe description + content blocks

### Marketing Examples
- Email sequences, newsletter drafts
- Paid ad copy sets (Google, Meta) with variants
- Blog outlines and full drafts with metadata suggestions
- Campaign briefs and calendars
- Marketing Kits
- Value prop and positioning drafts

## Core Functional Requirements
1. **Structured request intake**
   - Deliverable-type selection (MVP: Design, Marketing catalog)
   - Required fields per type (goal, audience, offer, brand constraints, references, due date)
   - File and link attachments
   - Optional conversational intake that still writes into structured fields
2. **Agent orchestration (agent-owned routing)**
   - Each request is assigned to an Agent Owner or agent cluster
   - Agents execute a defined production workflow: gather context → draft → validate against rules → generate variants → package → handoff
   - Workflow status is still visible to humans, but ownership remains agent-side
3. **“How it produces” controls (governance)**
   - Per-deliverable production recipes (step-by-step agent workflows)
   - Template library (prompt frameworks, required sections, tone constraints)
   - Company-specific rules (brand voice, compliance notes, forbidden claims, formatting standards)
   - Approval gates (for certain deliverables or clients)
4. **Secure context and IP controls (foundational)**
   - Multi-tenant isolation by company
   - Client-level and end-client-level context boundaries (no cross-client leakage)
   - Role-based access control and audit logs
   - Clear policy controls for: whether customer data is used for training, whether outputs are retained and for how long, what can be exported, shared, or copied
5. **Humanization and QA**
   - Review queue, inline comments, revision tracking
   - Checklist-based QA per deliverable type
   - “Client-ready” approval state required before export/share
6. **Packaging and delivery**
   - Deliverable packet includes: final content/design directions, assumptions and inputs used, recommended next steps, optional variants and rationale
   - Export formats (MVP): Google Doc, PDF, copy blocks, simple presentation output later

## Non-Functional Requirements
- Strong authentication, permissioning, and audit trails
- Data encryption in transit and at rest
- Separation of environments and tenant data
- Monitoring for misuse and prompt injection attempts
- Reliability and predictable output formatting
