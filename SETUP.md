# 🚀 Setup Guide - Task Orchestrator

## Quick Start with Docker (Recommended)

### Step 1: Clone and Navigate
```bash
cd task-orchestrator
```

### Step 2: Create Environment File
```bash
cp .env.example .env
# Edit .env if needed (defaults work for Docker)
```

### Step 3: Start Services
```bash
docker-compose up --build
```

This will start:
- PostgreSQL (port 5432)
- Redis (port 6379)
- FastAPI API (port 8000)
- Celery Worker

### Step 4: Run Migrations
In a new terminal:
```bash
docker-compose exec api alembic upgrade head
```

### Step 5: Seed Database (Optional)
```bash
docker-compose exec api python scripts/seed_data.py
```

### Step 6: Access the API
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

## Local Development Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Step 1: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Step 3: Setup Environment
```bash
cp .env.example .env
# Edit .env with your local database and Redis URLs
```

### Step 4: Start PostgreSQL and Redis
```bash
# Using Docker
docker-compose up -d postgres redis

# Or start them locally
```

### Step 5: Run Migrations
```bash
alembic upgrade head
```

### Step 6: Seed Database (Optional)
```bash
python scripts/seed_data.py
```

### Step 7: Start API Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 8: Start Celery Worker (New Terminal)
```bash
celery -A app.infrastructure.queue.celery_app worker --loglevel=info
```

## Testing

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

### Run Specific Test Type
```bash
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
```

## Code Quality

### Format Code
```bash
black .
```

### Lint Code
```bash
ruff check .
```

### Type Check
```bash
mypy .
```

### Run All Checks
```bash
make lint
```

## Using the API

### 1. Sign Up
```bash
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

Save the `access_token` from the response.

### 3. Create a Task
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Process Data",
    "task_type": "data_processing",
    "priority": "high",
    "parameters": {"file_path": "/data/file.csv"}
  }'
```

### 4. Check Task Status
```bash
curl "http://localhost:8000/api/v1/tasks/{task_id}" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Run migrations: `alembic upgrade head`

### Redis Connection Issues
- Ensure Redis is running
- Check REDIS_URL in .env
- Test connection: `redis-cli ping`

### Import Errors
- Activate virtual environment
- Install dependencies: `pip install -r requirements.txt`
- Check PYTHONPATH

### Celery Worker Not Processing Tasks
- Ensure Redis is running (Celery broker)
- Check CELERY_BROKER_URL in .env
- Restart worker: `docker-compose restart worker`

## Next Steps

1. Explore the API documentation at http://localhost:8000/docs
2. Create tasks and watch them process
3. Check task status via API
4. Review the code structure
5. Add your own features!


