import React, { useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Link,
  Rating,
  TextField,
  Button,
  Collapse,
} from "@mui/material";
import DownloadIcon from "@mui/icons-material/Download";
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

const FeedbackBox: React.FC<{
  onSubmit: (rating: number, comment: string) => void;
}> = ({ onSubmit }) => {
  const [rating, setRating] = useState<number | null>(null);
  const [comment, setComment] = useState("");
  const [submitted, setSubmitted] = useState(false);
  return (
    <Collapse in={!submitted}>
      <Box sx={{ mt: 1, mb: 1, p: 1, bgcolor: "#f5f5f5", borderRadius: 1 }}>
        <Typography variant="body2" sx={{ mb: 0.5 }}>
          Rate this output:
        </Typography>
        <Rating
          value={rating}
          onChange={(_, val) => setRating(val)}
          size="small"
        />
        <TextField
          size="small"
          label="Comments (optional)"
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          fullWidth
          sx={{ mt: 1, mb: 1 }}
        />
        <Button
          variant="contained"
          size="small"
          disabled={rating == null}
          onClick={() => {
            if (rating != null) {
              onSubmit(rating, comment);
              setSubmitted(true);
            }
          }}
        >
          Submit Feedback
        </Button>
        {submitted && (
          <Typography variant="caption" color="success.main">
            Thank you for your feedback!
          </Typography>
        )}
      </Box>
    </Collapse>
  );
};

