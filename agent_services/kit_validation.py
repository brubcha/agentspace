import json
from kit_templates import load_template_spec

def validate_kit_against_spec(kit: dict, spec: dict) -> list:
    """
    Validates the generated marketing kit against the template spec.
    Returns a list of error messages. If empty, the kit is valid.
    """
    errors = []
    # Check top-level required fields
    required_fields = ["template_id", "client", "assets", "document", "output_format", "template_version"]
    for field in required_fields:
        if field not in kit:
            errors.append(f"Missing required top-level field: {field}")
    # Check client fields
    client_fields = ["brand_name", "brand_url"]
    if "client" in kit:
        for field in client_fields:
            if field not in kit["client"]:
                errors.append(f"Missing client field: {field}")
    # Check document structure
    if "document" in kit:
        if "cover" not in kit["document"]:
            errors.append("Missing document.cover section")
        if "sections" not in kit["document"] or not isinstance(kit["document"]["sections"], list):
            errors.append("Missing or invalid document.sections (should be a list)")
    # Add more checks as needed based on spec
    # (e.g., required section order, front_matter, meta, etc.)
    return errors

# Example usage in marketing_agent.py:
# kit = ... # generated kit
# spec = load_template_spec()
# errors = validate_kit_against_spec(kit, spec)
# if errors:
#     return jsonify({'error': 'Validation failed', 'details': errors}), 400
# else:
#     return jsonify(kit)
