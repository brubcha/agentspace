Marketing Kit Template (Swift-style) v1

This folder contains two files:
1) marketing_kit_template_spec_v1.json
   - The fixed structure, allowed components, style tokens, and validation rules.
2) swift_marketing_kit_example_content.json
   - A sample content payload that follows the spec (partial, shortened for example).

How to use in an app
- Keep the template spec stable.
- For each new client, create a new content JSON using the same section ids and block types.
- Your renderer reads the spec first (styles, component rules, required order), then renders the content.

Recommended rendering pipeline
- JSON -> HTML (or DOCX) -> PDF
- Use the spec tokens to generate CSS (or DOCX styles) so every kit is identical in layout and hierarchy.

Parsing and validation tips
- Validate required sections and ordering before rendering.
- Reject content that includes an em dash character.
- Enforce table schema consistency (columns and row widths).
- Ensure KeyFindingsList indices are sequential.

Notes
- Page margins are set to 0.6 in, matching the narrow-margin preference.


Updates in v1.1 (prompt-extracted rules)
- Adds a strict authoring contract for Markdown output:
  - Output begins with three Markdown tables in this exact order:
    1) 📦 Kit Overview
    2) 🧭 Kit Structure
    3) Section-to-Engagement Index Mapping
  - No prose before these tables.
  - Do not rename titles or change columns.
  - [FILL] is allowed only inside these opening tables.
- Adds input governance rules:
  - Use only inputs provided (no new research).
  - Prefer most recent dated notes if conflicts exist.
  - Copy proof metrics and quotes exactly as provided.
- Adds additional required sections for downstream reuse:
  - Accessibility & Inclusivity Notes
  - Consistency Checklist

v1.4 changes

NEW IN v1.5
- Added section_block_templates in the template spec. These are canonical, ordered block skeletons (copy, lists, tables) for each required H2 section.
- Your generator can use these templates to produce consistent structure every time, swapping placeholder tokens (e.g., {{Brand}}) with client-specific inputs.
- Missing-input policy: use [FILL] only in the first two tables if needed, and do not add any "" or gaps section.
