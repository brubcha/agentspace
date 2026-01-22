import React from "react";
import { Button, Tooltip } from "@mui/material";
import { saveAs } from "file-saver";
import { downloadKitDoc } from "../utils/downloadKitDoc";

interface DownloadDocButtonProps {
  kitData: any;
}

const DownloadDocButton: React.FC<DownloadDocButtonProps> = ({ kitData }) => {
  const handleDownload = () => {
    if (!kitData) return;
    // Try to extract client name and request type from multiple possible locations
    // Robust extraction for client name and request type
    // Prefer original user input for client name if available
    let clientName =
      kitData.originalClientName ||
      kitData.client_name ||
      kitData.brand_name ||
      kitData.document?.client_name ||
      kitData.document?.brand_name ||
      kitData.client?.brand_name ||
      kitData.meta?.brand ||
      kitData.client ||
      "Client";
    let requestType =
      kitData.requestType ||
      kitData.request_type ||
      kitData.meta?.request_type ||
      kitData.type ||
      kitData.document?.request_type ||
      "Marketing Kit";
    clientName = String(clientName).replace(/[^a-z0-9]+/gi, "_");
    requestType = String(requestType).replace(/[^a-z0-9]+/gi, "_");
    // Use current date/time for download
    const now = new Date();
    const pad = (n: number) => n.toString().padStart(2, "0");
    const dateStr = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}_${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`;
    const filename = `${clientName}_${requestType}_${dateStr}.docx`;
    if (kitData?.document?.sections) {
      downloadKitDoc(
        kitData.document.sections,
        filename,
        requestType,
        clientName,
      );
    } else {
      console.warn(
        "DownloadDocButton: kitData.document.sections missing",
        kitData,
      );
    }
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
