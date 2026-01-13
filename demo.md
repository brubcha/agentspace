# AgentSpace Demo Guide

This guide will help you and your team test the full workflow of the AgentSpace Marketing Kit Generator, including filling out the form, uploading files, submitting a request, and downloading the generated kit.

---

## 1. Usage Guide

### Prerequisites

**For Non-Developers:**

1. Double-click the shortcut or run the provided start script (ask your team for a one-click launcher if available).
2. If you do not have a launcher, follow these steps:
   - Open a terminal (Command Prompt or PowerShell on Windows).
   - Navigate to the project folder (e.g., `cd Y:\Code\agentspace`).
   - Start the backend API:
     - Type: `cd api` and press Enter.
     - Type: `npm start` and press Enter.
   - Open a new terminal window.
   - Start the agent service:
     - Type: `cd agent_services` and press Enter.
     - Type: `python marketing_agent.py` and press Enter.
   - Open a third terminal window.
   - Start the frontend:
     - Type: `cd client` and press Enter.
     - Type: `npm start` and press Enter.
3. Open your web browser and go to [http://localhost:3000](http://localhost:3000).

> If you need a one-click launcher or run-automation, ask your development team to provide a script or shortcut for your platform.

### Steps

1. **Select Request**
   - In the dropdown, choose "Generate Marketing Kit" (the only option for now).
2. **Fill Out the Form**
   - Enter the client name, website, offering, target markets, competitors, and any additional details.
3. **Upload Files**
   - Drag and drop files (docs, PDFs, etc.) into the upload area, or click to select files.
4. **Submit**
   - Click the "Submit" button to send your request to the agent.
5. **View Chat History**
   - Your request and the agent's response will appear in the chat history below the form.
6. **Download the Kit**
   - Click the "Download this kit" link in any agent response to download the generated marketing kit as a Word document.

---

## 2. Video/Screen Capture

### Sample Demo Video

> [!IMPORTANT]
> A sample video demonstrating the full workflow will be linked here when available.

**How to add your own video:**

1. Record your screen using OBS Studio, Loom, Windows Game Bar, or Mac QuickTime.
2. Save the video and upload it to a platform (YouTube, OneDrive, Google Drive, etc.).
3. Replace the placeholder link below with your video URL:

```
Sample Demo Video: [Watch the demo](https://your-video-link-here)
```

---

---

## 3. Written Steps (Quick Reference)

1. Open the app in your browser.
2. Select "Generate Marketing Kit" from the dropdown.
3. Fill in all required fields.
4. Drag and drop or select files to upload.
5. Click "Submit."
6. Wait for the agent's response in the chat history.
7. Click "Download this kit" to get your Word document.

---

## Troubleshooting

- If you see errors, ensure all services are running and your .env is configured.
- For file upload issues, check that files are not too large and are supported types.
- For further help, contact the development team.

---

_Update this guide as the app evolves or new features are added._
