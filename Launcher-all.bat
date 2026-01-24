@echo off
REM One-click launcher for AgentSpace (Windows)

REM Start backend API
start cmd /k "cd /d %~dp0api && npm start"

REM Start agent microservice
start cmd /k "cd /d %~dp0 && .venv\Scripts\python.exe -m agent_services.marketing_agent"

REM Start React frontend
start cmd /k "cd /d %~dp0client && npm start"

echo All services are launching in new windows. You can close this window.
pause
