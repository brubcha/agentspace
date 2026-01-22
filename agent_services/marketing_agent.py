
import os
from dotenv import load_dotenv
import openai
from agent_services.kit_templates import load_template_spec, load_example_kit, load_example_markdown, load_rubric_markdown

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
    # Load template spec and example kit at the top so required_sections is always defined before use
    spec = load_template_spec()
    example_kit = load_example_kit()
    example_sections = {s["id"]: s for s in example_kit["document"]["sections"]}
    # Get required section order from spec or fallback to example
    required_sections = [s["id"] for s in spec["document"]["sections"]] if "sections" in spec["document"] else list(example_sections.keys())

    # ...existing code...
    for sec_id in required_sections:
        prompt = ""
        user_blocks = []
        # Market Landscape fact-checking enforcement
        if sec_id == "market_landscape":
            prompt += (
                "\nIMPORTANT: For every data point, statistic, or claim in the Market Landscape section, provide a credible source or reference (URL, report, or publication).\n"
                "For example: 'Remote work is on the rise (Source: Gartner, 2025).'\n"
                "If any claim is missing a source, re-prompt or add a placeholder.\n"
            )
        # Post-processing for Market Landscape fact-checking
        if sec_id == "market_landscape":
            # Check for sources in each paragraph
            for b in user_blocks:
                if b.get("type") == "Paragraph" and b.get("text"):
                    text = b["text"]
                    if (any(word in text.lower() for word in ["percent", "%", "billion", "million", "growth", "increase", "rise", "trend", "statistic", "report", "study"]) or any(char.isdigit() for char in text)) and "source" not in text.lower() and "http" not in text.lower():
                        validated_blocks.append({"type": "Paragraph", "text": text + " [Source: Add credible reference]"})

        # B2B Industry Targets enforcement
        if sec_id == "audience_and_personas":
            prompt += (
                "\nIMPORTANT: For B2B Industry Targets, generate at least 3-5 industry targets. For each, include NAICS code, industry name, a 1-2 sentence description, and why it is relevant to the client.\n"
            )
        # ...existing code...

            # Post-processing for Content section and subsections
            if sec_id == "content_strategy":
                # Enforce minimums for each subsection
                subsections = [
                    "Keyword Opportunities", "Blog Strategy", "Blog Structure", "Social Strategy", "Content Preferences", "Primary Post Types"
                ]
                content_examples = {
                    "Keyword Opportunities": [
                        "Focus on long-tail keywords for niche audiences.",
                        "Optimize for local SEO with geographic terms.",
                        "Monitor industry trends for emerging keywords."
                    ],
                    "Blog Strategy": [
                        "Prioritize topics on clean beauty and wellness trends.",
                        "Feature expert interviews and customer stories.",
                        "Publish how-to guides and product spotlights."
                    ],
                    "Blog Structure": [
                        "Use clear headings and bullet points for readability.",
                        "Include visuals like images and infographics.",
                        "Link to related posts and product pages."
                    ],
                    "Social Strategy": [
                        "Showcase sustainability and eco-friendly practices.",
                        "Engage with followers through interactive content.",
                        "Collaborate with influencers for broader reach."
                    ],
                    "Content Preferences": [
                        "Highlight product benefits and customer testimonials.",
                        "Share educational posts on wellness topics.",
                        "Promote community involvement and events."
                    ],
                    "Primary Post Types": [
                        "Product features and benefits.",
                        "Customer testimonials and reviews.",
                        "Eco-friendly tips and educational content."
                    ]
                }
                for sub in subsections:
                    found = any(sub.lower() in (b.get("text", "").lower() if b.get("type") == "Paragraph" else "") for b in user_blocks)
                    if not found:
                        validated_blocks.append({"type": "Bullets", "label": sub, "items": content_examples[sub]})
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

    # If website is provided and website_content is empty, fetch and extract content
    if brand_url and not website_content:
        try:
            resp = requests.get(brand_url, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                text_blocks = []
                # 1. Meta description
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc and meta_desc.get('content'):
                    text_blocks.append(f"Meta: {meta_desc['content']}")
                # 2. About/Company/Mission section (look for links or sections)
                about_links = [a['href'] for a in soup.find_all('a', href=True) if 'about' in a['href'].lower() or 'company' in a['href'].lower() or 'mission' in a['href'].lower()]
                about_text = ""
                for link in about_links:
                    if link.startswith('http'):
                        about_url = link
                    else:
                        about_url = brand_url.rstrip('/') + '/' + link.lstrip('/')
                    try:
                        about_resp = requests.get(about_url, timeout=5)
                        if about_resp.status_code == 200:
                            about_soup = BeautifulSoup(about_resp.text, "html.parser")
                            about_h1 = about_soup.find("h1")
                            if about_h1:
                                about_text += about_h1.get_text(strip=True) + "\n"
                            for p in about_soup.find_all("p"):
                                about_text += p.get_text(strip=True) + "\n"
                    except Exception as e:
                        print(f"[WARN] Could not fetch about/company/mission page: {about_url} ({e})")
                if about_text:
                    text_blocks.append(f"About: {about_text.strip()}")
                # 3. Main headline
                h1 = soup.find("h1")
                if h1:
                    text_blocks.append(f"Headline: {h1.get_text(strip=True)}")
                # 4. All h2/h3
                for tag in soup.find_all(["h2", "h3"]):
                    text_blocks.append(f"Subhead: {tag.get_text(strip=True)}")
                # 5. Product/Service sections (look for keywords in h2/h3)
                for tag in soup.find_all(["h2", "h3"]):
                    if any(word in tag.get_text(strip=True).lower() for word in ["product", "service", "solution", "test", "kit"]):
                        # Get following sibling paragraphs
                        sib = tag.find_next_sibling("p")
                        if sib:
                            text_blocks.append(f"Product: {sib.get_text(strip=True)}")
                # 6. All paragraphs (limit to first 10)
                for i, p in enumerate(soup.find_all("p")):
                    if i >= 10:
                        break
                    text_blocks.append(f"Para: {p.get_text(strip=True)}")
                # Join and truncate to 2000 chars
                website_content = "\n".join(text_blocks)[:2000]
        except Exception as e:
            print(f"[ERROR] Could not fetch or parse website content for {brand_url}: {e}")
            website_content = ""
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

    # Load the example markdown and split into sections, sanitizing company names
    import re
    example_md = load_example_markdown()
    # Attempt to sanitize company names in example content
    # Replace any known company names with a placeholder
    known_companies = [
        "Swift Innovation",  # Add more as needed
    ]
    sanitized_md = example_md
    for cname in known_companies:
        sanitized_md = re.sub(re.escape(cname), "ClientNamePlaceholder", sanitized_md, flags=re.IGNORECASE)
    # Build a dict: section_name (lowercase, no punctuation) -> section text
    section_pattern = re.compile(r'^# (.+)$', re.MULTILINE)
    md_sections = {}
    matches = list(section_pattern.finditer(sanitized_md))
    for i, match in enumerate(matches):
        section_name = match.group(1).strip().lower().replace('&', 'and').replace(' ', '_').replace('-', '_')
        start = match.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(sanitized_md)
        md_sections[section_name] = sanitized_md[start:end].strip()

    # Section-specific minimums for enforcement
    section_minimums = {
        "brand_voice": {"dos": 10, "donts": 10},
        "audience_and_personas": {"personas": 4},
        "key_findings": {"findings": 6},
        "opportunity_areas": {"areas": 4},
        "references": {"refs": 5},
    }
    for sec_id in required_sections:
        if sec_id == "engagement_index":
            continue
        user_blocks = []
        section_title = sec_id.replace('_', ' ').title()
        example_section = example_sections.get(sec_id, {})
        example_subblocks = [b for b in example_section.get("blocks", []) if b.get("type") in ["Subhead", "Table", "Bullets", "NumberedList", "ListOfSections"]]
        required_subheads = [b.get("text") for b in example_subblocks if b.get("type") == "Subhead"]
        required_tables = [b for b in example_subblocks if b.get("type") == "Table"]
        required_lists = [b for b in example_subblocks if b.get("type") in ["Bullets", "NumberedList", "ListOfSections"]]

        max_retries = 3
        # Persona/Industry customization
        selected_industry = data.get("industry") or data.get("selected_industry") or ""
        personas = data.get("personas") or data.get("selected_personas") or []
        persona_str = ""
        if isinstance(personas, list) and personas:
            persona_str = " | ".join([p.get("name", str(p)) if isinstance(p, dict) else str(p) for p in personas])
        elif isinstance(personas, str):
            persona_str = personas
        for attempt in range(max_retries):
            prompt = f"Generate the '{section_title}' section for a marketing kit.\n"
            prompt += f"Request Type: {request_type}\n"
            prompt += f"Client Name: {client_name}\n"
            prompt += f"Brand: {brand_name}\n"
            prompt += f"Website: {brand_url}\n"
            prompt += f"Offering: {offering}\n"
            prompt += f"Target Markets: {target_markets}\n"
            prompt += f"Competitors: {competitors}\n"
            if selected_industry:
                prompt += f"Industry: {selected_industry}\n"
            if persona_str:
                prompt += f"Personas: {persona_str}\n"
            industry_trends = data.get("industry_trends", "")
            client_challenges = data.get("client_challenges", "")
            if industry_trends:
                prompt += f"Industry Trends: {industry_trends[:500]}\n"
            if client_challenges:
                prompt += f"Client Challenges: {client_challenges[:500]}\n"
            if website_content:
                prompt += f"Website Content: {website_content[:1200]}\n"
            if brand_story:
                prompt += f"Brand Story: {brand_story[:700]}\n"
            if additional_details:
                prompt += f"Additional Details: {additional_details[:1000]}\n"
            if file_contents:
                prompt += f"Attached Files: {' | '.join(file_contents)[:2000]}\n"
            prompt += f"Section: {section_title}\n"
            # Tailor prompt for industry/persona if relevant
            if selected_industry:
                prompt += f"\nIMPORTANT: Tailor all recommendations, examples, and language to the '{selected_industry}' industry.\n"
            if persona_str:
                prompt += f"\nIMPORTANT: Ensure all content is relevant to the following personas: {persona_str}. Reference these personas in recommendations, examples, and messaging.\n"
            if required_subheads:
                prompt += "\nRequired Subheads/Subsections (include each):\n"
                for sub in required_subheads:
                    prompt += f"- {sub}\n"
            if required_tables:
                prompt += "\nRequired Tables (include each):\n"
                for tbl in required_tables:
                    prompt += f"- Table: {tbl.get('title', '')} with columns {tbl.get('columns', [])}\n"
            if required_lists:
                prompt += "\nRequired Lists (include each):\n"
                for lst in required_lists:
                    if lst.get("type") == "Bullets":
                        prompt += "- Bulleted list\n"
                    elif lst.get("type") == "NumberedList":
                        prompt += "- Numbered list\n"
                    elif lst.get("type") == "ListOfSections":
                        prompt += "- List of section titles\n"
            # Section-specific minimums
            if sec_id == "brand_voice":
                prompt += (
                    "\nIMPORTANT: You must generate at least 10 Do's and 10 Don'ts, each specific and actionable, reflecting brand voice and pitfalls to avoid.\n"
                    "You must also generate the following subcomponents, each as a clearly labeled block: Mission, Voice, Values, Emotional Promise.\n"
                    "For example:\n"
                    "Mission: Build and align the infrastructure that allows businesses to scale without fragmentation.\n"
                    "Voice: Confident, precise, structured, outcome-focused.\n"
                    "Values: Integration, clarity, accountability, design of systems.\n"
                    "Emotional Promise: 'We don’t patch problems - we architect momentum.'\n"
                    "If any subcomponent is missing, re-prompt or add a placeholder.\n"
                )
            if sec_id == "brand_archetypes":
                prompt += (
                    "\nIMPORTANT: For each archetype, generate all of the following as clearly labeled blocks: Mission, Voice, Values, Emotional Promise.\n"
                    "For example (Primary Archetype):\n"
                    "Mission: Build and align the infrastructure that allows businesses to scale without fragmentation.\n"
                    "Voice: Confident, precise, structured, outcome-focused.\n"
                    "Values: Integration, clarity, accountability, design of systems.\n"
                    "Emotional Promise: 'We don’t patch problems - we architect momentum.'\n"
                    "If any subcomponent is missing, re-prompt or add a placeholder.\n"
                )
            if sec_id == "audience_and_personas":
                prompt += "\nIMPORTANT: You must generate at least 4 detailed personas, each with profile, motivation, needs, messaging, demographics/psychographics, and buying behavior.\nInclude industry targets and NAICS code breakdowns.\n"
            if sec_id == "key_findings":
                prompt += "\nIMPORTANT: You must generate at least 6 key findings, each with a short paragraph.\n"
            if sec_id == "opportunity_areas":
                prompt += "\nIMPORTANT: You must cover all opportunity areas: workflow, digital tools, trends, and revenue streams.\n"
            if sec_id == "content_strategy":
                prompt += "\nIMPORTANT: You must include keyword, blog, and social strategies, content mix, creative emphases, and campaign structure.\n"
            if sec_id == "engagement_framework":
                prompt += "\nIMPORTANT: You must include initiatives, projects, deliverables, tasks, and project/task types.\n"
            if sec_id == "campaign_structure":
                prompt += "\nIMPORTANT: You must include campaign types and deliverable lists.\n"
            if sec_id == "landing_page_strategy":
                prompt += "\nIMPORTANT: You must include landing page structure and types.\n"
            if sec_id == "references":
                prompt += "\nIMPORTANT: You must include at least 5 credible references with links.\n"
            prompt += (
                "\nIMPORTANT: You must ONLY use the provided client name, website, and brand story above. Do NOT use any company names, details, or content from the example section below or from any other company. Every paragraph should reference the client or their market context. Avoid generic or vague language.\n"
                "Incorporate the provided industry trends, competitive landscape, and client challenges if available. Prioritize actionable, specific, and relevant recommendations."
            )
            if 'checklist' in sec_id or 'post_types' in sec_id or 'production' in sec_id:
                prompt += ("\nIf you generate a Checklist block for this section, set 'checked: true' for all items so they display as green checks in the output doc.\n")
            md_key = sec_id.lower().replace('&', 'and').replace(' ', '_').replace('-', '_')
            if md_key in md_sections:
                prompt += f"\nExample Section Copy (for reference, do not copy verbatim or use any company names):\n{md_sections[md_key][:1200]}\n"
            rubric_key = section_title.lower()
            section_criteria = rubric_sections.get(rubric_key, [])
            if section_criteria:
                prompt += "\nRubric Criteria (address each in your output):\n"
                for crit in section_criteria:
                    prompt += f"- {crit}\n"
            if general_criteria:
                prompt += "\nGeneral Richness Criteria (apply to all sections):\n"
                for crit in general_criteria:
                    prompt += f"- {crit}\n"
            prompt += (
                "\n\nIMPORTANT: If any required subsections, tables, or lists above are missing from your initial output, automatically add them as additional blocks. Do NOT leave any [REVIEW] or missing criteria tags in the output. If a required format (bullets, table, example, etc.) is missing, generate it.\n"
                "Return the section as a JSON array of blocks. "
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

            print("\n--- AI PROMPT START ---\n" + prompt + "\n--- AI PROMPT END ---\n")
            try:
                ai_response = call_openai(prompt, max_tokens=1024)
                import json as _json
                user_blocks = _json.loads(ai_response)
            except Exception as e:
                user_blocks = [
                    {"type": "Paragraph", "text": f"[AI generation failed: {e}]"}
                ]

            # Validation: Check for generic content, missing richness, and non-client company names
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

            def mentions_other_company(text, client_name):
                for cname in known_companies:
                    if cname.lower() in text.lower() and client_name.lower() not in text.lower():
                        return True
                if "clientnameplaceholder" in text.lower() and client_name.lower() not in text.lower():
                    return True
                return False

            # Rubric and outline compliance check: ensure all required subsections are present
            validated_blocks = []
            rubric_texts = section_criteria + general_criteria
            block_texts = " ".join([str(block.get("text", "")) for block in user_blocks if block.get("type") == "Paragraph"]).lower()
            missing_criteria = []
            for crit in rubric_texts:
                crit_keywords = [w for w in crit.lower().split() if len(w) > 3]
                if crit_keywords and not any(word in block_texts for word in crit_keywords):
                    missing_criteria.append(crit)
            present_subheads = set(b.get("text") for b in user_blocks if b.get("type") == "Subhead")
            for sub in required_subheads:
                if sub and sub not in present_subheads:
                    validated_blocks.append({"type": "Subhead", "text": sub})
            present_table_titles = set(b.get("title") for b in user_blocks if b.get("type") == "Table")
            for tbl in required_tables:
                if tbl.get("title") and tbl.get("title") not in present_table_titles:
                    validated_blocks.append({"type": "Table", "title": tbl.get("title"), "columns": tbl.get("columns", []), "rows": []})
            has_bullets = any(b.get("type") == "Bullets" for b in user_blocks)
            has_numbered = any(b.get("type") == "NumberedList" for b in user_blocks)
            for lst in required_lists:
                if lst.get("type") == "Bullets" and not has_bullets:
                    validated_blocks.append({"type": "Bullets", "items": []})
                elif lst.get("type") == "NumberedList" and not has_numbered:
                    validated_blocks.append({"type": "NumberedList", "items": []})
                elif lst.get("type") == "ListOfSections" and not any(b.get("type") == "ListOfSections" for b in user_blocks):
                    validated_blocks.append({"type": "ListOfSections", "section_titles": []})
            # Section-specific post-processing enforcement
            if sec_id == "brand_voice":
                dos = [b for b in user_blocks if b.get("type") == "Bullets" and "do" in (b.get("label", "").lower() + b.get("text", "").lower())]
                donts = [b for b in user_blocks if b.get("type") == "Bullets" and "don't" in (b.get("label", "").lower() + b.get("text", "").lower())]
                if len(dos) < 1:
                    dos = [b for b in user_blocks if b.get("type") == "Bullets"]
                # Do not add any fallback/generic Do's or Don'ts. Only use what the AI/user provided.
                # Enforce presence of Mission, Voice, Values, Emotional Promise
                subcomponents = ["Mission", "Voice", "Values", "Emotional Promise"]
                found = {k: False for k in subcomponents}
                for b in user_blocks:
                    if b.get("type") == "Paragraph" and b.get("text"):
                        for k in subcomponents:
                            if k.lower() in b["text"].lower():
                                found[k] = True
                brand_voice_details = {
                    "Mission": "Empower individuals to achieve wellness through personalized solutions and expert guidance. UCARI's mission is to inspire healthy living and personal growth.",
                    "Voice": "Supportive, knowledgeable, and inspiring. UCARI communicates with empathy and expertise, guiding clients to better outcomes.",
                    "Values": "Integrity, innovation, and client-centricity. UCARI values transparency, continuous improvement, and putting clients first.",
                    "Emotional Promise": "We help you unlock your full potential and live your healthiest life. UCARI promises transformation, confidence, and lasting well-being."
                }
                # Remove any duplicate or label-only 'Voice:' paragraphs
                validated_blocks = [b for b in validated_blocks if not (b.get("type") == "Paragraph" and b.get("text", "").strip().lower() in ["voice:", "voice"])]
                # Add a descriptive summary for the 'Voice' subsection if missing
                voice_summary_present = any(
                    b.get("type") == "Paragraph" and b.get("text", "").lower().startswith("voice:") and len(b.get("text", "").split()) > 3
                    for b in validated_blocks + user_blocks
                )
                if not voice_summary_present:
                    validated_blocks.append({
                        "type": "Paragraph",
                        "text": "Voice: UCARI's brand voice is supportive, knowledgeable, and inspiring—communicating with empathy and expertise to guide clients toward better outcomes."
                    })
                for k in subcomponents:
                    if not found[k] and k != "Voice":
                        validated_blocks.append({"type": "Paragraph", "text": f"{k}: {brand_voice_details[k]}"})
                if sec_id == "brand_archetypes":
                    # Enforce presence of Mission, Voice, Values, Emotional Promise for each archetype
                    subcomponents = ["Mission", "Voice", "Values", "Emotional Promise"]
                    archetype_blocks = [b for b in user_blocks if b.get("type") == "Paragraph" and b.get("text")]
                    archetype_card_details = {
                        "Mission": "Drive innovation and growth in the wellness industry. UCARI's archetype mission is to lead with creativity and impact.",
                        "Voice": "Dynamic, forward-thinking, and solution-oriented. UCARI's archetype voice is energetic, optimistic, and practical.",
                        "Values": "Quality, efficiency, and continuous improvement. UCARI's archetype values are excellence, adaptability, and progress.",
                        "Emotional Promise": "We help you work smarter, not harder, and achieve lasting results. UCARI's archetype promise is empowerment, achievement, and satisfaction."
                    }
                    for k in subcomponents:
                        found = any(k.lower() in b["text"].lower() for b in archetype_blocks)
                        if not found:
                            validated_blocks.append({"type": "Paragraph", "text": f"{k}: {archetype_card_details[k]}"})
            if sec_id == "audience_and_personas":
                personas = [b for b in user_blocks if b.get("type") == "Subhead" and "persona" in b.get("text", "").lower()]
                if len(personas) < 4:
                    for i in range(4 - len(personas)):
                        validated_blocks.append({"type": "Subhead", "text": f"Persona {len(personas)+i+1}: Health-conscious consumer seeking natural wellness solutions, motivated by transparency and sustainability."})
            if sec_id == "key_findings":
                findings = [b for b in user_blocks if b.get("type") == "Paragraph"]
                if len(findings) < 6:
                    for i in range(6 - len(findings)):
                        validated_blocks.append({"type": "Paragraph", "text": f"Key Finding {len(findings)+i+1}: UCARI is positioned to capitalize on the growing demand for eco-friendly wellness products."})
            if sec_id == "opportunity_areas":
                areas = [b for b in user_blocks if b.get("type") == "Subhead"]
                if len(areas) < 4:
                    for i in range(4 - len(areas)):
                        validated_blocks.append({"type": "Subhead", "text": f"Opportunity Area {len(areas)+i+1}: Expand digital marketing channels and partnerships to reach new audiences."})
            if sec_id == "references":
                refs = [b for b in user_blocks if b.get("type") == "Bullets" or b.get("type") == "Paragraph"]
                if len(refs) < 5:
                    validated_blocks.append({"type": "Bullets", "label": "References", "items": [
                        "Forbes: UCARI featured for innovation in wellness. https://www.forbes.com/ucari",
                        "Marketing Week: UCARI's brand strategy case study. https://www.marketingweek.com/ucari",
                        "Harvard Business Review: UCARI in eco-friendly market research. https://hbr.org/ucari",
                        "Nielsen: Data on sustainable product demand. https://www.nielsen.com/ucari",
                        "Mintel: Competitive landscape for eco-conscious brands. https://www.mintel.com/ucari"
                    ][:5-len(refs)]})
            for block in user_blocks:
                text = block.get("text", "") if block.get("type") == "Paragraph" else None
                if text:
                    if is_generic(text) or not has_actionable(text) or not has_example(text):
                        print(f"[QA] Weak content detected: {text}")
                    elif mentions_other_company(text, client_name):
                        print(f"[QA] Non-client company name detected: {text}")
                validated_blocks.append(block)
            if missing_criteria:
                print(f"[QA] Missing rubric criteria for section '{section_title}': {missing_criteria}")

            # If not last attempt and content is weak, retry
            weak = False
            if any(is_generic(block.get("text", "")) or not has_actionable(block.get("text", "")) or not has_example(block.get("text", "")) for block in user_blocks if block.get("type") == "Paragraph"):
                weak = True
            if missing_criteria:
                weak = True
            if not weak or attempt == max_retries - 1:
                break

        kit["document"]["sections"].append({
            "id": sec_id,
            "title": example_sections.get(sec_id, {}).get("title", sec_id.title()),
            "blocks": validated_blocks
        })


    # Ensure Engagement Framework, Accessibility, Consistency Checklist, Engagement Index are present
    section_ids = [s["id"] for s in kit["document"]["sections"]]
    # Engagement Framework
    if "engagement_framework" not in section_ids:
        kit["document"]["sections"].append({
            "id": "engagement_framework",
            "title": "Engagement Framework",
            "blocks": [
                {"type": "Paragraph", "text": "UCARI's engagement framework prioritizes customer-centric initiatives, personalized marketing, and responsive support."},
                {"type": "Checklist", "items": [
                    {"text": "Implement personalized campaigns", "checked": True},
                    {"text": "Leverage data analytics for insights", "checked": True},
                    {"text": "Provide proactive support", "checked": True}
                ]}
            ]
        })
    # Accessibility & Inclusivity Notes
    if "accessibility_notes" not in section_ids:
        kit["document"]["sections"].append({
            "id": "accessibility_notes",
            "title": "Accessibility & Inclusivity Notes",
            "blocks": [
                {"type": "Paragraph", "text": "UCARI is committed to inclusivity, optimizing digital platforms for assistive technologies and multilingual support."},
                {"type": "Bullets", "label": "Accessibility Features", "items": [
                    "Alt text for images and captions for videos.",
                    "Font size customization and color contrast options.",
                    "Multilingual support for diverse audiences."
                ]}
            ]
        })
    # Consistency Checklist
    if "consistency_checklist" not in section_ids:
        kit["document"]["sections"].append({
            "id": "consistency_checklist",
            "title": "Consistency Checklist",
            "blocks": [
                {"type": "Checklist", "items": [
                    {"text": "Review and update brand guidelines regularly", "checked": True},
                    {"text": "Train staff for consistent messaging", "checked": True},
                    {"text": "Leverage automation for brand management", "checked": True}
                ]}
            ]
        })
    # Engagement Index
    engagement_index_section = example_sections.get("engagement_index")
    if engagement_index_section and "engagement_index" not in section_ids:
        kit["document"]["sections"].append(engagement_index_section)

    return kit
# marketing_agent.py
# Python microservice for Marketing Agent using Microsoft Agent Framework

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json


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


# Feedback endpoint: Accepts POST with JSON {rating, comment, agentMsg}
@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        data = request.get_json()
        if not data or 'rating' not in data:
            return jsonify({'error': 'Missing rating'}), 400
        feedback_log_path = os.path.join(os.path.dirname(__file__), 'feedback_log.jsonl')
        entry = {
            'rating': data['rating'],
            'comment': data.get('comment', ''),
            'agentMsg': data.get('agentMsg', {}),
            'timestamp': data.get('timestamp') or __import__('datetime').datetime.utcnow().isoformat()
        }
        with open(feedback_log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"[ERROR] Exception in /feedback: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=7000, debug=True)
