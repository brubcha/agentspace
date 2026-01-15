# Marketing Agent Tool - Project Scaffold

## Overview

A monorepo tool for teams to communicate with AI agents. The MVP features a Marketing Agent that generates a Marketing Kit based on your structure, style, and example files. The UI is dynamic, user-friendly, and ready for future expansion.

---

## Project Structure

```

---

## Tech Stack

**Frontend**
- React (TypeScript)
- Material UI (@mui/material, @mui/icons-material)
- Emotion (styled, react)
- docx, file-saver
- Testing: Jest, Testing Library

**Backend**
- Node.js (Express)
- axios, cors, dotenv, multer

**Agent Services**
- Python microservices
- Microsoft Agent Framework (agent-framework-azure-ai)

**AI**
- GitHub Copilot (GPT-4.1)

---
root/
│
├── client/                  # React (TypeScript) frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── api/                     # Node.js backend API
│   ├── index.js
│   ├── routes/              # Modular routes for agents, users, models, etc.
│   ├── services/            # Service layer for agent orchestration, MCP, etc.
│   ├── auth/                # Authentication & authorization logic
│   ├── config/              # Config for multiple MCP servers, models, etc.
│   ├── package.json
│   └── ...
│
├── agent_services/          # Multiple agent microservices (Python, etc.)
│   ├── marketing_agent.py
│   ├── sales_agent.py
│   ├── ...
│   ├── requirements.txt
│   └── ...
│
├── mcp_servers/             # Config/scripts for multiple MCP servers
│   ├── foundry_server.json
│   ├── github_server.json
│   └── ...
│
```
