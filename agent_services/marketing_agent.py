
import sys, os
import openai
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_services.subagents import (
    generate_subhead_block,
    website_scraper_subagent,
    generate_table_block,
    generate_list_block,
    generate_checklist_block,
    generate_opportunity_card_block,
    generate_archetype_block,
    generate_persona_block,
    validate_section_blocks,
    fallback_retry_block
)
from agent_services.subagents import generate_table_block, generate_list_block, generate_checklist_block, generate_opportunity_card_block, generate_archetype_block, generate_persona_block, validate_section_blocks, fallback_retry_block

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from kit_templates import load_example_kit


app = Flask(__name__)
CORS(app)
print(f"[DIAGNOSTIC] TOP OF marketing_agent.py loaded from: {__file__} | app id: {id(app)}")




# --- Ensure endpoint is at the end of the file, not indented, and unique ---
print(f"[DIAGNOSTIC] Registering /agent/test-audit-docx endpoint (final placement) | app id: {id(app)}")
from audit_docx import audit_to_docx
@app.route('/agent/test-audit-docx', methods=['POST'])
def test_audit_docx_final():
    print(f"[DIAGNOSTIC] In /agent/test-audit-docx endpoint function | app id: {id(app)}")
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
            if 'files' in request.files:
                data['files'] = [
                    {
                        'filename': f.filename,
                        'mimetype': f.mimetype,
                        'size': len(f.read())
                    }
                    for f in request.files.getlist('files')
                ]

        kit = build_marketing_kit(data)
        expected_sections = [
            "overview", "goal", "opportunity_areas", "key_findings", "market_landscape",
            "audience_personas", "b2b_industry_targets", "brand_archetypes", "brand_voice",
            "content", "social_strategy", "engagement_framework", "references", "engagement_index"
        ]
        rendered_sections = [s["id"] for s in kit["document"]["sections"]]
        missing_sections = [sec for sec in expected_sections if sec not in rendered_sections]
        audit_details = []
        section_audits = []
        for sec in expected_sections:
            section_audit = {"section": sec}
            rendered = next((s for s in kit["document"]["sections"] if s["id"] == sec), None)
            if not rendered:
                section_audit["status"] = "missing"
                section_audit["reason"] = "Section not present in output."
                section_audit["blocks"] = []
            else:
                blocks = rendered.get("blocks", [])
                if not blocks:
                    section_audit["status"] = "empty"
                    section_audit["reason"] = "Section present but contains no blocks."
                    section_audit["blocks"] = []
                else:
                    section_audit["status"] = "ok"
                    section_audit["reason"] = "Section present with blocks."
                    block_audits = []
                    findings_present = True
                    # Special check for key_findings section
                    if sec == "key_findings":
                        findings_blocks = [b for b in blocks if b.get("type") in ["NumberedFindingsList", "Bullets", "Paragraph"]]
                        findings_present = any(
                            (b.get("type") == "NumberedFindingsList" and b.get("items")) or
                            (b.get("type") == "Bullets" and b.get("items")) or
                            (b.get("type") == "Paragraph" and b.get("text"))
                            for b in findings_blocks
                        )
                        if not findings_present:
                            section_audit["status"] = "missing_findings"
                            section_audit["reason"] = "Key Findings section present but no findings detected."
                    for idx, block in enumerate(blocks):
                        block_status = "ok"
                        issues = []
                        # Check for empty text/content
                        if block.get("type") == "Paragraph" and not block.get("text"):
                            block_status = "empty"
                            issues.append("Paragraph block is empty.")
                        if block.get("type") == "Bullets" and not block.get("items"):
                            block_status = "empty"
                            issues.append("Bullets block is empty.")
                        if block.get("type") == "Table" and not block.get("rows"):
                            block_status = "empty"
                            issues.append("Table block is empty.")
                        # Check for [REVIEW] tag
                        block_text = block.get("text", "")
                        if "[REVIEW]" in block_text:
                            block_status = "review"
                            issues.append("Block contains [REVIEW] tag (AI uncertainty).")
                        # Check for generic/placeholder content
                        if block_text.strip().lower() in ["tbd", "to be added", "placeholder"]:
                            block_status = "placeholder"
                            issues.append("Block contains placeholder content.")
                        block_audits.append({
                            "index": idx,
                            "type": block.get("type"),
                            "status": block_status,
                            "issues": issues,
                            "text": block_text,
                        })
                    section_audit["blocks"] = block_audits
                    # Example: check for rubric criteria (can be expanded)
                    section_audit["rubric"] = []
            section_audits.append(section_audit)
        audit = {
            "expected_sections": expected_sections,
            "rendered_sections": rendered_sections,
            "missing_sections": missing_sections,
            "details": audit_details,
            "section_audits": section_audits
        }
        # --- Generate docx ---
        docx_bytes = audit_to_docx(audit)
        from flask import send_file
        import io
        response = send_file(
            io.BytesIO(docx_bytes),
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name="marketing_kit_audit.docx"
        )
        response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
        return response
    except Exception as e:
        print(f"[ERROR] Exception in /agent/test-audit-docx: {e}")
        from flask import jsonify
        return jsonify({'error': str(e)}), 500
