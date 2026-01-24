import json
import os
import re

RUBRIC_PATH = os.path.join(os.path.dirname(__file__), 'marketing_kit_rubric.md')

# Load rubric section headers and criteria
SECTION_HEADER_RE = re.compile(r'^### \d+\. (.+)$', re.MULTILINE)
CRITERION_RE = re.compile(r'^- (.+)$', re.MULTILINE)

def load_rubric():
    with open(RUBRIC_PATH, encoding='utf-8') as f:
        rubric = f.read()
    sections = SECTION_HEADER_RE.findall(rubric)
    # Find criteria for each section
    section_criteria = {}
    for section in sections:
        pattern = rf'### \d+\. {re.escape(section)}\n((?:- .+\n)+)'
        match = re.search(pattern, rubric)
        if match:
            criteria = [c.strip('- ').strip() for c in match.group(1).splitlines() if c.strip().startswith('-')]
            section_criteria[section] = criteria
    return sections, section_criteria

def load_kit(path):
    with open(path, encoding='utf-8') as f:
        kit = json.load(f)
    return kit

def check_kit_against_rubric(kit, sections, section_criteria):
    found_sections = {s['title'].strip().lower(): s for s in kit['document']['sections']}
    results = []
    for section in sections:
        sec_key = section.strip().lower()
        present = any(sec_key in k for k in found_sections)
        criteria = section_criteria.get(section, [])
        sec_result = {'section': section, 'present': present, 'criteria': []}
        if present:
            blocks = found_sections[sec_key]['blocks']
            text = '\n'.join(str(b) for b in blocks)
            for crit in criteria:
                # Simple check: does the block text mention a keyword from the criterion?
                crit_keywords = [w for w in re.split(r'\W+', crit) if len(w) > 3]
                met = any(w.lower() in text.lower() for w in crit_keywords)
                sec_result['criteria'].append({'criterion': crit, 'met': met})
        else:
            for crit in criteria:
                sec_result['criteria'].append({'criterion': crit, 'met': False})
        results.append(sec_result)
    return results

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Check marketing kit JSON against rubric.')
    parser.add_argument('kit_json', help='Path to generated marketing kit JSON')
    args = parser.parse_args()
    sections, section_criteria = load_rubric()
    kit = load_kit(args.kit_json)
    results = check_kit_against_rubric(kit, sections, section_criteria)
    for sec in results:
        print(f"Section: {sec['section']} - Present: {sec['present']}")
        for crit in sec['criteria']:
            print(f"  - {crit['criterion']}: {'✔' if crit['met'] else '✘'}")
        print()
    # Optionally, fail if any must-have is missing
    missing = [sec for sec in results if not sec['present'] or not all(c['met'] for c in sec['criteria'])]
    if missing:
        print(f"\nFAIL: {len(missing)} sections/criteria not met.")
        exit(1)
    else:
        print("\nPASS: All rubric criteria met.")

if __name__ == '__main__':
    main()
