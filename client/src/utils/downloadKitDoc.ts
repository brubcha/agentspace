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

  // Main document sections
  const sections = kitData?.document?.sections || kitData?.sections || [];
  for (const section of sections) {
    if (!Array.isArray(section.blocks)) continue;
    for (const block of section.blocks) {
      if (block.type === "Paragraph") {
        if (
          block.text &&
          (block.text.includes("##") ||
            block.text.includes("**") ||
            block.text.includes("* "))
        ) {
          markdownToDocxParagraphs(block.text).forEach((p) => children.push(p));
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
            }),
          );
        }
      } else if (block.type === "Bullets" && Array.isArray(block.items)) {
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
        // Data rows (robust: ensure each row matches columns, pad/trim as needed)
        block.rows.forEach((row: any, rowIndex: number) => {
          let safeRow = Array.isArray(row)
            ? row.slice(0, block.columns.length)
            : row && typeof row === "object"
              ? Object.values(row).slice(0, block.columns.length)
              : typeof row === "string"
                ? [row]
                : [];
          // Pad with empty strings if row is too short
          while (safeRow.length < block.columns.length) {
            safeRow.push("");
          }
          tableRows.push(
            new TableRow({
              children: safeRow.map(
                (cell: string) =>
                  new TableCell({
                    children: [
                      new Paragraph({
                        children: [
                          new TextRun({
                            text:
                              typeof cell === "string"
                                ? cell
                                : JSON.stringify(cell),
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
    }
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

// --- Stubs for missing functions/variables ---
// Remove these and import real implementations as needed

function parseBold(text: string, style: any): TextRun[] {
  // Simple bold parser: **bold**
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((part) => {
    if (/^\*\*[^*]+\*\*$/.test(part)) {
      return new TextRun({
        text: part.replace(/\*\*/g, ""),
        bold: true,
        ...style,
      });
    }
    return new TextRun({ text: part, ...style });
  });
}

function markdownToDocxParagraphs(text: string): Paragraph[] {
  // Basic markdown: split by lines, parse bold
  return text.split(/\n+/).map(
    (line) =>
      new Paragraph({
        children: parseBold(line, {
          color: "000000",
          size: 24,
          font: "Roboto",
        }),
      }),
  );
}
