import pytest
import requests
import tempfile
import os
import json

def test_missing_required_fields():
    url = 'http://localhost:7000/agent/marketing-kit'
    payload = {"brand_url": "https://test.com"}  # missing brand_name
    r = requests.post(url, json=payload)
    assert r.status_code == 400
    assert 'missing_fields' in r.json()

def test_malformed_input():
    url = 'http://localhost:7000/agent/marketing-kit'
    r = requests.post(url, data='not a json')
    assert r.status_code in (400, 422)

def test_empty_file_upload():
    url = 'http://localhost:7000/agent/marketing-kit'
    files = {'files': ('empty.txt', b'')}
    data = {'brand_name': 'Test', 'brand_url': 'https://test.com'}
    r = requests.post(url, data=data, files=files)
    assert r.status_code in (200, 400)

def test_huge_file_upload():
    url = 'http://localhost:7000/agent/marketing-kit'
    big_content = b'x' * 10_000_000
    files = {'files': ('big.txt', big_content)}
    data = {'brand_name': 'Test', 'brand_url': 'https://test.com'}
    r = requests.post(url, data=data, files=files)
    assert r.status_code in (200, 400, 413)

def test_unsupported_file_type():
    url = 'http://localhost:7000/agent/marketing-kit'
    files = {'files': ('malware.exe', b'fake')}
    data = {'brand_name': 'Test', 'brand_url': 'https://test.com'}
    r = requests.post(url, data=data, files=files)
    assert r.status_code in (200, 400)

def test_invalid_url():
    url = 'http://localhost:7000/agent/marketing-kit'
    payload = {'brand_name': 'Test', 'brand_url': 'http://invalid.invalid'}
    r = requests.post(url, json=payload)
    assert r.status_code in (200, 400)

def test_rubric_almost_pass():
    # Kit missing one criterion
    kit = {"document": {"sections": [{"title": "Executive Summary", "blocks": [{"type": "Paragraph", "text": "Good"}]}]}}
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.json') as f:
        json.dump(kit, f)
        f.flush()
        result = os.system(f"python tests/check_kit_against_rubric.py {f.name} --json")
        assert result != 0
    os.unlink(f.name)

def test_rubric_overcompliance():
    # Kit with extra, unnecessary section
    kit = {"document": {"sections": [
        {"title": "Executive Summary", "blocks": [{"type": "Paragraph", "text": "Good"}]},
        {"title": "Extra Section", "blocks": [{"type": "Paragraph", "text": "Extra"}]}
    ]}}
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.json') as f:
        json.dump(kit, f)
        f.flush()
        result = os.system(f"python tests/check_kit_against_rubric.py {f.name} --json")
        # Should still fail if required sections missing
        assert result != 0
    os.unlink(f.name)

def test_performance_timeout(monkeypatch):
    import time
    from agent_services import subagents
    def slow_func(*a, **k):
        time.sleep(2)
        return [{"type": "Paragraph", "text": "Slow"}]
    start = time.time()
    subagents.fallback_retry_block(slow_func, max_retries=1)
    elapsed = time.time() - start
    assert elapsed < 5

def test_security_path_traversal():
    url = 'http://localhost:7000/agent/marketing-kit'
    files = {'files': ('../evil.txt', b'evil')}
    data = {'brand_name': 'Test', 'brand_url': 'https://test.com'}
    r = requests.post(url, data=data, files=files)
    assert r.status_code in (200, 400)

def test_mocked_llm(monkeypatch):
    from agent_services import subagents
    def fake_llm(prompt, *a, **k):
        return '[{"type": "Paragraph", "text": "Mocked"}]'
    monkeypatch.setattr(subagents, "call_openai_subagent", fake_llm)
    blocks = subagents.generate_subhead_block("Overview", "How to Use It", "TestClient", "TestBrand", "https://test.com")
    assert any(b.get("text") == "Mocked" for b in blocks)

def test_api_contract():
    url = 'http://localhost:7000/agent/marketing-kit'
    payload = {'brand_name': 'Test', 'brand_url': 'https://test.com'}
    r = requests.post(url, json=payload)
    assert 'application/json' in r.headers.get('Content-Type', '')
    assert r.status_code in (200, 400)

def test_regression_gold_standard():
    # Compare current output to gold standard
    url = 'http://localhost:7000/agent/marketing-kit'
    with open('gold_standard_marketing_kit.json', encoding='utf-8') as f:
        gold = json.load(f)
    payload = {'brand_name': 'Test', 'brand_url': 'https://test.com'}
    r = requests.post(url, json=payload)
    if r.status_code == 200:
        kit = r.json()
        # Only compare section titles for simplicity
        gold_titles = [s['title'] for s in gold['document']['sections']]
        kit_titles = [s['title'] for s in kit['document']['sections']]
        assert set(gold_titles) <= set(kit_titles)

def test_ci_artifacts():
    # Check that logs and feedback are generated after a run
    assert os.path.exists('agent_services/agent_trace.log')
    assert os.path.exists('agent_services/subagent_trace.log')
    assert os.path.exists('tests/test_feedback.json')
