import React from "react";
import { Button, Tooltip } from "@mui/material";
import { saveAs } from "file-saver";
import { Document, Packer, Paragraph, HeadingLevel, TextRun } from "docx";

interface DownloadDocButtonProps {
  kitData: any;
}

const DownloadDocButton: React.FC<DownloadDocButtonProps> = ({ kitData }) => {
  const handleDownload = async () => {
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
              (p: string) =>
                new Paragraph({ text: `[Image Placeholder: ${p}]` })
            ),
          ],
        },
      ],
    });
    const blob = await Packer.toBlob(doc);
    saveAs(blob, "marketing_kit.docx");
  };

  return (
    <Tooltip title="Download the generated marketing kit as a Word document.">
      <span>
        <Button
          variant="outlined"
          color="secondary"
          onClick={handleDownload}
          disabled={!kitData}
          sx={{ mt: 2 }}
        >
          Download Doc
        </Button>
      </span>
    </Tooltip>
  );
};

export default DownloadDocButton;
