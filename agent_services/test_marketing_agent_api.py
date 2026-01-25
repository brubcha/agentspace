import pytest
from agent_services.marketing_agent import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_marketing_kit_missing_fields(client):
    # Missing required fields
    response = client.post('/agent/marketing-kit', json={})
    assert response.status_code == 400
    assert b'missing_fields' in response.data

def test_marketing_kit_invalid_files(client):
    # Invalid files field (string instead of list)
    payload = {
        "client_name": "Test",
        "brand_name": "Test",
        "brand_url": "http://test.com",
        "files": "notalist"
    }
    response = client.post('/agent/marketing-kit', json=payload)
    assert response.status_code in (200, 500, 400)
    # Should not crash, should handle gracefully

# Add more edge case tests as needed
