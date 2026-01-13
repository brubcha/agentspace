import { saveAs } from "file-saver";
import { Document, Packer, Paragraph, HeadingLevel } from "docx";

export function downloadKitDoc(kitData: any, filename = "marketing_kit.docx") {
  if (!kitData) return;
  const doc = new Document({
    sections: [
      {
        properties: {},
        children: [
          new Paragraph({
            text: kitData.structure || "Marketing Kit",
            heading: HeadingLevel.HEADING_1,
          }),
          new Paragraph({
            text: kitData.style || "",
            heading: HeadingLevel.HEADING_2,
          }),
          new Paragraph({
            text: kitData.outline || "",
            heading: HeadingLevel.HEADING_3,
          }),
          ...(kitData.headings || []).map(
            (h: string) =>
              new Paragraph({ text: h, heading: HeadingLevel.HEADING_2 })
          ),
          new Paragraph({
            text: kitData.copy || "",
            heading: HeadingLevel.HEADING_3,
          }),
          ...(kitData.placeholders || []).map(
            (p: string) => new Paragraph({ text: `[Image Placeholder: ${p}]` })
          ),
        ],
      },
    ],
  });
  Packer.toBlob(doc).then((blob) => saveAs(blob, filename));
}
