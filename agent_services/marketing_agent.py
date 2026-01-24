from agent_services.kit_templates import load_example_kit


import sys
import os
import openai
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- Structured Logging Setup ---
LOG_PATH = os.path.join(os.path.dirname(__file__), 'agent_trace.log')
logger = logging.getLogger("agent_services")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_PATH, maxBytes=2*1024*1024, backupCount=3)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)

import re
class RedactSecretsFilter(logging.Filter):
    def __init__(self):
        super().__init__()
        self.patterns = [
            re.escape(os.environ.get('SECRET', 'SECRET1234')),
            re.escape(os.environ.get('BRAND_NAME', 'SECRET1234')),
            re.escape(os.environ.get('BRAND_URL', 'SECRET1234')),
            r'SECRET[0-9A-Za-z]*',
        ]
        self.patterns = [p for p in self.patterns if p]
    def filter(self, record):
        msg = record.getMessage()
        for pat in self.patterns:
            msg = re.sub(pat, '[REDACTED]', msg)
        record.msg = msg
        return True

# Add the filter to all handlers of the root logger, agent_services logger, Flask, and Werkzeug loggers
for log_name in (None, "agent_services", "flask.app", "werkzeug"):
    log = logging.getLogger(log_name) if log_name else logging.getLogger()
    for h in log.handlers:
        h.addFilter(RedactSecretsFilter())

def redact_secrets(s):
    # For any direct string redaction
    patterns = [
        re.escape(os.environ.get('SECRET', 'SECRET1234')),
        re.escape(os.environ.get('BRAND_NAME', 'SECRET1234')),
        re.escape(os.environ.get('BRAND_URL', 'SECRET1234')),
        r'SECRET[0-9A-Za-z]*',
    ]
    for pat in patterns:
        s = re.sub(pat, '[REDACTED]', s)
    return s


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

import re
class RedactSecretsFilter(logging.Filter):
    def __init__(self):
        super().__init__()
        self.patterns = [
            re.escape(os.environ.get('SECRET', 'SECRET1234')),
            re.escape(os.environ.get('BRAND_NAME', 'SECRET1234')),
            re.escape(os.environ.get('BRAND_URL', 'SECRET1234')),
            r'SECRET[0-9A-Za-z]*',
        ]
        self.patterns = [p for p in self.patterns if p]
    def filter(self, record):
        msg = record.getMessage()
        for pat in self.patterns:
            msg = re.sub(pat, '[REDACTED]', msg)
        record.msg = msg
        return True


# Add the filter to all handlers of the root logger, agent_services logger, Flask, and Werkzeug loggers
for log_name in (None, "agent_services", "flask.app", "werkzeug"):
    log = logging.getLogger(log_name) if log_name else logging.getLogger()
    for h in log.handlers:
        h.addFilter(RedactSecretsFilter())


def redact_secrets(s):
    # For any direct string redaction
    patterns = [
        re.escape(os.environ.get('SECRET', 'SECRET1234')),
        re.escape(os.environ.get('BRAND_NAME', 'SECRET1234')),
        re.escape(os.environ.get('BRAND_URL', 'SECRET1234')),
        r'SECRET[0-9A-Za-z]*',
    ]
    for pat in patterns:
        s = re.sub(pat, '[REDACTED]', s)
    return s

logger.info(redact_secrets('{"event": "startup", "file": "%s", "app_id": %d}' % (__file__, id(app))))




# --- Ensure endpoint is at the end of the file, not indented, and unique ---
logger.info(redact_secrets('{"event": "register_endpoint", "endpoint": "/agent/test-audit-docx", "app_id": %d}' % id(app)))
from agent_services.audit_docx import audit_to_docx

