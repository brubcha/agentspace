import json
import sys

# Usage: python list_missing_sections.py <kit_output.json> <gold_standard.json>
def main():
    if len(sys.argv) < 3:
        print("Usage: python list_missing_sections.py <kit_output.json> <gold_standard.json>")
        sys.exit(1)
    kit_path, gold_path = sys.argv[1:3]
    with open(kit_path, encoding='utf-8') as f:
        kit = json.load(f)
    with open(gold_path, encoding='utf-8') as f:
        gold = json.load(f)
    kit_sections = {s['id'] for s in kit['document']['sections']}
    gold_sections = {s['id'] for s in gold['document']['sections']}
    missing = gold_sections - kit_sections
    if missing:
        print(f"Missing sections in kit output: {sorted(missing)}")
    else:
        print("All required sections are present in kit output.")

if __name__ == "__main__":
    main()
