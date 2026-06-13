# Start ResearchGPT Backend on Port 8001
Start-Process cmd.exe -ArgumentList "/k cd backend && .\venv\Scripts\python.exe main.py" -WorkingDirectory $PSScriptRoot

# Start ResearchGPT Frontend on Port 5173
Start-Process cmd.exe -ArgumentList "/k cd frontend && npm run dev" -WorkingDirectory $PSScriptRoot
