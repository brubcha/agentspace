import pytest
from agent_services import subagents

# Mock OpenAI call for deterministic tests
def mock_call_openai_subagent(prompt, max_tokens=512, temperature=0.7, model="gpt-3.5-turbo"):
    # Always return a JSON array (list of blocks) for all subagent types
    import json
    if 'subhead' in prompt.lower():
        return json.dumps([
            {"type": "Subhead", "text": "Test Subhead"},
            {"type": "Paragraph", "text": "Test Paragraph"}
        ])
    if 'table' in prompt.lower():
        return json.dumps([
            {"type": "Table", "title": "Test Table", "columns": ["A", "B"], "rows": [["1", "2"]]}
        ])
    if 'checklist' in prompt.lower():
        return json.dumps([
            {"type": "Checklist", "title": "Test Checklist", "items": ["Check 1"]}
        ])
    if 'bullets' in prompt.lower() or 'list' in prompt.lower():
        return json.dumps([
            {"type": "Bullets", "title": "Test List", "items": ["Item 1", "Item 2"]}
        ])
    if 'persona' in prompt.lower():
        return json.dumps([
            {"type": "Persona", "title": "Test Persona", "description": "Desc", "attributes": {"age": 30}}
        ])
    if 'archetype' in prompt.lower():
        return json.dumps([
            {"type": "Archetype", "title": "Test Archetype", "description": "Desc", "attributes": {}}
        ])
    if 'opportunity card' in prompt.lower():
        return json.dumps([
            {"type": "OpportunityCard", "title": "Test Card", "description": "Desc", "actions": ["Act"]}
        ])
    if 'checklist' in prompt.lower():
        return json.dumps([
            {"type": "Checklist", "title": "Test Checklist", "items": ["Check 1"]}
        ])
    if 'qa validator' in prompt.lower() or 'review the following section blocks' in prompt.lower():
        # Try to infer the type from the prompt (simulate correct review type)
        import re
        match = re.search(r'\{"type": ?"([A-Za-z]+)"', prompt)
        block_type = match.group(1) if match else "Paragraph"
        return json.dumps([
            {"type": block_type, "text": "Test", "review": "OK"}
        ])
    return json.dumps([
        {"type": "Unknown", "text": "No match"}
    ])

@pytest.fixture(autouse=True)
def patch_openai(monkeypatch):
    monkeypatch.setattr(subagents, "call_openai_subagent", mock_call_openai_subagent)

def test_generate_subhead_block():
    blocks = subagents.generate_subhead_block("Section", "Subhead", "Client", "Brand", "URL")
    assert isinstance(blocks, list)
    assert blocks[0]["type"] == "Subhead"

def test_generate_table_block():
    blocks = subagents.generate_table_block("Section", "Table", "Client", "Brand", "URL", ["A", "B"])
    assert isinstance(blocks, list)
    assert blocks[0]["type"] == "Table"

def test_generate_list_block():
    blocks = subagents.generate_list_block("Section", "List", "Client", "Brand", "URL")
    assert isinstance(blocks, list)
    assert blocks[0]["type"] == "Bullets"

def test_generate_persona_block():
    blocks = subagents.generate_persona_block("Section", "Persona", "Client", "Brand", "URL")
    assert isinstance(blocks, list)
    assert blocks[0]["type"] == "Persona"


def test_generate_opportunity_card_block():
    blocks = subagents.generate_opportunity_card_block("Section", "Card", "Client", "Brand", "URL")
    assert isinstance(blocks, list)
    assert blocks[0]["type"] == "OpportunityCard"

def test_generate_checklist_block():
    blocks = subagents.generate_checklist_block("Section", "Checklist", "Client", "Brand", "URL")
    assert isinstance(blocks, list)
    assert blocks[0]["type"] == "Checklist"

def test_validate_section_blocks():
    blocks = subagents.validate_section_blocks("Section", [{"type": "Paragraph", "text": "Test"}], "Client", "Brand", "URL")
    assert isinstance(blocks, list)
    assert "review" in blocks[0]

