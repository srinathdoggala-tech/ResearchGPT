# Backend Documentation

## 🎬 Demonstration

A complete demonstration of the ResearchGPT multi-agent research pipeline is available at [`../assets/Demonstration.mp4`](../assets/Demonstration.mp4).

## Setup

```bash
cd backend
cp .env.example .env
pip install -r requirements.txt
python main.py
```

## Project Structure

- `agents/` - Multi-agent implementations
- `services/` - LLM and search services
- `graph/` - Workflow orchestration
- `api/` - FastAPI routes
- `tests/` - Test suites
- `config.py` - Configuration
- `main.py` - Application entry

## API Documentation

Access Swagger UI at: http://localhost:8000/docs
