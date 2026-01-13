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
  process.env.AGENT_SERVICE_URL || "http://localhost:7000";

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

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`API server running on port ${PORT}`);
});
