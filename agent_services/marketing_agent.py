
import os
import openai
from dotenv import load_dotenv
load_dotenv()

import flask
from flask import Flask, request, jsonify
from agent_services import subagents

app = Flask(__name__)

# Minimal marketing kit builder function

def build_marketing_kit(data):
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
    with open('y:/Code/agentspace/gold_standard_marketing_kit.json', encoding='utf-8') as f:
        gold = _json.load(f)
    gold_sections = {s['id']: s for s in gold['document']['sections']}

    def replace_placeholders(text):
        if not isinstance(text, str):
            return text
        return text.replace("[BRAND]", client_name).replace("[CLIENT]", client_name)

    # Helper to call OpenAI for dynamic copy
    def generate_dynamic_copy(section_title, gold_block, user_data):
        prompt = f"""
You are a marketing expert. Write a rich, detailed, and creative section for a marketing kit.
Section: {section_title}
Client Name: {client_name}
Website: {user_data.get('website', '')}
Offering: {user_data.get('offering', '')}
Target Markets: {user_data.get('target_markets', '')}
Competitors: {user_data.get('competitors', '')}
Additional Details: {user_data.get('additional_details', '')}

Use the following as a structural guide, but do NOT copy verbatim. Instead, generate new, original copy that is tailored to the client and context:
---
{gold_block.get('text', '') or gold_block.get('items', '') or gold_block.get('section_titles', '') or gold_block.get('columns', '')}
---
Respond in the appropriate format for the block type: {gold_block.get('type')}. For tables or lists, generate realistic, relevant content.
"""
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful marketing copywriter."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600
        )
        return response.choices[0].message.content.strip()

    for sec_id, sec_title in required_sections:
        blocks = []
        gold_blocks = gold_sections.get(sec_id, {}).get('blocks', [])
        for gold_block in gold_blocks:
            btype = gold_block.get('type')
            # Use OpenAI to generate dynamic content for each block type
            if btype in ['Paragraph', 'Subhead', 'Bullets', 'Checklist', 'ListOfSections', 'Table']:
                ai_content = generate_dynamic_copy(sec_title, gold_block, data)
                if btype == 'Paragraph':
                    blocks.append({"type": "Paragraph", "text": ai_content})
                elif btype == 'Subhead':
                    blocks.append({"type": "Subhead", "text": ai_content})
                elif btype == 'Bullets':
                    # Split lines for bullets
                    items = [line.strip('-• ').strip() for line in ai_content.split('\n') if line.strip()]
                    blocks.append({"type": "Bullets", "items": items})
                elif btype == 'Checklist':
                    items = [line.strip('-• ').strip() for line in ai_content.split('\n') if line.strip()]
                    blocks.append({"type": "Checklist", "title": sec_title, "items": items})
                elif btype == 'ListOfSections':
                    items = [line.strip('-• ').strip() for line in ai_content.split('\n') if line.strip()]
                    blocks.append({"type": "ListOfSections", "section_titles": items})
                elif btype == 'Table':
                    # For simplicity, treat AI output as markdown table or CSV
                    import csv
                    import io
                    rows = []
                    columns = []
                    if '|' in ai_content:
                        # Markdown table
                        lines = [l for l in ai_content.split('\n') if l.strip() and '---' not in l]
                        if lines:
                            columns = [c.strip() for c in lines[0].split('|') if c.strip()]
                            for row_line in lines[1:]:
                                row = [c.strip() for c in row_line.split('|') if c.strip()]
                                if row:
                                    rows.append(row)
                    else:
                        # CSV fallback
                        reader = csv.reader(io.StringIO(ai_content))
                        for i, row in enumerate(reader):
                            if i == 0:
                                columns = row
                            else:
                                rows.append(row)
                    blocks.append({"type": "Table", "columns": columns, "rows": rows})
            elif btype == 'Image':
                blocks.append({
                    "type": "Image",
                    "src": gold_block.get('src', ''),
                    "alt": replace_placeholders(gold_block.get('alt', ''))
                })
            elif btype == 'Archetype':
                # For archetype, fallback to static structure for now
                if sec_id in ("audience_archetypes", "brand_archetypes"):
                    columns = [replace_placeholders(col) for col in gold_block.get('columns', [
                        "Name/Title", "Mission", "Voice", "Values", "Emotional Promise", "Icon", "Voice in Action"
                    ])]
                    rows = [
                        [replace_placeholders(cell) for cell in row]
                        for row in gold_block.get('rows', [])
                    ]
                    blocks.append({
                        "type": "Table",
                        "columns": columns,
                        "rows": rows
                    })
                else:
                    blocks.append({
                        "type": "Archetype",
                        "title": replace_placeholders(gold_block.get('title', '')),
                        "description": replace_placeholders(gold_block.get('description', '')),
                        "attributes": {k: replace_placeholders(v) for k, v in gold_block.get('attributes', {}).items()},
                    })
            else:
                blocks.append({
                    "type": "Paragraph",
                    "text": f"[REVIEW] Placeholder for {sec_title} block type {btype}. Website: {website}"
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
        import json
        print("[DEBUG] Received request for /agent/marketing-kit")
        data = request.get_json(force=True)
        print(f"[DEBUG] Payload: {data}")
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
            print(f"[DEBUG] Missing fields: {missing}")
            return jsonify({"missing_fields": missing}), 400
        kit = build_marketing_kit(data)
        # Save kit as JSON for DOCX conversion
        with open('y:/Code/agentspace/tests/kit_output.json', 'w', encoding='utf-8') as f:
            json.dump(kit, f, ensure_ascii=False, indent=2)
        print("[DEBUG] Kit generated successfully")
        return jsonify(kit)
    except Exception as e:
        print(f"[ERROR] Exception in /agent/marketing-kit: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
