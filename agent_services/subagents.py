# DEBUG: Print import context to confirm which subagents.py is loaded and which Python is running
import sys
print(f"[DEBUG] Loaded subagents.py from {__file__} using Python {sys.executable}")
def generate_list_of_sections_block(section_title, section_titles, client_name, brand_name, brand_url, context=None):
    """
    Generates a ListOfSections block for a given section using a focused prompt.
    """
    import json as _json
    import re
    logger.info(_json.dumps({
        "event": "enter_generate_list_of_sections_block",
        "section_title": section_title,
        "section_titles": section_titles,
        "client_name": client_name,
        "brand_name": brand_name,
        "brand_url": brand_url
    }))
    rubric_criteria = load_rubric_criteria(section_title)
    prompt = f"""
Generate a block listing the included sections for the '{section_title}' section of a marketing kit.
Client Name: {client_name}
Brand: {brand_name}
Website: {brand_url}
Rubric Criteria: {rubric_criteria}
Section Titles: {section_titles}
"""
    if context:
        prompt += f"Context: {context}\n"
    prompt += (
        "IMPORTANT: Use ONLY the provided section_titles, client, website, and file context. Do NOT use generic, template, or example content. "
        "After generating, review your output: Does it meet ALL rubric criteria? Is it as rich and specific as the gold standard? If not, revise and improve before returning. "
        "Return a JSON block: {\"type\": \"ListOfSections\", \"section_titles\": [...] } only."
    )
    try:
        logger.info('{"event": "call_openai_subagent", "function": "generate_list_of_sections_block"}')
        ai_response = call_openai_subagent(prompt)
        logger.info(_json.dumps({"event": "listofsections_llm_raw_response", "response": ai_response}))
        # Robust JSON extraction
        match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if match:
            block = _json.loads(match.group(0))
        else:
            block = _json.loads(ai_response)
        if not isinstance(block, list):
            block = [block]
        # Post-generation QA validation
        validated = validate_section_blocks(section_title, block, client_name, brand_name, brand_url, rubric_criteria)
        # If validation fails, retry once with a revise-and-improve instruction
        if any('review' in b and b['review'] for b in validated):
            logger.info('{"event": "listofsections_block_retry", "reason": "validation failed, retrying with revise instruction"}')
            retry_prompt = prompt + "\nIf your previous output was flagged as generic or not rubric-compliant, revise and improve it now."
            ai_response = call_openai_subagent(retry_prompt)
            match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if match:
                block = _json.loads(match.group(0))
            else:
                block = _json.loads(ai_response)
            if not isinstance(block, list):
                block = [block]
            validated = validate_section_blocks(section_title, block, client_name, brand_name, brand_url, rubric_criteria)
        logger.info(_json.dumps({
            "event": "exit_generate_list_of_sections_block",
            "result_count": len(validated)
        }))
        return validated
    except Exception as e:
        logger.error(_json.dumps({
            "event": "error_generate_list_of_sections_block",
            "error": str(e),
            "raw_response": locals().get('ai_response', None)
        }))
        return [
            {"type": "ListOfSections", "section_titles": section_titles, "error": f"[AI generation failed: {e}]"}
        ]
