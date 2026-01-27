# agent_services Documentation

## Overview

This directory contains Python microservices for the Marketing Agent system. The primary service is `marketing_agent.py`, which generates a gold standard-compliant marketing kit using OpenAI and post-processing logic.

## Key Features (2026 Update)

- **Gold Standard Compliance:**
  - All sections and block types are generated to match `gold_standard_marketing_kit.json`.
  - Section and block order, structure, and formatting are enforced.
- **Markdown Post-Processing:**
  - Output is cleaned and standardized using `markdown_postprocess.py`.
  - Headings, lists, tables, and placeholders are normalized for QA and professional delivery.
- **Placeholder Replacement:**
  - All `[BRAND]` and `[CLIENT]` placeholders are replaced throughout all fields, including bullets, tables, and lists.
- **Automated QA:**
  - Use `tests/detailed_gap_analysis.py` to compare generated markdown to the gold standard and rubric.

## Usage

- Run the marketing agent via the Flask API (`/agent/marketing-kit`) or as a module.
- After generation, the kit is saved as both JSON and cleaned markdown for further processing or QA.
- To validate output, run:

```
python tests/detailed_gap_analysis.py tests/UCARI_MarketingKit_test.md gold_standard_marketing_kit.json tests/marketing_kit_rubric.md
```

## Main Files

- `marketing_agent.py`: Main agent logic
- `markdown_postprocess.py`: Markdown cleanup utility
- `kit_templates.py`: JSON-to-markdown conversion
- `subagents.py`: Validation, QA, and block helpers

## Best Practices

- Always update the gold standard and agent logic together.
- Use the gap analysis script after any changes to ensure compliance.
- Review the README in the project root for full-stack setup instructions.
