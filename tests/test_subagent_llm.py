from agent_services.subagents import generate_paragraph_block

if __name__ == "__main__":
    section_title = "Test Section"
    paragraph_text = "This is a test paragraph prompt."
    client_name = "TestClient"
    brand_name = "TestBrand"
    brand_url = "https://test.com"
    result = generate_paragraph_block(section_title, paragraph_text, client_name, brand_name, brand_url)
    print(result)
