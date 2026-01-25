
import flask
from flask import Flask, request, jsonify
from agent_services import subagents

app = Flask(__name__)

# Minimal marketing kit builder function

def build_marketing_kit(data):
    website = data.get("website", "[FILL]")
    brand_url = data.get("brand_url", website)
    brand_name = data.get("brand_name", "[BRAND]")
    client_name = data.get("client_name", "[CLIENT]")
    required_sections = [
        ("executive_summary_overview_purpose", "Executive Summary / Overview & Purpose"),
        ("brand_framework_goal", "Brand Framework / The Goal"),
        ("audience_archetypes", "Audience Archetypes"),
        ("key_messaging", "Key Messaging"),
        ("product_service_overview", "Product/Service Overview"),
        ("feature_benefit_table", "Feature/Benefit Table"),
        ("competitive_differentiation", "Competitive Differentiation"),
        ("go_to_market_checklist", "Go-to-Market Checklist"),
        ("sample_campaign_concepts", "Sample Campaign Concepts"),
        ("website_content_audit_summary", "Website/Content Audit Summary"),
        ("attachments_references", "Attachments/References"),
        ("key_findings", "Key Findings / Opportunities & Challenges"),
        ("market_landscape", "Market Landscape"),
        ("channel_opportunities", "Channel Opportunities"),
        ("audience_personas", "Audience & User Personas"),
        ("b2b_industry_targets", "B2B Industry Targets"),
        ("industry_codes_data_broker_research", "Industry Codes & Data Broker Research"),
        ("brand_archetypes", "Brand Archetypes"),
        ("brand_voice", "Brand Voice"),
        ("client_dos_donts", "Client Do’s & Don’ts"),
        ("content_keyword_strategy", "Content & Keyword Strategy"),
        ("social_strategy", "Social Strategy"),
        ("social_production_checklist", "Social Production Checklist"),
        ("campaign_structure", "Campaign Structure"),
        ("landing_page_strategy", "Landing Page Strategy"),
        ("engagement_framework", "Engagement Framework")
    ]
    kit = {"document": {"sections": []}}
    for sec_id, sec_title in required_sections:
        blocks = []
        # Example: Use subagents for dynamic content generation
        if sec_id == "executive_summary_overview_purpose":
            blocks.extend(subagents.generate_subhead_block(sec_title, "Executive Summary", client_name, brand_name, brand_url))
        elif sec_id == "brand_framework_goal":
            blocks.extend(subagents.generate_table_block(sec_title, "Brand Framework Table", client_name, brand_name, brand_url, ["Attribute", "Description", "Example"]))
            blocks.extend(subagents.generate_subhead_block(sec_title, "Vision-level Goal", client_name, brand_name, brand_url))
            blocks.extend(subagents.generate_subhead_block(sec_title, "Measurable Objective", client_name, brand_name, brand_url))
        elif sec_id == "audience_archetypes":
            blocks.extend(subagents.generate_table_block(sec_title, "Audience Archetypes", client_name, brand_name, brand_url, ["Name/Title", "Mission", "Voice", "Values", "Emotional Promise", "Icon", "Voice in Action"]))
        elif sec_id == "key_messaging":
            blocks.extend(subagents.generate_subhead_block(sec_title, "Key Messaging Overview", client_name, brand_name, brand_url))
            blocks.extend(subagents.generate_table_block(sec_title, "Key Messaging Table", client_name, brand_name, brand_url, ["Channel", "Voice in Action"]))
        elif sec_id == "product_service_overview":
            blocks.extend(subagents.generate_subhead_block(sec_title, "Product/Service Overview", client_name, brand_name, brand_url))
        elif sec_id == "feature_benefit_table":
            blocks.extend(subagents.generate_table_block(sec_title, "Feature/Benefit Table", client_name, brand_name, brand_url, ["Feature", "Benefit"]))
        elif sec_id == "competitive_differentiation":
            blocks.extend(subagents.generate_subhead_block(sec_title, "Competitive Differentiation", client_name, brand_name, brand_url))
        elif sec_id == "go_to_market_checklist":
            blocks.extend(subagents.generate_checklist_block(sec_title, "Go-to-Market Checklist", client_name, brand_name, brand_url))
        elif sec_id == "sample_campaign_concepts":
            blocks.extend(subagents.generate_subhead_block(sec_title, "Sample Campaign Concepts", client_name, brand_name, brand_url))
        elif sec_id == "website_content_audit_summary":
            blocks.extend(subagents.generate_subhead_block(sec_title, "Website/Content Audit Summary", client_name, brand_name, brand_url))
        elif sec_id == "attachments_references":
            blocks.extend(subagents.generate_list_block(sec_title, "Attachments/References", client_name, brand_name, brand_url))
            blocks.extend(subagents.generate_subhead_block(sec_title, "Source Quality/Recency Check", client_name, brand_name, brand_url))
        elif sec_id == "key_findings":
            blocks.extend(subagents.generate_list_block(sec_title, "Key Findings / Opportunities & Challenges", client_name, brand_name, brand_url))
            blocks.extend(subagents.generate_table_block(sec_title, "Opportunities Table", client_name, brand_name, brand_url, ["Icon", "Opportunity Area", "Description"]))
        elif sec_id == "market_landscape":
            blocks.extend(subagents.generate_list_block(sec_title, "Market Landscape Bullets", client_name, brand_name, brand_url))
            # Image block could be added here if needed
        elif sec_id == "channel_opportunities":
            blocks.extend(subagents.generate_table_block(sec_title, "Channel Opportunities", client_name, brand_name, brand_url, ["Channel", "Opportunity Insight", "Recommendation", "Rationale for Deprioritizing"]))
        elif sec_id == "audience_personas":
            blocks.extend(subagents.generate_table_block(sec_title, "Audience & User Personas", client_name, brand_name, brand_url, ["Name/Title", "Motivation", "Needs", "Messaging", "Demographic", "Psychographic", "Buying Behavior"]))
        elif sec_id == "b2b_industry_targets":
            blocks.extend(subagents.generate_table_block(sec_title, "B2B Industry Targets", client_name, brand_name, brand_url, ["Category", "Subtype", "Rationale"]))
        elif sec_id == "industry_codes_data_broker_research":
            blocks.extend(subagents.generate_table_block(sec_title, "Industry Codes Table", client_name, brand_name, brand_url, ["Industry", "NAICS Code", "Description"]))
            blocks.extend(subagents.generate_table_block(sec_title, "Data Broker Table", client_name, brand_name, brand_url, ["Data Broker", "Global Companies", "USA Companies", "Description"]))
            blocks.extend(subagents.generate_subhead_block(sec_title, "White Space Summary", client_name, brand_name, brand_url))
        elif sec_id == "brand_archetypes":
            blocks.extend(subagents.generate_table_block(sec_title, "Brand Archetypes", client_name, brand_name, brand_url, ["Name/Title", "Mission", "Voice", "Values", "Emotional Promise", "Icon", "Voice in Action"]))
        elif sec_id == "brand_voice":
            blocks.extend(subagents.generate_subhead_block(sec_title, "Brand Voice Overview", client_name, brand_name, brand_url))
            blocks.extend(subagents.generate_table_block(sec_title, "Brand Voice Table", client_name, brand_name, brand_url, ["Channel", "Voice in Action"]))
            blocks.extend(subagents.generate_table_block(sec_title, "Factual Foundation Table", client_name, brand_name, brand_url, ["Factual Foundation", "Example"]))
            blocks.extend(subagents.generate_table_block(sec_title, "Tagline Table", client_name, brand_name, brand_url, ["Tagline", "Status", "Rationale"]))
        elif sec_id == "client_dos_donts":
            blocks.extend(subagents.generate_table_block(sec_title, "Do Table", client_name, brand_name, brand_url, ["Do", "Example"]))
            blocks.extend(subagents.generate_table_block(sec_title, "Don't Table", client_name, brand_name, brand_url, ["Don't", "Example"]))
            blocks.extend(subagents.generate_list_block(sec_title, "Most Common Pitfalls", client_name, brand_name, brand_url))
        elif sec_id == "content_keyword_strategy":
            blocks.extend(subagents.generate_table_block(sec_title, "Content & Keyword Strategy", client_name, brand_name, brand_url, ["Category", "Keyword", "Search Volume", "Intent"]))
            blocks.extend(subagents.generate_list_block(sec_title, "Phased Keyword Analysis", client_name, brand_name, brand_url))
            blocks.extend(subagents.generate_list_block(sec_title, "Blog Strategy", client_name, brand_name, brand_url))
            blocks.extend(subagents.generate_table_block(sec_title, "Blog Structure Table", client_name, brand_name, brand_url, ["Blog Structure"]))
            blocks.extend(subagents.generate_subhead_block(sec_title, "Required Word Count", client_name, brand_name, brand_url))
        elif sec_id == "social_strategy":
            blocks.extend(subagents.generate_list_block(sec_title, "Social Strategy Framework", client_name, brand_name, brand_url))
        elif sec_id == "social_production_checklist":
            blocks.extend(subagents.generate_list_block(sec_title, "Social Production Checklist", client_name, brand_name, brand_url))
        elif sec_id == "campaign_structure":
            blocks.extend(subagents.generate_table_block(sec_title, "Campaign Structure Table", client_name, brand_name, brand_url, ["Deliverable", "Count"]))
            blocks.extend(subagents.generate_list_block(sec_title, "Sample Campaign Timeline", client_name, brand_name, brand_url))
            blocks.extend(subagents.generate_list_block(sec_title, "Minimum Viable Campaign Checklist", client_name, brand_name, brand_url))
        elif sec_id == "landing_page_strategy":
            blocks.extend(subagents.generate_table_block(sec_title, "Landing Page Table", client_name, brand_name, brand_url, ["Section", "Description"]))
            blocks.extend(subagents.generate_table_block(sec_title, "Landing Page CTA Table", client_name, brand_name, brand_url, ["Type", "CTA"]))
            # Image block could be added here if needed
        elif sec_id == "engagement_framework":
            blocks.extend(subagents.generate_list_block(sec_title, "Engagement Framework Hierarchy", client_name, brand_name, brand_url))
            blocks.extend(subagents.generate_table_block(sec_title, "Engagement Framework Table", client_name, brand_name, brand_url, ["Initiative", "Alignment Points", "Target Audiences"]))
            blocks.extend(subagents.generate_list_block(sec_title, "RACI Matrix", client_name, brand_name, brand_url))
        else:
            # Fallback: add a placeholder paragraph
            blocks.append({
                "type": "Paragraph",
                "text": f"[REVIEW] Placeholder for {sec_title} section. Website: {website}"
            })
        section = {
            "id": sec_id,
            "title": sec_title,
            "blocks": blocks
        }
        kit["document"]["sections"].append(section)
    return kit

@app.route("/agent/marketing-kit", methods=["POST"])
def marketing_kit_endpoint():
    try:
        data = request.get_json(force=True)
        # Check for required fields (example: brand_name, brand_url)
        required_fields = ["brand_url"]
        missing = [field for field in required_fields if field not in data or not data[field]]
        if missing:
                return jsonify({"missing_fields": missing}), 400
        kit = build_marketing_kit(data)
        return jsonify(kit)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
