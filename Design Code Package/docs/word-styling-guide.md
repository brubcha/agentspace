# Word Document Styling Guide for Marketing Kit Output

This guide translates the React visual design into Word document formatting specifications for AgentSpace's `.docx` output.

---

## Document-Wide Settings

### Page Layout
- **Margins**: 0.5 inches (all sides) - Creates narrow margins matching the Google Doc design
- **Page Size**: US Letter (8.5" × 11")
- **Orientation**: Portrait

### Default Font
- **Font Family**: System default (Calibri or Arial)
- **Base Font Size**: 11pt
- **Line Spacing**: 1.15 (115%)
- **Text Color**: #111827 (dark gray/black)

---

## Block Type Specifications

### 1. Paragraph Block

**Standard Paragraph**
- Font Size: 11pt
- Font Weight: Normal (400)
- Color: #374151 (medium gray)
- Line Height: 1.6
- Spacing After: 12pt
- Spacing Before: 0pt
- Alignment: Left

**Implementation (python-docx):**
```python
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

paragraph = document.add_paragraph(content)
paragraph_format = paragraph.paragraph_format
paragraph_format.space_after = Pt(12)
paragraph_format.line_spacing = 1.6

run = paragraph.runs[0]
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(55, 65, 81)  # #374151
```

---

### 2. Heading Blocks

#### Heading Level 2 (Main Section Titles)
- Font Size: 30pt
- Font Weight: Bold (700)
- Color: #111827 (near black)
- Spacing Before: 24pt
- Spacing After: 16pt
- Border Bottom: 2pt solid #E5E7EB (light gray)

**Implementation:**
```python
heading = document.add_heading(level=2)
heading.text = content
heading_format = heading.paragraph_format
heading_format.space_before = Pt(24)
heading_format.space_after = Pt(16)

run = heading.runs[0]
run.font.size = Pt(30)
run.font.bold = True
run.font.color.rgb = RGBColor(17, 24, 39)

# Add bottom border (requires direct XML manipulation or table workaround)
```

#### Heading Level 3 (Subsection Titles)
- Font Size: 20pt (1.25rem)
- Font Weight: Bold (700)
- Color: #111827
- Spacing Before: 18pt
- Spacing After: 12pt

**Implementation:**
```python
heading = document.add_heading(level=3)
heading.text = content
heading_format = heading.paragraph_format
heading_format.space_before = Pt(18)
heading_format.space_after = Pt(12)

run = heading.runs[0]
run.font.size = Pt(20)
run.font.bold = True
run.font.color.rgb = RGBColor(17, 24, 39)
```

#### Heading Level 4 (Sub-subsection Titles)
- Font Size: 18pt (1.125rem)
- Font Weight: Semibold (600)
- Color: #1F2937 (dark gray)
- Spacing Before: 15pt
- Spacing After: 9pt

**Implementation:**
```python
heading = document.add_heading(level=4)
heading.text = content
heading_format = heading.paragraph_format
heading_format.space_before = Pt(15)
heading_format.space_after = Pt(9)

run = heading.runs[0]
run.font.size = Pt(18)
run.font.bold = True
run.font.color.rgb = RGBColor(31, 41, 55)
```

#### Heading Level 5 (Minor Subsection Titles)
- Font Size: 16pt (1rem)
- Font Weight: Semibold (600)
- Color: #374151 (medium gray)
- Spacing Before: 12pt
- Spacing After: 6pt

**Implementation:**
```python
heading = document.add_heading(level=5)
heading.text = content
heading_format = heading.paragraph_format
heading_format.space_before = Pt(12)
heading_format.space_after = Pt(6)

run = heading.runs[0]
run.font.size = Pt(16)
run.font.bold = True
run.font.color.rgb = RGBColor(55, 65, 81)
```

---

### 3. Bullets Block

**Standard Bullet List**
- Bullet Style: Solid disc (•)
- Font Size: 11pt
- Color: #374151
- Left Indent: 0.25 inches
- Line Height: 1.6
- Spacing Between Items: 6pt

**Rich Text Bullets (with bold/inline formatting)**
- Supports **bold text** inline
- Bold portions use Font Weight: 600
- Maintains same spacing as standard bullets

