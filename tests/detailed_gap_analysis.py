import json
import re
import sys

# Usage: python detailed_gap_analysis.py <markdown_file> <gold_standard_json> <rubric_md>
def load_markdown_sections(md_path):
    with open(md_path, encoding='utf-8') as f:
        lines = f.readlines()
    sections = {}
    current = None
    for line in lines:
        header = re.match(r"^#+\s*([A-Za-z0-9 /&\-]+)", line)
        if header:
            current = header.group(1).strip().upper()
            sections[current] = []
        elif current:
            sections[current].append(line.strip())
    return sections

def load_gold_standard(json_path):
    with open(json_path, encoding='utf-8') as f:
        gold = json.load(f)
    sections = {}
    for sec in gold['document']['sections']:
        sections[sec['title'].upper()] = sec['blocks']
    return sections

def load_rubric(md_path):
    with open(md_path, encoding='utf-8') as f:
        lines = f.readlines()
    rubric = {}
    current = None
    for line in lines:
        header = re.match(r"^###?\s*([0-9A-Za-z /&\-]+)", line)
        if header:
            current = header.group(1).strip().upper()
            rubric[current] = []
        elif current:
            rubric[current].append(line.strip())
    return rubric

def analyze_section(section, gold_blocks, rubric_lines, md_lines):
    print(f"\n=== Section: {section} ===")
    if not md_lines:
        print("FAIL: Section missing in markdown output.")
        return
    print("PASS: Section present in markdown output.")
    # Check block types and counts
    gold_types = [b['type'] for b in gold_blocks]
    print(f"Gold standard block types: {gold_types}")
    # Attempt to infer block types from markdown lines
    md_types = []
    for l in md_lines:
        if l.strip().startswith('|') and not l.strip().startswith('---'):
            md_types.append('Table')
        elif l.strip().startswith('- [ ]'):
            md_types.append('Checklist')
        elif l.strip().startswith('-') or l.strip().startswith('*'):
            md_types.append('Bullets')
        elif l.strip().startswith('###'):
            md_types.append('Subhead')
        elif l.strip() and not l.strip().startswith('#'):
            md_types.append('Paragraph')
    print(f"Markdown inferred block types: {md_types}")
    # Compare block type order
    if len(md_types) < len(gold_types):
        print(f"FAIL: Fewer blocks in markdown ({len(md_types)}) than gold standard ({len(gold_types)})")
    elif len(md_types) > len(gold_types):
        print(f"WARN: More blocks in markdown ({len(md_types)}) than gold standard ({len(gold_types)})")
    # Compare type order (simple, not robust to extra lines)
    for i, (g, m) in enumerate(zip(gold_types, md_types)):
        if g != m:
            print(f"FAIL: Block type mismatch at position {i+1}: expected {g}, got {m}")
    # Print rubric requirements
    if rubric_lines:
        print("Rubric requirements:")
        for r in rubric_lines:
            if r:
                print(f"  - {r}")
    # Print sample content
    print("Sample markdown content:")
    for l in md_lines[:10]:
        print(f"  {l}")
    # Check for placeholders and suspicious content
    placeholders = [l for l in md_lines if any(p in l for p in ['[BRAND]', '[CLIENT]', '[FILL]', '[PLACEHOLDER]', '[TODO]'])]
    if placeholders:
        print(f"FAIL: Placeholders found: {placeholders}")
    else:
        print("PASS: No placeholders found.")

    # Check for empty lines/blocks
    empty_lines = [i+1 for i, l in enumerate(md_lines) if l.strip() == '']
    if len(empty_lines) > 3:
        print(f"WARN: Multiple empty lines detected at: {empty_lines}")

    # Check for suspicious formatting (e.g., malformed tables)
    malformed_tables = [l for l in md_lines if l.count('|') == 1 and l.strip().startswith('|')]
    if malformed_tables:
        print(f"WARN: Possible malformed tables: {malformed_tables}")

    # Check for awkward phrasing (simple heuristic: repeated words, 'lorem', etc.)
    awkward_lines = [l for l in md_lines if re.search(r'\b(\w+) \1\b', l, re.IGNORECASE) or 'lorem' in l.lower()]
    if awkward_lines:
        print(f"WARN: Possible awkward phrasing: {awkward_lines}")

def main():
    if len(sys.argv) < 4:
        print("Usage: python detailed_gap_analysis.py <markdown_file> <gold_standard_json> <rubric_md>")
        sys.exit(1)
    md_path, gold_json, rubric_md = sys.argv[1:4]
    md_sections = load_markdown_sections(md_path)
    gold_sections = load_gold_standard(gold_json)
    rubric = load_rubric(rubric_md)
    for section in gold_sections:
        analyze_section(section, gold_sections[section], rubric.get(section, []), md_sections.get(section, []))

if __name__ == "__main__":
    main()
