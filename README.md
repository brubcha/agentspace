# Marketing Agent Tool - Project Scaffold

#

# Getting Started (Local Setup)

#

# 1. **Install dependencies**

# - In each of the following folders, run `npm install` (or `pip install -r requirements.txt` for Python):

# - `client/` (React frontend)

# - `api/` (Node.js backend)

# - `agent_services/` (Python microservices)

#

# 2. **Start the application**

# - Use the `launcher-all.bat` file in the root directory to launch all required services (frontend, backend, and agent microservices) at once.

# - This will open the necessary terminals and start the servers for local development.

#

# 3. **Access the app**

# - Once all services are running, open your browser to [http://localhost:3000](http://localhost:3000) to use the application.

#

# ---

#

# Notes for Developers

#

# - Always use `launcher-all.bat` to ensure all services are started in the correct order.

# - Review the `requirements.txt` in `agent_services/` for Python dependencies.

# - Environment variables may be required for API keys (see `.env.example` files if present).

# - For troubleshooting, check the terminal output for each service.

#

## Overview

A monorepo tool for teams to communicate with AI agents. The MVP features a Marketing Agent that generates a Marketing Kit based on your structure, style, and example files. The UI is dynamic, user-friendly, and ready for future expansion.

---

## Color Reference for Output Documents

The project uses a comprehensive color reference for all docx and web output, ensuring brand consistency and accessibility. The color palette is documented in:

**Design Code Package/output-doc/marketing-kit-color-refereence.md**

- This file lists all table, list, callout, card, and text colors with hex/RGB values and usage notes.
- The frontend docx generator (see `client/src/utils/designTokens.ts` and `downloadKitDoc.ts`) uses these tokens for all output styling.
- To update or expand the color palette, edit the markdown file and sync changes to `designTokens.ts`.

Refer to this file when designing new output features or reviewing color usage for accessibility and brand alignment.

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
