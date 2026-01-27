

import os
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler
import openai
from dotenv import load_dotenv
load_dotenv()


import flask
from flask import Flask, request, jsonify
from agent_services import subagents
from agent_services.markdown_postprocess import clean_markdown


LOG_PATH = os.path.join(os.path.dirname(__file__), 'marketing_agent_trace.log')
logger = logging.getLogger("marketing_agent")
logger.setLevel(logging.INFO)
handler = ConcurrentRotatingFileHandler(LOG_PATH, maxBytes=2*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)

app = Flask(__name__)

# Minimal marketing kit builder function

def build_marketing_kit(data):
    import time
    logger.info("[build_marketing_kit] START at %s", time.strftime('%X'))
    logger.info("[build_marketing_kit] Called with data: %s", str(data))
    website = data.get("website", "[FILL]")
    brand_url = data.get("brand_url", website)
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
    # Load gold standard for block type and order
    import json as _json
    try:
        with open('y:/Code/agentspace/gold_standard_marketing_kit.json', encoding='utf-8') as f:
            gold = _json.load(f)
    except Exception as e:
        logger.error("[build_marketing_kit] Failed to load gold standard: %s", str(e))
        raise
    gold_sections = {s['id']: s for s in gold['document']['sections']}

    def replace_placeholders(text):
        if isinstance(text, str):
            return text.replace("[BRAND]", client_name).replace("[CLIENT]", client_name)
        elif isinstance(text, list):
            return [replace_placeholders(t) for t in text]
        elif isinstance(text, dict):
            return {k: replace_placeholders(v) for k, v in text.items()}
        return text

    # Helper to call Anthropic Claude for dynamic copy
    def claude_prompt(section_title, client_name, user_data, gold_block):
        import anthropic
        import os
Client Name: {client_name}
Website: {user_data.get('website', '')}
Offering: {user_data.get('offering', '')}
Target Markets: {user_data.get('target_markets', '')}
Competitors: {user_data.get('competitors', '')}
Additional Details: {user_data.get('additional_details', '')}

Use the following as a structural guide, but do NOT copy verbatim. Instead, generate new, original copy that is tailored to the client and context:
{gold_block.get('text', '') or gold_block.get('items', '') or gold_block.get('section_titles', '') or gold_block.get('columns', '')}
Respond in the appropriate format for the block type: {gold_block.get('type')}. For tables or lists, generate realistic, relevant content.
"""
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        if gold_blocks:
            for idx, gold_block in enumerate(gold_blocks):
        import anthropic
        import os
        global logger
        prompt = f"""
                btype = gold_block.get('type')
                # Call Claude for each block
                block_content = claude_prompt(sec_title, client_name, data, gold_block)
                block = {"type": btype}
                # Assign content to the correct field based on block type
                if btype == 'Table':
                    block['columns'] = gold_block.get('columns', [])
                    block['rows'] = []
                    # Attempt to parse table rows from Claude output
                    block['text'] = block_content
                elif btype == 'Bullets':
                    block['items'] = [item.strip() for item in block_content.split('\n') if item.strip()]
                elif btype == 'Paragraph':
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        logger.info(f"[Claude API] Calling Claude for section '{section_title}' with block type '{gold_block.get('type')}'")
        logger.info(f"[Claude API] Prompt: {prompt}")
        # --- Claude API call ---
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            temperature=0.7,
            system="You are a marketing expert.",
            messages=[{"role": "user", "content": prompt}]
        )
        logger.info(f"[Claude API] Response: {response.content if hasattr(response, 'content') else response}")
        return response.content if hasattr(response, 'content') else response
                    block['text'] = block_content
                elif btype == 'Checklist':
                    block['items'] = [item.strip() for item in block_content.split('\n') if item.strip()]
                elif btype == 'ListOfSections':
                    block['section_titles'] = [item.strip() for item in block_content.split('\n') if item.strip()]
                elif btype == 'Image':
                    block['src'] = gold_block.get('src', '')
                    block['alt'] = block_content
                elif btype == 'Archetype':
                    block['title'] = gold_block.get('title', sec_title)
                    block['description'] = block_content
                elif btype == 'Persona':
                    block['title'] = gold_block.get('title', sec_title)
                    block['description'] = block_content
                elif btype == 'OpportunityCard':
                    block['title'] = gold_block.get('title', sec_title)
                    block['description'] = block_content
                else:
                    block['text'] = block_content
                block['coerced'] = True
                blocks.append(block)
        # If no blocks were generated, add an empty section to guarantee presence
        section_issues = []
        if not blocks:
            section_issues.append(f"Section '{sec_title}' is missing all blocks.")
        for block in blocks:
            if isinstance(block, dict) and 'review' in block and block['review']:
                section_issues.append(f"Section '{sec_title}' block issue: {block['review']}")
        if section_issues:
            validation_issues.extend(section_issues)
        section = {
            "id": sec_id,
            "title": sec_title,
            "blocks": blocks
        }
        kit["document"]["sections"].append(section)
        logger.info(f"[build_marketing_kit] Finished section: {sec_id} in {time.time() - section_start:.2f}s")
    if validation_issues:
        logger.warning(f"[build_marketing_kit] Validation issues found: {validation_issues}")
        kit["validation_issues"] = validation_issues
    logger.info("[build_marketing_kit] END at %s", time.strftime('%X'))
    return kit

