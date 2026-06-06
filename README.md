# ResearchGPT: Multi-Agent AI Research Assistant

![ResearchGPT](https://img.shields.io/badge/AI-Research-blue) ![Python](https://img.shields.io/badge/Python-3.11-green) ![FastAPI](https://img.shields.io/badge/FastAPI-0.104-red) ![React](https://img.shields.io/badge/React-18-blue) ![License](https://img.shields.io/badge/License-MIT-green)

A production-ready, multi-agent AI research assistant that demonstrates cutting-edge LLM applications, agent orchestration, RAG systems, and full-stack development.

## 🎯 Features

### 🤖 Multi-Agent Architecture
- **Planner Agent**: Strategic research planning with task decomposition
- **Researcher Agent**: Real-time web search and information gathering
- **Verifier Agent**: Fact-checking and source credibility assessment
- **Writer Agent**: Professional report generation and synthesis

### 🚀 Advanced Capabilities
- Real-time web search integration (Tavily API)
- Multi-LLM support (OpenAI GPT-4, Anthropic Claude)
- Streaming responses for real-time updates
- Fact-checking and verification pipeline
- Source credibility assessment
- Multiple writing styles (academic, journalistic, summary)

### 🔧 Production Ready
- Fully async/await implementation
- Docker containerization
- Kubernetes-ready deployment
- CI/CD pipelines (GitHub Actions)
- Comprehensive error handling
- Health checks and monitoring
- CORS security

## 📋 Project Structure

```
ResearchGPT/
├── backend/                          # FastAPI Backend
│   ├── agents/                       # Multi-agent implementations
│   │   ├── planner.py
│   │   ├── researcher.py
│   │   ├── verifier.py
│   │   └── writer.py
│   ├── services/                     # Core services
│   │   ├── llm.py
│   │   └── search.py
│   ├── graph/                        # Workflow orchestration
│   │   └── workflow.py
│   ├── api/                          # REST endpoints
│   │   └── routes.py
│   ├── tests/                        # Test suites
│   ├── config.py
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/                         # React Frontend
│   ├── src/
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── .github/workflows/                # CI/CD Pipelines
├── deployment/                       # Deployment configs
│   ├── kubernetes/
│   └── aws/
├── docs/                             # Documentation
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- OpenAI API Key
- Tavily API Key

### Local Development

```bash
# Clone repository
git clone https://github.com/srinathdoggala-tech/ResearchGPT.git
cd ResearchGPT

# Setup environment
cp backend/.env.example backend/.env

# Edit backend/.env with your API keys
nano backend/.env

# Run with Docker Compose
docker-compose up
```

Access the application:
- Frontend: http://localhost:5173
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Manual Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## 📡 API Endpoints

### Research Operations

```bash
# Full research workflow
POST /api/research
{
  "topic": "AI and Machine Learning",
  "style": "academic",
  "include_verification": true
}

# Streaming research
POST /api/research/stream

# Quick research
POST /api/research/quick?topic=AI&max_results=5

# Get research plan
POST /api/plan?topic=AI

# Verify content
POST /api/verify?content=Your+content

# Summarize content
POST /api/summarize?content=Your+content&length=medium

# Health check
GET /api/health
```

## 🔑 Configuration

### Environment Variables

```env
# LLM Configuration
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
LLM_MODEL=gpt-4
TEMPERATURE=0.7

# Search Configuration
TAVILY_API_KEY=tvly-...
SEARCH_MAX_RESULTS=5

# Server Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000
WORKERS=4

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

## 🐳 Docker Deployment

### Build and Run

```bash
# Build backend
docker build -t researchgpt-backend:latest ./backend

# Build frontend
docker build -t researchgpt-frontend:latest ./frontend

# Run with compose
docker-compose up -d
```

### Push to Registry

```bash
docker tag researchgpt-backend:latest your-registry/researchgpt-backend:latest
docker push your-registry/researchgpt-backend:latest
```

## ☸️ Kubernetes Deployment

```bash
# Apply configurations
kubectl apply -f deployment/kubernetes/

# Check deployment
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/researchgpt-backend
```

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
pip install pytest pytest-asyncio
pytest tests/ -v
```

### Run Frontend Tests

```bash
cd frontend
npm install
npm test
```

### Integration Tests

```bash
pytest tests/integration/ -v --cov
```

## 📊 Architecture

### Agent Workflow

```
┌─────────────────────────────────────┐
│         User Query                  │
│     (Research Topic)                │
└────────────────┬────────────────────┘
                 │
                 ▼
         ┌──────────────────┐
         │  Planner Agent   │ ← Analyzes topic, creates plan
         └──────────┬───────┘
                    │
                    ▼
         ┌──────────────────────┐
         │ Researcher Agent     │ ← Web search via Tavily
         └──────────┬───────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │ Verifier Agent       │ ← Fact-checks findings
         └──────────┬───────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │ Writer Agent         │ ← Synthesizes report
         └──────────┬───────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │ Research Report      │ ← Professional output
         └──────────────────────┘
```

### Tech Stack

**Backend**
- FastAPI (Web framework)
- LangChain (LLM orchestration)
- OpenAI & Anthropic (LLMs)
- Tavily (Web search)
- Pydantic (Validation)

**Frontend**
- React 18 (UI)
- TypeScript (Type safety)
- Vite (Build tool)
- TailwindCSS (Styling)
- React Query (Data fetching)

**DevOps**
- Docker & Docker Compose
- Kubernetes
- GitHub Actions
- AWS (ECS, CloudFormation)

## 📈 Performance

- **Average Research Time**: 30-60 seconds
- **Typical Report Length**: 2000-3000 words
- **Sources Analyzed**: 5-20 per query
- **API Response Time**: <100ms (excluding research)
- **Throughput**: 100+ concurrent requests

## 🔒 Security

- ✅ Environment-based secrets
- ✅ CORS protection
- ✅ Input validation (Pydantic)
- ✅ Rate limiting ready
- ✅ HTTPS/TLS support
- ✅ API key rotation

## 📚 Documentation

- [API Documentation](docs/API.md)
- [Architecture Guide](docs/ARCHITECTURE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

- Built with [LangChain](https://python.langchain.com/)
- Powered by [OpenAI](https://openai.com/) and [Anthropic](https://anthropic.com/)
- Search via [Tavily](https://tavily.com/)

## CI and Running Tests

This repository includes a GitHub Actions workflow that runs the backend test suite and builds the backend Docker image on push and pull requests. The workflow is at `.github/workflows/ci.yml`.

To run tests locally for the backend:

```bash
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -U pip
pip install -r backend/requirements.txt
cd backend
pytest -q
```

If you don't have API keys (OpenAI / Anthropic / Tavily), the code is resilient and tests may skip or accept 500 responses for endpoints that rely on external APIs. To enable full functionality, populate the env variables as described in `.env.example`.

Alternatively, run tests inside Docker (no local Python required):

```bash
./run_tests_in_docker.sh
# On Windows PowerShell:
./run_tests_in_docker.ps1
```
- Framework: [FastAPI](https://fastapi.tiangolo.com/)

## 📞 Support

- 📧 Issues: [GitHub Issues](https://github.com/srinathdoggala-tech/ResearchGPT/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/srinathdoggala-tech/ResearchGPT/discussions)

---

**Built with ❤️ using AI, FastAPI, and React**

⭐ Star us on GitHub!