def generate_paragraph_block(section_title, paragraph_text, client_name, brand_name, brand_url, context=None):
    """
    Generates a paragraph block for a given section using a focused prompt.
    """
    import json as _json
    import re
    logger.info(_json.dumps({
        "event": "enter_generate_paragraph_block",
        "section_title": section_title,
        "paragraph_text": paragraph_text,
        "client_name": client_name,
        "brand_name": brand_name,
        "brand_url": brand_url
    }))
    rubric_criteria = load_rubric_criteria(section_title)
    prompt = f"""
Generate a rich, client-specific paragraph for the '{section_title}' section of a marketing kit.
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
        "Cite real details from the context. Make the paragraph vivid, actionable, and specific to the client. "
        "After generating, review your output: Does it meet ALL rubric criteria? Is it as rich and specific as the gold standard? If not, revise and improve before returning. "
        "Return a JSON block: {\"type\": \"Paragraph\", \"text\": \"...\"} only."
    )
    try:
        logger.info('{"event": "call_openai_subagent", "function": "generate_paragraph_block"}')
        ai_response = call_openai_subagent(prompt)
        logger.info(_json.dumps({"event": "paragraph_llm_raw_response", "response": ai_response}))
        # Robust JSON extraction
        match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if match:
            block = _json.loads(match.group(0))
        else:
            block = _json.loads(ai_response)
        if not isinstance(block, list):
            block = [block]
        # Post-generation QA validation
        validated = validate_section_blocks(section_title, block, client_name, brand_name, brand_url, rubric_criteria)
        # If validation fails, retry once with a revise-and-improve instruction
        if any('review' in b and b['review'] for b in validated):
            logger.info('{"event": "paragraph_block_retry", "reason": "validation failed, retrying with revise instruction"}')
            retry_prompt = prompt + "\nIf your previous output was flagged as generic or not rubric-compliant, revise and improve it now."
            ai_response = call_openai_subagent(retry_prompt)
            match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if match:
                block = _json.loads(match.group(0))
            else:
                block = _json.loads(ai_response)
            if not isinstance(block, list):
                block = [block]
            validated = validate_section_blocks(section_title, block, client_name, brand_name, brand_url, rubric_criteria)
        logger.info(_json.dumps({
            "event": "exit_generate_paragraph_block",
            "result_count": len(validated)
        }))
        return validated
    except Exception as e:
        logger.error(_json.dumps({
            "event": "error_generate_paragraph_block",
            "error": str(e),
            "raw_response": locals().get('ai_response', None)
        }))
        return [
            {"type": "Paragraph", "text": paragraph_text, "error": f"[AI generation failed: {e}]"}
        ]
def call_openai_subagent(prompt, max_tokens=512, temperature=0.7, model="gpt-3.5-turbo"):
    """
    Calls the OpenAI API to get a completion for the given prompt.
    """
    import os
    import openai
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("[call_openai_subagent] OPENAI_API_KEY environment variable not set.")
        raise RuntimeError("OPENAI_API_KEY environment variable not set.")
    else:
        logger.info("[call_openai_subagent] OPENAI_API_KEY is loaded (length: %d)", len(api_key))
    logger.info("[call_openai_subagent] Prompt: %s", prompt)
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        result = response.choices[0].message.content
        logger.info("[call_openai_subagent] Response: %s", result)
        return result
    except Exception as e:
        logger.error("[call_openai_subagent] OpenAI API call failed: %s", str(e))
        raise

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
        "IMPORTANT: For each block, check and flag the following:\n"
        "- Is the content generic, repetitive, or missing actionable advice?\n"
        "- Does it reference the client and include specific, relevant data, statistics, or proof points where required?\n"
        "- Are all required recommendations, evidence, and unique insights present?\n"
        "- Is there any redundancy or missing content compared to the rubric?\n"
        "If any issue is found, add a field 'review' with a clear reason (e.g., 'missing data', 'redundant', 'not actionable', 'no proof', 'does not match rubric'). Return the validated blocks as a JSON array."
    )
    try:
        ai_response = call_openai_subagent(prompt, max_tokens=1024)
        validated_blocks = _json.loads(ai_response)
        logger.info(_json.dumps({
            "event": "validate_section",
            "section": section_title,
            "result": "success"
        }))
        return validated_blocks
    except Exception as e:
        for block in blocks:
            block['review'] = f"[QA validation failed: {e}]"
        logger.error(_json.dumps({
            "event": "validate_section",
            "section": section_title,
            "result": "fail",
            "error": str(e)
        }))
        return blocks
from typing import Callable, Any, List, Dict
import logging
logger = logging.getLogger("subagents")

def generate_subhead_block(section_title, subhead_text, client_name, brand_name, brand_url, context=None):
    """
    Generates a subhead (paragraph/heading) block for a given section using a focused prompt.
    """
    import json as _json
    import re
    logger.info(_json.dumps({
        "event": "enter_generate_subhead_block",
        "section_title": section_title,
        "subhead_text": subhead_text,
        "client_name": client_name,
        "brand_name": brand_name,
        "brand_url": brand_url
    }))
    rubric_criteria = load_rubric_criteria(section_title)
    prompt = f"""
