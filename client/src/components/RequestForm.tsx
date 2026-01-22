import React, { useState, useRef } from "react";
import { useTheme } from "@mui/material/styles";
import {
  Box,
  MenuItem,
  TextField,
  Button,
  Typography,
  Tooltip,
} from "@mui/material";

const requestOptions = [
  {
    value: "marketing_kit",
    label: "Marketing Kit",
    tooltip: "Create a marketing kit for your client.",
  },
  // Add more request types as needed
];

const RequestForm: React.FC<{ onSubmit: (data: any) => void }> = ({
  onSubmit,
}) => {
  const [requestType, setRequestType] = useState("");
  const [clientName, setClientName] = useState("");
  const [website, setWebsite] = useState("");
  const [offering, setOffering] = useState("");
  const [targetMarkets, setTargetMarkets] = useState("");
  const [competitors, setCompetitors] = useState("");
  const [additionalDetails, setAdditionalDetails] = useState("");
  // Store files as { filename, content } objects
  // Store files as File objects
  const [files, setFiles] = useState<File[]>([]);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const theme = useTheme();
  // Dynamic fields based on requestType
  const renderFields = () => {
    switch (requestType) {
      case "marketing_kit":
        return (
          <>
            <Tooltip title="Enter the client name for the marketing kit.">
              <TextField
                label="Client Name"
                value={clientName}
                onChange={(e) => setClientName(e.target.value)}
                fullWidth
                margin="normal"
                required
              />
            </Tooltip>
            <Tooltip title="Enter the website URL for the client.">
              <TextField
                label="Website"
                value={website}
                onChange={(e) => setWebsite(e.target.value)}
                fullWidth
                margin="normal"
                required
              />
            </Tooltip>
            <Tooltip title="Describe the offering (product/service).">
              <TextField
                label="Offering"
                value={offering}
                onChange={(e) => setOffering(e.target.value)}
                fullWidth
                margin="normal"
              />
            </Tooltip>
            <Tooltip title="List the target markets.">
              <TextField
                label="Target Markets"
                value={targetMarkets}
                onChange={(e) => setTargetMarkets(e.target.value)}
                fullWidth
                margin="normal"
              />
            </Tooltip>
            <Tooltip title="List competitors (comma separated or one per line).">
              <TextField
                label="Competitors"
                value={competitors}
                onChange={(e) => setCompetitors(e.target.value)}
                fullWidth
                margin="normal"
                multiline
                minRows={2}
              />
            </Tooltip>
            <Tooltip title="Add any additional details or requirements.">
              <TextField
                label="Additional Details"
                value={additionalDetails}
                onChange={(e) => setAdditionalDetails(e.target.value)}
                fullWidth
                margin="normal"
                multiline
                minRows={2}
              />
            </Tooltip>
            <Box
              sx={{
                border: isDragOver
                  ? `2.5px solid ${theme.palette.primary.main}`
                  : "2px dashed #aaa",
                borderRadius: 2,
                p: 2,
                textAlign: "center",
                mt: 2,
                mb: 2,
                background: isDragOver ? "#e3f2fd" : "#fafafa",
                cursor: "pointer",
                position: "relative",
                overflow: "hidden",
                transition: "border 0.2s, background 0.2s",
                boxShadow: isDragOver
                  ? `0 0 0 2px ${theme.palette.primary.main}`
                  : undefined,
              }}
              onDragOver={(e) => {
                e.preventDefault();
                e.stopPropagation();
                setIsDragOver(true);
              }}
              onDragLeave={(e) => {
                e.preventDefault();
                e.stopPropagation();
                setIsDragOver(false);
              }}
              onDrop={async (e) => {
                e.preventDefault();
                e.stopPropagation();
                setIsDragOver(false);
                const droppedFiles = Array.from(e.dataTransfer.files);
                if (droppedFiles.length > 0) {
                  setFiles((prev) => [...prev, ...droppedFiles]);
                  console.log("Dropped files:", droppedFiles);
                }
              }}
              onClick={() => fileInputRef.current?.click()}
            >
              <Typography
                variant="body2"
                sx={(theme) => ({
                  color:
                    theme.palette.mode === "dark" ? "#000" : "text.secondary",
                })}
              >
                Drag and drop files here, or click to select files
              </Typography>
              <input
                ref={fileInputRef}
                type="file"
                multiple
                style={{
                  position: "absolute",
                  width: 1,
                  height: 1,
                  top: 0,
                  left: 0,
                  opacity: 0,
                  pointerEvents: "none",
                }}
                tabIndex={-1}
                onChange={async (e) => {
                  const fileList = e.target.files;
                  if (fileList && fileList.length > 0) {
                    setFiles((prev) => [...prev, ...Array.from(fileList)]);
                  }
                }}
              />
              {files.length > 0 && (
                <Box sx={{ mt: 1 }}>
                  {files.map((file, idx) => (
                    <Typography
                      key={idx}
                      variant="caption"
                      sx={(theme) => ({ color: theme.palette.primary.main })}
                    >
                      {file.name}
                    </Typography>
                  ))}
                </Box>
              )}
            </Box>
          </>
        );
      default:
        return null;
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Map frontend fields to backend-expected keys
    onSubmit({
      request_type: requestType,
      client_name: clientName,
      brand_name: clientName, // for compatibility
      brand_url: website,
      website: website, // for compatibility
      offering,
      target_markets: targetMarkets,
      competitors,
      additional_details: additionalDetails,
      files, // Now array of File objects
    });
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2, mb: 2 }}>
      <Tooltip title="Choose the type of request to make to the agent.">
        <TextField
          select
          label="Request Type"
          value={requestType}
          onChange={(e) => setRequestType(e.target.value)}
          fullWidth
          margin="normal"
          required
          error={!requestType}
          helperText={!requestType ? "Please select a request type" : ""}
        >
          <MenuItem value="" disabled>
            -- Select Request Type --
          </MenuItem>
          {requestOptions.map((option) => (
            <MenuItem key={option.value} value={option.value}>
              {option.label}
            </MenuItem>
          ))}
        </TextField>
      </Tooltip>
      {renderFields()}
      <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>
        Submit
      </Button>
    </Box>
  );
};

export default RequestForm;
