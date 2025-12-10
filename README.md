# 🚀 Task Orchestrator - Advanced Python Project

A production-grade distributed task processing and API platform built with Python, demonstrating enterprise-level architecture, async programming, and modern best practices.

## 🎯 Features

- **Distributed Task Processing**: Celery-based background task execution with priority queues
- **RESTful API**: FastAPI with JWT authentication, rate limiting, and WebSocket support
- **Real-time Updates**: WebSocket connections for live task status updates
- **Caching Layer**: Redis for caching, session management, and pub/sub
- **Database**: PostgreSQL with async SQLAlchemy 2.0 and Alembic migrations
- **Production Ready**: Docker, CI/CD, comprehensive testing, logging, and monitoring

## 🏗️ Architecture

This project follows **Clean Architecture** principles with three main layers:

```
┌─────────────────────────────────────┐
│         API Layer (FastAPI)         │
│  Routes, Schemas, Middleware, WS    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│      Application Layer (Services)    │
│    Use Cases, DTOs, Interfaces       │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│    Infrastructure Layer              │
│  Database, Cache, Queue, External    │
└─────────────────────────────────────┘
```

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL 15+
- **Cache/Queue**: Redis 7+
- **Task Queue**: Celery 5.3+
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Testing**: Pytest with async support
- **Code Quality**: Black, Ruff, MyPy
- **Containerization**: Docker & Docker Compose

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd task-orchestrator

# Copy environment file
cp .env.example .env

# Start all services
docker-compose up --build

# Run migrations
docker-compose exec api alembic upgrade head

# Seed database (optional)
docker-compose exec api python scripts/seed_data.py
```

The API will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

### Option 2: Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Start PostgreSQL and Redis (via Docker or locally)
docker-compose up -d postgres redis

# Run migrations
alembic upgrade head

# Start the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, start Celery worker
celery -A app.infrastructure.queue.celery_app worker --loglevel=info
```

## 📁 Project Structure

```
task-orchestrator/
├── app/
│   ├── domain/              # Domain layer (business logic)
│   ├── application/         # Application layer (use cases)
│   ├── infrastructure/      # Infrastructure layer (external services)
│   ├── api/                 # API layer (routes, schemas)
│   ├── workers/             # Celery workers
│   ├── config.py            # Configuration
│   └── main.py              # FastAPI app entry point
├── tests/                   # Test suite
├── scripts/                 # Utility scripts
├── alembic/                 # Database migrations
├── docker/                  # Docker files
└── .github/workflows/       # CI/CD pipelines
```

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Run specific test type
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Run with Docker
docker-compose exec api pytest
```

## 🔧 Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Type check
mypy .

# Run all checks
make lint
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentication

1. **Sign up**: `POST /api/v1/auth/signup`
2. **Login**: `POST /api/v1/auth/login` (returns JWT token)
3. **Use token**: Add `Authorization: Bearer <token>` header to protected routes

## 📝 Example Usage

### Create a Task

```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Process Data",
    "task_type": "data_processing",
    "priority": "high",
    "parameters": {"file_path": "/data/file.csv"}
  }'
```

### Check Task Status

```bash
curl "http://localhost:8000/api/v1/tasks/{task_id}" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🐳 Docker Services

- **api**: FastAPI application
- **worker**: Celery worker
- **postgres**: PostgreSQL database
- **redis**: Redis cache and message broker

## 🔄 CI/CD

GitHub Actions workflows:
- **CI**: Run tests, linting, type checking on every push
- **CD**: Deploy to staging/production (configure as needed)

## 📊 Monitoring

- Health checks: `/api/v1/health` and `/api/v1/ready`
- Structured logging with correlation IDs
- Ready for Prometheus metrics integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and quality checks
5. Submit a pull request

## 📄 License

MIT License

## 🎓 Learning Resources

This project demonstrates:
- Clean Architecture patterns
- Async/await programming
- Type hints and type safety
- Design patterns (Repository, Factory, Strategy)
- Production best practices
- Docker containerization
- CI/CD pipelines

## 🆘 Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Run migrations: `alembic upgrade head`

### Redis Connection Issues
- Verify Redis container is running
- Check REDIS_URL in .env

### Import Errors
- Ensure you're in the project root
- Activate virtual environment
- Install dependencies: `pip install -r requirements.txt`

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ using Python, FastAPI, and modern best practices**

