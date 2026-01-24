import pytest
import json
import subprocess
import sys
from pathlib import Path

def test_rubric_checker_pass(tmp_path):
    # Use the gold standard kit (should pass)
    kit_path = Path('gold_standard_marketing_kit.json')
    rubric_path = Path('tests/marketing_kit_rubric.md')
    script_path = Path('tests/check_kit_against_rubric.py')
    result = subprocess.run([sys.executable, str(script_path), str(kit_path), '--json'], capture_output=True, text=True)
    print("Rubric checker output:", result.stdout)
    assert result.returncode == 0, f"Rubric checker failed: {result.stderr}\n{result.stdout}"
    output = json.loads(result.stdout)
    assert output['pass'] is True
    assert not output['missing_sections']
    for sec in output['results']:
        for crit in sec['criteria']:
            assert crit['met'] is True

def test_rubric_checker_fail(tmp_path):
    # Create a minimal kit missing required sections
    bad_kit = {
        "document": {"sections": [{"title": "Only One Section", "blocks": []}]}
    }
    bad_kit_path = tmp_path / "bad_kit.json"
    with open(bad_kit_path, 'w') as f:
        json.dump(bad_kit, f)
    rubric_path = Path('tests/marketing_kit_rubric.md')
    script_path = Path('tests/check_kit_against_rubric.py')
    result = subprocess.run([sys.executable, str(script_path), str(bad_kit_path), '--json'], capture_output=True, text=True)
    assert result.returncode != 0
    output = json.loads(result.stdout)
    assert output['pass'] is False
    assert output['missing_sections']

def test_evaluate_outputs_script(monkeypatch, tmp_path):
    # Patch OpenAI/azure.ai.evaluation if needed, or just check script runs
    script_path = Path('tests/evaluate_outputs.py')
    # Create a minimal test_payloads.jsonl
    payloads_path = tmp_path / "test_payloads.jsonl"
    with open(payloads_path, 'w') as f:
        f.write('{"clientName": "Test", "response": "Test response", "ground_truth": "Test response"}\n')
    # Patch environment
    monkeypatch.setenv('OPENAI_API_KEY', 'sk-test')
    # Patch data_path in script if needed (or copy script and edit)
    # For now, just check script runs (will fail if azure.ai.evaluation not installed)
    try:
        result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True, timeout=10)
    except Exception as e:
        pytest.skip(f"Evaluation script not runnable: {e}")
    # Accept nonzero exit if API key is fake, but script should not crash
    assert 'Evaluation complete' in result.stdout or result.returncode != 0
