import {
  Document,
  Packer,
  Paragraph,
  TextRun,
  HeadingLevel,
  Table,
  TableRow,
  TableCell,
  WidthType,
  BorderStyle,
  AlignmentType,
  VerticalAlign,
} from "docx";
import { designTokens } from "./designTokens";
import { saveAs } from "file-saver";

// Simple markdown parser for headings and bold
function parseMarkdownToRuns(text: string): TextRun[] {
  const runs = [];
  // Headings: ##, ###, ####, etc. at start of line
  const headingMatch = text.match(/^(#{2,6})\s+(.*)$/);
  if (headingMatch) {
    const level = headingMatch[1].length;
    const content = headingMatch[2];
    let size = designTokens.fontSize.heading2;
    let color = designTokens.colors.heading2;
    let font = "Open Sans";
    if (level === 2) {
      size = 30;
      color = "#111827";
    } // H2
    if (level === 3) {
      size = 20;
      color = "#111827";
    }
    if (level === 4) {
      size = 18;
      color = "#1F2937";
    }
    if (level === 5) {
      size = 16;
      color = "#374151";
    }
    runs.push(new TextRun({ text: content, bold: true, size, color, font }));
    return runs;
  }
  // Inline bold: **text**
  let lastIndex = 0;
  const boldRegex = /\*\*(.+?)\*\*/g;
  let match;
  while ((match = boldRegex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      runs.push(
        new TextRun({
          text: text.slice(lastIndex, match.index),
          font: "Roboto",
          color: designTokens.colors.primaryText,
          size: designTokens.fontSize.base,
        }),
      );
    }
    runs.push(
      new TextRun({
        text: match[1],
        bold: true,
        font: "Roboto",
        color: designTokens.colors.primaryText,
        size: designTokens.fontSize.base,
      }),
    );
    lastIndex = match.index + match[0].length;
  }
  if (lastIndex < text.length) {
    runs.push(
      new TextRun({
        text: text.slice(lastIndex),
        font: "Roboto",
        color: designTokens.colors.primaryText,
        size: designTokens.fontSize.base,
      }),
    );
  }
  if (runs.length === 0) {
    runs.push(
      new TextRun({
        text,
        font: "Roboto",
        color: designTokens.colors.primaryText,
        size: designTokens.fontSize.base,
      }),
    );
  }
  return runs;
}

// ...existing code...

export function downloadKitDoc(
  arr: any[],
  filename: string,
  requestType?: string,
  clientName?: string,
) {
  const children: any[] = [];
  const dividerAfter = [
    /* section titles to add divider after */
  ];

  if (!Array.isArray(arr)) {
    console.warn("downloadKitDoc: arr is not an array", arr);
    return;
  }
  console.log("downloadKitDoc: sections input", arr);

  let engagementIndexRendered = false;
  arr.forEach((section, idx) => {
    // Insert Request Type and Client Name before Overview section
    if (
      section &&
      (section.id?.toLowerCase() === "overview" ||
        section.title?.toLowerCase().includes("overview"))
    ) {
      if (requestType) {
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: requestType,
                bold: true,
                color: designTokens.colors.heading1,
                size: designTokens.fontSize.heading1,
                font: "Open Sans",
              }),
            ],
            spacing: {
              before: designTokens.spacing.heading1Before,
              after: designTokens.spacing.heading1After / 2,
            },
          }),
        );
      }
      if (clientName) {
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: clientName,
                bold: false,
                color: designTokens.colors.heading2,
                size: designTokens.fontSize.heading2,
                font: "Open Sans",
              }),
            ],
            spacing: {
              before: 0,
              after: designTokens.spacing.heading2After,
            },
          }),
        );
      }
    }
    if (!section || !Array.isArray(section.blocks)) {
      console.warn(
        "downloadKitDoc: section missing or blocks not array",
        section,
      );
      return;
    }
    // Debug: Log all block titles and types in this section
    section.blocks.forEach((block: any, bIdx: number) => {
      if (block && block.title) {
        console.log(
          `DEBUG: Section[${idx}] Block[${bIdx}] Title: '${block.title}', Type: '${block.type}'`,
          block,
        );
      } else {
        console.log(
          `DEBUG: Section[${idx}] Block[${bIdx}] (no title), Type: '${block?.type}'`,
          block,
        );
      }
    });

    // Special handling for Engagement Index section if present
    if (
      section.id &&
      section.id.toLowerCase() === "engagement_index" &&
      Array.isArray(section.blocks) &&
      section.blocks.length === 1
    ) {
      const block = section.blocks[0];
      if (block && Array.isArray(block.columns) && Array.isArray(block.rows)) {
        // Render the Engagement Index table regardless of block type/title
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: section.title || "Engagement Index",
                color: designTokens.colors.heading3,
                size: designTokens.fontSize.heading3,
                font: "Open Sans",
              }),
            ],
            spacing: { after: designTokens.spacing.heading3After },
          }),
        );
        const headerRow = new TableRow({
          children: block.columns.map(
            (col: string) =>
              new TableCell({
                children: [
                  new Paragraph({
                    children: [
                      new TextRun({
                        text: col,
                        color: designTokens.colors.tableCellText,
                        size: designTokens.fontSize.tableHeader,
                        font: "Roboto",
                      }),
                    ],
                    spacing: { after: designTokens.spacing.tableCellPadding },
                  }),
                ],
                shading: {
                  fill: designTokens.colors.tableHeaderBg,
                },
                borders: {
                  top: {
                    color: designTokens.colors.tableBorder,
                    size: 4,
                    style: "single",
                  },
                  bottom: {
                    color: designTokens.colors.tableBorder,
                    size: 4,
                    style: "single",
                  },
                  left: {
                    color: designTokens.colors.tableBorder,
                    size: 4,
                    style: "single",
                  },
                  right: {
                    color: designTokens.colors.tableBorder,
                    size: 4,
                    style: "single",
                  },
                },
                width: { size: 1000, type: WidthType.DXA },
              }),
          ),
        });
        const bodyRows = block.rows.map(
          (row: string[], rIdx: number) =>
            new TableRow({
              children: row.map(
                (cell: string) =>
                  new TableCell({
                    children: [
                      new Paragraph({
                        children: [
                          new TextRun({
                            text: cell,
                            color: designTokens.colors.tableCellText,
                            size: designTokens.fontSize.tableCell,
                            font: "Roboto",
                          }),
                        ],
                        spacing: {
                          after: designTokens.spacing.tableCellPadding,
                        },
                      }),
                    ],
                    shading: {
                      fill:
                        rIdx % 2 === 0
                          ? designTokens.colors.tableRow
                          : designTokens.colors.tableRowAlt,
                    },
                    borders: {
                      top: {
                        color: designTokens.colors.tableBorder,
                        size: 2,
                        style: "single",
                      },
                      bottom: {
                        color: designTokens.colors.tableBorder,
                        size: 2,
                        style: "single",
                      },
                      left: {
                        color: designTokens.colors.tableBorder,
                        size: 2,
                        style: "single",
                      },
                      right: {
                        color: designTokens.colors.tableBorder,
                        size: 2,
                        style: "single",
                      },
                    },
                    width: { size: 1000, type: WidthType.DXA },
                  }),
              ),
            }),
        );
        children.push(
          new Table({
            rows: [headerRow, ...bodyRows],
            width: { size: 10000, type: WidthType.DXA },
            alignment: AlignmentType.CENTER,
          }),
        );
        return;
      }
    }
    // Section title as heading
    children.push(
      new Paragraph({
        children: [
          new TextRun({
            text: section.title || `Section ${idx + 1}`,
            bold: true,
            color: designTokens.colors.heading1,
            size: designTokens.fontSize.heading1,
            font: "Open Sans",
          }),
        ],
        spacing: {
          before: designTokens.spacing.heading1Before,
          after: designTokens.spacing.heading1After,
        },
      }),
    );
    section.blocks.forEach((block: any, bIdx: number) => {
      // Subhead block
      if (block.type === "Subhead" && block.text) {
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: block.text.replace("[REVIEW]", "").trim(),
                bold: true,
                color: designTokens.colors.heading2,
                size: designTokens.fontSize.heading2,
                font: "Open Sans",
              }),
            ],
            spacing: {
              before: designTokens.spacing.heading2Before,
              after: designTokens.spacing.heading2After,
            },
          }),
        );
        return;
      }

      // Info block
      if (block.type === "INFO" && block.text) {
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: block.text.replace("[REVIEW]", "").trim(),
                color: designTokens.colors.infoText,
                font: "Roboto",
                size: designTokens.fontSize.base,
              }),
            ],
            shading: { fill: designTokens.colors.infoBg },
            spacing: { after: designTokens.spacing.paragraphAfter },
          }),
        );
        return;
      }

      // Paragraph block (rich text)
      if (block.type === "Paragraph" && block.text) {
        const cleanText = block.text.replace("[REVIEW]", "").trim();
        const runs = parseMarkdownToRuns(cleanText);
        children.push(
          new Paragraph({
            children: runs,
            spacing: { after: designTokens.spacing.paragraphAfter },
          }),
        );
        return;
      }
      // Paragraph block (rich text)
      if (block.type === "Paragraph" && block.content) {
        let runs = [];
        if (Array.isArray(block.content)) {
          block.content.forEach((part: any) => {
            runs.push(
              new TextRun({
                text: part.text || part,
                bold: !!part.bold,
                italics: !!part.italic,
                color: designTokens.colors.primaryText,
                font: "Roboto",
                size: designTokens.fontSize.base,
                underline: part.underline
                  ? { type: "single", color: designTokens.colors.primaryText }
                  : undefined,
              }),
            );
          });
        } else {
          runs.push(
            new TextRun({
              text: block.content,
              color: designTokens.colors.primaryText,
              font: "Roboto",
              size: designTokens.fontSize.base,
            }),
          );
        }
        children.push(
          new Paragraph({
            children: runs,
            spacing: { after: designTokens.spacing.paragraphAfter },
          }),
        );
        return;
      }

      // Bullets block (rich text)
      if (block.type === "Bullets" && Array.isArray(block.items)) {
        block.items.forEach((item: any) => {
          let runs: TextRun[] = [];
          if (Array.isArray(item)) {
            item.forEach((part: any) => {
              if (typeof part.text === "string") {
                runs = runs.concat(parseMarkdownToRuns(part.text));
              } else {
                runs.push(
                  new TextRun({
                    text: part.text || part,
                    bold: !!part.bold,
                    italics: !!part.italic,
                    color: "000000",
                    font: "Roboto",
                    size: designTokens.fontSize.base,
                    underline: part.underline
                      ? { type: "single", color: "000000" }
                      : undefined,
                  }),
                );
              }
            });
          } else if (typeof item === "string") {
            runs = parseMarkdownToRuns(item);
          } else {
            runs.push(
              new TextRun({
                text: item,
                color: "000000",
                font: "Roboto",
                size: designTokens.fontSize.base,
              }),
            );
          }
          children.push(
            new Paragraph({
              children: runs,
              bullet: { level: 0 },
              spacing: { after: designTokens.spacing.bulletAfter },
            }),
          );
        });
        return;
      }

      // NumberedList block
      if (block.type === "NumberedList" && Array.isArray(block.items)) {
        block.items.forEach((item: any, i: number) => {
          children.push(
            new Paragraph({
              children: [
                new TextRun({
                  text: `${i + 1}. ${item.text}`,
                  color: "000000", // Black for numbered list
                  size: designTokens.fontSize.base,
                  font: "Roboto",
                  bold: true,
                }),
              ],
              numbering: { reference: "numbered-list", level: 0 },
              spacing: { after: designTokens.spacing.bulletAfter },
            }),
          );
        });
        return;
      }

      // Heading block
      if (block.type === "Heading" && block.content && block.level) {
        const headingMap: {
          [key: string]: {
            level: (typeof HeadingLevel)[keyof typeof HeadingLevel];
            color: string;
            size: number;
            before: number;
            after: number;
          };
        } = {
          "1": {
            level: HeadingLevel.HEADING_1,
            color: designTokens.colors.heading1,
            size: designTokens.fontSize.heading1,
            before: designTokens.spacing.heading1Before,
            after: designTokens.spacing.heading1After,
          },
          "2": {
            level: HeadingLevel.HEADING_2,
            color: designTokens.colors.heading2,
            size: designTokens.fontSize.heading2,
            before: designTokens.spacing.heading2Before,
            after: designTokens.spacing.heading2After,
          },
          "3": {
            level: HeadingLevel.HEADING_3,
            color: designTokens.colors.heading3,
            size: designTokens.fontSize.heading3,
            before: designTokens.spacing.heading3Before,
            after: designTokens.spacing.heading3After,
          },
          "4": {
            level: HeadingLevel.HEADING_4,
            color: designTokens.colors.heading3,
            size: designTokens.fontSize.heading3,
            before: designTokens.spacing.heading3Before,
            after: designTokens.spacing.heading3After,
          },
          "5": {
            level: HeadingLevel.HEADING_5,
            color: designTokens.colors.heading3,
            size: designTokens.fontSize.heading3,
            before: designTokens.spacing.heading3Before,
            after: designTokens.spacing.heading3After,
          },
        };
        const levelNum = String(block.level);
        const h = headingMap[levelNum] || headingMap["2"];
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: block.content,
                bold: true,
                color: h.color,
                size: h.size,
                font: "Open Sans",
              }),
            ],
            heading: h.level,
            spacing: {
              before: h.before,
              after: h.after,
            },
          }),
        );
        return;
      }

      // Table block (generic)
      if (
        block.type === "Table" &&
        Array.isArray(block.rows) &&
        Array.isArray(block.columns)
      ) {
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: block.title || "Table",
                bold: true,
                color: "000000", // Black for table title
                size: designTokens.fontSize.heading3,
                font: "Open Sans",
              }),
            ],
            spacing: { after: designTokens.spacing.heading3After },
          }),
        );
        // Table header row
        const headerRow = new TableRow({
          children: block.columns.map(
            (col: string) =>
              new TableCell({
                children: [
                  new Paragraph({
                    children: [
                      new TextRun({
                        text: col,
                        bold: true,
                        color: "000000", // Black for table header text
                        size: designTokens.fontSize.tableHeader,
                        font: "Roboto",
                      }),
                    ],
                    spacing: { after: designTokens.spacing.tableCellPadding },
                  }),
                ],
                shading: {
                  fill: designTokens.colors.tableHeaderBg,
                },
                borders: {
                  top: {
                    color: designTokens.colors.tableBorder,
                    size: 4,
                    style: "single",
                  },
                  bottom: {
                    color: designTokens.colors.tableBorder,
                    size: 4,
                    style: "single",
                  },
                  left: {
                    color: designTokens.colors.tableBorder,
                    size: 4,
                    style: "single",
                  },
                  right: {
                    color: designTokens.colors.tableBorder,
                    size: 4,
                    style: "single",
                  },
                },
                width: { size: 1000, type: WidthType.DXA },
              }),
          ),
        });
        // Table body rows with zebra striping
        const bodyRows = block.rows.map(
          (row: string[], rIdx: number) =>
            new TableRow({
              children: row.map(
                (cell: string) =>
                  new TableCell({
                    children: [
                      new Paragraph({
                        children: [
                          new TextRun({
                            text: cell,
                            color: "000000", // Black for table cell text
                            size: designTokens.fontSize.tableCell,
                            font: "Roboto",
                          }),
                        ],
                        spacing: {
                          after: designTokens.spacing.tableCellPadding,
                        },
                      }),
                    ],
                    shading: {
                      fill:
                        rIdx % 2 === 0
                          ? designTokens.colors.tableRow
                          : designTokens.colors.tableRowAlt,
                    },
                    borders: {
                      top: {
                        color: designTokens.colors.tableBorder,
                        size: 2,
                        style: "single",
                      },
                      bottom: {
                        color: designTokens.colors.tableBorder,
                        size: 2,
                        style: "single",
                      },
                      left: {
                        color: designTokens.colors.tableBorder,
                        size: 2,
                        style: "single",
                      },
                      right: {
                        color: designTokens.colors.tableBorder,
                        size: 2,
                        style: "single",
                      },
                    },
                    width: { size: 1000, type: WidthType.DXA },
                  }),
              ),
            }),
        );
        children.push(
          new Table({
            rows: [headerRow, ...bodyRows],
            width: { size: 10000, type: WidthType.DXA },
            alignment: AlignmentType.CENTER,
          }),
        );
        return;
      }

      // Fallback for unknown block types
      // If block type is not recognized, skip rendering instead of showing error text
      // ...existing code...
      // Callout block
      if (block.type === "Callout" && block.variant && block.text) {
        let bg, border, color;
        if (block.variant === "info") {
          bg = designTokens.colors.infoBg;
          border = designTokens.colors.infoBorder;
          color = designTokens.colors.infoText;
        } else if (block.variant === "warning") {
          bg = designTokens.colors.warningBg;
          border = designTokens.colors.warningBorder;
          color = designTokens.colors.warningText;
        } else if (block.variant === "success") {
          bg = designTokens.colors.successBg;
          border = designTokens.colors.successBorder;
          color = designTokens.colors.successText;
        } else {
          bg = designTokens.colors.infoBg;
          border = designTokens.colors.infoBorder;
          color = designTokens.colors.infoText;
        }
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: `[${block.variant.toUpperCase()}] `,
                bold: true,
                color,
                font: "Roboto",
                size: designTokens.fontSize.base,
              }),
              new TextRun({
                text: block.text,
                color,
                font: "Roboto",
                size: designTokens.fontSize.base,
              }),
            ],
            shading: { fill: bg },
            spacing: { after: designTokens.spacing.paragraphAfter },
            border: {
              top: { color: border, size: 6, style: "single" },
              bottom: { color: border, size: 6, style: "single" },
              left: { color: border, size: 6, style: "single" },
              right: { color: border, size: 6, style: "single" },
            },
          }),
        );
        return;
      }

      // ArchetypeCard block
      if (
        block.type === "ArchetypeCard" &&
        block.variant &&
        block.label &&
        block.text
      ) {
        let bg, border, labelBg, labelText;
        if (block.variant === "primary") {
          bg = designTokens.colors.primaryGradientStart;
          border = designTokens.colors.primaryBorder;
          labelBg = designTokens.colors.primaryLabelBg;
          labelText = designTokens.colors.primaryLabelText;
        } else {
          bg = designTokens.colors.secondaryGradientStart;
          border = designTokens.colors.secondaryBorder;
          labelBg = designTokens.colors.secondaryLabelBg;
          labelText = designTokens.colors.secondaryLabelText;
        }
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: `[${block.label}] `,
                bold: true,
                color: labelText,
                font: "Roboto",
                shading: { fill: labelBg },
                size: designTokens.fontSize.base,
              }),
              new TextRun({
                text: block.text,
                color: designTokens.colors.primaryText,
                font: "Roboto",
                size: designTokens.fontSize.base,
              }),
            ],
            shading: { fill: bg },
            spacing: { after: designTokens.spacing.paragraphAfter },
            border: {
              top: { color: border, size: 6, style: "single" },
              bottom: { color: border, size: 6, style: "single" },
              left: { color: border, size: 6, style: "single" },
              right: { color: border, size: 6, style: "single" },
            },
          }),
        );
        return;
      }

      // Checklist block
      if (block.type === "Checklist" && Array.isArray(block.items)) {
        block.items.forEach((item: any) => {
          children.push(
            new Paragraph({
              children: [
                new TextRun({
                  text: item.checked ? "✔ " : "✗ ",
                  color: item.checked
                    ? designTokens.colors.checkMarkGreen
                    : designTokens.colors.xMarkRed,
                  font: "Roboto",
                  bold: true,
                  size: designTokens.fontSize.base,
                }),
                new TextRun({
                  text: item.text,
                  color: designTokens.colors.primaryText,
                  font: "Roboto",
                  size: designTokens.fontSize.base,
                }),
              ],
              spacing: { after: designTokens.spacing.bulletAfter },
            }),
          );
        });
        return;
      }

      // OpportunityCard block
      if (block.type === "OpportunityCard" && block.title && block.body) {
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: `[Opportunity] `,
                bold: true,
                color: designTokens.colors.opportunityCardTitle,
                font: "Roboto",
                size: designTokens.fontSize.base,
              }),
              new TextRun({
                text: block.title,
                bold: true,
                color: designTokens.colors.opportunityCardTitle,
                font: "Roboto",
                size: designTokens.fontSize.base,
              }),
              new TextRun({
                text: " - ",
                color: designTokens.colors.opportunityCardTitle,
                font: "Roboto",
                size: designTokens.fontSize.base,
              }),
              new TextRun({
                text: block.body,
                color: designTokens.colors.opportunityCardBody,
                font: "Roboto",
                size: designTokens.fontSize.base,
              }),
            ],
            shading: { fill: designTokens.colors.opportunityCardBg },
            spacing: { after: designTokens.spacing.paragraphAfter },
            border: {
              top: {
                color: designTokens.colors.opportunityCardBorder,
                size: 6,
                style: "single",
              },
              bottom: {
                color: designTokens.colors.opportunityCardBorder,
                size: 6,
                style: "single",
              },
              left: {
                color: designTokens.colors.opportunityCardBorder,
                size: 6,
                style: "single",
              },
              right: {
                color: designTokens.colors.opportunityCardBorder,
                size: 6,
                style: "single",
              },
            },
          }),
        );
        return;
      }
      // Subsection title: Heading 2/3 for blocks with a title (except Factual Foundations)
      if (block.title && block.type !== "Table") {
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: block.title,
                color: designTokens.colors.heading2,
                size: designTokens.fontSize.heading2,
                font: "Open Sans",
              }),
            ],
            spacing: {
              before: designTokens.spacing.heading2Before,
              after: designTokens.spacing.heading2After,
            },
          }),
        );
      }
      // Handle Factual Foundations Table as before
      if (
        block.type === "Table" &&
        block.title === "Factual Foundations" &&
        Array.isArray(block.rows) &&
        Array.isArray(block.columns)
      ) {
        const [essence, purpose, personality] = block.rows[0];
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: "Brand Essence",
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
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: essence,
                color: designTokens.colors.primaryText,
                font: "Roboto",
              }),
            ],
            spacing: { after: designTokens.spacing.paragraphAfter },
          }),
        );
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: "Brand Purpose",
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
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: purpose,
                color: designTokens.colors.primaryText,
                font: "Roboto",
              }),
            ],
            spacing: { after: designTokens.spacing.paragraphAfter },
          }),
        );
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: "Brand Personality",
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
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: personality,
                color: designTokens.colors.primaryText,
                font: "Roboto",
              }),
            ],
            spacing: { after: designTokens.spacing.paragraphAfter },
          }),
        );
        return;
      }

      // Paragraph block
      if (block.type === "Paragraph" && block.content) {
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: block.content,
                color: designTokens.colors.primaryText,
                size: designTokens.fontSize.base,
                font: "Roboto",
              }),
            ],
            spacing: { after: designTokens.spacing.paragraphAfter },
          }),
        );
        return;
      }

      // Bullets block
      if (block.type === "Bullets" && Array.isArray(block.items)) {
        block.items.forEach((item: string) => {
          children.push(
            new Paragraph({
              children: [
                new TextRun({
                  text: item,
                  color: designTokens.colors.bulletGray,
                  size: designTokens.fontSize.base,
                  font: "Roboto",
                }),
              ],
              bullet: { level: 0 },
              spacing: { after: designTokens.spacing.bulletAfter },
            }),
          );
        });
        return;
      }

      // NumberedList block
      if (block.type === "NumberedList" && Array.isArray(block.items)) {
        block.items.forEach((item: any, i: number) => {
          children.push(
            new Paragraph({
              children: [
                new TextRun({
                  text: `${i + 1}. ${item.text}`,
                  color: designTokens.colors.orangeGradientStart,
                  size: designTokens.fontSize.base,
                  font: "Roboto",
                  bold: true,
                }),
              ],
              numbering: { reference: "numbered-list", level: 0 },
              spacing: { after: designTokens.spacing.bulletAfter },
            }),
          );
        });
        return;
      }

      // Table block (generic)
      if (
        block.type === "Table" &&
        Array.isArray(block.rows) &&
        Array.isArray(block.columns)
      ) {
        // Only render Engagement Index table once
        if (
          block.title &&
          block.title.toLowerCase().includes("engagement index")
        ) {
          if (!engagementIndexRendered) {
            engagementIndexRendered = true;
            children.push(
              new Paragraph({
                children: [
                  new TextRun({
                    text: block.title,
                    color: designTokens.colors.heading3,
                    size: designTokens.fontSize.heading3,
                    font: "Open Sans",
                  }),
                ],
                spacing: { after: designTokens.spacing.heading3After },
              }),
            );
            const headerRow = new TableRow({
              children: block.columns.map(
                (col: string) =>
                  new TableCell({
                    children: [
                      new Paragraph({
                        children: [
                          new TextRun({
                            text: col,
                            color: designTokens.colors.tableCellText,
                            size: designTokens.fontSize.tableHeader,
                            font: "Roboto",
                          }),
                        ],
                        spacing: {
                          after: designTokens.spacing.tableCellPadding,
                        },
                      }),
                    ],
                    shading: {
                      fill: designTokens.colors.tableHeaderBg,
                    },
                    borders: {
                      top: {
                        color: designTokens.colors.tableBorder,
                        size: 4,
                        style: "single",
                      },
                      bottom: {
                        color: designTokens.colors.tableBorder,
                        size: 4,
                        style: "single",
                      },
                      left: {
                        color: designTokens.colors.tableBorder,
                        size: 4,
                        style: "single",
                      },
                      right: {
                        color: designTokens.colors.tableBorder,
                        size: 4,
                        style: "single",
                      },
                    },
                    width: { size: 1000, type: WidthType.DXA },
                  }),
              ),
            });
            const bodyRows = block.rows.map(
              (row: string[], rIdx: number) =>
                new TableRow({
                  children: row.map(
                    (cell: string) =>
                      new TableCell({
                        children: [
                          new Paragraph({
                            children: [
                              new TextRun({
                                text: cell,
                                color: designTokens.colors.tableCellText,
                                size: designTokens.fontSize.tableCell,
                                font: "Roboto",
                              }),
                            ],
                            spacing: {
                              after: designTokens.spacing.tableCellPadding,
                            },
                          }),
                        ],
                        shading: {
                          fill:
                            rIdx % 2 === 0
                              ? designTokens.colors.tableRow
                              : designTokens.colors.tableRowAlt,
                        },
                        borders: {
                          top: {
                            color: designTokens.colors.tableBorder,
                            size: 2,
                            style: "single",
                          },
                          bottom: {
                            color: designTokens.colors.tableBorder,
                            size: 2,
                            style: "single",
                          },
                          left: {
                            color: designTokens.colors.tableBorder,
                            size: 2,
                            style: "single",
                          },
                          right: {
                            color: designTokens.colors.tableBorder,
                            size: 2,
                            style: "single",
                          },
                        },
                        width: { size: 1000, type: WidthType.DXA },
                      }),
                  ),
                }),
            );
            children.push(
              new Table({
                rows: [headerRow, ...bodyRows],
                width: { size: 10000, type: WidthType.DXA },
                alignment: AlignmentType.CENTER,
              }),
            );
          }
        } else {
          // Render other tables as usual
          children.push(
            new Paragraph({
              children: [
                new TextRun({
                  text: block.title || "Table",
                  color: designTokens.colors.heading3,
                  size: designTokens.fontSize.heading3,
                  font: "Open Sans",
                }),
              ],
              spacing: { after: designTokens.spacing.heading3After },
            }),
          );
          const headerRow = new TableRow({
            children: block.columns.map(
              (col: string) =>
                new TableCell({
                  children: [
                    new Paragraph({
                      children: [
                        new TextRun({
                          text: col,
                          color: designTokens.colors.tableCellText,
                          size: designTokens.fontSize.tableHeader,
                          font: "Roboto",
                        }),
                      ],
                      spacing: { after: designTokens.spacing.tableCellPadding },
                    }),
                  ],
                  shading: {
                    fill: designTokens.colors.tableHeaderBg,
                  },
                  borders: {
                    top: {
                      color: designTokens.colors.tableBorder,
                      size: 4,
                      style: "single",
                    },
                    bottom: {
                      color: designTokens.colors.tableBorder,
                      size: 4,
                      style: "single",
                    },
                    left: {
                      color: designTokens.colors.tableBorder,
                      size: 4,
                      style: "single",
                    },
                    right: {
                      color: designTokens.colors.tableBorder,
                      size: 4,
                      style: "single",
                    },
                  },
                  width: { size: 1000, type: WidthType.DXA },
                }),
            ),
          });
          const bodyRows = block.rows.map(
            (row: string[], rIdx: number) =>
              new TableRow({
                children: row.map(
                  (cell: string) =>
                    new TableCell({
                      children: [
                        new Paragraph({
                          children: [
                            new TextRun({
                              text: cell,
                              color: designTokens.colors.tableCellText,
                              size: designTokens.fontSize.tableCell,
                              font: "Roboto",
                            }),
                          ],
                          spacing: {
                            after: designTokens.spacing.tableCellPadding,
                          },
                        }),
                      ],
                      shading: {
                        fill:
                          rIdx % 2 === 0
                            ? designTokens.colors.tableRow
                            : designTokens.colors.tableRowAlt,
                      },
                      borders: {
                        top: {
                          color: designTokens.colors.tableBorder,
                          size: 2,
                          style: "single",
                        },
                        bottom: {
                          color: designTokens.colors.tableBorder,
                          size: 2,
                          style: "single",
                        },
                        left: {
                          color: designTokens.colors.tableBorder,
                          size: 2,
                          style: "single",
                        },
                        right: {
                          color: designTokens.colors.tableBorder,
                          size: 2,
                          style: "single",
                        },
                      },
                      width: { size: 1000, type: WidthType.DXA },
                    }),
                ),
              }),
          );
          children.push(
            new Table({
              rows: [headerRow, ...bodyRows],
              width: { size: 10000, type: WidthType.DXA },
              alignment: AlignmentType.CENTER,
            }),
          );
        }
        return;
      }

      // Fallback for unknown block types
      // Do not render anything for unknown block types
    });
    // ...existing code...
  });

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
  Packer.toBlob(doc)
    .then((blob) => {
      try {
        saveAs(blob, filename);
        console.log('Word document generated and saved:', filename);
      } catch (saveErr) {
        console.error('Error saving Word document:', saveErr);
        alert('Error saving Word document. See console for details.');
      }
    })
    .catch((err) => {
      console.error('Error generating Word document:', err);
      alert('Error generating Word document. See console for details.');
    });
}
