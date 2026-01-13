import React from "react";
import { Box, Typography, Paper, Link } from "@mui/material";
import { downloadKitDoc } from "../utils/downloadKitDoc";

interface ChatMessage {
  role: "user" | "agent";
  content: string | any;
  timestamp: string;
}

function isKitData(content: any) {
  // Heuristic: has document, client, or front_matter fields
  return (
    content && (content.document || content.client || content.front_matter)
  );
}

const ChatHistory: React.FC<{ history: ChatMessage[] }> = ({ history }) => (
  <Box sx={{ mt: 2, mb: 2 }}>
    <Typography variant="h6" gutterBottom>
      Chat History
    </Typography>
    {history.length === 0 ? (
      <Typography variant="body2" color="text.secondary">
        No chat history yet.
      </Typography>
    ) : (
      history.map((msg, idx) => (
        <Paper
          key={idx}
          sx={{
            p: 2,
            mb: 1,
            background: msg.role === "user" ? "#e3f2fd" : "#f3e5f5",
          }}
        >
          <Typography variant="caption" color="text.secondary">
            {msg.role === "user" ? "You" : "Agent"} @ {msg.timestamp}
          </Typography>
          {msg.role === "agent" && isKitData(msg.content) ? (
            <>
              <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                {msg.content.client?.brand_name ||
                  msg.content.meta?.brand ||
                  "Marketing Kit"}
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                {msg.content.document?.cover?.doc_title || "Marketing Kit"}
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                Sections:{" "}
                {Array.isArray(msg.content.document?.sections)
                  ? msg.content.document.sections
                      .map((s: any) => s.title)
                      .join(", ")
                  : "N/A"}
              </Typography>
              <Link
                component="button"
                variant="body2"
                onClick={() => {
                  // Build filename: ClientName_RequestType_YYYYMMDD_HHMMSS.docx
                  const clientName = (
                    msg.content.client?.brand_name || "Client"
                  ).replace(/[^a-z0-9]+/gi, "_");
                  const requestType = (
                    msg.content.requestType || "MarketingKit"
                  ).replace(/[^a-z0-9]+/gi, "_");
                  // Use the chat timestamp, format as YYYYMMDD_HHMMSS
                  const date = new Date(msg.timestamp);
                  const pad = (n: number) => n.toString().padStart(2, "0");
                  const dateStr = `${date.getFullYear()}${pad(
                    date.getMonth() + 1
                  )}${pad(date.getDate())}_${pad(date.getHours())}${pad(
                    date.getMinutes()
                  )}${pad(date.getSeconds())}`;
                  const filename = `${clientName}_${requestType}_${dateStr}.docx`;
                  downloadKitDoc(msg.content, filename);
                }}
                sx={{ mt: 1 }}
              >
                Download this kit
              </Link>
            </>
          ) : (
            <Typography variant="body1">
              {typeof msg.content === "string"
                ? msg.content
                : JSON.stringify(msg.content)}
            </Typography>
          )}
        </Paper>
      ))
    )}
  </Box>
);

export default ChatHistory;
