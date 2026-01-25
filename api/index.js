// Basic Express server for Marketing Agent API
const express = require("express");
const cors = require("cors");
require("dotenv").config();

const multer = require("multer");
const upload = multer({ dest: "uploads/" });

const app = express();
app.use(cors());
app.use(express.json());

// Health check
app.get("/api/health", (req, res) => {
  res.json({ status: "ok" });
});

// Connect to Python agent microservice
const axios = require("axios");
const AGENT_SERVICE_URL =
  process.env.AGENT_SERVICE_URL || "http://127.0.0.1:5000";

// Proxy route for test compatibility
app.post("/agent/marketing-kit", async (req, res) => {
  try {
    const agentRes = await axios.post(
      `${AGENT_SERVICE_URL}/agent/marketing-kit`,
      req.body
    );
    res.status(agentRes.status).json(agentRes.data);
  } catch (err) {
    if (err.response) {
      res.status(err.response.status).json(err.response.data);
    } else {
      res.status(500).json({
        message: "Error connecting to agent microservice",
        error: err.message,
      });
    }
  }
});
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
      data
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

const PORT = process.env.PORT || 7000;
app.listen(PORT, () => {
  console.log(`API server running on port ${PORT}`);
});
