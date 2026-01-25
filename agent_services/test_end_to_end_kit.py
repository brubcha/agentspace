import requests
import json
import pytest

def test_end_to_end_kit_generation():
    # Load a sample payload (can be replaced with more comprehensive test cases)
    with open('tests/test_payload.json', 'r') as f:
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
        'executive_summary_overview_purpose': ['Paragraph', 'Subhead', 'ListOfSections'],
        'brand_framework_goal': ['Table', 'Paragraph'],
        'audience_archetypes': ['Table'],
        'key_messaging': ['Paragraph', 'Table'],
        'product_service_overview': ['Paragraph'],
        'feature_benefit_table': ['Table'],
        'competitive_differentiation': ['Paragraph'],
        'go_to_market_checklist': ['Bullets'],
        'sample_campaign_concepts': ['Paragraph'],
        'website_content_audit_summary': ['Paragraph'],
        'attachments_references': ['Bullets', 'Paragraph'],
        'key_findings': ['Bullets', 'Table'],
        'market_landscape': ['Bullets', 'Image'],
        'channel_opportunities': ['Table'],
        'audience_personas': ['Table'],
        'b2b_industry_targets': ['Table', 'Image'],
        'industry_codes_data_broker_research': ['Table', 'Paragraph'],
        'brand_archetypes': ['Table'],
        'brand_voice': ['Paragraph', 'Table'],
        'client_dos_donts': ['Table', 'Bullets'],
        'content_keyword_strategy': ['Table', 'Bullets', 'Paragraph'],
        'social_strategy': ['Bullets'],
        'social_production_checklist': ['Bullets'],
        'campaign_structure': ['Table', 'Bullets'],
        'landing_page_strategy': ['Table', 'Image'],
        'engagement_framework': ['Bullets', 'Table']
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