Generate a subhead (short paragraph or heading) for the '{section_title}' section of a marketing kit.
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
        "Cite real details from the context. Make the subhead vivid, actionable, and specific to the client. "
        "After generating, review your output: Does it meet ALL rubric criteria? Is it as rich and specific as the gold standard? If not, revise and improve before returning. "
        "Return a JSON block: {\"type\": \"Subhead\", \"text\": \"...\"} only."
    )
    try:
        logger.info('{"event": "call_openai_subagent", "function": "generate_subhead_block"}')
        ai_response = call_openai_subagent(prompt)
        logger.info(_json.dumps({"event": "subhead_llm_raw_response", "response": ai_response}))
        # Robust JSON extraction
        match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if match:
            block = _json.loads(match.group(0))
        else:
            block = _json.loads(ai_response)
        if not isinstance(block, list):
            block = [block]
        # Post-generation QA validation
        validated = validate_section_blocks(section_title, block, client_name, brand_name, brand_url, rubric_criteria)
        # If validation fails, retry once with a revise-and-improve instruction
        if any('review' in b and b['review'] for b in validated):
            logger.info('{"event": "subhead_block_retry", "reason": "validation failed, retrying with revise instruction"}')
            retry_prompt = prompt + "\nIf your previous output was flagged as generic or not rubric-compliant, revise and improve it now."
            ai_response = call_openai_subagent(retry_prompt)
            match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if match:
                block = _json.loads(match.group(0))
            else:
                block = _json.loads(ai_response)
            if not isinstance(block, list):
                block = [block]
            validated = validate_section_blocks(section_title, block, client_name, brand_name, brand_url, rubric_criteria)
        logger.info(_json.dumps({
            "event": "exit_generate_subhead_block",
            "result_count": len(validated)
        }))
        return validated
    except Exception as e:
        logger.error(_json.dumps({
            "event": "error_generate_subhead_block",
            "error": str(e),
            "raw_response": locals().get('ai_response', None)
        }))
        return [
            {"type": "Subhead", "text": subhead_text, "error": f"[AI generation failed: {e}]"}
        ]

import os
import re
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler

