from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

def audit_to_docx(audit: dict) -> bytes:
    doc = Document()
    doc.add_heading('Marketing Kit Audit Report', 0)

    # Expected vs Rendered Sections
    doc.add_heading('Section Summary', level=1)
    doc.add_paragraph(f"Expected Sections: {', '.join(audit.get('expected_sections', []))}")
    doc.add_paragraph(f"Rendered Sections: {', '.join(audit.get('rendered_sections', []))}")
    missing = audit.get('missing_sections', [])
    if missing:
        doc.add_paragraph(f"Missing Sections: {', '.join(missing)}")
    else:
        doc.add_paragraph("No missing sections.")

    # Enhanced Section-by-Section Audit
    section_audits = audit.get('section_audits', [])
    for section in section_audits:
        doc.add_heading(f"Section: {section.get('section', '')}", level=2)
        status = section.get('status', '')
        doc.add_paragraph(f"Status: {status}")
        doc.add_paragraph(f"Reason: {section.get('reason', '')}")
        # Highlight missing findings in Key Findings section
        if section.get('section', '') == 'key_findings' and status == 'missing_findings':
            p = doc.add_paragraph()
            run = p.add_run("WARNING: No findings detected in Key Findings section!")
            run.bold = True
            run.font.color.rgb = (255, 0, 0)
        blocks = section.get('blocks', [])
        if blocks:
            doc.add_heading('Block Details', level=3)
            table = doc.add_table(rows=1, cols=5)
            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = 'Index'
            hdr_cells[1].text = 'Type'
            hdr_cells[2].text = 'Status'
            hdr_cells[3].text = 'Issues'
            hdr_cells[4].text = 'Text'
            for b in blocks:
                row_cells = table.add_row().cells
                row_cells[0].text = str(b.get('index', ''))
                row_cells[1].text = b.get('type', '')
                row_cells[2].text = b.get('status', '')
                row_cells[3].text = ", ".join(b.get('issues', []))
                row_cells[4].text = b.get('text', '')[:100]  # Truncate for readability
        else:
            doc.add_paragraph("No blocks found in this section.")

    # Save to bytes
    from io import BytesIO
    f = BytesIO()
    doc.save(f)
    f.seek(0)
    return f.read()
