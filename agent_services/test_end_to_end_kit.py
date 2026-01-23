import requests
import json
import pytest

def test_end_to_end_kit_generation():
    # Load a sample payload (can be replaced with more comprehensive test cases)
    with open('agent_services/test_payload.json', 'r') as f:
        payload = json.load(f)
    # Assume the backend is running locally on port 7000
    url = 'http://localhost:7000/agent/marketing-kit'
    response = requests.post(url, json=payload, timeout=120)
    assert response.status_code == 200
    kit = response.json()
    # Basic structure checks
    assert 'document' in kit
    assert 'sections' in kit['document']
    assert isinstance(kit['document']['sections'], list)
    # Check that at least one section is present and has blocks
    assert len(kit['document']['sections']) > 0
    # Map of expected block types per section (based on subagent usage)
    expected_block_types = {
        'overview': ['Paragraph', 'Subhead'],
        'market_landscape': ['Table', 'Bullets'],
        'key_opportunities': ['Bullets', 'Paragraph', 'Checklist'],
        'launch_checklist': ['Checklist'],
        'opportunity_cards': ['OpportunityCard'],
        'brand_archetype': ['Archetype'],
        'audience_personas': ['Persona', 'Bullets'],
        'b2b_industry_targets': ['Table', 'Bullets'],
        'key_findings': ['NumberedFindingsList'],
        'opportunity_areas': ['Subhead', 'Checklist'],
        # Add other sections as needed
    }
    # Check each section for expected block types and fallback/QA logic
    for section in kit['document']['sections']:
        assert 'blocks' in section
        assert isinstance(section['blocks'], list)
        assert len(section['blocks']) > 0
        sec_id = section.get('id')
        block_types = [block.get('type') for block in section['blocks'] if 'type' in block]
        # If section is in expected_block_types, check for at least one expected type
        if sec_id in expected_block_types:
            found = any(bt in block_types for bt in expected_block_types[sec_id])
            assert found, f"Section '{sec_id}' missing expected block types: {expected_block_types[sec_id]}"
        # Check fallback/retry and QA validation logic
        for block in section['blocks']:
            # Fallback/retry: look for 'review' field indicating retry/fallback or QA
            if 'review' in block:
                assert isinstance(block['review'], str)
                assert block['review'].strip() != '', f"Block review field is empty: {block['review']}"
