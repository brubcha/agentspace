import os
from dotenv import load_dotenv
import openai

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

    for sec_id in required_sections:
        if sec_id == "engagement_index":
            continue
        user_blocks = []
        # Compose a prompt for OpenAI based on section and user data
        section_title = sec_id.replace('_', ' ').title()
        prompt = f"Generate the '{section_title}' section for a marketing kit.\n"
        prompt += f"Request Type: {request_type}\n"
        prompt += f"Client Name: {client_name}\n"
        prompt += f"Brand: {brand_name}\n"
        prompt += f"Website: {brand_url}\n"
        prompt += f"Offering: {offering}\n"
        prompt += f"Target Markets: {target_markets}\n"
        prompt += f"Competitors: {competitors}\n"
        if website_content:
            prompt += f"Website Content: {website_content[:1000]}\n"  # Limit to 1000 chars for prompt size
        if brand_story:
            prompt += f"Brand Story: {brand_story[:500]}\n"  # Limit to 500 chars
        if additional_details:
            prompt += f"Additional Details: {additional_details[:1000]}\n"
        if file_contents:
            prompt += f"Attached Files: {' | '.join(file_contents)[:2000]}\n"  # Limit total file content for prompt size
        prompt += f"Section: {section_title}\n"
        prompt += ("\nIMPORTANT: For this section, use specific examples, data, and actionable recommendations relevant to the client's industry and context. Avoid generic or vague language. Every paragraph should reference the client or their market context. If you cannot provide a concrete example or recommendation, leave a [REVIEW] tag for human review.\n")
        # Special handling for checklists: always mark as checked
        if 'checklist' in sec_id or 'post_types' in sec_id or 'production' in sec_id:
            prompt += ("\nIf you generate a Checklist block for this section, set 'checked: true' for all items so they display as green checks in the output doc.\n")
        # Add a few-shot example from the markdown if available
        md_key = sec_id.lower().replace('&', 'and').replace(' ', '_').replace('-', '_')
        if md_key in md_sections:
            prompt += f"\nExample Section Copy (for reference, do not copy verbatim):\n{md_sections[md_key][:1200]}\n"
        # Add rubric criteria for this section
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
            "Each block should be an object with a 'type' field and the appropriate fields for that type. "
            "Supported block types include: "
            "- Paragraph: {type: 'Paragraph', text: string} "
            "- Bullets: {type: 'Bullets', items: [string]} "
            "- Table: {type: 'Table', title: string, columns: [string], rows: [[string]]} "
            "- Subhead: {type: 'Subhead', text: string} "
            "- Callout: {type: 'Callout', variant: 'info'|'warning'|'success', text: string} "
            "- ArchetypeCard: {type: 'ArchetypeCard', variant: 'primary'|'secondary', label: string, text: string} "
            "- Checklist: {type: 'Checklist', items: [{text: string, checked: boolean}]} "
            "- NumberedList: {type: 'NumberedList', items: [{text: string}]} "
            "For example: "
            "[{\"type\": \"Paragraph\", \"text\": \"...\"}], "
            "[{\"type\": \"Bullets\", \"items\": [\"...\", \"...\"]}], "
            "[{\"type\": \"Table\", \"title\": \"...\", \"columns\": [\"...\"], \"rows\": [[\"...\"]]}], "
            "[{\"type\": \"Callout\", \"variant\": \"info\", \"text\": \"Important note...\"}], "
            "[{\"type\": \"ArchetypeCard\", \"variant\": \"primary\", \"label\": \"Primary Archetype\", \"text\": \"Description...\"}], "
            "[{\"type\": \"Checklist\", \"items\": [{\"text\": \"Item 1\", \"checked\": true}, {\"text\": \"Item 2\", \"checked\": false}]}], "
            "[{\"type\": \"NumberedList\", \"items\": [{\"text\": \"Step 1\"}, {\"text\": \"Step 2\"}]}] "
            "Use the example copy as a guide for structure. "
            "Do not include any explanation or prose outside the JSON."
        )


        # DEBUG: Print the prompt to verify file content is included
        print("\n--- AI PROMPT START ---\n" + prompt + "\n--- AI PROMPT END ---\n")
        try:
            ai_response = call_openai(prompt, max_tokens=1024)
            import json as _json
            user_blocks = _json.loads(ai_response)
        except Exception as e:
            user_blocks = [
                {"type": "Paragraph", "text": f"[AI generation failed: {e}]"}
            ]

        # Validation: Check for generic content and missing richness elements
        def is_generic(text):
            generic_phrases = [
                "in today's world", "businesses should", "it is important to", "companies can benefit", "in conclusion", "overall", "as a result", "the following", "this section", "the company", "organization should", "industry leaders", "market trends", "key takeaway", "best practices"
            ]
            return any(phrase in text.lower() for phrase in generic_phrases)

        def has_actionable(text):
            actionable_phrases = ["should", "recommend", "next step", "action", "implement", "consider", "strategy", "plan", "suggest"]
            return any(phrase in text.lower() for phrase in actionable_phrases)

        def has_example(text):
            return "for example" in text.lower() or "such as" in text.lower() or "e.g." in text.lower()

        validated_blocks = []
        for block in user_blocks:
            if block.get("type") == "Paragraph":
                text = block.get("text", "")
                if is_generic(text) or not has_actionable(text) or not has_example(text):
                    block["text"] = f"[REVIEW] {text}"
            validated_blocks.append(block)

        kit["document"]["sections"].append({
            "id": sec_id,
            "title": example_sections.get(sec_id, {}).get("title", sec_id.title()),
            "blocks": validated_blocks
        })

    # Always append Engagement Index section from example
    engagement_index_section = example_sections.get("engagement_index")
    if engagement_index_section:
        kit["document"]["sections"].append(engagement_index_section)

    # Always append Engagement Index section from example
    engagement_index_section = example_sections.get("engagement_index")
    if engagement_index_section:
        kit["document"]["sections"].append(engagement_index_section)

    return kit
# marketing_agent.py
# Python microservice for Marketing Agent using Microsoft Agent Framework

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from kit_templates import load_example_kit

app = Flask(__name__)
CORS(app)



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
        return jsonify(kit)
    except Exception as e:
        print(f"[ERROR] Exception in /agent/marketing-kit: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=7000, debug=True)
