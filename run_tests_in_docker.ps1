# PowerShell script to run backend tests in Docker (Windows)
Param()
docker run --rm -v ${PWD}\backend:/app -w /app python:3.11-slim pwsh -c "apt-get update >/dev/null; apt-get install -y gcc >/dev/null; pip install -U pip >/dev/null; pip install -r requirements.txt >/dev/null; pytest -q"
