import os
import json

# Load the example and spec files (paths can be adjusted as needed)
EXAMPLE_PATH = os.path.join(os.path.dirname(__file__), '../swift_marketing_kit_example_content_v1_5.json')
SPEC_PATH = os.path.join(os.path.dirname(__file__), '../marketing_kit_template_spec_v1_5.json')

def load_example_kit():
    with open(EXAMPLE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_template_spec():
    with open(SPEC_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)
