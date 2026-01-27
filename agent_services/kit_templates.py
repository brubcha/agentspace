def kit_to_markdown(kit: dict) -> str:
    """
    Converts a marketing kit JSON (as produced by build_marketing_kit) to markdown.
    - Sections as ## headers
    - Blocks as appropriate markdown (paragraphs, lists, tables, etc.)
    """
    md = []
    # Load gold standard section order and titles
    import os, json
    gold_path = os.path.join(os.path.dirname(__file__), '../gold_standard_marketing_kit.json')
    with open(gold_path, encoding='utf-8') as f:
        gold = json.load(f)
    gold_sections = gold['document']['sections']
    kit_sections = {s['id']: s for s in kit.get('document', {}).get('sections', [])}
    for gold_section in gold_sections:
        sec_id = gold_section['id']
        title = gold_section.get('title', '')
        md.append(f"## {title}")
        section = kit_sections.get(sec_id)
        section_blocks = section.get('blocks', []) if section and section.get('blocks') else []
        # Always output a blank line after the header if no blocks or section is missing
        # For all sections, only render actual content from kit output
        if not section_blocks:
            md.append("")
            continue
        for block in section_blocks:
            btype = block.get('type')
            if btype == 'Paragraph':
                text = block.get('text', '').strip()
                if text:
                    md.append(text)
            elif btype == 'Subhead':
                text = block.get('text', '').strip()
                if text:
                    md.append(f"### {text}")
            elif btype == 'Bullets':
                items = block.get('items', [])
                for item in items:
                    md.append(f"- {item.strip()}")
            elif btype == 'Checklist':
                title = block.get('title', '').strip()
                if title:
                    md.append(f"### {title}")
                for item in block.get('items', []):
                    md.append(f"- [ ] {item.strip()}")
            elif btype == 'ListOfSections':
                for st in block.get('section_titles', []):
                    md.append(f"- {st.strip()}")
            elif btype == 'Table':
                columns = block.get('columns', [])
                rows = block.get('rows', [])
                if columns:
                    md.append(' | '.join(columns))
                    md.append(' | '.join(['---'] * len(columns)))
                    for row in rows:
                        md.append(' | '.join(row))
            elif btype == 'Image':
                src = block.get('src', '')
                alt = block.get('alt', '')
                md.append(f"![{alt}]({src})")
            elif btype == 'Archetype':
                title = block.get('title', '').strip()
                desc = block.get('description', '').strip()
                if title:
                    md.append(f"### {title}")
                if desc:
                    md.append(desc)
                attrs = block.get('attributes', {})
                for k, v in attrs.items():
                    md.append(f"- **{k.replace('_', ' ').title()}**: {v}")
            elif btype == 'Persona':
                title = block.get('title', '').strip()
                desc = block.get('description', '').strip()
                attrs = block.get('attributes', {})
                if title:
                    md.append(f"### {title}")
                if desc:
                    md.append(desc)
                for k, v in attrs.items():
                    md.append(f"- **{k.replace('_', ' ').title()}**: {v}")
            elif btype == 'OpportunityCard':
                title = block.get('title', '').strip()
                desc = block.get('description', '').strip()
                if title:
                    md.append(f"### {title}")
                if desc:
                    md.append(desc)
            elif btype == 'NumberedList':
                items = block.get('items', [])
                for idx, item in enumerate(items, 1):
                    md.append(f"{idx}. {item.strip()}")
            elif btype == 'Callout':
                text = block.get('text', '').strip()
                if text:
                    md.append(f"> {text}")
            else:
                # Unknown block type: show type and text if available
                text = block.get('text', '').strip()
                md.append(f"**[{btype}]** {text}")
        md.append("")  # Blank line between sections
    return '\n'.join(md).strip()

import os
RUBRIC_PATH = os.path.join(os.path.dirname(__file__), '../Design Code Package/output-doc/marketing_kit_rubric.md')

def load_rubric_markdown():
    with open(RUBRIC_PATH, 'r', encoding='utf-8') as f:
        return f.read()

import os
import json
EXAMPLE_MD_PATH = os.path.join(os.path.dirname(__file__), '../Design Code Package/output-doc/example_output_copy.md')

def load_example_markdown():
    with open(EXAMPLE_MD_PATH, 'r', encoding='utf-8') as f:
        return f.read()


# Use the gold standard as the primary example kit
EXAMPLE_PATH = os.path.join(os.path.dirname(__file__), '../gold_standard_marketing_kit.json')
SPEC_PATH = os.path.join(os.path.dirname(__file__), '../marketing_kit_template_spec_v1_5.json')

def load_example_kit():
    with open(EXAMPLE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_template_spec():
    with open(SPEC_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)
