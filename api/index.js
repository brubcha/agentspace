// Basic Express server for Marketing Agent API
const express = require("express");
const cors = require("cors");
require("dotenv").config();

const multer = require("multer");
const upload = multer({
  dest: "uploads/",
  limits: { fileSize: 50 * 1024 * 1024 },
});

const app = express();
app.use(cors());

// Health check
app.get("/api/health", express.json({ limit: "50mb" }), (req, res) => {
  res.json({ status: "ok" });
});

// Connect to Python agent microservice
const axios = require("axios");
const AGENT_SERVICE_URL =
  process.env.AGENT_SERVICE_URL || "http://localhost:7000";

// Only multer handles file uploads for this route (no express.json or urlencoded)
app.post("/api/agent", upload.array("files"), async (req, res) => {
  try {
    let data = req.body;
    // If files are present, add file info to data
    if (req.files && req.files.length > 0) {
      data.files = req.files.map((f) => ({
        originalname: f.originalname,
        mimetype: f.mimetype,
        path: f.path,
        size: f.size,
      }));
    }
    const agentRes = await axios.post(
      `${AGENT_SERVICE_URL}/agent/marketing-kit`,
      data,
    );
    res.json(agentRes.data);
  } catch (err) {
    console.error("Error connecting to agent microservice:", err.message);
    res.status(500).json({
      message: "Error connecting to agent microservice",
      error: err.message,
    });
  }
});


// Feedback endpoint: proxy to Python backend
app.post("/api/feedback", express.json({ limit: "2mb" }), async (req, res) => {
  try {
    const feedbackRes = await axios.post(
      `${AGENT_SERVICE_URL}/feedback`,
      req.body
    );
    res.json(feedbackRes.data);
  } catch (err) {
    console.error("Error posting feedback to agent service:", err.message);
    res.status(500).json({ message: "Error posting feedback", error: err.message });
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`API server running on port ${PORT}`);
});
