# Website Scraper Subagent
def website_scraper_subagent(brand_url, max_length=2000):
    """
    Fetches and summarizes content from the provided client website.
    Returns a string summary for use in prompt construction or downstream subagents.
    """
    import requests
    from bs4 import BeautifulSoup
    try:
        resp = requests.get(brand_url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Extract visible text from the main body
        texts = soup.stripped_strings
        content = ' '.join(texts)
        # Truncate to max_length characters
        summary = content[:max_length]
        return summary
    except Exception as e:
        return f"[Website scrape failed: {e}]"
# Fallback/Retry Subagent
def fallback_retry_block(generator_func, *args, max_retries=2, **kwargs):
    """
    Attempts to call a subagent generator function with retries on failure.
    """
    last_result = None
    for attempt in range(max_retries):
        result = generator_func(*args, **kwargs)
        # If no error in result, return immediately
        if result and not any('error' in block for block in result):
            return result
        last_result = result
    # If still failing after retries, append a review note
    for block in last_result or []:
        if 'error' in block:
            block['review'] = '[Fallback/Retry] Block failed after retries.'
    return last_result or []
# QA/Validation Subagent
def validate_section_blocks(section_title, blocks, client_name, brand_name, brand_url, rubric_criteria=None, general_criteria=None):
    """
    Validates section blocks for richness, specificity, and rubric compliance using a focused prompt.
    """
    import json as _json
    prompt = f"""
You are a marketing kit QA validator. Review the following section blocks for the '{section_title}' section.
Client Name: {client_name}
Brand: {brand_name}
Website: {brand_url}
Blocks: {_json.dumps(blocks)}
"""
    if rubric_criteria:
        prompt += f"Rubric Criteria: {rubric_criteria}\n"
    if general_criteria:
        prompt += f"General Richness Criteria: {general_criteria}\n"
    prompt += (
        "IMPORTANT: For each block, if it is generic, lacks actionable advice, or does not reference the client, add a field 'review' with a reason. Return the validated blocks as a JSON array."
    )
    try:
        ai_response = call_openai_subagent(prompt, max_tokens=1024)
        validated_blocks = _json.loads(ai_response)
        return validated_blocks
    except Exception as e:
        # Fallback: mark all blocks for review
        for block in blocks:
            block['review'] = f"[QA validation failed: {e}]"
        return blocks
# Checklist Generator Subagent
def generate_checklist_block(section_title, checklist_title, client_name, brand_name, brand_url, context=None):
    """
    Generates a checklist block for a given section using a focused prompt.
    """
    prompt = f"""
Generate a checklist titled '{checklist_title}' for the '{section_title}' section of a marketing kit.
Client Name: {client_name}
Brand: {brand_name}
Website: {brand_url}
"""
    if context:
        prompt += f"Context: {context}\n"
    prompt += (
        "IMPORTANT: Make the checklist actionable and specific to the client. Return a JSON block: {\"type\": \"Checklist\", \"title\": \"...\", \"items\": [ ... ]} only."
    )
    try:
        import json as _json
        ai_response = call_openai_subagent(prompt)
        block = _json.loads(ai_response)
        if isinstance(block, list):
            return block
        else:
            return [block]
    except Exception as e:
        return [
            {"type": "Checklist", "title": checklist_title, "items": [], "error": f"[AI generation failed: {e}]"}
        ]
# Opportunity Card Generator Subagent
def generate_opportunity_card_block(section_title, card_title, client_name, brand_name, brand_url, context=None):
    """
    Generates an opportunity card block for a given section using a focused prompt.
    """
    prompt = f"""
Generate an opportunity card titled '{card_title}' for the '{section_title}' section of a marketing kit.
Client Name: {client_name}
Brand: {brand_name}
Website: {brand_url}
"""
    if context:
        prompt += f"Context: {context}\n"
    prompt += (
        "IMPORTANT: Make the opportunity card vivid, actionable, and specific to the client. Return a JSON block: {\"type\": \"OpportunityCard\", \"title\": \"...\", \"description\": \"...\", \"actions\": [ ... ]} only."
    )
    try:
        import json as _json
        ai_response = call_openai_subagent(prompt)
        block = _json.loads(ai_response)
        if isinstance(block, list):
            return block
        else:
            return [block]
    except Exception as e:
        return [
            {"type": "OpportunityCard", "title": card_title, "description": "", "actions": [], "error": f"[AI generation failed: {e}]"}
        ]
# Archetype Generator Subagent
def generate_archetype_block(section_title, archetype_title, client_name, brand_name, brand_url, context=None):
    """
    Generates a brand archetype block for a given section using a focused prompt.
    """
    prompt = f"""
Generate a brand archetype card titled '{archetype_title}' for the '{section_title}' section of a marketing kit.
Client Name: {client_name}
Brand: {brand_name}
Website: {brand_url}
"""
    if context:
        prompt += f"Context: {context}\n"
    prompt += (
        "IMPORTANT: Make the archetype vivid, actionable, and specific to the client. Return a JSON block: {\"type\": \"Archetype\", \"title\": \"...\", \"description\": \"...\", \"attributes\": { ... }} only."
    )
    try:
        import json as _json
        ai_response = call_openai_subagent(prompt)
        block = _json.loads(ai_response)
        if isinstance(block, list):
            return block
        else:
            return [block]
    except Exception as e:
        return [
            {"type": "Archetype", "title": archetype_title, "description": "", "attributes": {}, "error": f"[AI generation failed: {e}]"}
        ]
# Persona Generator Subagent
def generate_persona_block(section_title, persona_title, client_name, brand_name, brand_url, context=None):
    """
    Generates a persona block for a given section using a focused prompt.
    """
    prompt = f"""
Generate a persona card titled '{persona_title}' for the '{section_title}' section of a marketing kit.
Client Name: {client_name}
Brand: {brand_name}
Website: {brand_url}
"""
    if context:
        prompt += f"Context: {context}\n"
    prompt += (
        "IMPORTANT: Make the persona vivid, actionable, and specific to the client. Return a JSON block: {\"type\": \"Persona\", \"title\": \"...\", \"description\": \"...\", \"attributes\": { ... }} only."
    )
    try:
        import json as _json
        ai_response = call_openai_subagent(prompt)
        block = _json.loads(ai_response)
        if isinstance(block, list):
            return block
        else:
            return [block]
    except Exception as e:
        return [
            {"type": "Persona", "title": persona_title, "description": "", "attributes": {}, "error": f"[AI generation failed: {e}]"}
        ]
# List Generator Subagent
def generate_list_block(section_title, list_title, client_name, brand_name, brand_url, context=None):
    """
    Generates a list block for a given section using a focused prompt.
    """
    prompt = f"""
Generate a bullet list titled '{list_title}' for the '{section_title}' section of a marketing kit.
Client Name: {client_name}
Brand: {brand_name}
Website: {brand_url}
"""
    if context:
        prompt += f"Context: {context}\n"
    prompt += (
        "IMPORTANT: Make the list actionable and specific to the client. Return a JSON block: {\"type\": \"Bullets\", \"title\": \"...\", \"items\": [ ... ]} only."
    )
    try:
        import json as _json
        ai_response = call_openai_subagent(prompt)
        block = _json.loads(ai_response)
        if isinstance(block, list):
            return block
        else:
            return [block]
    except Exception as e:
        return [
            {"type": "Bullets", "title": list_title, "items": [], "error": f"[AI generation failed: {e}]"}
        ]
# Table Generator Subagent
def generate_table_block(section_title, table_title, client_name, brand_name, brand_url, columns, context=None):
    """
    Generates a table block for a given section using a focused prompt.
    """
    prompt = f"""
Generate a table titled '{table_title}' for the '{section_title}' section of a marketing kit.
Client Name: {client_name}
Brand: {brand_name}
Website: {brand_url}
Columns: {', '.join(columns)}
"""
    if context:
        prompt += f"Context: {context}\n"
    prompt += (
        "IMPORTANT: Make the table actionable and specific to the client. Return a JSON block: {\"type\": \"Table\", \"title\": \"...\", \"columns\": [...], \"rows\": [[...], ...]} only."
    )
    try:
        import json as _json
        ai_response = call_openai_subagent(prompt)
        block = _json.loads(ai_response)
        if isinstance(block, list):
            return block
        else:
            return [block]
    except Exception as e:
        return [
            {"type": "Table", "title": table_title, "columns": columns, "rows": [], "error": f"[AI generation failed: {e}]"}
        ]
import os
from dotenv import load_dotenv
import openai

def call_openai_subagent(prompt, max_tokens=512, temperature=0.7, model="gpt-3.5-turbo"):
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
    return response.choices[0].message.content.strip()

def generate_subhead_block(section_title, subhead, client_name, brand_name, brand_url, context=None):
    """
    Generates a narrative block for a given subhead using a focused prompt.
    """
    prompt = f"""
Generate the '{subhead}' subsection for the '{section_title}' section of a marketing kit.
Client Name: {client_name}
Brand: {brand_name}
Website: {brand_url}
"""
    if context:
        prompt += f"Context: {context}\n"
    prompt += (
        "IMPORTANT: Be vivid, actionable, and specific to the client. Do not use generic content. Return a JSON block: {\"type\": \"Subhead\", \"text\": \"...\"} followed by a {\"type\": \"Paragraph\", \"text\": \"...\"}."
    )
    try:
        import json as _json
        import re
        ai_response = call_openai_subagent(prompt)
        # Try to extract all JSON objects/arrays from the response robustly
        json_blocks = []
        # Find all JSON objects or arrays in the response
        matches = re.findall(r'(\{[^\{\}]*\}|\[[^\[\]]*\])', ai_response, re.DOTALL)
        for match in matches:
            try:
                parsed = _json.loads(match)
                if isinstance(parsed, list):
                    json_blocks.extend(parsed)
                else:
                    json_blocks.append(parsed)
            except Exception:
                continue
        if json_blocks:
            return json_blocks
        # Fallback: try to parse the whole response as a list
        try:
            return _json.loads(ai_response)
        except Exception:
            pass
        # Fallback: try to parse as two JSON objects
        parts = ai_response.split('}')
        blocks = []
        for part in parts:
            if '{' in part:
                try:
                    blocks.append(_json.loads(part + '}'))
                except Exception:
                    continue
        if blocks:
            return blocks
        raise ValueError("No valid JSON block found in AI response")
    except Exception as e:
        return [
            {"type": "Subhead", "text": subhead},
            {"type": "Paragraph", "text": f"[AI generation failed for '{subhead}': {e}]"}
        ]

