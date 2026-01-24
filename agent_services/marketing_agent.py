from agent_services.kit_templates import load_example_kit

import sys
import os
import openai
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
marketing_agent.py
------------------
Main Flask microservice for the Marketing Agent. Handles requests for marketing kit generation, audit, and document output.
Endpoints:
    /agent/marketing-kit
    /agent/test-audit-docx
"""

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

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from agent_services.kit_templates import load_example_kit



app: Flask = Flask(__name__)
CORS(app)
print(f"[DIAGNOSTIC] TOP OF marketing_agent.py loaded from: {__file__} | app id: {id(app)}")




# --- Ensure endpoint is at the end of the file, not indented, and unique ---
print(f"[DIAGNOSTIC] Registering /agent/test-audit-docx endpoint (final placement) | app id: {id(app)}")
from agent_services.audit_docx import audit_to_docx

@app.route('/agent/test-audit-docx', methods=['POST'])
def test_audit_docx_final() -> 'Response':
    """
    Endpoint to audit the generated marketing kit and return a DOCX report.
    Accepts POST requests with kit data.
    """
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

def build_marketing_kit(data):
    # Robust input validation and defaults
    required_fields = [
        "brand_name", "brand_url", "offering", "target_markets", "competitors"
    ]
    # No longer fill missing fields with '[Not Provided]'; handled by endpoint validation

    differentiators = data.get("differentiators", [])
    if isinstance(differentiators, str):
        differentiators = [d.strip() for d in differentiators.split(",") if d.strip()]

    # Always initialize kit structure
    kit = {"document": {"sections": []}}

    # Real section generation: only include sections with real, generated content
    import concurrent.futures
    required_sections = [
        "overview", "goal", "opportunity_areas", "key_findings", "market_landscape",
        "audience_personas", "b2b_industry_targets", "brand_archetypes", "brand_voice",
        "content", "social_strategy", "engagement_framework", "references", "engagement_index"
    ]
    warnings = []
    # Scrape website content if brand_url is provided
    website_content = ""
    if data.get("brand_url"):
        try:
            website_content = website_scraper_subagent(data["brand_url"], max_length=2000)
        except Exception as e:
            website_content = f"[Website scrape failed: {e}]"

    # Read attached document text if present (e.g., Brand Story)
    file_contents = []
    if "files" in data:
        import os
        for f in data["files"]:
            try:
                # Only process text-based files (e.g., .txt, .md, .pdf if text extraction is implemented)
                if f["filename"].lower().endswith(('.txt', '.md')):
                    with open(os.path.join("agent_services", f["filename"]), "r", encoding="utf-8") as file:
                        file_contents.append(file.read())
                # PDF extraction could be added here if needed
            except Exception as e:
                file_contents.append(f"[File read failed: {f['filename']}: {e}]")

    def generate_section(sec_id):
        try:
            brand = data.get("brand_name", "[FILL]")
            url = data.get("brand_url", "[FILL]")
            offering = data.get("offering", "[FILL]")
            target_markets = data.get("target_markets", "[FILL]")
            competitors = data.get("competitors", "[FILL]")
            # Compose context for all section prompts
            context_parts = []
            if website_content:
                context_parts.append(f"Website Content: {website_content}")
            if file_contents:
                context_parts.append(f"Attached Files: {' | '.join(file_contents)}")
            # Optionally, you could add OpenAI web search here if your API plan supports it (e.g., Bing Search or OpenAI's web-enabled models)
            # For now, only use scraped and attached content
            base_context = "\n".join(context_parts)
            # Overview
            if sec_id == "overview":
                return {
                    "id": sec_id,
                    "title": "Overview",
                    "blocks": generate_subhead_block(
                        "Overview", "Overview", brand, brand, url,
                        context=(
                            f"Purpose and use of the kit for {brand}. Offering: {offering}. Target markets: {target_markets}. "
                            "You may use general industry context and best practices, but do not invent any client-specific facts or numbers.\n" + base_context
                        )
                    )
                }
            # The Goal
            if sec_id == "goal":
                return {
                    "id": sec_id,
                    "title": "The Goal",
                    "blocks": generate_subhead_block(
                        "The Goal", "The Goal", brand, brand, url,
                        context=(
                            f"Primary business/marketing goal for {brand}. Target market: {target_markets}. Offering: {offering}. "
                            "You may use general industry context and best practices, but do not invent any client-specific facts or numbers.\n" + base_context
                        )
                    )
                }
            # Opportunity Areas
            if sec_id == "opportunity_areas":
                return {
                    "id": sec_id,
                    "title": "Opportunity Areas",
                    "blocks": generate_subhead_block(
                        "Opportunity Areas", "Opportunity Areas", brand, brand, url,
                        context=(
                            f"3-4 opportunity areas for {brand}. Use provided offering: {offering} and target markets: {target_markets}. "
                            "You may use general industry trends and best practices, but do not invent any client-specific facts or numbers.\n" + base_context
                        )
                    )
                }
            # Key Findings
            if sec_id == "key_findings":
                return {
                    "id": sec_id,
                    "title": "Key Findings",
                    "blocks": generate_list_block(
                        "Key Findings",
                        "Key Findings",
                        brand,
                        brand,
                        url,
                        context=(
                            f"5-6 key findings for {brand}. Use provided competitors: {competitors} and offering: {offering}. "
                            "You may use general industry benchmarks, but do not invent any client-specific facts or numbers.\n" + base_context
                        )
                    )
                }
            # Market Landscape
            if sec_id == "market_landscape":
                return {
                    "id": sec_id,
                    "title": "Market Landscape",
                    "blocks": [
                        *generate_subhead_block(
                            "Market Landscape", "Market Landscape", brand, brand, url,
                            context=(
                                f"Macro trends, competitor landscape, and channel opportunities for {brand}. Use provided offering: {offering}, competitors: {competitors}, and target markets: {target_markets}. "
                                "You may use general industry research, but do not invent any client-specific facts or numbers.\n" + base_context
                            )
                        ),
                        *generate_list_block(
                            "Market Landscape",
                            "Key Market Trends and Opportunities",
                            brand,
                            brand,
                            url,
                            context=(
                                f"List 3-5 key market trends, competitor patterns, and channel opportunities for {brand}. Use provided offering: {offering}, competitors: {competitors}, and target markets: {target_markets}. "
                                "You may use general industry research, but do not invent any client-specific facts or numbers.\n" + base_context
                            )
                        )
                    ]
                }
            # Audience & User Personas
            if sec_id == "audience_personas":
                personas = []
                for i in range(3):
                    personas.extend(generate_persona_block(
                        "Audience & User Personas", f"Persona {i+1}", brand, brand, url,
                        context=(
                            f"Target markets: {target_markets}. Offering: {offering}. "
                            "You may use general persona research for the industry, but do not invent any client-specific facts or numbers.\n" + base_context
                        )
                    ))
                return {
                    "id": sec_id,
                    "title": "Audience & User Personas",
                    "blocks": personas
                }
            # B2B Industry Targets
            if sec_id == "b2b_industry_targets":
                return {
                    "id": sec_id,
                    "title": "B2B Industry Targets",
                    "blocks": generate_table_block(
                        "B2B Industry Targets", "Key Industry Targets", brand, brand, url, ["Company Type", "Description", "Example"],
                        context=(
                            f"Offering: {offering}. Target markets: {target_markets}. "
                            "You may use general industry research, but do not invent any client-specific facts or numbers.\n" + base_context
                        )
                    )
                }
            # Brand Archetypes
            if sec_id == "brand_archetypes":
                return {
                    "id": sec_id,
                    "title": "Brand Archetypes",
                    "blocks": generate_archetype_block(
                        "Brand Archetypes", "Primary Archetype", brand, brand, url,
                        context=(
                            f"Offering: {offering}. Target markets: {target_markets}. "
                            "You may use general archetype research, but do not invent any client-specific facts or numbers.\n" + base_context
                        )
                    ) + generate_archetype_block(
                        "Brand Archetypes", "Secondary Archetype", brand, brand, url,
                        context=(
                            f"Offering: {offering}. Target markets: {target_markets}. "
                            "You may use general archetype research, but do not invent any client-specific facts or numbers.\n" + base_context
                        )
                    )
                }
            # Brand Voice
            if sec_id == "brand_voice":
                return {
                    "id": sec_id,
                    "title": "Brand Voice",
                    "blocks": generate_subhead_block(
                        "Brand Voice", "Brand Voice", brand, brand, url,
                        context=(
                            f"Voice, tone, and messaging for {brand}. Offering: {offering}. "
                            "You may use general brand voice best practices, but do not invent any client-specific facts or numbers.\n" + base_context
                        )
                    )
                }
            # Content
            if sec_id == "content":
                return {
                    "id": sec_id,
                    "title": "Content",
                    "blocks": generate_subhead_block(
                        "Content", "Content", brand, brand, url,
                        context=(
                            f"Content strategy and topics for {brand}. Offering: {offering}. "
                            "You may use general content strategy best practices, but do not invent any client-specific facts or numbers.\n" + base_context
                        )
                    )
                }
            # Social Strategy
            if sec_id == "social_strategy":
                return {
                    "id": sec_id,
                    "title": "Social Strategy",
                    "blocks": generate_subhead_block(
                        "Social Strategy", "Social Strategy", brand, brand, url,
                        context=(
                            f"Social content and campaign strategy for {brand}. Offering: {offering}. "
                            "You may use general social strategy best practices, but do not invent any client-specific facts or numbers.\n" + base_context
                        )
                    )
                }
            # Engagement Framework
            if sec_id == "engagement_framework":
                return {
                    "id": sec_id,
                    "title": "Engagement Framework",
                    "blocks": generate_checklist_block(
                        "Engagement Framework", "Engagement Framework Checklist", brand, brand, url,
                        context=(
                            f"Offering: {offering}. Target markets: {target_markets}. "
                            "You may use general engagement best practices, but do not invent any client-specific facts or numbers.\n" + base_context
                        )
                    )
                }
            # References
            if sec_id == "references":
                return {
                    "id": sec_id,
                    "title": "References",
                    "blocks": generate_list_block(
                        "References", "References", brand, brand, url,
                        context=(
                            f"Offering: {offering}. Competitors: {competitors}. "
                            "You may use general reference list best practices, but do not invent any client-specific facts or numbers.\n" + base_context
                        )
                    )
                }
            # Engagement Index
            if sec_id == "engagement_index":
                return {
                    "id": sec_id,
                    "title": "Engagement Index",
                    "blocks": generate_table_block(
                        "Engagement Index", "Engagement Index Table", brand, brand, url, ["Metric", "Score", "Notes"],
                        context=(
                            f"Offering: {offering}. Target markets: {target_markets}. "
                            "You may use general engagement index best practices, but do not invent any client-specific facts or numbers.\n" + base_context
                        )
                    )
                }
        except Exception as e:
            warnings.append(f"Section {sec_id} failed: {e}")
            return None
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_sec = {executor.submit(generate_section, sec_id): sec_id for sec_id in required_sections}
        for future in concurrent.futures.as_completed(future_to_sec):
            section = future.result()
            if section and section.get("blocks"):
                kit["document"]["sections"].append(section)

    if warnings:
        kit["warnings"] = warnings
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
        # Input validation: check for required fields

        # Only require brand_name and brand_url
        required_fields = ["brand_name", "brand_url"]
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({
                "error": "Missing required fields.",
                "missing_fields": missing_fields
            }), 400

        # Set optional fields to 'Not provided' if missing or empty
        for opt_field in ["offering", "target_markets", "competitors", "additional_details"]:
            if not data.get(opt_field):
                data[opt_field] = "Not provided"

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
        from agent_services.audit_docx import audit_to_docx
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
