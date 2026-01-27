from docx import Document
import sys

# Usage: python extract_docx_text.py <docx_path>
def extract_text(docx_path):
    doc = Document(docx_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return '\n'.join(text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_docx_text.py <docx_path>")
        sys.exit(1)
    docx_path = sys.argv[1]
    print(extract_text(docx_path))
