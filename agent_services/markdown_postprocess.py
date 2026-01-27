"""
markdown_postprocess.py

Utility for cleaning and standardizing markdown output for marketing kits.
- Normalizes heading levels (## for sections, ### for blocks)
- Removes duplicate/misplaced headers
- Cleans up markdown artifacts (extra symbols, whitespace)
- Ensures proper markdown for tables/lists
"""
import re

def clean_markdown(md: str) -> str:
    # Normalize line endings
    md = md.replace('\r\n', '\n').replace('\r', '\n')
    lines = md.split('\n')
    cleaned = []
    last_section = None
    seen_sections = set()
    for line in lines:
        # Normalize section headers to '##'
        m = re.match(r'^(#+)\s*(.+)', line)
        if m:
            level, title = m.group(1), m.group(2).strip()
            # Remove duplicate section headers
            if level == '#' or level == '##':
                if title.lower() in seen_sections:
                    continue
                seen_sections.add(title.lower())
                line = f'## {title}'
                last_section = title.lower()
            elif level == '###':
                line = f'### {title}'
        # Remove stray markdown symbols
        line = re.sub(r'^[\-•]+\s*', '- ', line)
        # Remove excessive whitespace
        line = line.strip()
        if line:
            cleaned.append(line)
    # Remove consecutive duplicate headers
    out = []
    prev = ''
    for l in cleaned:
        if l == prev and l.startswith('## '):
            continue
        out.append(l)
        prev = l
    return '\n'.join(out)