# --- Structured Logging Setup ---
LOG_PATH = os.path.join(os.path.dirname(__file__), 'subagent_trace.log')
logger = logging.getLogger("subagents")
logger.setLevel(logging.INFO)
handler = ConcurrentRotatingFileHandler(LOG_PATH, maxBytes=2*1024*1024, backupCount=3)
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
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; agentspace-bot/1.0)'}
        resp = requests.get(brand_url, headers=headers, timeout=10)
        logger.info('{"event": "website_scrape_attempt", "url": "%s", "status_code": "%s", "final_url": "%s"}' % (brand_url, getattr(resp, 'status_code', 'N/A'), getattr(resp, 'url', 'N/A')))
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        texts = soup.stripped_strings
        content = ' '.join(texts)
        summary = content[:max_length]
        logger.info('{"event": "website_scrape", "url": "%s", "status": "success", "length": %d}' % (brand_url, len(summary)))
        return summary
    except requests.exceptions.SSLError as ssl_err:
        logger.error('{"event": "website_scrape", "url": "%s", "status": "ssl_error", "error": "%s"}' % (brand_url, str(ssl_err).replace('"', "'")))
        return f"[Website scrape failed: SSL error. The server may not support modern SSL/TLS or your environment is missing root certificates. Details: {ssl_err}]"
    except requests.exceptions.ConnectionError as conn_err:
        # Distinguish DNS errors
        if 'NameResolutionError' in str(conn_err) or 'getaddrinfo failed' in str(conn_err):
            logger.error('{"event": "website_scrape", "url": "%s", "status": "dns_error", "error": "%s"}' % (brand_url, str(conn_err).replace('"', "'")))
            return f"[Website scrape failed: DNS resolution error. The domain name could not be resolved. Details: {conn_err}]"
        logger.error('{"event": "website_scrape", "url": "%s", "status": "connection_error", "error": "%s"}' % (brand_url, str(conn_err).replace('"', "'")))
        return f"[Website scrape failed: Connection error. The server may be down or unreachable. Details: {conn_err}]"
    except requests.exceptions.Timeout as timeout_err:
        logger.error('{"event": "website_scrape", "url": "%s", "status": "timeout", "error": "%s"}' % (brand_url, str(timeout_err).replace('"', "'")))
        return f"[Website scrape failed: Timeout. The server took too long to respond. Details: {timeout_err}]"
    except requests.exceptions.RequestException as req_err:
        logger.error('{"event": "website_scrape", "url": "%s", "status": "request_exception", "error": "%s"}' % (brand_url, str(req_err).replace('"', "'")))
        return f"[Website scrape failed: Request error. Details: {req_err}]"
    except Exception as e:
        logger.error('{"event": "website_scrape", "url": "%s", "status": "fail", "error": "%s"}' % (brand_url, str(e).replace('"', "'")))
        return f"[Website scrape failed: Unexpected error. Details: {e}]"
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
    import json as _json
    logger.info(_json.dumps({
        "event": "enter_generate_checklist_block",
        "section_title": section_title,
        "checklist_title": checklist_title,
        "client_name": client_name,
        "brand_name": brand_name,
        "brand_url": brand_url
    }))
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
        "All items must be rubric-compliant and match the gold standard in structure, order, and formatting. "
        "After generating, review your output: Does it meet ALL rubric criteria? Is it as rich and specific as the gold standard? If not, revise and improve before returning. "
        "Return a JSON block: {\"type\": \"Checklist\", \"title\": \"...\", \"items\": [ ... ]} only."
    )
    try:
        logger.info('{"event": "call_openai_subagent", "function": "generate_checklist_block"}')
        import json as _json
        ai_response = call_openai_subagent(prompt)
        block = _json.loads(ai_response)
        if not isinstance(block, list):
            block = [block]
        # Post-generation QA validation
        validated = validate_section_blocks(section_title, block, client_name, brand_name, brand_url, rubric_criteria)
        # If validation fails, retry once with a revise-and-improve instruction
        if any('review' in b and b['review'] for b in validated):
            logger.info('{"event": "checklist_block_retry", "reason": "validation failed, retrying with revise instruction"}')
            retry_prompt = prompt + "\nIf your previous output was flagged as generic or not rubric-compliant, revise and improve it now."
            ai_response = call_openai_subagent(retry_prompt)
            block = _json.loads(ai_response)
            if not isinstance(block, list):
                block = [block]
            validated = validate_section_blocks(section_title, block, client_name, brand_name, brand_url, rubric_criteria)
        logger.info(_json.dumps({
            "event": "exit_generate_checklist_block",
            "result_count": len(validated)
        }))
        return validated
    except Exception as e:
        import json as _json
        logger.error(_json.dumps({
            "event": "error_generate_checklist_block",
            "error": str(e)
        }))
        return [
            {"type": "Checklist", "title": checklist_title, "items": [], "error": f"[AI generation failed: {e}]"}
        ]