**Implementation:**
```python
# Simple bullet
paragraph = document.add_paragraph(item_text, style='List Bullet')
paragraph_format = paragraph.paragraph_format
paragraph_format.space_after = Pt(6)
paragraph_format.line_spacing = 1.6

run = paragraph.runs[0]
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(55, 65, 81)

# Rich text bullet with bold
paragraph = document.add_paragraph(style='List Bullet')
# Add normal text
run1 = paragraph.add_run("Summary")
run1.font.bold = True
run1.font.size = Pt(11)
# Add rest
run2 = paragraph.add_run(", show a before-after...")
run2.font.size = Pt(11)
run2.font.color.rgb = RGBColor(55, 65, 81)
```

---

### 4. Numbered List Block

**Numbered List Format**
- Number Style: 01, 02, 03, etc. (two-digit with leading zero)
- Font Size: 11pt
- Font Weight: Bold for number, normal for text
- Color: #111827
- Left Indent: 0.5 inches
- Hanging Indent: 0.25 inches
- Spacing After Each Item: 16pt

**Title Format (within each numbered item)**
- Font Weight: Bold (700)
- Font Size: 18pt
- Color: #111827
- Spacing After Title: 8pt

**Description Format**
- Font Weight: Normal
- Font Size: 11pt
- Color: #374151

**Implementation:**
```python
# Create numbered list with custom format
for index, item in enumerate(items, 1):
    # Number paragraph
    num_para = document.add_paragraph()
    num_run = num_para.add_run(f"{index:02d} ")
    num_run.font.bold = True
    num_run.font.size = Pt(11)
    num_run.font.color.rgb = RGBColor(17, 24, 39)
    
    # Title on same line
    title_run = num_para.add_run(item['title'])
    title_run.font.bold = True
    title_run.font.size = Pt(18)
    title_run.font.color.rgb = RGBColor(17, 24, 39)
    
    # Description paragraph
    desc_para = document.add_paragraph(item['description'])
    desc_para.paragraph_format.left_indent = Pt(36)  # 0.5 inches
    desc_para.paragraph_format.space_after = Pt(16)
    
    desc_run = desc_para.runs[0]
    desc_run.font.size = Pt(11)
    desc_run.font.color.rgb = RGBColor(55, 65, 81)
```

---

### 5. Table Block

**Table Structure**
- Border: 1pt solid #D1D5DB (light gray)
- Cell Padding: 12pt (all sides)
- Width: 100% of page width

**Header Row**
- Background Color: #111827 (near black)
- Text Color: #FFFFFF (white)
- Font Weight: Semibold (600)
- Font Size: 11pt
- Text Transform: Uppercase
- Letter Spacing: 0.05em (slight tracking)

