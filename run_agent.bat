@echo off
cd /d "C:\Users\ST_12\OneDrive\Documents\Claude Projects\moso-comms-agent"

:: Load ANTHROPIC_API_KEY from .env
for /f "tokens=2 delims==" %%a in ('findstr "ANTHROPIC_API_KEY" .env') do set ANTHROPIC_API_KEY=%%a

:: Set encoding for Unicode email subjects
set PYTHONIOENCODING=utf-8

:: Run the agent in watch mode (polls every 3 minutes)
.venv\Scripts\python.exe -m src.main run --watch
