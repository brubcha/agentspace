

import json
import os
import sys
import argparse

# Ensure agent_services is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from agent_services.kit_templates import kit_to_markdown

def main():
    parser = argparse.ArgumentParser(description="Convert kit_output.json to markdown.")
    parser.add_argument('--input', type=str, default=os.path.join(current_dir, 'kit_output.json'), help='Input kit JSON file path')
    parser.add_argument('--output', type=str, default=os.path.join(current_dir, 'kit_output_converted.md'), help='Output markdown file path')
    args = parser.parse_args()

    with open(args.input, encoding='utf-8') as f:
        kit = json.load(f)

    md = kit_to_markdown(kit)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(md)

    print(f'Conversion complete: {args.output}')

if __name__ == "__main__":
    main()
