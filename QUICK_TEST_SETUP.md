# 🚀 Quick Test Setup (Without Docker)

This guide helps you run the project locally for testing without Docker.

## Option 1: Full Setup with PostgreSQL & Redis (Recommended for Production Testing)

### Prerequisites
- Python 3.11+
- PostgreSQL 15+ (or use Docker for just PostgreSQL/Redis)
- Redis 7+ (or use Docker for just PostgreSQL/Redis)

### Steps

1. **Install PostgreSQL and Redis** (or use Docker Desktop for just these services)

2. **Create Virtual Environment**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. **Install Dependencies**
```powershell
pip install -r requirements.txt
```

4. **Update .env file** for local database:
```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/task_orchestrator
SYNC_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/task_orchestrator
REDIS_URL=redis://localhost:6379/0
```

5. **Run Migrations**
```powershell
alembic upgrade head
```

6. **Start API**
```powershell
uvicorn app.main:app --reload
```

## Option 2: Simplified Test (SQLite + Mock Redis)

For quick testing, we can modify to use SQLite. Let me create a test configuration.


