import pytest
import requests
import json

def test_marketing_kit_all_sections():
    # This test assumes the backend is running locally on port 7000
    payload = {
        "brand_name": "TestBrand",
        "brand_url": "https://testbrand.com",
        "offering": "Test offering",
        "target_markets": "Test market",
        "competitors": "Competitor1, Competitor2"
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
    for sec in required_sections:
        assert sec in found_ids, f"Missing section: {sec}"
        section = next(s for s in sections if s.get('id') == sec)
        assert section.get('blocks'), f"Section '{sec}' is empty"
        # Optionally, check for at least one non-empty block
        assert any(b for b in section['blocks'] if b), f"Section '{sec}' has no valid blocks"
