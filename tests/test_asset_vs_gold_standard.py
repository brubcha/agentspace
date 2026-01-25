import json
import re
from pathlib import Path

GOLD_STANDARD_PATH = Path('y:/Code/agentspace/gold_standard_marketing_kit.json')
RUBRIC_PATH = Path('y:/Code/agentspace/tests/marketing_kit_rubric.md')
USER_MD_PATH = Path('y:/Code/agentspace/tests/UCARI_MarketingKit_test.md')

# Helper to load gold standard sections in order
def load_gold_standard_sections():
    with open(GOLD_STANDARD_PATH, encoding='utf-8') as f:
        data = json.load(f)
    return [s['title'] for s in data['document']['sections']]

def extract_sections_from_md(md_text):
    # Assumes sections are marked by ## or ###
    section_re = re.compile(r'^(##+\s+.+)$', re.MULTILINE)
    return [m.strip('# ').strip() for m in section_re.findall(md_text)]

def compare_section_order(user_sections, gold_sections):
    missing = [s for s in gold_sections if s not in user_sections]
    extra = [s for s in user_sections if s not in gold_sections]
    order_match = user_sections == gold_sections
    return missing, extra, order_match


def extract_tables_from_md(md_text):
    # Returns a list of (section, table_header, table_rows)
    tables = []
    section = None
    lines = md_text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith('##'):
            section = line.strip('# ').strip()
        if line.strip().startswith('|') and '---' in lines[i+1]:
            header = lines[i].strip()
            rows = []
            for j in range(i+2, len(lines)):
                if not lines[j].strip().startswith('|'):
                    break
                rows.append(lines[j].strip())
            tables.append((section, header, rows))
    return tables

def extract_bullets_from_md(md_text):
    # Returns a dict of section -> list of bullets
    bullets = {}
    section = None
    for line in md_text.splitlines():
        if line.startswith('##'):
            section = line.strip('# ').strip()
        if line.strip().startswith('•') or line.strip().startswith('- '):
            bullets.setdefault(section, []).append(line.strip())
    return bullets

def extract_paragraphs_from_md(md_text):
    # Returns a dict of section -> list of paragraphs
    paras = {}
    section = None
    for line in md_text.splitlines():
        if line.startswith('##'):
            section = line.strip('# ').strip()
        elif section and line.strip() and not line.strip().startswith(('•', '- ', '|', '#')):
            paras.setdefault(section, []).append(line.strip())
    return paras

def main():
    user_md = USER_MD_PATH.read_text(encoding='utf-8')
    gold_sections = load_gold_standard_sections()
    user_sections = extract_sections_from_md(user_md)
    missing, extra, order_match = compare_section_order(user_sections, gold_sections)
    print('--- Section Order Check ---')
    print('Order matches gold standard:', order_match)
    print('Missing sections:', missing)
    print('Extra/unexpected sections:', extra)

    # Table/Block/Rubric checks
    print('\n--- Section Content Checks ---')
    tables = extract_tables_from_md(user_md)
    bullets = extract_bullets_from_md(user_md)
    paras = extract_paragraphs_from_md(user_md)
    # Example: Check for required table columns in Feature/Benefit Table
    for section, header, rows in tables:
        if 'Feature/Benefit Table' in section:
            required_cols = ['Feature', 'Benefit', 'Proof Point']
            actual_cols = [c.strip() for c in header.split('|')[1:-1]]
            missing_cols = [c for c in required_cols if c not in actual_cols]
            if missing_cols:
                print(f"Section '{section}' missing columns: {missing_cols}")
    # Example: Check for bullets in Go-to-Market Checklist
    if 'Go-to-Market Checklist' in bullets:
        if len(bullets['Go-to-Market Checklist']) < 8:
            print("Go-to-Market Checklist has fewer than 8 items.")
    # Example: Check for paragraphs in Executive Summary
    if 'Executive Summary / Overview & Purpose' in paras:
        if len(paras['Executive Summary / Overview & Purpose']) < 2:
            print("Executive Summary section has fewer than 2 paragraphs.")
    # TODO: Add more rubric-driven checks for each section

if __name__ == '__main__':
    main()