# Opportunity Card Generator Subagent
def generate_opportunity_card_block(section_title, card_title, client_name, brand_name, brand_url, context=None):
    import json as _json
    logger.info(_json.dumps({
        "event": "enter_generate_opportunity_card_block",
        "section_title": section_title,
        "card_title": card_title,
        "client_name": client_name,
        "brand_name": brand_name,
        "brand_url": brand_url
    }))
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
        "After generating, review your output: Does it meet ALL rubric criteria? Is it as rich and specific as the gold standard? If not, revise and improve before returning. "
        "Return a JSON block: {\"type\": \"OpportunityCard\", \"title\": \"...\", \"description\": \"...\", \"actions\": [ ... ]} only."
    )
    try:
        logger.info('{"event": "call_openai_subagent", "function": "generate_opportunity_card_block"}')
        import json as _json
        ai_response = call_openai_subagent(prompt)
        block = _json.loads(ai_response)
        if not isinstance(block, list):
            block = [block]
        validated = validate_section_blocks(section_title, block, client_name, brand_name, brand_url, rubric_criteria)
        # If validation fails, retry once with a revise-and-improve instruction
        if any('review' in b and b['review'] for b in validated):
            logger.info('{"event": "opportunity_card_block_retry", "reason": "validation failed, retrying with revise instruction"}')
            retry_prompt = prompt + "\nIf your previous output was flagged as generic or not rubric-compliant, revise and improve it now."
            ai_response = call_openai_subagent(retry_prompt)
            block = _json.loads(ai_response)
            if not isinstance(block, list):
                block = [block]
            validated = validate_section_blocks(section_title, block, client_name, brand_name, brand_url, rubric_criteria)
        logger.info(_json.dumps({
            "event": "exit_generate_opportunity_card_block",
            "result_count": len(validated)
        }))
        return validated
    except Exception as e:
        import json as _json
        logger.error(_json.dumps({
            "event": "error_generate_opportunity_card_block",
            "error": str(e)
        }))
        return [
            {"type": "OpportunityCard", "title": card_title, "description": "", "actions": [], "error": f"[AI generation failed: {e}]"}
        ]
# Archetype Generator Subagent
def generate_archetype_block(section_title, archetype_title, client_name, brand_name, brand_url, context=None):
    import json as _json
    logger.info(_json.dumps({
        "event": "enter_generate_archetype_block",
        "section_title": section_title,
        "archetype_title": archetype_title,
        "client_name": client_name,
        "brand_name": brand_name,
        "brand_url": brand_url
    }))
    """
    Generates a brand archetype block for a given section using a focused prompt.
    """
    rubric_criteria = load_rubric_criteria(section_title)
    prompt = f"""
You are a world-class brand strategist. Generate a list of 2-4 vivid, actionable, and client-specific audience archetypes for the '{section_title}' section of a marketing kit.
Client Name: {client_name}
Brand: {brand_name}
Website: {brand_url}
Rubric Criteria: {rubric_criteria}
"""
    if context:
        prompt += f"Context: {context}\n"
    prompt += (
        "IMPORTANT: Use ONLY the provided client, website, and file context. Do NOT use generic, template, or example content. "
        "Each archetype must be unique, relevant to the brand, and reference real details from the client/context. "
        "For each, include: title, description, mission, voice, values, emotional promise, icon, and a sample 'voice in action' phrase. "
        "Output a JSON array of objects, each with: type='Archetype', title, description, attributes (with keys: mission, voice, values, emotional_promise, icon, voice_in_action). "
        "Example: [{\"type\": \"Archetype\", \"title\": \"The Guide\", \"description\": \"Empowers through knowledge...\", \"attributes\": {\"mission\": \"...\", ...}}] "
        "After generating, review your output: Does it meet ALL rubric criteria? Is it as rich and specific as the gold standard? If not, revise and improve before returning. "
        "Return ONLY valid JSON."
    )
    try:
        logger.info('{"event": "call_openai_subagent", "function": "generate_archetype_block"}')
        ai_response = call_openai_subagent(prompt)
        logger.info(_json.dumps({"event": "archetype_llm_raw_response", "response": ai_response}))
        block = _json.loads(ai_response)
        result = []
        def coerce_archetype(b):
            # If it looks like an archetype, set type
            if b.get('type') == 'Archetype':
                return b
            # Heuristic: has title, description, attributes with mission, etc.
            attrs = b.get('attributes', {})
            if (
                isinstance(attrs, dict)
                and 'mission' in attrs and 'voice' in attrs and 'values' in attrs
                and 'emotional_promise' in attrs and 'icon' in attrs and 'voice_in_action' in attrs
            ):
                b['type'] = 'Archetype'
            return b
        if isinstance(block, list):
            for b in block:
                result.append(coerce_archetype(b))
        else:
            result.append(coerce_archetype(block))
        validated = validate_section_blocks(section_title, result, client_name, brand_name, brand_url, rubric_criteria)
        # If validation fails, retry once with a revise-and-improve instruction
        if any('review' in b and b['review'] for b in validated):
            logger.info('{"event": "archetype_block_retry", "reason": "validation failed, retrying with revise instruction"}')
            retry_prompt = prompt + "\nIf your previous output was flagged as generic or not rubric-compliant, revise and improve it now."
            ai_response = call_openai_subagent(retry_prompt)
            block = _json.loads(ai_response)
            result = []
            if isinstance(block, list):
                for b in block:
                    result.append(coerce_archetype(b))
            else:
                result.append(coerce_archetype(block))
            validated = validate_section_blocks(section_title, result, client_name, brand_name, brand_url, rubric_criteria)
        logger.info(_json.dumps({
            "event": "exit_generate_archetype_block",
            "result_count": len(validated)
        }))
        return validated
    except Exception as e:
        logger.error(_json.dumps({
            "event": "error_generate_archetype_block",
            "error": str(e)
        }))
        return [
            {"type": "Archetype", "title": archetype_title, "description": "", "attributes": {}, "error": f"[AI generation failed: {e}]"}
        ]