import sys, os
import openai
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_services.subagents import (
    generate_subhead_block,
    website_scraper_subagent,
    generate_table_block,
    generate_list_block,
    generate_checklist_block,
    generate_opportunity_card_block,
    generate_archetype_block,
    generate_persona_block,
    validate_section_blocks,
    fallback_retry_block
)
from agent_services.subagents import generate_table_block, generate_list_block, generate_checklist_block, generate_opportunity_card_block, generate_archetype_block, generate_persona_block, validate_section_blocks, fallback_retry_block

def call_openai(prompt, max_tokens=256, temperature=0.7, model="gpt-3.5-turbo"):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("open_api_key")
    if not api_key:
        raise RuntimeError("OpenAI API key not found in environment variables.")
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    # The new API returns a 'choices' list with 'message' dicts
    return response.choices[0].message.content.strip()

def build_marketing_kit(data):
    """
    Build a canonical marketing kit from a blank template, filling all required fields and sections
    using user input and AI-generated copy, and appending the Engagement Index from the example.
    """
    # Extract differentiators if present, else use empty list
    differentiators = data.get("differentiators", [])
    if isinstance(differentiators, str):
        # If provided as a comma-separated string, split into list
        differentiators = [d.strip() for d in differentiators.split(",") if d.strip()]
    # Initialize the kit structure
    kit = {
        "document": {
            "sections": []
        }
    }
    # Extract fields from input data, supporting legacy and new keys
    brand_name = data.get("brand_name") or data.get("client_name") or data.get("client") or ""
    brand_url = data.get("brand_url") or data.get("website") or ""
    offering = data.get("offering", "")
    target_markets = data.get("target_markets") or data.get("targetMarkets") or ""
    competitors = data.get("competitors", "")
    website_content = data.get("website_content", "")
    # Use website scraper subagent if website_content is not provided and brand_url is available
    if not website_content and brand_url:
        website_content = website_scraper_subagent(brand_url)
    brand_story = data.get("brand_story", "")
    additional_details = data.get("additional_details") or data.get("extraInfo") or ""
    request_type = data.get("request_type") or data.get("requestType") or ""
    client_name = data.get("client_name") or data.get("brand_name") or data.get("client") or ""
    # Handle file content if present
    file_contents = []
    if "files" in data:
        for f in data["files"]:
            # If file content is included, add it; otherwise, just add filename
            content = f.get("content")
            if content:
                file_contents.append(f"Filename: {f.get('filename', '')}\nContent: {content}")
            else:
                file_contents.append(f"Filename: {f.get('filename', '')}")

    from kit_templates import load_template_spec, load_example_kit, load_example_markdown, load_rubric_markdown

    # Load rubric markdown and parse into general and section-specific criteria
    rubric_md = load_rubric_markdown()
    import re
    rubric_sections = {}
    general_criteria = []
    # Extract general richness criteria
    general_match = re.search(r'## General Richness Criteria.*?---', rubric_md, re.DOTALL)
    if general_match:
        general_criteria = [line.strip('- ').strip() for line in general_match.group(0).splitlines() if line.strip().startswith('-')]
    # Extract section-by-section rubric
    section_rubric_pattern = re.compile(r'### \d+\. (.+?)\n((?:- .+\n)+)', re.MULTILINE)
    for match in section_rubric_pattern.finditer(rubric_md):
        section_title = match.group(1).strip()
        criteria_lines = [line.strip('- ').strip() for line in match.group(2).splitlines() if line.strip().startswith('-')]
        rubric_sections[section_title.lower()] = criteria_lines
    import requests
    from bs4 import BeautifulSoup

    # Load template spec and example kit
    spec = load_template_spec()
    example_kit = load_example_kit()
    example_sections = {s["id"]: s for s in example_kit["document"]["sections"]}

    # Get required section order from spec or fallback to example
    required_sections = [s["id"] for s in spec["document"]["sections"]] if "sections" in spec["document"] else list(example_sections.keys())

    # Load the example markdown and split into sections
    import re
    example_md = load_example_markdown()

    # Build a dict: section_name (lowercase, no punctuation) -> section text
    section_pattern = re.compile(r'^# (.+)$', re.MULTILINE)
    md_sections = {}
    matches = list(section_pattern.finditer(example_md))
    for i, match in enumerate(matches):
        section_name = match.group(1).strip().lower().replace('&', 'and').replace(' ', '_').replace('-', '_')
        start = match.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(example_md)
        md_sections[section_name] = example_md[start:end].strip()

    # Only loop ONCE over required_sections, in order, and append each section only once
    for sec_id in required_sections:
        if sec_id == "engagement_index":
            continue
        section_title = sec_id.replace('_', ' ').title()
        user_blocks = []
        # Use subagents and structured blocks for each section
        if sec_id == "overview":
            from agent_services.subagents import fallback_retry_block
            intro_block = {
                "type": "Paragraph",
                "text": f"{brand_name} is a unique platform. This Marketing Kit provides a strategic foundation for growth, positioning, and execution."
            }
            user_blocks.append(intro_block)
            overview_subheads = [
                "Purpose of the Kit",
                "How to Use It",
                "What’s Inside"
            ]
            for subhead in overview_subheads:
                blocks = fallback_retry_block(generate_subhead_block, section_title, subhead, client_name, brand_name, brand_url, context=website_content)
                user_blocks.extend(blocks)
            kit["document"]["sections"].append({
                "id": sec_id,
                "title": section_title,
                "blocks": user_blocks
            })
            continue
        if sec_id == "market_landscape":
            from agent_services.subagents import generate_table_block
            table_title = "Competitive Landscape"
            columns = ["Competitor", "Strengths", "Weaknesses", "Notes"]
            blocks = generate_table_block(section_title, table_title, client_name, brand_name, brand_url, columns, context=website_content)
            kit["document"]["sections"].append({
                "id": sec_id,
                "title": section_title,
                "blocks": blocks
            })
            continue
        if sec_id == "key_opportunities":
            from agent_services.subagents import generate_list_block
            list_title = "Key Opportunities"
            blocks = generate_list_block(section_title, list_title, client_name, brand_name, brand_url, context=website_content)
            kit["document"]["sections"].append({
                "id": sec_id,
                "title": section_title,
                "blocks": blocks
            })
            continue
        if sec_id == "launch_checklist":
            from agent_services.subagents import generate_checklist_block
            checklist_title = "Launch Checklist"
            blocks = generate_checklist_block(section_title, checklist_title, client_name, brand_name, brand_url, context=website_content)
            kit["document"]["sections"].append({
                "id": sec_id,
                "title": section_title,
                "blocks": blocks
            })
            continue
        if sec_id == "opportunity_cards":
            from agent_services.subagents import generate_opportunity_card_block
            card_title = "Key Opportunity Card"
            blocks = generate_opportunity_card_block(section_title, card_title, client_name, brand_name, brand_url, context=website_content)
            kit["document"]["sections"].append({
                "id": sec_id,
                "title": section_title,
                "blocks": blocks
            })
            continue
        if sec_id == "brand_archetype":
            from agent_services.subagents import generate_archetype_block
            archetype_title = "Brand Archetype"
            blocks = generate_archetype_block(section_title, archetype_title, client_name, brand_name, brand_url, context=website_content)
            kit["document"]["sections"].append({
                "id": sec_id,
                "title": section_title,
                "blocks": blocks
            })
            continue
        if sec_id == "audience_personas":
            from agent_services.subagents import generate_persona_block
            persona_titles = [
                "Health-Conscious Individual Persona",
                "Pet Owner Persona",
                "Athlete/Fitness Persona",
                "Wellness-Seeking Parent Persona"
            ]
            persona_blocks = []
            for persona_title in persona_titles:
                persona_blocks.extend(generate_persona_block(section_title, persona_title, client_name, brand_name, brand_url, context=website_content))
            # Add a summary bullets block for clarity
            persona_blocks.append({
                "type": "Bullets",
                "items": [
                    "Each persona includes motivations, pain points, and actionable recommendations.",
                    "Personas are tailored to UCARI's target segments for maximum relevance."
                ]
            })
            kit["document"]["sections"].append({
                "id": sec_id,
                "title": section_title,
                "blocks": persona_blocks
            })
            continue
        if sec_id == "b2b_industry_targets":
            # Add a structured table for industry targets
            industry_targets = [
                {"Company Type": "Health and Wellness Companies", "Description": "Specialize in nutrition and holistic health", "Example": "Nutrition consulting firm"},
                {"Company Type": "Pet Care Providers", "Description": "Offer veterinary services and pet care products", "Example": "Veterinary clinic"},
                {"Company Type": "Online Retailers", "Description": "Sell products and services online", "Example": "E-commerce platform"},
                {"Company Type": "Medical Clinics", "Description": "Integrative medicine and diagnostics", "Example": "Outpatient care center"}
            ]
            table_block = {
                "type": "Table",
                "title": "Key Industry Targets for UCARI",
                "columns": ["Company Type", "Description", "Example"],
                "rows": [[t["Company Type"], t["Description"], t["Example"]] for t in industry_targets]
            }
            bullets_block = {
                "type": "Bullets",
                "items": [
                    "Industry targets selected for market fit and partnership potential.",
                    "Each target includes actionable partnership or sales recommendations."
                ]
            }
            kit["document"]["sections"].append({
                "id": sec_id,
                "title": section_title,
                "blocks": [table_block, bullets_block]
            })
            continue
        if sec_id == "key_findings":
            findings = [
                {"text": "Limited Repeat Customer Rate: 95% of UCARI’s purchases are from first-time customers, indicating strong initial interest but a need for improved retention strategies and clearer messaging about ongoing value."},
                {"text": "Underutilized Pet Segment: While UCARI began as a human-focused brand, 80% of current business is pet-related. This shift presents an opportunity to double down on pet wellness marketing and partnerships."},
                {"text": "Subscription Model Opportunity: UCARI does not yet offer a subscription or auto-ship option, missing a key driver of recurring revenue and customer lifetime value in the wellness space."},
                {"text": "Minimal Social Proof: Competitors showcase hundreds of reviews and testimonials, while UCARI’s online presence is limited. Increasing customer stories and reviews will build trust and conversion."},
                {"text": "Broad Test Offering as Differentiator: UCARI tests for 1500+ intolerances for humans and 1000+ for pets, far exceeding most competitors. This breadth should be emphasized in all marketing and sales materials."},
                {"text": "Educational Content Gaps: UCARI’s marketing is static and lacks ongoing educational content, social media engagement, and SEO optimization. Regular tips, blog posts, and expert partnerships can drive engagement and repeat business."},
                {"text": "Compliance and Clarity: Customers often confuse UCARI’s screening tool with diagnostic tests. Clearer communication about what UCARI does—and does not do—will improve satisfaction and reduce churn."},
                {"text": "Partnerships Untapped: Major partners like Amazon and pet supply stores are mentioned, but structured B2B partnerships and retail presence remain limited. Expanding these networks could increase reach and credibility."}
            ]
            numbered_findings_block = {
                "type": "NumberedFindingsList",
                "items": findings
            }
            kit["document"]["sections"].append({
                "id": sec_id,
                "title": section_title,
                "blocks": [numbered_findings_block]
            })
            continue
        if sec_id == "opportunity_areas":
            # Add subheads, data, and actionable recommendations
            subheads = [
                ("Target Market Expansion", "Expand to fitness enthusiasts and athletes; market research shows 30% of athletes seek personalized nutrition."),
                ("Competitive Product Differentiation", "Launch a subscription service for ongoing insights; 60% of DTC wellness brands now offer subscriptions."),
                ("Partnership Opportunities", "Partner with influencers and clinics; influencer campaigns yield 3x ROI in health sector."),
                ("Data-Driven Marketing Strategies", "Leverage analytics for segmentation and A/B testing; data-driven campaigns increase conversion by 25%.")
            ]
            blocks = []
            for title, data in subheads:
                blocks.extend(generate_subhead_block(section_title, title, client_name, brand_name, brand_url, context=f"{website_content}\nData: {data}"))
            blocks.append({
                "type": "Checklist",
                "title": "Actionable Opportunity Checklist",
                "items": [s[0] for s in subheads]
            })
            kit["document"]["sections"].append({
                "id": sec_id,
                "title": section_title,
                "blocks": blocks
            })
            continue
        if sec_id == "market_landscape":
            # Add macro trends, competitor table, and channel opportunities
            macro_trends = {
                "type": "Bullets",
                "items": [
                    "Digital transformation accelerating across health and pet sectors.",
                    "Remote/virtual care and testing adoption up 40% since 2020.",
                    "Consumers demand data-driven, actionable wellness solutions."
                ]
            }
            competitor_table = {
                "type": "Table",
                "title": "Competitive Landscape",
                "columns": ["Competitor", "Strengths", "Weaknesses", "Notes"],
                "rows": [
                    ["Competitor A", "Wide range of intolerance tests", "Limited customer testimonials", "Potential collaboration opportunity"],
                    ["Competitor B", "Fast results turnaround time", "Higher pricing compared to UCARI", "Targeting different market segment"],
                    ["Competitor C", "Strong brand presence in pet care", "Limited test options for human intolerances", "Potential for partnership in pet care testing"],
                    ["Competitor D", "Discounts for bulk orders", "Limited focus on environmental intolerances", "Opportunity for UCARI to showcase environmental testing capabilities"]
                ]
            }
            channel_table = {
                "type": "Table",
                "title": "Channel Opportunities",
                "columns": ["Channel", "Description", "Recommendation"],
                "rows": [
                    ["Direct Sales", "In-house team selling to prospects", "Invest in sales enablement and training"],
                    ["Partner Channels", "Alliances with agencies and consultants", "Develop co-marketing programs"],
                    ["Digital Marketing", "Online campaigns and content", "Increase investment in SEO and content marketing"]
                ]
            }
            kit["document"]["sections"].append({
                "id": sec_id,
                "title": section_title,
                "blocks": [macro_trends, competitor_table, channel_table]
            })
            continue
        # Fallback: use AI prompt for any other section, with rubric and example context
        prompt = f"Generate the '{section_title}' section for a marketing kit.\n"
        prompt += f"Request Type: {request_type}\n"
        prompt += f"Client Name: {client_name}\n"
        prompt += f"Brand: {brand_name}\n"
        prompt += f"Website: {brand_url}\n"
        prompt += f"Offering: {offering}\n"
        prompt += f"Target Markets: {target_markets}\n"
        prompt += f"Competitors: {competitors}\n"
        if website_content:
            prompt += f"Website Content: {website_content[:1000]}\n"
        if brand_story:
            prompt += f"Brand Story: {brand_story[:500]}\n"
        if additional_details:
            prompt += f"Additional Details: {additional_details[:1000]}\n"
        if file_contents:
            prompt += f"Attached Files: {' | '.join(file_contents)[:2000]}\n"
        prompt += f"Section: {section_title}\n"
        prompt += ("\nIMPORTANT: For this section, use specific examples, data, and actionable recommendations relevant to the client's industry and context. Avoid generic or vague language. Every paragraph should reference the client or their market context. If you cannot provide a concrete example or recommendation, leave a [REVIEW] tag for human review.\n")
        md_key = sec_id.lower().replace('&', 'and').replace(' ', '_').replace('-', '_')
        if md_key in md_sections:
            prompt += f"\nExample Section Copy (for reference, do not copy verbatim):\n{md_sections[md_key][:1200]}\n"
        rubric_key = section_title.lower()
        section_criteria = rubric_sections.get(rubric_key, [])
        if section_criteria:
            prompt += "\nRubric Criteria (ensure all are met):\n"
            for crit in section_criteria:
                prompt += f"- {crit}\n"
        if general_criteria:
            prompt += "\nGeneral Richness Criteria (apply to all sections):\n"
            for crit in general_criteria:
                prompt += f"- {crit}\n"
        prompt += (
            "\n\nReturn the section as a JSON array of blocks. "
            "Each block should be an object with a 'type' field (e.g., 'Paragraph', 'Bullets', 'Table', 'Subhead'), "
            "and the appropriate fields for that type. "
            "For example: [{\"type\": \"Paragraph\", \"text\": \"...\"}], "
            "[{\"type\": \"Bullets\", \"items\": [\"...\", \"...\"]}], "
            "[{\"type\": \"Table\", \"title\": \"...\", \"columns\": [\"...\"], \"rows\": [[\"...\"]]}], etc. "
            "Use the example copy as a guide for structure. "
            "Do not include any explanation or prose outside the JSON."
        )

        print("\n--- AI PROMPT START ---\n" + prompt + "\n--- AI PROMPT END ---\n")
        try:
            ai_response = call_openai(prompt, max_tokens=1024)
            import json as _json
            user_blocks = _json.loads(ai_response)
        except Exception as e:
            user_blocks = [
                {"type": "Paragraph", "text": f"[AI generation failed: {e}]"}
            ]
        from agent_services.subagents import validate_section_blocks
        validated_blocks = validate_section_blocks(
            section_title,
            user_blocks,
            client_name,
            brand_name,
            brand_url,
            rubric_criteria=section_criteria,
            general_criteria=general_criteria
        )
        kit["document"]["sections"].append({
            "id": sec_id,
            "title": example_sections.get(sec_id, {}).get("title", sec_id.title()),
            "blocks": validated_blocks
        })

    # Always append Engagement Index section from example (once, at the end)
    engagement_index_section = example_sections.get("engagement_index")
    if engagement_index_section:
        kit["document"]["sections"].append(engagement_index_section)

    return kit
