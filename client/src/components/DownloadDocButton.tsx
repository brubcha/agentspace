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
    downloadKitDoc(kitData, "marketing_kit.docx");
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