const ChatHistory: React.FC<{ history: ChatMessage[] }> = ({ history }) => {
  // Track feedback state for each agent message by index
  const [feedback, setFeedback] = useState<{
    [idx: number]: { rating: number; comment: string };
  }>({});
  return (
    <Box sx={{ mt: 2, mb: 2 }}>
      {history.length === 0 ? (
        <Typography variant="body2" color="text.secondary">
          No chat history yet.
        </Typography>
      ) : (
        history.map((msg, idx) => (
          <Paper
            key={idx}
            sx={(theme) => ({
              p: 2,
              mb: 1,
              background: msg.role === "user" ? "#e3f2fd" : "#f3e5f5",
              color: theme.palette.mode === "dark" ? "#000" : "inherit",
            })}
          >
            <Typography
              variant="caption"
              sx={(theme) => ({
                color:
                  theme.palette.mode === "dark" ? "#000" : "text.secondary",
              })}
            >
              {msg.role === "user" ? "You" : "Agent"} @ {msg.timestamp}
            </Typography>
            {msg.role === "agent" && isKitData(msg.content) ? (
              <>
                <Typography
                  variant="subtitle1"
                  sx={(theme) => ({
                    fontWeight: 600,
                    color: theme.palette.mode === "dark" ? "#000" : "inherit",
                  })}
                >
                  {msg.content.client?.brand_name ||
                    msg.content.meta?.brand ||
                    "Marketing Kit"}
                </Typography>
                <Typography
                  variant="body2"
                  sx={(theme) => ({
                    mb: 1,
                    color: theme.palette.mode === "dark" ? "#000" : "inherit",
                  })}
                >
                  {msg.content.document?.cover?.doc_title || "Marketing Kit"}
                </Typography>
                <Typography
                  variant="body2"
                  sx={(theme) => ({
                    mb: 1,
                    color: theme.palette.mode === "dark" ? "#000" : "inherit",
                  })}
                >
                  {Array.isArray(msg.content.document?.sections)
                    ? msg.content.document.sections
                        .map((s: any) => s.title)
                        .filter(
                          (title: string) =>
                            ![
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
                            ].includes(title),
                        )
                        .join(", ")
                    : "N/A"}
                </Typography>
                <Link
                  component="button"
                  variant="body2"
                  onClick={() => {
                    // Build filename: ClientName_RequestType_YYYYMMDD_HHMMSS.docx
                    // Robust extraction for client name and request type
                    const clientName = (
                      msg.content.originalClientName ||
                      msg.content.client_name ||
                      msg.content.brand_name ||
                      msg.content.document?.client_name ||
                      msg.content.document?.brand_name ||
                      msg.content.client?.brand_name ||
                      msg.content.meta?.brand ||
                      msg.content.client ||
                      "Client"
                    ).replace(/[^a-z0-9]+/gi, "_");
                    const rawRequestType =
                      msg.content.requestType ||
                      msg.content.request_type ||
                      msg.content.meta?.request_type ||
                      msg.content.type ||
                      msg.content.document?.request_type ||
                      "Marketing Kit";
                    const sanitizedRequestType = rawRequestType.replace(
                      /[^a-z0-9]+/gi,
                      "_",
                    );
                    // Use the chat timestamp, format as YYYYMMDD_HHMMSS
                    const date = new Date(msg.timestamp);
                    const pad = (n: number) => n.toString().padStart(2, "0");
                    const dateStr = `${date.getFullYear()}${pad(
                      date.getMonth() + 1,
                    )}${pad(date.getDate())}_${pad(date.getHours())}${pad(
                      date.getMinutes(),
                    )}${pad(date.getSeconds())}`;
                    const filename = `${clientName}_${sanitizedRequestType}_${dateStr}.docx`;
                    if (msg.content?.document?.sections) {
                      downloadKitDoc(
                        msg.content.document.sections,
                        filename,
                        rawRequestType,
                        clientName,
                      );
                    } else {
                      console.warn(
                        "ChatHistory: msg.content.document.sections missing",
                        msg.content,
                      );
                    }
                  }}
                  sx={{
                    mt: 1,
                    display: "inline-flex",
                    alignItems: "center",
                    gap: 0.5,
                  }}
                >
                  <DownloadIcon fontSize="small" sx={{ mr: 0.5 }} /> Download
                </Link>
                {/* Feedback UI for agent output */}
                {feedback[idx] ? (
                  <Typography
                    variant="caption"
                    color="success.main"
                    sx={{ mt: 1 }}
                  >
                    Thank you for your feedback!
                  </Typography>
                ) : (
                  <FeedbackBox
                    onSubmit={async (rating, comment) => {
                      setFeedback((prev) => ({
                        ...prev,
                        [idx]: { rating, comment },
                      }));
                      try {
                        await fetch("/api/feedback", {
                          method: "POST",
                          headers: { "Content-Type": "application/json" },
                          body: JSON.stringify({
                            rating,
                            comment,
                            agentMsg: msg,
                            timestamp: new Date().toISOString(),
                          }),
                        });
                      } catch (err) {
                        // Optionally handle error (e.g., show a message)
                        console.error("Feedback submission failed", err);
                      }
                    }}
                  />
                )}
              </>
            ) : (
              // Render user message as a vertical stack, collapsible if > 5 lines
              <UserMessageCollapsible content={msg.content} />
            )}
          </Paper>
        ))
      )}
    </Box>
  );
};

// Collapsible user message component
const UserMessageCollapsible: React.FC<{ content: string }> = ({ content }) => {
  const [expanded, setExpanded] = React.useState(false);
  if (typeof content !== "string") return <>{JSON.stringify(content)}</>;
  const lines = content.split(/\r?\n/);
  const showCollapse = lines.length > 5;
  const visibleLines = expanded ? lines : lines.slice(0, 5);
  return (
    <Box>
      {visibleLines.map((line, i) => (
        <Typography
          key={i}
          variant="body1"
          sx={(theme) => ({
            color: theme.palette.mode === "dark" ? "#000" : "inherit",
            whiteSpace: "pre-line",
            fontFamily: "monospace",
          })}
        >
          {line}
        </Typography>
      ))}
      {showCollapse && !expanded && (
        <Typography
          variant="body2"
          color="primary"
          sx={{ cursor: "pointer", mt: 1, fontWeight: 600 }}
          onClick={() => setExpanded(true)}
        >
          Read more
        </Typography>
      )}
    </Box>
  );
};

export default ChatHistory;