@app.route('/agent/test-audit-docx', methods=['POST'])
def test_audit_docx_final() -> 'Response':
    """
    Endpoint to audit the generated marketing kit and return a DOCX report.
    Accepts POST requests with kit data.
    """
    logger.info(redact_secrets('{"event": "endpoint_call", "endpoint": "/agent/test-audit-docx", "app_id": %d}' % id(app)))
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
        logger.error(redact_secrets('{"event": "error", "endpoint": "/agent/test-audit-docx", "error": "%s"}' % str(e).replace('"', "'")))
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


    def generate_section(sec_id, sec_title):
        try:
            brand = data.get("brand_name", "[FILL]")
            url = data.get("brand_url", "[FILL]")
            offering = data.get("offering", "[FILL]")
            target_markets = data.get("target_markets", "[FILL]")
            competitors = data.get("competitors", "[FILL]")
            context_parts = []
            if website_content:
                context_parts.append(f"Website Content: {website_content}")
            if file_contents:
                context_parts.append(f"Attached Files: {' | '.join(file_contents)}")
            base_context = "\n".join(context_parts)

            # Map each section to the appropriate block generator(s)
            if sec_id == "executive_summary_overview_purpose":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_subhead_block(
                        sec_title, sec_title, brand, brand, url,
                        context=(f"Purpose and use of the kit for {brand}. Offering: {offering}. Target markets: {target_markets}.\n" + base_context)
                    )
                }
            if sec_id == "brand_framework_goal":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_table_block(
                        sec_title, "Brand Framework Table", brand, brand, url, ["Attribute", "Description", "Example"],
                        context=(f"Brand purpose, promise, personality, values, voice, positioning for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "audience_archetypes":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_archetype_block(
                        sec_title, "Audience Archetype", brand, brand, url,
                        context=(f"Audience archetypes for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "key_messaging":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_table_block(
                        sec_title, "Key Messaging Table", brand, brand, url, ["Message Pillar", "Supporting Points", "Proof/Example"],
                        context=(f"Key messaging pillars for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "product_service_overview":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_subhead_block(
                        sec_title, sec_title, brand, brand, url,
                        context=(f"Product/service overview for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "feature_benefit_table":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_table_block(
                        sec_title, "Feature/Benefit Table", brand, brand, url, ["Feature", "Benefit", "Proof Point"],
                        context=(f"Feature/benefit mapping for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "competitive_differentiation":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_table_block(
                        sec_title, "Competitive Differentiation Table", brand, brand, url, ["Competitor", "Differentiator", "Why It Matters"],
                        context=(f"Competitive differentiation for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "go_to_market_checklist":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_checklist_block(
                        sec_title, "Go-to-Market Checklist", brand, brand, url,
                        context=(f"Go-to-market checklist for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "sample_campaign_concepts":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_table_block(
                        sec_title, "Sample Campaign Concepts Table", brand, brand, url, ["Concept Name", "Description", "Channel(s)", "KPI/Goal"],
                        context=(f"Sample campaign concepts for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "website_content_audit_summary":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_table_block(
                        sec_title, "Website/Content Audit Summary Table", brand, brand, url, ["Page/Asset", "Strengths", "Gaps", "Recommendations"],
                        context=(f"Website/content audit summary for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "attachments_references":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_list_block(
                        sec_title, "Attachments/References", brand, brand, url,
                        context=(f"List of all files, links, or resources referenced or used in the kit for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "key_findings":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_list_block(
                        sec_title, sec_title, brand, brand, url,
                        context=(f"Key findings, opportunities, and challenges for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "market_landscape":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_subhead_block(
                        sec_title, sec_title, brand, brand, url,
                        context=(f"Market landscape for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "channel_opportunities":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_table_block(
                        sec_title, "Channel Opportunities Table", brand, brand, url, ["Channel", "Opportunity Insight", "Recommendation", "Rationale for Deprioritizing"],
                        context=(f"Channel opportunities for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "audience_personas":
                personas = []
                for i in range(3):
                    personas.extend(generate_persona_block(
                        sec_title, f"Persona {i+1}", brand, brand, url,
                        context=(f"Audience/user personas for {brand}.\n" + base_context)
                    ))
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": personas
                }
            if sec_id == "b2b_industry_targets":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_table_block(
                        sec_title, "B2B Industry Targets Table", brand, brand, url, ["Category", "Subtype", "Rationale"],
                        context=(f"B2B industry targets for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "industry_codes_data_broker_research":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_table_block(
                        sec_title, "Industry Codes Table", brand, brand, url, ["Industry", "NAICS Code", "Description"],
                        context=(f"Industry codes and data broker research for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "brand_archetypes":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_archetype_block(
                        sec_title, "Primary Archetype", brand, brand, url,
                        context=(f"Brand archetypes for {brand}.\n" + base_context)
                    ) + generate_archetype_block(
                        sec_title, "Secondary Archetype", brand, brand, url,
                        context=(f"Brand archetypes for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "brand_voice":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_subhead_block(
                        sec_title, sec_title, brand, brand, url,
                        context=(f"Brand voice for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "client_dos_donts":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_table_block(
                        sec_title, "Client Do’s & Don’ts Table", brand, brand, url, ["Do", "Example", "Don't", "Example"],
                        context=(f"Client do’s and don’ts for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "content_keyword_strategy":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_table_block(
                        sec_title, "Content & Keyword Strategy Table", brand, brand, url, ["Category", "Keyword", "Search Volume", "Intent"],
                        context=(f"Content and keyword strategy for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "social_strategy":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_subhead_block(
                        sec_title, sec_title, brand, brand, url,
                        context=(f"Social strategy for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "social_production_checklist":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_checklist_block(
                        sec_title, "Social Production Checklist", brand, brand, url,
                        context=(f"Social production checklist for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "campaign_structure":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_table_block(
                        sec_title, "Campaign Structure Table", brand, brand, url, ["Deliverable", "Count"],
                        context=(f"Campaign structure for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "landing_page_strategy":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_table_block(
                        sec_title, "Landing Page Strategy Table", brand, brand, url, ["Section", "Description"],
                        context=(f"Landing page strategy for {brand}.\n" + base_context)
                    )
                }
            if sec_id == "engagement_framework":
                return {
                    "id": sec_id,
                    "title": sec_title,
                    "blocks": generate_checklist_block(
                        sec_title, "Engagement Framework Checklist", brand, brand, url,
                        context=(f"Engagement framework for {brand}.\n" + base_context)
                    )
                }
        except Exception as e:
            warnings.append(f"Section {sec_id} failed: {e}")
            return None
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_sec = {executor.submit(generate_section, sec_id, sec_title): (sec_id, sec_title) for sec_id, sec_title in required_sections}
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

        # Redact sensitive fields before logging
        redacted_data = dict(data)
        for sensitive in ["brand_name", "brand_url"]:
            if sensitive in redacted_data:
                redacted_data[sensitive] = "[REDACTED]"
        logger.info(redact_secrets('{"event": "request_received", "endpoint": "/agent/marketing-kit", "data": %s}' % json.dumps(redacted_data).replace('"', "'")))
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
        logger.info(redact_secrets('{"event": "response_ready", "endpoint": "/agent/marketing-kit", "kit_preview": "%s"}' % json.dumps(kit)[:500].replace('"', "'")))

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
        logger.error(redact_secrets('{"event": "error", "endpoint": "/agent/marketing-kit", "error": "%s"}' % str(e).replace('"', "'")))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info(redact_secrets('{"event": "startup", "file": "%s", "app_id": %d}' % (__file__, id(app))))
    logger.info(redact_secrets('{"event": "registered_routes", "routes": %s}' % [str(rule) for rule in app.url_map.iter_rules()]))
    for rule in app.url_map.iter_rules():
        logger.info(redact_secrets('{"event": "route", "route": "%s"}' % str(rule)))
    app.run(port=7000, debug=False)
