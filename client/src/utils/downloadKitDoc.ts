import { saveAs } from "file-saver";
import {
  Document,
  Packer,
  Paragraph,
  HeadingLevel,
  TextRun,
  Table,
  TableRow,
  TableCell,
  WidthType,
  AlignmentType,
} from "docx";
import { designTokens } from "./designTokens";
// @ts-ignore
import { lexer } from "marked";

// Helper to split text into TextRuns for bold (**...**)
function parseBold(text: string, baseStyle: any = {}): TextRun[] {
  const runs: TextRun[] = [];
  let lastIndex = 0;
  const boldRegex = /\*\*(.*?)\*\*/g;
  let match;
  while ((match = boldRegex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      runs.push(
        new TextRun({ text: text.slice(lastIndex, match.index), ...baseStyle }),
      );
    }
    runs.push(new TextRun({ text: match[1], bold: true, ...baseStyle }));
    lastIndex = match.index + match[0].length;
  }
  if (lastIndex < text.length) {
    runs.push(new TextRun({ text: text.slice(lastIndex), ...baseStyle }));
  }
  return runs;
}

// Helper: Convert markdown string to docx Paragraph/TextRun array
function markdownToDocxParagraphs(md: string): Paragraph[] {
  const tokens = lexer(md);
  const paragraphs: Paragraph[] = [];
  tokens.forEach((token: any) => {
    if (token.type === "heading") {
      const level = token.depth;
      paragraphs.push(
        new Paragraph({
          children: parseBold(token.text, {
            bold: level <= 3,
            color:
              level === 1
                ? designTokens.colors.heading1
                : level === 2
                  ? designTokens.colors.heading2
                  : designTokens.colors.subhead,
            size:
              level === 1
                ? designTokens.fontSize.heading1
                : level === 2
                  ? designTokens.fontSize.heading2
                  : designTokens.fontSize.subhead,
            font:
              level === 1 ? "Inter" : level === 2 ? "Montserrat" : "Open Sans",
          }),
          heading:
            level === 1
              ? HeadingLevel.HEADING_1
              : level === 2
                ? HeadingLevel.HEADING_2
                : HeadingLevel.HEADING_3,
          spacing: {
            before:
              level === 1
                ? designTokens.spacing.heading1Before
                : level === 2
                  ? designTokens.spacing.heading2Before
                  : designTokens.spacing.subheadBefore,
            after:
              level === 1
                ? designTokens.spacing.heading1After
                : level === 2
                  ? designTokens.spacing.heading2After
                  : designTokens.spacing.subheadAfter,
          },
        }),
      );
    } else if (token.type === "paragraph") {
      paragraphs.push(
        new Paragraph({
          children: parseBold(token.text, {
            color: designTokens.colors.foreground,
            size: designTokens.fontSize.base,
            font: "Roboto",
          }),
          spacing: { after: designTokens.spacing.paragraphAfter },
          alignment: AlignmentType.LEFT,
        }),
      );
    } else if (token.type === "list") {
      token.items.forEach((item: any) => {
        paragraphs.push(
          new Paragraph({
            children: [
              ...parseBold("• ", {
                color: designTokens.colors.foreground,
                size: designTokens.fontSize.base,
                font: "Lato",
              }),
              ...parseBold(item.text, {
                color: designTokens.colors.foreground,
                size: designTokens.fontSize.base,
                font: "Lato",
              }),
            ],
            spacing: { after: designTokens.spacing.bulletAfter },
            alignment: AlignmentType.LEFT,
          }),
        );
      });
    }
    // Add more token types as needed (blockquote, code, etc.)
  });
  return paragraphs;
}