**Data Rows**
- Background Color: Alternating white (#FFFFFF) and very light gray (#F9FAFB)
- Text Color: #374151
- Font Size: 11pt
- Font Weight: Normal
- Vertical Alignment: Top

**Implementation:**
```python
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# Create table
table = document.add_table(rows=len(data)+1, cols=len(headers))
table.style = 'Table Grid'

# Header row
header_row = table.rows[0]
for idx, header_text in enumerate(headers):
    cell = header_row.cells[idx]
    cell.text = header_text.upper()
    
    # Header styling
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), '111827')  # Black background
    cell._element.get_or_add_tcPr().append(shading_elm)
    
    paragraph = cell.paragraphs[0]
    run = paragraph.runs[0]
    run.font.color.rgb = RGBColor(255, 255, 255)  # White text
    run.font.bold = True
    run.font.size = Pt(11)

# Data rows with alternating background
for row_idx, row_data in enumerate(data, 1):
    row = table.rows[row_idx]
    
    # Alternating row color
    bg_color = 'FFFFFF' if row_idx % 2 == 1 else 'F9FAFB'
    
    for col_idx, cell_text in enumerate(row_data):
        cell = row.cells[col_idx]
        cell.text = cell_text
        
        # Cell background
        shading_elm = OxmlElement('w:shd')
        shading_elm.set(qn('w:fill'), bg_color)
        cell._element.get_or_add_tcPr().append(shading_elm)
        
        # Cell text styling
        paragraph = cell.paragraphs[0]
        run = paragraph.runs[0]
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(55, 65, 81)
        
        # Vertical alignment
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
```

---

### 6. Checklist Block

**Visual Design:**
- Each item has a green checkmark (✓) followed by text
- Checkmark Color: #10B981 (green)
- Checkmark Size: 14pt
- Text starts 8pt after checkmark
- Spacing Between Items: 8pt

**Implementation:**
```python
for item in checklist_items:
    paragraph = document.add_paragraph()
    
    # Green checkmark
    check_run = paragraph.add_run("✓ ")
    check_run.font.color.rgb = RGBColor(16, 185, 129)  # Green
    check_run.font.size = Pt(14)
    check_run.font.bold = True
    
    # Item text
    text_run = paragraph.add_run(item)
    text_run.font.size = Pt(11)
    text_run.font.color.rgb = RGBColor(55, 65, 81)
    
    paragraph.paragraph_format.space_after = Pt(8)
    paragraph.paragraph_format.line_spacing = 1.6
```

---

### 7. Subsection Block

**Container Format:**
- Background Color: #F9FAFB (very light gray)
- Border Left: 3pt solid #E5E7EB (light gray accent)
- Padding: 16pt (all sides)
- Margin Bottom: 16pt

**Title Format:**
- Font Size: 16pt
- Font Weight: Semibold (600)
- Color: #111827
- Spacing After: 12pt

**Content:**
- Inherits all standard block formatting within the subsection

**Implementation:**
```python
# Word doesn't have direct "container" concept
# Use a single-cell table as a workaround

table = document.add_table(rows=1, cols=1)
cell = table.rows[0].cells[0]

# Cell background and border
shading_elm = OxmlElement('w:shd')
shading_elm.set(qn('w:fill'), 'F9FAFB')
cell._element.get_or_add_tcPr().append(shading_elm)

# Left border (3pt gray)
tc_borders = OxmlElement('w:tcBorders')
left_border = OxmlElement('w:left')
left_border.set(qn('w:val'), 'single')
left_border.set(qn('w:sz'), '18')  # 3pt = 18 eighths of a point
left_border.set(qn('w:color'), 'E5E7EB')
tc_borders.append(left_border)
cell._element.get_or_add_tcPr().append(tc_borders)

# Add title
title_para = cell.add_paragraph(title_text)
title_run = title_para.runs[0]
title_run.font.size = Pt(16)
title_run.font.bold = True
title_run.font.color.rgb = RGBColor(17, 24, 39)
title_para.paragraph_format.space_after = Pt(12)

# Add content blocks within the cell
# (add paragraphs, bullets, etc. to the cell)
```

---

### 8. Opportunity Cards Block

**Card Design (4 cards in Opportunity Areas section):**
- Layout: Each card in a 2-column table (icon column + content column)
- Icon Column Width: 60pt
- Content Column Width: Remaining width
- Border: 1pt solid #E5E7EB
- Cell Padding: 16pt

**Orange Circle Icon:**
- Shape: Circle
- Diameter: 40pt
- Background Color: #F97316 (orange)
- Contains: White number (01, 02, 03, 04)
- Number Font: 16pt, Bold, White (#FFFFFF)

**Title Format:**
- Font Size: 16pt
- Font Weight: Bold (700)
- Color: #111827
- Spacing After: 8pt

**Description Format:**
- Font Size: 11pt
- Color: #374151
- Line Height: 1.6

**Implementation:**
```python
# Create 2-column table for each card
for index, card in enumerate(cards, 1):
    table = document.add_table(rows=1, cols=2)
    
    # Icon cell
    icon_cell = table.rows[0].cells[0]
    icon_cell.width = Pt(60)
    
    # Add orange circle with number (use text box or shape)
    # Note: python-docx has limited shape support, may need workaround
    icon_para = icon_cell.paragraphs[0]
    icon_run = icon_para.add_run(f" {index:02d} ")
    icon_run.font.size = Pt(16)
    icon_run.font.bold = True
    icon_run.font.color.rgb = RGBColor(255, 255, 255)
    
    # Orange background (use highlighting or shading)
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), 'F97316')
    icon_para._element.get_or_add_pPr().append(shading)
    icon_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Content cell
    content_cell = table.rows[0].cells[1]
    
    # Title
    title_para = content_cell.add_paragraph(card['title'])
    title_run = title_para.runs[0]
    title_run.font.size = Pt(16)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(17, 24, 39)
    title_para.paragraph_format.space_after = Pt(8)
    
    # Description
    desc_para = content_cell.add_paragraph(card['description'])
    desc_run = desc_para.runs[0]
    desc_run.font.size = Pt(11)
    desc_run.font.color.rgb = RGBColor(55, 65, 81)
    
    # Add spacing after card
    document.add_paragraph().paragraph_format.space_after = Pt(12)
```

**Alternative Simpler Implementation:**
```python
# Use emoji or bullet with orange color instead of circle shape
for index, card in enumerate(cards, 1):
    para = document.add_paragraph()
    
    # Orange number
    num_run = para.add_run(f"{index:02d} ")
    num_run.font.color.rgb = RGBColor(249, 115, 22)  # Orange
    num_run.font.size = Pt(16)
    num_run.font.bold = True
    
    # Title
    title_run = para.add_run(card['title'])
    title_run.font.bold = True
    title_run.font.size = Pt(16)
    
    # Description on next line
    desc_para = document.add_paragraph(card['description'])
    desc_para.paragraph_format.left_indent = Pt(36)
    desc_para.paragraph_format.space_after = Pt(12)
```

---

### 9. Archetype Card Block

**Card Design (2 gradient cards in Brand Archetypes section):**

**Primary Archetype Card (Orange Gradient):**
- Background: Linear gradient from #F97316 (orange) to #FB923C (lighter orange)
- Border Radius: 12pt (rounded corners - limited support in Word)
- Padding: 20pt
- Border: 1pt solid #EA580C (darker orange)

**Secondary Archetype Card (Green Gradient):**
- Background: Linear gradient from #10B981 (green) to #34D399 (lighter green)
- Border Radius: 12pt
- Padding: 20pt
- Border: 1pt solid #059669 (darker green)

**Icon:**
- Size: 32pt
- Color: White (#FFFFFF)
- Spacing After: 12pt

**Title:**
- Font Size: 20pt
- Font Weight: Bold (700)
- Color: White (#FFFFFF)
- Spacing After: 12pt

**Content:**
- Font Size: 11pt
- Color: White (#FFFFFF) with 95% opacity
- Line Height: 1.6
- Spacing After: 16pt

**Metadata (Mission, Voice, Values, Emotional Promise):**
- Label Font Weight: Bold
- Label Color: White with 90% opacity
- Value Color: White with 95% opacity
- Spacing Between Items: 8pt

**Implementation:**
```python
# Use single-cell table with colored background
# Note: Word doesn't support gradients natively, use solid color approximation

# Primary (Orange)
table = document.add_table(rows=1, cols=1)
cell = table.rows[0].cells[0]

# Orange background (use middle gradient color)
shading = OxmlElement('w:shd')
shading.set(qn('w:fill'), 'FA8C3A')  # Average of gradient colors
cell._element.get_or_add_tcPr().append(shading)

# Add border
tc_borders = OxmlElement('w:tcBorders')
for border_name in ['top', 'left', 'bottom', 'right']:
    border = OxmlElement(f'w:{border_name}')
    border.set(qn('w:val'), 'single')
    border.set(qn('w:sz'), '6')  # 1pt
    border.set(qn('w:color'), 'EA580C')
    tc_borders.append(border)
cell._element.get_or_add_tcPr().append(tc_borders)

# Icon (use emoji or special character)
icon_para = cell.add_paragraph("🏗️")  # Or appropriate icon
icon_para.runs[0].font.size = Pt(32)
icon_para.paragraph_format.space_after = Pt(12)

# Title
title_para = cell.add_paragraph("Primary: Architect (System Builder)")
title_run = title_para.runs[0]
title_run.font.size = Pt(20)
title_run.font.bold = True
title_run.font.color.rgb = RGBColor(255, 255, 255)
title_para.paragraph_format.space_after = Pt(12)

# Description
desc_para = cell.add_paragraph(description_text)
desc_run = desc_para.runs[0]
desc_run.font.size = Pt(11)
desc_run.font.color.rgb = RGBColor(255, 255, 255)
desc_para.paragraph_format.space_after = Pt(16)

# Metadata
metadata = [
    ("Mission:", mission_text),
    ("Voice:", voice_text),
    ("Values:", values_text),
    ("Emotional Promise:", promise_text)
]

for label, value in metadata:
    meta_para = cell.add_paragraph()
    
    # Bold label
    label_run = meta_para.add_run(label)
    label_run.font.bold = True
    label_run.font.size = Pt(11)
    label_run.font.color.rgb = RGBColor(255, 255, 255)
    
    # Value
    value_run = meta_para.add_run(f" {value}")
    value_run.font.size = Pt(11)
    value_run.font.color.rgb = RGBColor(255, 255, 255)
    
    meta_para.paragraph_format.space_after = Pt(8)
```

**Simplified Alternative:**
```python
# Use shaded paragraph with no table
paragraph = document.add_paragraph()

# Apply orange background to entire paragraph
shading = OxmlElement('w:shd')
shading.set(qn('w:fill'), 'FA8C3A')
paragraph._element.get_or_add_pPr().append(shading)

# Add all content as runs within the paragraph
# (Less flexible but simpler)
```

---

### 10. Two-Column Layout Block

**Used for:** Archetype cards side-by-side

**Layout:**
- 2-column table structure
- Equal column widths (50% each)
- Gap between columns: 16pt
- No visible borders

**Implementation:**
```python
# Create 2-column table
table = document.add_table(rows=1, cols=2)
table.style = 'Table Grid'
table.autofit = False
table.allow_autofit = False

# Remove borders
for row in table.rows:
    for cell in row.cells:
        tc_pr = cell._element.get_or_add_tcPr()
        tc_borders = OxmlElement('w:tcBorders')
        for border in ['top', 'left', 'bottom', 'right']:
            border_el = OxmlElement(f'w:{border}')
            border_el.set(qn('w:val'), 'none')
            tc_borders.append(border_el)
        tc_pr.append(tc_borders)

# Add content to each cell
left_cell = table.rows[0].cells[0]
right_cell = table.rows[0].cells[1]

# Insert archetype cards into each cell
```

---

## Color Palette Reference

### Primary Colors
- **Near Black**: #111827 (RGB: 17, 24, 39) - Main headings, numbers
- **Dark Gray**: #1F2937 (RGB: 31, 41, 55) - H4 headings
- **Medium Gray**: #374151 (RGB: 55, 65, 81) - Body text, H5 headings
- **Light Gray**: #6B7280 (RGB: 107, 114, 128) - Secondary text
- **Very Light Gray**: #F9FAFB (RGB: 249, 250, 251) - Backgrounds
- **Border Gray**: #E5E7EB (RGB: 229, 231, 235) - Borders, dividers
- **Lighter Border Gray**: #D1D5DB (RGB: 209, 213, 219) - Table borders

### Accent Colors
- **Orange**: #F97316 (RGB: 249, 115, 22) - Opportunity cards, primary archetype
- **Light Orange**: #FB923C (RGB: 251, 146, 60) - Gradient end
- **Dark Orange**: #EA580C (RGB: 234, 88, 12) - Borders
- **Green**: #10B981 (RGB: 16, 185, 129) - Checkmarks, secondary archetype
- **Light Green**: #34D399 (RGB: 52, 211, 153) - Gradient end
- **Dark Green**: #059669 (RGB: 5, 150, 105) - Borders

### Text Colors
- **Primary Text**: #111827
- **Body Text**: #374151
- **White Text**: #FFFFFF (RGB: 255, 255, 255) - On colored backgrounds

---

## Special Formatting Notes

### Rich Text Support
Many blocks support mixed formatting within a single item:
- **Bold text** inline with normal text
- Separate runs for different styles
- Maintain consistent spacing

### Spacing Consistency
- Maintain breathing room between sections
- Standard bottom spacing: 12pt for paragraphs
- Larger spacing (16-24pt) between major sections
- Consistent line height: 1.6 for readability

### Typography Hierarchy
1. **H2** (30pt) - Major sections with bottom border
2. **H3** (20pt) - Subsections
3. **H4** (18pt) - Sub-subsections
4. **H5** (16pt) - Minor divisions
5. **Body** (11pt) - All content text

---

## Python Library Recommendations

### Primary: `python-docx`
```bash
pip install python-docx
```

**Pros:**
- Most popular and well-documented
- Good for basic formatting
- Easy to learn

**Cons:**
- Limited shape/gradient support
- Complex border/shading requires XML manipulation
- No native gradient backgrounds

### For Advanced Formatting: `docx` + direct XML manipulation
```python
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
```

### Alternative: `docxcompose` (for merging multiple documents)
Useful if generating sections separately and combining.

---

## Testing Checklist

When implementing Word output, verify:

- [ ] Margins are 0.5" (narrow)
- [ ] All heading levels render at correct sizes
- [ ] Tables have black headers with white text
- [ ] Alternating row colors in tables
- [ ] Orange numbered circles visible in Opportunity Areas
- [ ] Green checkmarks visible in Key Findings
- [ ] Archetype cards have colored backgrounds (orange/green)
- [ ] All text colors match specification
- [ ] Spacing between sections is consistent
- [ ] Bullet points are properly indented
- [ ] Rich text formatting (bold) renders correctly
- [ ] Document opens correctly in Microsoft Word
- [ ] Document opens correctly in Google Docs
- [ ] Font sizes are readable and match visual design

---

## Example: Complete Block Implementation

Here's a complete example for the "Key Findings" section showing all 6 numbered items:

```python
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

document = Document()

# Set document margins
sections = document.sections
for section in sections:
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

# Section heading (H2)
heading = document.add_heading('Key Findings', level=2)
heading_format = heading.paragraph_format
heading_format.space_before = Pt(24)
heading_format.space_after = Pt(16)
run = heading.runs[0]
run.font.size = Pt(30)
run.font.bold = True
run.font.color.rgb = RGBColor(17, 24, 39)

# Key Findings data
findings = [
    {
        "title": "Fragmentation is the Core Problem",
        "description": "Most businesses piece together agencies, consultants, and disconnected tools. This creates silos, wasted spend, and stalled execution. Swift was designed to remove fragmentation by embedding all disciplines under one roof."
    },
    {
        "title": "Independence is Reshaping Work",
        "description": "By 2027, 60% of the workforce will be independent, and most companies already outsource or hire globally. Swift's model embraces this shift, connecting distributed expertise into a unified system."
    },
    # ... (remaining 4 items)
]

# Render each finding
for index, finding in enumerate(findings, 1):
    # Title with number
    title_para = document.add_paragraph()
    
    # Number (bold)
    num_run = title_para.add_run(f"{index:02d} ")
    num_run.font.bold = True
    num_run.font.size = Pt(18)
    num_run.font.color.rgb = RGBColor(17, 24, 39)
    
    # Title (bold)
    title_run = title_para.add_run(finding['title'])
    title_run.font.bold = True
    title_run.font.size = Pt(18)
    title_run.font.color.rgb = RGBColor(17, 24, 39)
    
    title_para.paragraph_format.space_before = Pt(12)
    title_para.paragraph_format.space_after = Pt(8)
    
    # Description as bullet point
    desc_para = document.add_paragraph(finding['description'], style='List Bullet')
    desc_run = desc_para.runs[0]
    desc_run.font.size = Pt(11)
    desc_run.font.color.rgb = RGBColor(55, 65, 81)
    
    desc_para.paragraph_format.left_indent = Pt(36)
    desc_para.paragraph_format.space_after = Pt(16)
    desc_para.paragraph_format.line_spacing = 1.6

# Save
document.save('marketing_kit_key_findings.docx')
```

---

## Quick Reference Chart

| Element | Font Size | Weight | Color | Spacing After |
|---------|-----------|--------|-------|---------------|
| H2 | 30pt | Bold | #111827 | 16pt |
| H3 | 20pt | Bold | #111827 | 12pt |
| H4 | 18pt | Semibold | #1F2937 | 9pt |
| H5 | 16pt | Semibold | #374151 | 6pt |
| Body Text | 11pt | Normal | #374151 | 12pt |
| Bullet Item | 11pt | Normal | #374151 | 6pt |
| Table Header | 11pt | Semibold | #FFFFFF on #111827 | - |
| Table Cell | 11pt | Normal | #374151 | - |
| Checklist | 11pt | Normal | #374151 (✓ is #10B981) | 8pt |

---

## Contact & Updates

This specification is based on the React visual design built in Figma Make. If you need clarification on any styling detail or encounter implementation challenges with `python-docx`, refer back to the live React application as the source of truth for visual design.

**Last Updated:** January 2025
