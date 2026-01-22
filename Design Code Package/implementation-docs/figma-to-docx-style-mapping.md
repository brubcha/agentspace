# Figma/Tailwind to Word (docx) Style Mapping

This document provides a reference for translating Figma Make and Tailwind CSS styles from the Design Code Package into Word (docx) document styles for downloadable output.

---

## Heading Styles

| Figma/Tailwind Class                  | theme.css Variable     | Word (docx) Style Mapping                          |
| ------------------------------------- | ---------------------- | -------------------------------------------------- |
| text-xl font-bold text-gray-900       | --font-size, --primary | Heading 1: Font size 20pt, Bold, Color #212121     |
| text-lg font-semibold text-gray-800   | --font-size, --primary | Heading 2: Font size 18pt, SemiBold, Color #424242 |
| text-base font-semibold text-gray-700 | --font-size, --primary | Heading 3: Font size 16pt, SemiBold, Color #616161 |
| mb-4 mt-6 (margin)                    | --radius               | Paragraph spacing before/after                     |

---

## Paragraph Styles

| Figma/Tailwind Class                    | theme.css Variable     | Word (docx) Style Mapping                               |
| --------------------------------------- | ---------------------- | ------------------------------------------------------- |
| text-base leading-relaxed text-gray-800 | --font-size, --primary | Normal: Font size 16pt, Color #424242, Line spacing 1.5 |
| mb-4 (margin-bottom)                    | --radius               | Space after paragraph                                   |

---

## Table Styles

| Figma/Tailwind Class               | theme.css Variable     | Word (docx) Style Mapping                    |
| ---------------------------------- | ---------------------- | -------------------------------------------- |
| bg-black text-white font-semibold  | --primary, --card      | Header row: Background #000, Text #fff, Bold |
| border border-gray-300             | --border               | Table border: Color #d1d5db, 0.5pt solid     |
| px-6 py-3 (padding)                | --radius               | Cell padding: 8pt left/right, 6pt top/bottom |
| bg-white / bg-gray-50 (row colors) | --card, --muted        | Alternating row colors: #fff / #f9fafb       |
| text-sm text-gray-800              | --font-size, --primary | Cell text: Font size 14pt, Color #424242     |

---

## Design Tokens

| theme.css Variable | Example Value   | Word (docx) Mapping      |
| ------------------ | --------------- | ------------------------ |
| --font-size        | 16px            | Base font size (16pt)    |
| --primary          | #030213         | Main text color          |
| --secondary        | oklch(0.95 ...) | Accent color             |
| --radius           | 0.625rem        | Table/paragraph spacing  |
| --card             | #ffffff         | Table/section background |

---

## Design Tokens Mapping

| theme.css Variable   | Figma/Tailwind Usage             | Word (docx) Style Mapping            |
| -------------------- | -------------------------------- | ------------------------------------ |
| --font-size          | text-base, text-xl, etc.         | Font size (mapped per section)       |
| --primary            | text-primary, bg-primary         | Main text color, heading color       |
| --secondary          | text-secondary, bg-secondary     | Secondary text color, highlights     |
| --muted              | text-muted, bg-muted             | Muted/secondary backgrounds          |
| --accent             | text-accent, bg-accent           | Accent color for highlights          |
| --card               | bg-card                          | Table/section backgrounds            |
| --border             | border, border-color             | Table borders, cell borders          |
| --radius             | rounded, px-6 py-3               | Table cell/paragraph spacing/padding |
| --font-weight-medium | font-semibold                    | Medium/bold text                     |
| --font-weight-normal | font-normal                      | Normal text                          |
| --destructive        | text-destructive, bg-destructive | Error/alert colors                   |
| --background         | bg-base                          | Page background color                |
| --foreground         | text-base                        | Default text color                   |

---

## Implementation Notes

- In your docx generation code (downloadKitDoc.ts), reference these tokens for colors, font sizes, weights, borders, and spacing.
- Example: Use theme.css --primary for heading colors, --border for table borders, --radius for cell/paragraph spacing.
- For dynamic mapping, consider importing theme.css variables into your code or maintaining a tokens.json for programmatic access.
- Update this mapping as you add or change theme variables.

---

## Implementation Summary (2026-01-21)

- All major theme.css design tokens (colors, font sizes, weights, spacing, radii, borders) are mapped to Word (docx) styles.
- The designTokens.ts object mirrors theme.css and is now used throughout downloadKitDoc.ts for headings, paragraphs, tables, and lists.
- Table headers, cells, and list items use mapped colors, font sizes, and spacing for full design fidelity.
- Page margins are set to 0.5 inch for consistent layout.
- All mapping tables and implementation notes are up to date.

**Next steps:**

- Continue validating output and update tokens/mapping as design evolves.
- Document any new tokens or edge cases as they arise.

---

## Font Mapping (Actual Files)

| Section       | Recommended Font    | Font File(s) Used                              |
| ------------- | ------------------- | ---------------------------------------------- |
| Heading 1     | Inter Bold          | Inter-VariableFont_opsz,wght.ttf               |
| Heading 2     | Montserrat SemiBold | (Add Montserrat font files here if downloaded) |
| Subheading    | Open Sans Medium    | OpenSans-VariableFont_wdth,wght.ttf            |
| Body          | Roboto Regular      | Roboto-VariableFont_wdth.ttf                   |
| Bullets/Lists | Lato Regular        | Lato-Regular.ttf                               |

**Font File Locations:**

- Inter: fonts/Lato-Roboto-opensans-montserrat-inter/Inter/Inter-VariableFont_opsz,wght.ttf
- Lato: fonts/Lato-Roboto-opensans-montserrat-inter/Lato/Lato-Regular.ttf
- Open Sans: fonts/Lato-Roboto-opensans-montserrat-inter/Open_Sans/OpenSans-VariableFont_wdth,wght.ttf
- Roboto: fonts/Lato-Roboto-opensans-montserrat-inter/Roboto/Roboto-VariableFont_wdth.ttf
- Montserrat: (Add Montserrat font files to fonts/Lato-Roboto-opensans-montserrat-inter/Montserrat/)

**Usage:**

- Reference these font files in your docx export logic for each mapped section.
- Update this table if you add more font weights or styles.

---

Use this table as a reference when updating the Word document export logic to match the Figma design.