export function downloadKitDoc(kitData: any, filename = "marketing_kit.docx") {
  if (!kitData) return;
  const children: any[] = [];
  // Title (Heading 1 style)
  children.push(
    new Paragraph({
      children: [
        new TextRun({
          text: "Marketing Kit",
          bold: true,
          color: designTokens.colors.heading1,
          size: designTokens.fontSize.heading1,
          font: "Inter",
        }),
      ],
      heading: HeadingLevel.HEADING_1,
      spacing: {
        before: designTokens.spacing.heading1Before,
        after: designTokens.spacing.heading1After,
      },
    }),
  );

  // Ensure all required sections are present (based on template spec/example)
  const requiredSections = [
    "Overview",
    "The Goal",
    "Opportunity Areas",
    "Key Findings",
    "Market Landscape",
    "Audience & User Personas",
    "B2B Industry Targets",
    "Brand Archetypes",
    "Brand Voice",
    "Content",
    "Social Strategy",
    "Engagement Framework",
    "References",
    "Engagement Index",
  ];
  if (kitData.document && Array.isArray(kitData.document.sections)) {
    // Build a map of present section titles (case-insensitive)
    const presentSections = new Set(
      kitData.document.sections.map((s: any) =>
        (s.title || s.id || "").toLowerCase(),
      ),
    );
    // Add missing sections as empty
    requiredSections.forEach((title) => {
      if (!presentSections.has(title.toLowerCase())) {
        kitData.document.sections.push({
          title,
          id: title.replace(/\s+/g, "_").toLowerCase(),
          blocks: [],
        });
      }
    });
    // Sort sections to match required order
    kitData.document.sections.sort((a: any, b: any) => {
      const aIdx = requiredSections.findIndex(
        (t) => t.toLowerCase() === (a.title || a.id || "").toLowerCase(),
      );
      const bIdx = requiredSections.findIndex(
        (t) => t.toLowerCase() === (b.title || b.id || "").toLowerCase(),
      );
      return aIdx - bIdx;
    });
    // Render each section
    kitData.document.sections.forEach((section: any) => {
      // Section Heading (Heading 2 style)
      children.push(
        new Paragraph({
          children: [
            new TextRun({
              text: section.title || section.id,
              bold: true,
              color: designTokens.colors.heading2,
              size: designTokens.fontSize.heading2,
              font: "Montserrat",
            }),
          ],
          heading: HeadingLevel.HEADING_2,
          spacing: {
            before: designTokens.spacing.heading2Before,
            after: designTokens.spacing.heading2After,
          },
        }),
      );
      if (Array.isArray(section.blocks)) {
        section.blocks.forEach((block: any) => {
          // Remove [REVIEW] tags and skip empty review blocks
          if (block.type === "Paragraph" && block.text && block.text.trim().startsWith("[REVIEW]")) {
            // If the rest is empty or just markdown heading, skip
            const cleaned = block.text.replace(/^\[REVIEW\]\s*/i, "").trim();
            if (!cleaned || cleaned === "###" || cleaned === "##" || cleaned === "#") {
              return; // skip this block
            }
            block.text = cleaned;
          }
          if (block.type === "Paragraph") {
            // If block.text contains markdown, parse and convert to styled docx
            if (
              block.text &&
              (block.text.includes("##") ||
                block.text.includes("**") ||
                block.text.includes("* "))
            ) {
              markdownToDocxParagraphs(block.text).forEach((p) =>
                children.push(p),
              );
            } else {
              children.push(
                new Paragraph({
                  children: [
                    new TextRun({
                      text: block.text || "",
                      color: designTokens.colors.foreground,
                      size: designTokens.fontSize.base,
                      font: "Roboto",
                    }),
                  ],
                  spacing: { after: designTokens.spacing.paragraphAfter },
                  alignment: AlignmentType.LEFT,
                })
              );
            }
          } else if (block.type === "Bullets" && Array.isArray(block.items)) {
            // Bullets/List items with bold parsing
            block.items.forEach((item: string) => {
              children.push(
                new Paragraph({
                  children: [
                    ...parseBold("• ", {
                      color: designTokens.colors.foreground,
                      size: designTokens.fontSize.base,
                      font: "Lato",
                    }),
                    ...parseBold(item, {
                      color: designTokens.colors.foreground,
                      size: designTokens.fontSize.base,
                      font: "Lato",
                    }),
                  ],
                  spacing: { after: designTokens.spacing.bulletAfter },
                  alignment: AlignmentType.LEFT,
                }),
              );
            });
          } else if (block.type === "Subhead") {
            children.push(
              new Paragraph({
                children: [
                  new TextRun({
                    text: block.text || "",
                    bold: true,
                    color: designTokens.colors.subhead,
                    size: designTokens.fontSize.subhead,
                    font: "Open Sans",
                  }),
                ],
                heading: HeadingLevel.HEADING_3,
                spacing: {
                  before: designTokens.spacing.subheadBefore,
                  after: designTokens.spacing.subheadAfter,
                },
              }),
            );
          } else if (
            block.type === "ListOfSections" &&
            Array.isArray(block.section_titles)
          ) {
            children.push(
              new Paragraph({
                children: [
                  new TextRun({
                    text: "Sections Included:",
                    bold: true,
                    color: designTokens.colors.subhead,
                    size: designTokens.fontSize.subhead,
                    font: "Open Sans",
                  }),
                ],
                heading: HeadingLevel.HEADING_3,
                spacing: {
                  before: designTokens.spacing.subheadBefore,
                  after: designTokens.spacing.subheadAfter,
                },
              }),
            );
            block.section_titles.forEach((title: string) => {
              children.push(
                new Paragraph({
                  children: [
                    new TextRun({
                      text: `- ${title}`,
                      color: designTokens.colors.foreground,
                      size: designTokens.fontSize.base,
                      font: "Lato",
                    }),
                  ],
                  spacing: { after: designTokens.spacing.sectionTitleAfter },
                  alignment: AlignmentType.LEFT,
                }),
              );
            });
          } else if (
            block.type === "Table" &&
            Array.isArray(block.rows) &&
            Array.isArray(block.columns)
          ) {
            // Table with mapped styles
            children.push(
              new Paragraph({
                children: [
                  new TextRun({
                    text: block.title || "Table",
                    bold: true,
                    color: designTokens.colors.subhead,
                    size: designTokens.fontSize.subhead,
                    font: "Open Sans",
                  }),
                ],
                heading: HeadingLevel.HEADING_3,
                spacing: {
                  before: designTokens.spacing.subheadBefore,
                  after: designTokens.spacing.subheadAfter,
                },
              }),
            );
            // Build table rows
            const tableRows = [];
            // Header row
            tableRows.push(
              new TableRow({
                children: block.columns.map(
                  (col: string) =>
                    new TableCell({
                      children: [
                        new Paragraph({
                          children: [
                            new TextRun({
                              text: col,
                              bold: true,
                              color: designTokens.colors.tableHeaderFg,
                              size: designTokens.fontSize.tableHeader,
                              font: "Open Sans",
                            }),
                          ],
                          alignment: AlignmentType.LEFT,
                        }),
                      ],
                      shading: { fill: designTokens.colors.tableHeaderBg },
                      margins: {
                        top: designTokens.spacing.tableCellPadding,
                        bottom: designTokens.spacing.tableCellPadding,
                        left: designTokens.spacing.tableCellPadding,
                        right: designTokens.spacing.tableCellPadding,
                      },
                      borders: {
                        top: {
                          color: designTokens.colors.border,
                          size: 4,
                          style: "single",
                        },
                        bottom: {
                          color: designTokens.colors.border,
                          size: 4,
                          style: "single",
                        },
                        left: {
                          color: designTokens.colors.border,
                          size: 4,
                          style: "single",
                        },
                        right: {
                          color: designTokens.colors.border,
                          size: 4,
                          style: "single",
                        },
                      },
                      width: { size: 1000, type: WidthType.DXA },
                    }),
                ),
              }),
            );
            // Data rows
            block.rows.forEach((row: any[], rowIndex: number) => {
              tableRows.push(
                new TableRow({
                  children: row.map(
                    (cell: string) =>
                      new TableCell({
                        children: [
                          new Paragraph({
                            children: [
                              new TextRun({
                                text: cell,
                                color: designTokens.colors.foreground,
                                size: designTokens.fontSize.tableCell,
                                font: "Roboto",
                              }),
                            ],
                            alignment: AlignmentType.LEFT,
                          }),
                        ],
                        shading: {
                          fill:
                            rowIndex % 2 === 0
                              ? designTokens.colors.tableRow
                              : designTokens.colors.tableRowAlt,
                        },
                        margins: {
                          top: designTokens.spacing.tableCellPadding,
                          bottom: designTokens.spacing.tableCellPadding,
                          left: designTokens.spacing.tableCellPadding,
                          right: designTokens.spacing.tableCellPadding,
                        },
                        borders: {
                          top: {
                            color: designTokens.colors.border,
                            size: 4,
                            style: "single",
                          },
                          bottom: {
                            color: designTokens.colors.border,
                            size: 4,
                            style: "single",
                          },
                          left: {
                            color: designTokens.colors.border,
                            size: 4,
                            style: "single",
                          },
                          right: {
                            color: designTokens.colors.border,
                            size: 4,
                            style: "single",
                          },
                        },
                        width: { size: 1000, type: WidthType.DXA },
                      }),
                  ),
                }),
              );
            });
            children.push(
              new Table({
                rows: tableRows,
                width: { size: 10000, type: WidthType.DXA },
              }),
            );
          }
          // Handle StaticEngagementIndexTables blocks
          else if (
            block.type === "StaticEngagementIndexTables" &&
            Array.isArray(block.tables)
          ) {
            block.tables.forEach((table: any) => {
              children.push(
                new Paragraph({
                  children: [
                    new TextRun({
                      text: table.title || "Table",
                      bold: true,
                      color: designTokens.colors.subhead,
                      size: designTokens.fontSize.subhead,
                      font: "Open Sans",
                    }),
                  ],
                  heading: HeadingLevel.HEADING_3,
                  spacing: {
                    before: designTokens.spacing.subheadBefore,
                    after: designTokens.spacing.subheadAfter,
                  },
                }),
              );
              // Table header
              const tableRows = [];
              if (Array.isArray(table.columns)) {
                tableRows.push(
                  new TableRow({
                    children: table.columns.map(
                      (col: string) =>
                        new TableCell({
                          children: [
                            new Paragraph({
                              children: [
                                new TextRun({
                                  text: col,
                                  bold: true,
                                  color: "FFFFFF",
                                  size: designTokens.fontSize.tableHeader,
                                  font: "Open Sans",
                                }),
                              ],
                              alignment: AlignmentType.LEFT,
                            }),
                          ],
                          shading: { fill: "000000" },
                          margins: {
                            top: 120,
                            bottom: 120,
                            left: 160,
                            right: 160,
                          },
                          borders: {
                            top: { color: "d1d5db", size: 4, style: "single" },
                            bottom: {
                              color: "d1d5db",
                              size: 4,
                              style: "single",
                            },
                            left: { color: "d1d5db", size: 4, style: "single" },
                            right: {
                              color: "d1d5db",
                              size: 4,
                              style: "single",
                            },
                          },
                          width: { size: 1000, type: WidthType.DXA },
                        }),
                    ),
                  }),
                );
              }
              // Table rows
              if (Array.isArray(table.rows)) {
                table.rows.forEach((row: any[], rowIndex: number) => {
                  tableRows.push(
                    new TableRow({
                      children: row.map(
                        (cell: string) =>
                          new TableCell({
                            children: [
                              new Paragraph({
                                children: [
                                  new TextRun({
                                    text: cell,
                                    color: designTokens.colors.foreground,
                                    size: designTokens.fontSize.base,
                                    font: "Roboto",
                                  }),
                                ],
                                alignment: AlignmentType.LEFT,
                              }),
                            ],
                            shading: {
                              fill: rowIndex % 2 === 0 ? "FFFFFF" : "F9FAFB",
                            },
                            margins: {
                              top: 120,
                              bottom: 120,
                              left: 160,
                              right: 160,
                            },
                            borders: {
                              top: {
                                color: "d1d5db",
                                size: 4,
                                style: "single",
                              },
                              bottom: {
                                color: "d1d5db",
                                size: 4,
                                style: "single",
                              },
                              left: {
                                color: "d1d5db",
                                size: 4,
                                style: "single",
                              },
                              right: {
                                color: "d1d5db",
                                size: 4,
                                style: "single",
                              },
                            },
                            width: { size: 1000, type: WidthType.DXA },
                          }),
                      ),
                    }),
                  );
                });
              }
              children.push(
                new Table({
                  rows: tableRows,
                  width: { size: 10000, type: WidthType.DXA },
                }),
              );
            });
          }
        });
      }
    });
  }
  const doc = new Document({
    sections: [
      {
        properties: {
          page: {
            margin: {
              top: 720, // 0.5 inch
              right: 720,
              bottom: 720,
              left: 720,
            },
          },
        },
        children,
      },
    ],
  });
  Packer.toBlob(doc).then((blob) => saveAs(blob, filename));
}
