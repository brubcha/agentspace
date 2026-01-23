import requests
import json
import pytest

def test_end_to_end_kit_generation():
    # Load a sample payload (can be replaced with more comprehensive test cases)
    with open('agent_services/test_payload.json', 'r') as f:
        payload = json.load(f)
    # Assume the backend is running locally on port 5000
    url = 'http://localhost:5000/agent/marketing-kit'
    response = requests.post(url, json=payload, timeout=30)
    assert response.status_code == 200
    kit = response.json()
    # Basic structure checks
    assert 'document' in kit
    assert 'sections' in kit['document']
    assert isinstance(kit['document']['sections'], list)
    # Check that at least one section is present and has blocks
    assert len(kit['document']['sections']) > 0
    for section in kit['document']['sections']:
        assert 'blocks' in section
        assert isinstance(section['blocks'], list)
        # Optionally, check for at least one block per section
        assert len(section['blocks']) > 0
        # Optionally, check for expected block types
        for block in section['blocks']:
            assert 'type' in block
