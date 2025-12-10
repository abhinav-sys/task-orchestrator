# 🚀 Run the Project Locally - Step by Step

## Prerequisites Check

✅ Python 3.11+ (You have: Python 3.11.9)
❌ Docker (Not installed - we'll use Option 2)
❌ PostgreSQL (Need to install or use Docker)
❌ Redis (Need to install or use Docker)

## Option 1: Install Docker Desktop (Easiest - Recommended)

### Step 1: Download Docker Desktop
1. Go to: https://www.docker.com/products/docker-desktop
2. Download Docker Desktop for Windows
3. Install and restart your computer
4. Start Docker Desktop

### Step 2: Run the Project
```powershell
cd "C:\Users\Aspire7\Desktop\git hub projects\boost2\task-orchestrator"

# Start all services (PostgreSQL, Redis, API, Worker)
docker-compose up --build

# In another terminal, run migrations
docker-compose exec api alembic upgrade head

# Seed database (optional)
docker-compose exec api python scripts/seed_data.py
```

### Step 3: Access the API
- Open browser: http://localhost:8000/docs
- You'll see the interactive API documentation!

## Option 2: Local Setup (Without Docker)

### Step 1: Install PostgreSQL
1. Download: https://www.postgresql.org/download/windows/
2. Install with default settings
3. Remember the password you set (default user: postgres)

### Step 2: Install Redis
1. Download: https://github.com/microsoftarchive/redis/releases
2. Or use WSL: `wsl --install` then `sudo apt-get install redis`
3. Or use Docker just for Redis: `docker run -d -p 6379:6379 redis:7-alpine`

### Step 3: Create Database
```sql
-- Open PostgreSQL (pgAdmin or psql)
CREATE DATABASE task_orchestrator;
```

### Step 4: Setup Python Environment
```powershell
cd "C:\Users\Aspire7\Desktop\git hub projects\boost2\task-orchestrator"

# Create virtual environment
python -m venv venv

# Activate (PowerShell)
.\venv\Scripts\Activate.ps1

# If activation fails, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt
```

### Step 5: Configure Environment
Edit `.env` file:
```env
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/task_orchestrator
SYNC_DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/task_orchestrator
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_URL=redis://localhost:6379/1
CELERY_BROKER_URL=redis://localhost:6379/2
CELERY_RESULT_BACKEND=redis://localhost:6379/3
```

### Step 6: Run Migrations
```powershell
alembic upgrade head
```

### Step 7: Start Services

**Terminal 1 - API Server:**
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Celery Worker:**
```powershell
celery -A app.infrastructure.queue.celery_app worker --loglevel=info
```

### Step 8: Access API
- Open: http://localhost:8000/docs

## Option 3: Quick Test (Minimal Setup)

If you just want to see the code structure without running the full app:

```powershell
# Run the demo script
python simple_demo.py

# Explore the code
# - Read app/domain/entities/task.py
# - Read app/application/services/task_service.py
# - Read app/api/v1/routes/tasks.py
```

## 🧪 Testing the API

Once running, try these in the Swagger UI at `/docs`:

### 1. Sign Up
```
POST /api/v1/auth/signup
{
  "email": "test@example.com",
  "username": "testuser",
  "password": "password123"
}
```

### 2. Login
```
POST /api/v1/auth/login
username: test@example.com
password: password123
```
Copy the `access_token` from response.

### 3. Create Task
```
POST /api/v1/tasks
Headers: Authorization: Bearer YOUR_ACCESS_TOKEN
{
  "name": "Process Data",
  "task_type": "data_processing",
  "priority": "high",
  "parameters": {"file_path": "/data/file.csv"}
}
```

### 4. Check Task Status
```
GET /api/v1/tasks/{task_id}
Headers: Authorization: Bearer YOUR_ACCESS_TOKEN
```

## 🐛 Troubleshooting

### "Module not found" errors
```powershell
pip install -r requirements.txt
```

### "Database connection failed"
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Check password is correct

### "Redis connection failed"
- Check Redis is running
- Verify REDIS_URL in .env
- Test: `redis-cli ping` (should return PONG)

### "Port already in use"
- Change PORT in .env
- Or stop the service using port 8000

## 📚 Understanding the Code

See `UNDERSTANDING_THE_CODE.md` for a detailed walkthrough of how the code works.

## ✅ Success Checklist

- [ ] Docker Desktop installed OR PostgreSQL + Redis installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] .env file configured
- [ ] Database migrations run (`alembic upgrade head`)
- [ ] API server running (`uvicorn app.main:app --reload`)
- [ ] Celery worker running (if using background tasks)
- [ ] API docs accessible at http://localhost:8000/docs

---

**Recommended:** Install Docker Desktop - it's the easiest way to run everything with one command!


