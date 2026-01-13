import { saveAs } from "file-saver";
import { Document, Packer, Paragraph, HeadingLevel } from "docx";

export function downloadKitDoc(kitData: any, filename = "marketing_kit.docx") {
  if (!kitData) return;
  const children: any[] = [];
  // Title
  children.push(new Paragraph({ text: "Marketing Kit", heading: HeadingLevel.HEADING_1 }));
  // Render each section
  if (kitData.document && Array.isArray(kitData.document.sections)) {
    kitData.document.sections.forEach((section: any) => {
      children.push(new Paragraph({ text: section.title || section.id, heading: HeadingLevel.HEADING_2 }));
      if (Array.isArray(section.blocks)) {
        section.blocks.forEach((block: any) => {
          if (block.type === "Paragraph") {
            children.push(new Paragraph({ text: block.text || "" }));
          } else if (block.type === "Bullets" && Array.isArray(block.items)) {
            block.items.forEach((item: string) => {
              children.push(new Paragraph({ text: `• ${item}` }));
            });
          } else if (block.type === "Subhead") {
            children.push(new Paragraph({ text: block.text || "", heading: HeadingLevel.HEADING_3 }));
          } else if (block.type === "ListOfSections" && Array.isArray(block.section_titles)) {
            children.push(new Paragraph({ text: "Sections Included:", heading: HeadingLevel.HEADING_3 }));
            block.section_titles.forEach((title: string) => {
              children.push(new Paragraph({ text: `- ${title}` }));
            });
          } else if (block.type === "Table" && Array.isArray(block.rows) && Array.isArray(block.columns)) {
            // Simple table rendering: columns as header, rows as lines
            children.push(new Paragraph({ text: block.title || "Table", heading: HeadingLevel.HEADING_3 }));
            children.push(new Paragraph({ text: block.columns.join(" | ") }));
            block.rows.forEach((row: any[]) => {
              children.push(new Paragraph({ text: row.join(" | ") }));
            });
          }
          // Add more block types as needed
        });
      }
    });
  }
  const doc = new Document({
    sections: [
      {
        properties: {},
        children,
      },
    ],
  });
  Packer.toBlob(doc).then((blob) => saveAs(blob, filename));
}