# Persona Generator Subagent
def generate_persona_block(section_title, persona_title, client_name, brand_name, brand_url, context=None):
    import json as _json
    logger.info(_json.dumps({
        "event": "enter_generate_persona_block",
        "section_title": section_title,
        "persona_title": persona_title,
        "client_name": client_name,
        "brand_name": brand_name,
        "brand_url": brand_url
    }))
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
        "After generating, review your output: Does it meet ALL rubric criteria? Is it as rich and specific as the gold standard? If not, revise and improve before returning. "
        "Return a JSON block: {\"type\": \"Persona\", \"title\": \"...\", \"description\": \"...\", \"attributes\": { ... }} only."
    )
    try:
        logger.info('{"event": "call_openai_subagent", "function": "generate_persona_block"}')
        import json as _json
        ai_response = call_openai_subagent(prompt)
        block = _json.loads(ai_response)
        if not isinstance(block, list):
            block = [block]
        validated = validate_section_blocks(section_title, block, client_name, brand_name, brand_url, rubric_criteria)
        # If validation fails, retry once with a revise-and-improve instruction
        if any('review' in b and b['review'] for b in validated):
            logger.info('{"event": "persona_block_retry", "reason": "validation failed, retrying with revise instruction"}')
            retry_prompt = prompt + "\nIf your previous output was flagged as generic or not rubric-compliant, revise and improve it now."
            ai_response = call_openai_subagent(retry_prompt)
            block = _json.loads(ai_response)
            if not isinstance(block, list):
                block = [block]
            validated = validate_section_blocks(section_title, block, client_name, brand_name, brand_url, rubric_criteria)
        logger.info(f'{{"event": "exit_generate_persona_block", "result_count": {len(validated)}}}')
        return validated
    except Exception as e:
        import json as _json
        logger.error(_json.dumps({
            "event": "error_generate_persona_block",
            "error": str(e)
        }))
        return [
            {"type": "Persona", "title": persona_title, "description": "", "attributes": {}, "error": f"[AI generation failed: {e}]"}
        ]
