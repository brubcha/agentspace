import React, { useState, useMemo, useEffect } from "react";
import IconButton from "@mui/material/IconButton";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import {
  ThemeProvider,
  CssBaseline,
  Container,
  Box,
  Typography,
  CircularProgress,
  Backdrop,
} from "@mui/material";
import { lightTheme, darkTheme } from "./theme";
import NavBar from "./components/NavBar";
import WelcomeMessage from "./components/WelcomeMessage";
import RequestForm from "./components/RequestForm";

import ChatHistory from "./components/ChatHistory";

interface ChatMessage {
  role: "user" | "agent";
  content: string;
  timestamp: string;
}

const CHAT_HISTORY_KEY = "agentspace_chat_history";

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [kitData, setKitData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem(CHAT_HISTORY_KEY);
    if (stored) setChatHistory(JSON.parse(stored));
  }, []);

  useEffect(() => {
    localStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify(chatHistory));
  }, [chatHistory]);

  const handleToggleDarkMode = () => setDarkMode((prev) => !prev);

  const handleRequest = async (data: any) => {
    // Compose a user message for chat history using mapped fields
    // Compose left-aligned list with NA for missing fields
    const getVal = (v: any) => (v && String(v).trim() ? v : "NA");
    const filesList =
      data.files && Array.isArray(data.files) && data.files.length > 0
        ? data.files
            .map(
              (f: any) =>
                `  - ${f.name ? f.name : f.filename ? f.filename : "[unnamed file]"}`,
            )
            .join("\n")
        : "  - NA";
    const userMsg: ChatMessage = {
      role: "user",
      content:
        `Request: ${getVal(data.request_type || data.requestType)}\n` +
        `Client: ${getVal(data.client_name || data.brand_name || data.client)}\n` +
        `Website: ${getVal(data.brand_url || data.website)}\n` +
        `Offering: ${getVal(data.offering)}\n` +
        `Target Markets: ${getVal(data.target_markets)}\n` +
        `Competitors: ${getVal(data.competitors)}\n` +
        `Additional Details: ${getVal(data.additional_details)}\n` +
        `Files:` +
        (filesList ? `\n${filesList}` : "\n  - NA"),
      timestamp: new Date().toLocaleString(),
    };

    setChatHistory((prev) => [...prev, userMsg]);
    setKitData(null);
    setError(null);
    setLoading(true);

    try {
      let res, result;
      // Always send as JSON (files as array of { filename, content })
      res = await fetch("http://localhost:7000/agent/marketing-kit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) {
        const errText = await res.text();
        setError(`API error: ${res.status} ${res.statusText} - ${errText}`);
        console.error("API error:", res.status, res.statusText, errText);
        return;
      }
      result = await res.json();
      console.log("Agent response:", result);
      // Attach original client name from user input for filename use
      const originalClientName =
        data.client_name || data.brand_name || data.client || "";
      const agentMsg: ChatMessage = {
        role: "agent",
        content: { ...(result.message || result), originalClientName },
        timestamp: new Date().toLocaleString(),
      };
      setChatHistory((prev) => [...prev, agentMsg]);
      if (
        result.structure ||
        result.style ||
        result.outline ||
        result.copy ||
        result.document
      ) {
        setKitData({ ...result, originalClientName });
      }
    } catch (err: any) {
      setError("Network or server error: " + (err?.message || err));
      setChatHistory((prev) => [
        ...prev,
        {
          role: "agent",
          content: "Error: Could not reach agent service.",
          timestamp: new Date().toLocaleString(),
        },
      ]);
      console.error("Request error:", err);
    } finally {
      setLoading(false);
    }
  };

  const theme = useMemo(() => (darkMode ? darkTheme : lightTheme), [darkMode]);

  const [chatOpen, setChatOpen] = useState(true);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <NavBar darkMode={darkMode} onToggleDarkMode={handleToggleDarkMode} />
      <Box sx={{ display: "flex", height: "calc(100vh - 64px)" }}>
        {/* Left panel: Chat History */}
        <Box
          sx={{
            width: chatOpen ? 320 : 0,
            minWidth: chatOpen ? 220 : 0,
            maxWidth: chatOpen ? 400 : 0,
            borderRight: chatOpen ? 1 : 0,
            borderColor: "divider",
            bgcolor: "background.paper",
            overflowY: "auto",
            pt: 2,
            px: 2,
            transition:
              "width 0.3s cubic-bezier(.4,2,.6,1), min-width 0.3s cubic-bezier(.4,2,.6,1), max-width 0.3s cubic-bezier(.4,2,.6,1)",
            position: "relative",
            boxShadow: chatOpen ? 1 : 0,
          }}
        >
          {chatOpen && (
            <>
              <Typography variant="h6" sx={{ px: 2, mb: 1 }}>
                Chat History
              </Typography>
              <ChatHistory history={chatHistory} />
            </>
          )}
        </Box>
        {/* Hide/unhide button, always visible between panels */}
        <Box
          sx={{
            position: "relative",
            zIndex: 3,
            width: 0,
            display: "flex",
            alignItems: "flex-start",
          }}
        >
          <IconButton
            size="small"
            onClick={() => setChatOpen((v) => !v)}
            sx={{
              position: "fixed",
              top: 88,
              left: chatOpen ? 320 - 16 : -16,
              zIndex: 1301,
              width: 32,
              height: 32,
              bgcolor: "background.paper",
              border: 1,
              borderColor: "divider",
              boxShadow: 1,
              p: 0,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              borderRadius: "50%",
              transition: "left 0.3s",
            }}
          >
            {chatOpen ? <ChevronLeftIcon /> : <ChevronRightIcon />}
          </IconButton>
        </Box>
        {/* Main panel: Form, Welcome, Errors */}
        <Box sx={{ flex: 1, p: 3, overflowY: "auto" }}>
          <Container maxWidth="md">
            <WelcomeMessage />
            {error && (
              <Box sx={{ color: "red", mb: 2 }}>
                <strong>Error:</strong> {error}
              </Box>
            )}
            <RequestForm onSubmit={handleRequest} />
            {/* Centered overlay spinner when loading */}
            <Backdrop
              sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 2 }}
              open={loading}
            >
              <Box
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                }}
              >
                <CircularProgress color="inherit" />
                <Typography variant="h6" color="inherit" sx={{ mt: 2 }}>
                  Compiling your asset…
                </Typography>
              </Box>
            </Backdrop>
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;