@app.route("/agent/marketing-kit", methods=["POST"])
def marketing_kit_endpoint():
    import json
    logger.info("[marketing_kit_endpoint] Received request for /agent/marketing-kit")
    try:
        data = request.get_json(force=True)
    except Exception as e:
        logger.error("[marketing_kit_endpoint] JSON decode error: %s", str(e))
        return jsonify({"error": "Malformed JSON in request. Please check your payload."}), 400
    logger.info("[marketing_kit_endpoint] Payload: %s", str(data))
    # Check for required fields matching the frontend form
    required_fields = [
        "client_name",
        "website",
        "offering",
        "target_markets",
        "competitors",
        "additional_details",
        "files"
    ]
    missing = []
    # Fields that can be empty strings
    allow_empty = {"offering", "target_markets", "competitors", "additional_details"}
    for field in required_fields:
        if field not in data:
            missing.append(field)
        elif field == "files" and not isinstance(data[field], list):
            missing.append(field)
        elif field != "files":
            if not data[field] and field not in allow_empty:
                missing.append(field)
    if missing:
        logger.warning("[marketing_kit_endpoint] Missing fields: %s", str(missing))
        return jsonify({"missing_fields": missing}), 400
    try:
        kit = build_marketing_kit(data)
        # Check for ?format=markdown query param
        fmt = request.args.get('format', '').lower()
        if fmt == 'markdown':
            try:
                from agent_services.kit_templates import kit_to_markdown
                md = kit_to_markdown(kit)
                md_clean = clean_markdown(md)
                logger.info("[marketing_kit_endpoint] Markdown export successful")
                return md_clean, 200, {'Content-Type': 'text/markdown; charset=utf-8'}
            except Exception as e:
                logger.warning("[marketing_kit_endpoint] Markdown export failed: %s", str(e))
                return f"[ERROR] Markdown export failed: {e}", 500
        # Save kit as JSON for DOCX conversion
        with open('y:/Code/agentspace/tests/kit_output.json', 'w', encoding='utf-8') as f:
            json.dump(kit, f, ensure_ascii=False, indent=2)
        logger.info("[marketing_kit_endpoint] Kit generated and saved successfully")
        return jsonify(kit)
    except Exception as e:
        logger.error("[marketing_kit_endpoint] Exception: %s", str(e))
        return jsonify({"error": str(e)}), 400

    # The following except block was incorrectly indented. It should only catch exceptions from the outer try.

@app.errorhandler(Exception)
def handle_exception(e):
    logger = logging.getLogger("marketing_agent")
    logger.error("[marketing_kit_endpoint] Exception: %s", str(e))
    return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