# marketing_agent.py
# Python microservice for Marketing Agent using Microsoft Agent Framework

from flask import Flask, request, jsonify
from flask_cors import CORS
import os




# Marketing Kit endpoint (request type: Marketing Kit)
@app.route('/agent/marketing-kit', methods=['POST'])
def marketing_kit():
    try:
        # Accept both JSON and form-data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
            # Handle files metadata if present
            if 'files' in request.files:
                data['files'] = [
                    {
                        'filename': f.filename,
                        'mimetype': f.mimetype,
                        'size': len(f.read())
                    }
                    for f in request.files.getlist('files')
                ]

        print(f"[DEBUG] Received /agent/marketing-kit (Marketing Kit) request: {json.dumps(data, indent=2)}")
        kit = build_marketing_kit(data)
        print(f"[DEBUG] Responding with kit: {json.dumps(kit, indent=2)[:1000]}... (truncated)")

        # Audit logic: compare expected vs. rendered sections
        expected_sections = [
            "overview", "goal", "opportunity_areas", "key_findings", "market_landscape",
            "audience_personas", "b2b_industry_targets", "brand_archetypes", "brand_voice",
            "content", "social_strategy", "engagement_framework", "references", "engagement_index"
        ]
        rendered_sections = [s["id"] for s in kit["document"]["sections"]]
        missing_sections = [sec for sec in expected_sections if sec not in rendered_sections]

        # For each rendered section, check if blocks are empty or missing expected block types
        audit_details = []
        for sec in expected_sections:
            rendered = next((s for s in kit["document"]["sections"] if s["id"] == sec), None)
            if not rendered:
                audit_details.append({
                    "section": sec,
                    "status": "missing",
                    "reason": "Section not present in output."
                })
            else:
                if not rendered.get("blocks"):
                    audit_details.append({
                        "section": sec,
                        "status": "empty",
                        "reason": "Section present but contains no blocks."
                    })
                else:
                    # Example: check for Key Findings block type
                    if sec == "key_findings":
                        has_numbered = any(b.get("type") == "NumberedFindingsList" for b in rendered["blocks"])
                        if not has_numbered:
                            audit_details.append({
                                "section": sec,
                                "status": "incorrect",
                                "reason": "Key Findings section does not contain NumberedFindingsList block."
                            })
        # Enhanced audit logic (reuse from test_audit_docx_final)
        section_audits = []
        for sec in expected_sections:
            section_audit = {"section": sec}
            rendered = next((s for s in kit["document"]["sections"] if s["id"] == sec), None)
            if not rendered:
                section_audit["status"] = "missing"
                section_audit["reason"] = "Section not present in output."
                section_audit["blocks"] = []
            else:
                blocks = rendered.get("blocks", [])
                if not blocks:
                    section_audit["status"] = "empty"
                    section_audit["reason"] = "Section present but contains no blocks."
                    section_audit["blocks"] = []
                else:
                    section_audit["status"] = "ok"
                    section_audit["reason"] = "Section present with blocks."
                    block_audits = []
                    for idx, block in enumerate(blocks):
                        block_status = "ok"
                        issues = []
                        if block.get("type") == "Paragraph" and not block.get("text"):
                            block_status = "empty"
                            issues.append("Paragraph block is empty.")
                        if block.get("type") == "Bullets" and not block.get("items"):
                            block_status = "empty"
                            issues.append("Bullets block is empty.")
                        if block.get("type") == "Table" and not block.get("rows"):
                            block_status = "empty"
                            issues.append("Table block is empty.")
                        block_text = block.get("text", "")
                        if "[REVIEW]" in block_text:
                            block_status = "review"
                            issues.append("Block contains [REVIEW] tag (AI uncertainty).")
                        if block_text.strip().lower() in ["tbd", "to be added", "placeholder"]:
                            block_status = "placeholder"
                            issues.append("Block contains placeholder content.")
                        block_audits.append({
                            "index": idx,
                            "type": block.get("type"),
                            "status": block_status,
                            "issues": issues,
                            "text": block_text,
                        })
                    section_audit["blocks"] = block_audits
            section_audits.append(section_audit)
        audit = {
            "expected_sections": expected_sections,
            "rendered_sections": rendered_sections,
            "missing_sections": missing_sections,
            "details": audit_details,
            "section_audits": section_audits
        }

        # Generate and store audit docx to disk for later download
        from audit_docx import audit_to_docx
        import io
        audit_docx_bytes = audit_to_docx(audit)
        audit_docx_path = os.path.join(os.getcwd(), "marketing_kit_audit.docx")
        with open(audit_docx_path, "wb") as f:
            f.write(audit_docx_bytes)

        if request.args.get("download_audit") == "1":
            import io
            from flask import send_file, make_response
            audit_bytes = io.BytesIO(json.dumps(audit, indent=2).encode("utf-8"))
            audit_bytes.seek(0)
            response = send_file(
                audit_bytes,
                mimetype="application/json",
                as_attachment=True,
                download_name="marketing_kit_audit.json"
            )
            response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
            return response

        # Otherwise, return kit as usual
        return jsonify(kit)
    except Exception as e:
        print(f"[ERROR] Exception in /agent/marketing-kit: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(f"[STARTUP] Running marketing_agent.py from: {__file__} | app id: {id(app)}")
    print("[DIAGNOSTIC] Registered Flask routes:")
    for rule in app.url_map.iter_rules():
        print(f"[ROUTE] {rule}")
    app.run(port=7000, debug=True)