# List Generator Subagent
def generate_list_block(section_title, list_title, client_name, brand_name, brand_url, context=None):
    import json as _json
    logger.info(_json.dumps({
        "event": "enter_generate_list_block",
        "section_title": section_title,
        "list_title": list_title,
        "client_name": client_name,
        "brand_name": brand_name,
        "brand_url": brand_url
    }))
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
        "After generating, review your output: Does it meet ALL rubric criteria? Is it as rich and specific as the gold standard? If not, revise and improve before returning. "
        "Return a JSON block: {\"type\": \"Bullets\", \"title\": \"...\", \"items\": [ ... ]} only."
    )
    try:
        logger.info('{"event": "call_openai_subagent", "function": "generate_list_block"}')
        import json as _json
        ai_response = call_openai_subagent(prompt)
        block = _json.loads(ai_response)
        if isinstance(block, list):
            logger.info(_json.dumps({
                "event": "exit_generate_list_block",
                "result_count": len(block)
            }))
            validated = validate_section_blocks(section_title, block, client_name, brand_name, brand_url, rubric_criteria)
        else:
            logger.info(_json.dumps({
                "event": "exit_generate_list_block",
                "result_count": 1
            }))
            block = [block]
            validated = validate_section_blocks(section_title, block, client_name, brand_name, brand_url, rubric_criteria)
        # If validation fails, retry once with a revise-and-improve instruction
        if any('review' in b and b['review'] for b in validated):
            logger.info('{"event": "list_block_retry", "reason": "validation failed, retrying with revise instruction"}')
            retry_prompt = prompt + "\nIf your previous output was flagged as generic or not rubric-compliant, revise and improve it now."
            ai_response = call_openai_subagent(retry_prompt)
            block = _json.loads(ai_response)
            if not isinstance(block, list):
                block = [block]
            validated = validate_section_blocks(section_title, block, client_name, brand_name, brand_url, rubric_criteria)
        return validated
    except Exception as e:
        import json as _json
        logger.error(_json.dumps({
            "event": "error_generate_list_block",
            "error": str(e)
        }))
        return [
            {"type": "Bullets", "title": list_title, "items": [], "error": f"[AI generation failed: {e}]"}
        ]
# Table Generator Subagent
def generate_table_block(section_title, table_title, client_name, brand_name, brand_url, columns, context=None):
    import json as _json
    logger.info(_json.dumps({
        "event": "enter_generate_table_block",
        "section_title": section_title,
        "table_title": table_title,
        "client_name": client_name,
        "brand_name": brand_name,
        "brand_url": brand_url,
        "columns": columns
    }))
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
        "All columns and rows must be rubric-compliant and match the gold standard in structure, order, and formatting. "
        "Generate at least 3 fully filled rows. Each cell must be rich, specific, and client-relevant. "
        "After generating, review your output: Does it meet ALL rubric criteria? Is it as rich and specific as the gold standard? If not, revise and improve before returning. "
        "Return ONLY valid JSON: {\"type\": \"Table\", \"title\": \"...\", \"columns\": [...], \"rows\": [[...], ...]}"
    )

    # Defensive: ensure rows is always a list of lists, even if missing or malformed
    # This logic is now handled after AI response parsing, not before
    try:
        logger.info('{"event": "call_openai_subagent", "function": "generate_table_block"}')
        import json as _json
        import re
        ai_response = call_openai_subagent(prompt)
        logger.info(_json.dumps({"event": "table_llm_raw_response", "response": ai_response}))
        # Robust JSON extraction
        match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if match:
            block = _json.loads(match.group(0))
        else:
            block = _json.loads(ai_response)
        if not isinstance(block, list):
            block = [block]
        validated = validate_section_blocks(section_title, block, client_name, brand_name, brand_url, rubric_criteria)
        # If validation fails, retry once with a revise-and-improve instruction
        if any('review' in b and b['review'] for b in validated):
            logger.info('{"event": "table_block_retry", "reason": "validation failed, retrying with revise instruction"}')
            retry_prompt = prompt + "\nIf your previous output was flagged as generic or not rubric-compliant, revise and improve it now."
            ai_response = call_openai_subagent(retry_prompt)
            match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if match:
                block = _json.loads(match.group(0))
            else:
                block = _json.loads(ai_response)
            if not isinstance(block, list):
                block = [block]
            validated = validate_section_blocks(section_title, block, client_name, brand_name, brand_url, rubric_criteria)
        logger.info(_json.dumps({
            "event": "exit_generate_table_block",
            "result_count": len(validated)
        }))
        return validated
    except Exception as e:
        import json as _json
        logger.error(_json.dumps({
            "event": "error_generate_table_block",
            "error": str(e),
            "raw_response": locals().get('ai_response', None)
        }))
        return [
            {"type": "Table", "title": table_title, "columns": columns, "rows": [], "error": f"[AI generation failed: {e}]"}
        ]

# Ensure .env variables are loaded at import time
import os
from dotenv import load_dotenv
load_dotenv()

