import React, { useState, useMemo, useEffect } from "react";
import { ThemeProvider, CssBaseline, Container, Box } from "@mui/material";
import { lightTheme, darkTheme } from "./theme";
import NavBar from "./components/NavBar";
import WelcomeMessage from "./components/WelcomeMessage";
import RequestForm from "./components/RequestForm";

import ChatHistory from "./components/ChatHistory";
import DownloadDocButton from "./components/DownloadDocButton";

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

  useEffect(() => {
    const stored = localStorage.getItem(CHAT_HISTORY_KEY);
    if (stored) setChatHistory(JSON.parse(stored));
  }, []);

  useEffect(() => {
    localStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify(chatHistory));
  }, [chatHistory]);

  const handleToggleDarkMode = () => setDarkMode((prev) => !prev);

  const handleRequest = async (data: any) => {
    const userMsg: ChatMessage = {
      role: "user",
      content:
        `Request: ${data.requestType}\nClient: ${
          data.clientName || data.client || ""
        }\n` + (data.extraInfo ? "Extra: " + data.extraInfo : ""),
      timestamp: new Date().toLocaleString(),
    };
    setChatHistory((prev) => [...prev, userMsg]);
    setKitData(null);
    setError(null);

    try {
      let res, result;
      // If files are present, use FormData
      if (data.files && data.files.length > 0) {
        const formData = new FormData();
        Object.entries(data).forEach(([key, value]) => {
          if (key === "files" && Array.isArray(value)) {
            (value as File[]).forEach((file) => formData.append("files", file));
          } else if (typeof value === "string") {
            formData.append(key, value);
          }
        });
        res = await fetch("/api/agent", {
          method: "POST",
          body: formData,
        });
      } else {
        res = await fetch("/api/agent", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });
      }
      if (!res.ok) {
        const errText = await res.text();
        setError(`API error: ${res.status} ${res.statusText} - ${errText}`);
        console.error("API error:", res.status, res.statusText, errText);
        return;
      }
      result = await res.json();
      console.log("Agent response:", result);
      const agentMsg: ChatMessage = {
        role: "agent",
        content: result.message || result,
        timestamp: new Date().toLocaleString(),
      };
      setChatHistory((prev) => [...prev, agentMsg]);
      if (result.structure || result.style || result.outline || result.copy) {
        setKitData(result);
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
    }
  };

  const theme = useMemo(() => (darkMode ? darkTheme : lightTheme), [darkMode]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <NavBar darkMode={darkMode} onToggleDarkMode={handleToggleDarkMode} />
      <Container maxWidth="md">
        <WelcomeMessage />
        {error && (
          <Box sx={{ color: "red", mb: 2 }}>
            <strong>Error:</strong> {error}
          </Box>
        )}
        <RequestForm onSubmit={handleRequest} />
        <ChatHistory history={chatHistory} />
        <Box textAlign="center">
          <DownloadDocButton kitData={kitData} />
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
