import pytest
import requests
import json

def test_marketing_kit_all_sections():
    # This test assumes the backend is running locally on port 7000
    payload = {
        "client_name": "TestClient",
        "website": "https://swiftinnovation.io/",
        "offering": "Test offering",
        "target_markets": "Test market",
        "competitors": "Competitor1, Competitor2",
        "additional_details": "Test additional details",
        "files": []
    }
    url = 'http://localhost:7000/agent/marketing-kit'
    response = requests.post(url, json=payload, timeout=60)
    assert response.status_code == 200, f"API returned {response.status_code}: {response.text}"
    kit = response.json()
    assert 'document' in kit and 'sections' in kit['document']
    sections = kit['document']['sections']
    # List of required section titles/ids (update as needed to match your gold standard)
    required_sections = [
        "executive_summary_overview_purpose",
        "brand_framework_goal",
        "audience_archetypes",
        "key_messaging",
        "product_service_overview",
        "feature_benefit_table",
        "competitive_differentiation",
        "go_to_market_checklist",
        "sample_campaign_concepts",
        "website_content_audit_summary",
        "attachments_references",
        "key_findings",
        "market_landscape",
        "channel_opportunities",
        "audience_personas",
        "b2b_industry_targets",
        "industry_codes_data_broker_research",
        "brand_archetypes",
        "brand_voice",
        "client_dos_donts",
        "content_keyword_strategy",
        "social_strategy",
        "social_production_checklist",
        "campaign_structure",
        "landing_page_strategy",
        "engagement_framework"
    ]
    found_ids = [s.get('id') for s in sections]
    # Load gold standard for block type validation
    with open('y:/Code/agentspace/gold_standard_marketing_kit.json', encoding='utf-8') as f:
        gold = json.load(f)
    gold_sections = {s['id']: s for s in gold['document']['sections']}
    for sec in required_sections:
        assert sec in found_ids, f"Missing section: {sec}"
        section = next(s for s in sections if s.get('id') == sec)
        assert section.get('blocks'), f"Section '{sec}' is empty"
        # Check block types and order match gold standard
        gold_blocks = gold_sections[sec]['blocks']
        actual_types = [b.get('type') for b in section['blocks'] if b]
        gold_types = [b.get('type') for b in gold_blocks if b]
        assert actual_types[:len(gold_types)] == gold_types, (
            f"Section '{sec}' block types/order mismatch.\nExpected: {gold_types}\nActual:   {actual_types}")
