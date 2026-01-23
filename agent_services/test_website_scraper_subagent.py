import pytest
from agent_services.subagents import website_scraper_subagent

def test_website_scraper_subagent_success(monkeypatch):
    class MockResponse:
        def __init__(self, text):
            self.text = text
        def raise_for_status(self):
            pass
    def mock_get(url, timeout=10):
        html = """
        <html><body>
        <h1>About Us</h1>
        <p>Welcome to TestCo, your trusted partner for widgets.</p>
        <div>Contact us at info@testco.com</div>
        </body></html>
        """
        return MockResponse(html)
    monkeypatch.setattr("requests.get", mock_get)
    summary = website_scraper_subagent("http://testco.com")
    assert "TestCo" in summary
    assert "widgets" in summary

def test_website_scraper_subagent_failure(monkeypatch):
    def mock_get(url, timeout=10):
        raise Exception("Network error")
    monkeypatch.setattr("requests.get", mock_get)
    summary = website_scraper_subagent("http://fail.com")
    assert "scrape failed" in summary.lower()
