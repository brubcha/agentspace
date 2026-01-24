
import os
import re
import logging
from logging.handlers import RotatingFileHandler

# --- Structured Logging Setup ---
LOG_PATH = os.path.join(os.path.dirname(__file__), 'subagent_trace.log')
logger = logging.getLogger("subagents")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_PATH, maxBytes=2*1024*1024, backupCount=3)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)

# Rubric loader (shared for all subagents)
def load_rubric_criteria(section_title, rubric_path=None):
    rubric_path = rubric_path or os.path.join(os.path.dirname(__file__), '../tests/marketing_kit_rubric.md')
    SECTION_HEADER_RE = re.compile(r'^### \d+\. (.+)$', re.MULTILINE)
    with open(rubric_path, encoding='utf-8') as f:
        rubric = f.read()
    sections = SECTION_HEADER_RE.findall(rubric)
    # Find criteria for the given section
    pattern = rf'### \d+\. {re.escape(section_title)}\n((?:- .+\n)+)'
    match = re.search(pattern, rubric)
    if match:
        criteria = [c.strip('- ').strip() for c in match.group(1).splitlines() if c.strip().startswith('-')]
        return criteria
    return []

# Website Scraper Subagent
def website_scraper_subagent(brand_url: str, max_length: int = 2000) -> str:
    """
    Fetches and summarizes content from the provided client website.
    Args:
        brand_url (str): The URL of the brand website to scrape.
        max_length (int): Maximum length of summary to return.
    Returns:
        str: Summary of website content or error message.
    """
    import requests
    from bs4 import BeautifulSoup
    try:
        resp = requests.get(brand_url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        texts = soup.stripped_strings
        content = ' '.join(texts)
        summary = content[:max_length]
        logger.info('{"event": "website_scrape", "url": "%s", "status": "success"}' % brand_url)
        return summary
    except Exception as e:
        logger.error('{"event": "website_scrape", "url": "%s", "status": "fail", "error": "%s"}' % (brand_url, str(e).replace('"', "'")))
        return f"[Website scrape failed: {e}]"
# Fallback/Retry Subagent
from typing import Callable, Any, List, Dict
def fallback_retry_block(generator_func: Callable, *args, max_retries: int = 2, **kwargs) -> List[Dict[str, Any]]:
    """
    Attempts to call a subagent generator function with retries on failure.
    Args:
        generator_func (Callable): The subagent function to call.
        max_retries (int): Number of retry attempts.
    Returns:
        List[Dict]: List of blocks, possibly with error/review notes.
    """
    last_result = None
    for attempt in range(max_retries):
        result = generator_func(*args, **kwargs)
        logger.info('{"event": "subagent_call", "func": "%s", "attempt": %d, "result": "%s"}' % (generator_func.__name__, attempt+1, "success" if result else "fail"))
        if result and not any('error' in block for block in result):
            return result
        last_result = result
    for block in last_result or []:
        if 'error' in block:
            block['review'] = '[Fallback/Retry] Block failed after retries.'
    logger.warning('{"event": "subagent_fallback", "func": "%s", "result": "fail_after_retries"}' % generator_func.__name__)
    return last_result or []
# QA/Validation Subagent
def validate_section_blocks(section_title, blocks, client_name, brand_name, brand_url, rubric_criteria=None, general_criteria=None):
    """
    Validates section blocks for richness, specificity, and rubric compliance using a focused prompt.
    """
    import json as _json
    if rubric_criteria is None:
        rubric_criteria = load_rubric_criteria(section_title)
    prompt = f"""
You are a marketing kit QA validator. Review the following section blocks for the '{section_title}' section.
Client Name: {client_name}
Brand: {brand_name}
Website: {brand_url}
Blocks: {_json.dumps(blocks)}
Rubric Criteria: {rubric_criteria}
"""
    if general_criteria:
        prompt += f"General Richness Criteria: {general_criteria}\n"
    prompt += (
        "IMPORTANT: For each block, if it is generic, lacks actionable advice, or does not reference the client, add a field 'review' with a reason. Return the validated blocks as a JSON array."
    )
    try:
        ai_response = call_openai_subagent(prompt, max_tokens=1024)
        validated_blocks = _json.loads(ai_response)
        logger.info('{"event": "validate_section", "section": "%s", "result": "success"}' % section_title)
        return validated_blocks
    except Exception as e:
        for block in blocks:
            block['review'] = f"[QA validation failed: {e}]"
        logger.error('{"event": "validate_section", "section": "%s", "result": "fail", "error": "%s"}' % (section_title, str(e).replace('"', "'")))
        return blocks
# Checklist Generator Subagent
def generate_checklist_block(section_title, checklist_title, client_name, brand_name, brand_url, context=None):
    """
    Generates a checklist block for a given section using a focused prompt.
    """
    rubric_criteria = load_rubric_criteria(section_title)
    prompt = f"""
Generate a checklist titled '{checklist_title}' for the '{section_title}' section of a marketing kit.
Client Name: {client_name}
Brand: {brand_name}
Website: {brand_url}
Rubric Criteria: {rubric_criteria}
"""
    if context:
        prompt += f"Context: {context}\n"
    prompt += (
        "IMPORTANT: Use ONLY the provided client, website, and file context. Do NOT use generic, template, or example content. "
        "Match the richness, structure, and actionable detail of the gold standard sample in 'tests/UCARI_MarketingKit_GoldStandardSample.md'. "
        "Cite real details from the context. Make the checklist actionable and specific to the client. "
        "Return a JSON block: {\"type\": \"Checklist\", \"title\": \"...\", \"items\": [ ... ]} only."
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
    rubric_criteria = load_rubric_criteria(section_title)
    prompt = f"""
Generate an opportunity card titled '{card_title}' for the '{section_title}' section of a marketing kit.
Client Name: {client_name}
Brand: {brand_name}
Website: {brand_url}
Rubric Criteria: {rubric_criteria}
"""
    if context:
        prompt += f"Context: {context}\n"
    prompt += (
        "IMPORTANT: Use ONLY the provided client, website, and file context. Do NOT use generic, template, or example content. "
        "Match the richness, structure, and actionable detail of the gold standard sample in 'tests/UCARI_MarketingKit_GoldStandardSample.md'. "
        "Cite real details from the context. Make the opportunity card vivid, actionable, and specific to the client. "
        "Return a JSON block: {\"type\": \"OpportunityCard\", \"title\": \"...\", \"description\": \"...\", \"actions\": [ ... ]} only."
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
    rubric_criteria = load_rubric_criteria(section_title)
    prompt = f"""
Generate a brand archetype card titled '{archetype_title}' for the '{section_title}' section of a marketing kit.
Client Name: {client_name}
Brand: {brand_name}
Website: {brand_url}
Rubric Criteria: {rubric_criteria}
"""
    if context:
        prompt += f"Context: {context}\n"
    prompt += (
        "IMPORTANT: Use ONLY the provided client, website, and file context. Do NOT use generic, template, or example content. "
        "Match the richness, structure, and actionable detail of the gold standard sample in 'tests/UCARI_MarketingKit_GoldStandardSample.md'. "
        "Cite real details from the context. Make the archetype vivid, actionable, and specific to the client. "
        "Return a JSON block: {\"type\": \"Archetype\", \"title\": \"...\", \"description\": \"...\", \"attributes\": { ... }} only."
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
    rubric_criteria = load_rubric_criteria(section_title)
    prompt = f"""
Generate a persona card titled '{persona_title}' for the '{section_title}' section of a marketing kit.
Client Name: {client_name}
Brand: {brand_name}
Website: {brand_url}
Rubric Criteria: {rubric_criteria}
"""
    if context:
        prompt += f"Context: {context}\n"
    prompt += (
        "IMPORTANT: Use ONLY the provided client, website, and file context. Do NOT use generic, template, or example content. "
        "Match the richness, structure, and actionable detail of the gold standard sample in 'tests/UCARI_MarketingKit_GoldStandardSample.md'. "
        "Cite real details from the context. Make the persona vivid, actionable, and specific to the client. "
        "Return a JSON block: {\"type\": \"Persona\", \"title\": \"...\", \"description\": \"...\", \"attributes\": { ... }} only."
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
    rubric_criteria = load_rubric_criteria(section_title)
    prompt = f"""
Generate a bullet list titled '{list_title}' for the '{section_title}' section of a marketing kit.
Client Name: {client_name}
Brand: {brand_name}
Website: {brand_url}
Rubric Criteria: {rubric_criteria}
"""
    if context:
        prompt += f"Context: {context}\n"
    prompt += (
        "IMPORTANT: Use ONLY the provided client, website, and file context. Do NOT use generic, template, or example content. "
        "Match the richness, structure, and actionable detail of the gold standard sample in 'tests/UCARI_MarketingKit_GoldStandardSample.md'. "
        "Cite real details from the context. Make the list actionable and specific to the client. "
        "Return a JSON block: {\"type\": \"Bullets\", \"title\": \"...\", \"items\": [ ... ]} only."
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
    rubric_criteria = load_rubric_criteria(section_title)
    prompt = f"""
Generate a table titled '{table_title}' for the '{section_title}' section of a marketing kit.
Client Name: {client_name}
Brand: {brand_name}
Website: {brand_url}
Columns: {', '.join(columns)}
Rubric Criteria: {rubric_criteria}
"""
    if context:
        prompt += f"Context: {context}\n"
    prompt += (
        "IMPORTANT: Use ONLY the provided client, website, and file context. Do NOT use generic, template, or example content. "
        "Match the richness, structure, and actionable detail of the gold standard sample in 'tests/UCARI_MarketingKit_GoldStandardSample.md'. "
        "Cite real details from the context. Make the table actionable and specific to the client. "
        "Return a JSON block: {\"type\": \"Table\", \"title\": \"...\", \"columns\": [...], \"rows\": [[...], ...]} only."
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
        "IMPORTANT: Use ONLY the provided client, website, and file context. Do NOT use generic, template, or example content. "
        "Match the richness, structure, and actionable detail of the gold standard sample in 'tests/UCARI_MarketingKit_GoldStandardSample.md'. "
        "Cite real details from the context. Be vivid, actionable, and specific to the client. "
        "Return a JSON block: {\"type\": \"Subhead\", \"text\": \"...\"} followed by a {\"type\": \"Paragraph\", \"text\": \"...\"}."
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

