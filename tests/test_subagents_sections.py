import pytest
from agent_services import subagents

def test_generate_subhead_block():
    blocks = subagents.generate_subhead_block("Overview", "How to Use It", "TestClient", "TestBrand", "https://test.com")
    assert isinstance(blocks, list)
    assert any(b.get("type") == "Subhead" for b in blocks)

def test_generate_table_block():
    blocks = subagents.generate_table_block("Brand Framework", "Attributes Table", "TestClient", "TestBrand", "https://test.com", ["Attribute", "Description", "Example"])
    assert isinstance(blocks, list)
    assert any(b.get("type") == "Table" for b in blocks)

def test_generate_list_block():
    blocks = subagents.generate_list_block("Key Findings", "Findings List", "TestClient", "TestBrand", "https://test.com")
    assert isinstance(blocks, list)
    assert any(b.get("type") == "Bullets" or b.get("type") == "List" for b in blocks)

def test_generate_checklist_block():
    block = subagents.generate_checklist_block("Go-to-Market Checklist", "Checklist", "TestClient", "TestBrand", "https://test.com")
    assert isinstance(block, dict) or isinstance(block, list)

def test_generate_opportunity_card_block():
    blocks = subagents.generate_opportunity_card_block("Opportunity Areas", "Opportunity Card", "TestClient", "TestBrand", "https://test.com")
    assert isinstance(blocks, list)
    assert any(b.get("type") == "OpportunityCard" for b in blocks)

def test_generate_archetype_block():
    blocks = subagents.generate_archetype_block("Brand Archetypes", "Primary Archetype", "TestClient", "TestBrand", "https://test.com")
    assert isinstance(blocks, list)
    assert any(b.get("type") == "Archetype" for b in blocks)

def test_generate_persona_block():
    blocks = subagents.generate_persona_block("Audience & User Personas", "Persona 1", "TestClient", "TestBrand", "https://test.com")
    assert isinstance(blocks, list)
    assert any(b.get("type") == "Persona" for b in blocks)

def test_validate_section_blocks():
    blocks = [{"type": "Paragraph", "text": "Test content."}]
    validated = subagents.validate_section_blocks("Overview", blocks, "TestClient", "TestBrand", "https://test.com")
    assert isinstance(validated, list)

def test_fallback_retry_block_success():
    def always_success(*args, **kwargs):
        return [{"type": "Paragraph", "text": "Success"}]
    result = subagents.fallback_retry_block(always_success)
    assert isinstance(result, list)
    assert result[0]["type"] == "Paragraph"

def test_fallback_retry_block_failure():
    def always_fail(*args, **kwargs):
        return [{"error": "fail"}]
    result = subagents.fallback_retry_block(always_fail)
    assert isinstance(result, list)
    assert result[0]["review"].startswith("[Fallback/Retry]")
