# 🚀 Task Orchestrator

A production-grade distributed task processing and API platform built with Python, FastAPI, and Clean Architecture. This project demonstrates enterprise-level software development practices, async programming, and modern Python best practices.

## 👨‍💻 Developer

**Abhinav Soni**

- 🔗 [LinkedIn Profile](https://www.linkedin.com/in/abhinav-soni-9475661b5/)
- 💼 [Naukri Profile](https://www.naukri.com/mnjuser/profile)
- 📧 Open to opportunities in Python Development, Backend Engineering, and Full-Stack Development

---

## 🎯 Features

- **Distributed Task Processing**: Celery-based background task execution with priority queues
- **RESTful API**: FastAPI with JWT authentication, rate limiting, and comprehensive error handling
- **Caching Layer**: Redis for caching, session management, and message queuing
- **Database**: PostgreSQL with async SQLAlchemy 2.0 and Alembic migrations
- **Production Ready**: Docker containerization, CI/CD pipeline, comprehensive testing, structured logging

## 🏗️ Architecture

This project follows **Clean Architecture** principles with clear separation of concerns:

```
┌─────────────────────────────────────┐
│         API Layer (FastAPI)         │
│  Routes, Schemas, Middleware         │
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
- **Database**: PostgreSQL 15+ with SQLAlchemy 2.0 (async)
- **Cache/Queue**: Redis 7+
- **Task Queue**: Celery 5.3+
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Testing**: Pytest with async support
- **Code Quality**: Black, Ruff, MyPy
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git

## 🚀 Quick Start

### Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/abhinav-sys/task-orchestrator.git
cd task-orchestrator

# Copy environment file
cp env.example .env

# Start all services
docker-compose up --build

# Run migrations
docker-compose exec api alembic upgrade head
```

The API will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

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

## 📝 API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Create new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user

### Tasks
- `POST /api/v1/tasks` - Create new task
- `GET /api/v1/tasks` - List tasks (paginated)
- `GET /api/v1/tasks/{id}` - Get task details
- `PUT /api/v1/tasks/{id}` - Update task
- `POST /api/v1/tasks/{id}/cancel` - Cancel task
- `DELETE /api/v1/tasks/{id}` - Delete task

### Users
- `GET /api/v1/users/me` - Get profile
- `PUT /api/v1/users/me` - Update profile

### Health
- `GET /api/v1/health` - Health check
- `GET /api/v1/health/ready` - Readiness check

## 🐳 Docker Services

- **api**: FastAPI application
- **worker**: Celery worker
- **postgres**: PostgreSQL database
- **redis**: Redis cache and message broker

## 🔄 CI/CD

GitHub Actions workflows:
- **CI**: Run tests, linting, type checking on every push
- Automated code quality checks

## 📊 Key Highlights

- ✅ Clean Architecture implementation
- ✅ Full async/await programming
- ✅ Comprehensive type hints (MyPy strict mode)
- ✅ Production-ready error handling and logging
- ✅ Docker containerization
- ✅ Database migrations with Alembic
- ✅ JWT-based authentication
- ✅ Rate limiting and security best practices

## 🎓 What This Project Demonstrates

- **Clean Architecture**: Separation of concerns, dependency inversion
- **Async Programming**: High-performance async operations
- **Type Safety**: Full type coverage with MyPy
- **Design Patterns**: Repository, Factory, Strategy patterns
- **Production Best Practices**: Error handling, logging, monitoring
- **DevOps**: Docker, CI/CD, containerization

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Built with ❤️ by [Abhinav Soni](https://www.linkedin.com/in/abhinav-soni-9475661b5/)**

**Connect with me:**
- 🔗 [LinkedIn](https://www.linkedin.com/in/abhinav-soni-9475661b5/)
- 💼 [Naukri](https://www.naukri.com/mnjuser/profile)
