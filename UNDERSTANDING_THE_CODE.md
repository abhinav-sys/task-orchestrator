# 📚 Understanding the Code - Step by Step

## 🎯 Quick Overview

This project demonstrates **Clean Architecture** - a way to organize code that separates business logic from technical details.

## 📖 How to Read This Codebase

### 1. Start with Domain Layer (Pure Business Logic)

**File: `app/domain/entities/task.py`**
```python
# This is a pure Python class - no database, no framework dependencies
class Task:
    def start(self):
        """Business rule: When task starts, update status and timestamp"""
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.utcnow()
    
    def complete(self, result):
        """Business rule: When task completes, save result"""
        self.status = TaskStatus.COMPLETED
        self.result = result
```

**Why it matters:** This is your business logic. It doesn't care if you use PostgreSQL, MySQL, or MongoDB. It's testable without any database.

### 2. Application Layer (Use Cases)

**File: `app/application/services/task_service.py`**
```python
class TaskService:
    async def create_task(self, user_id, task_data):
        # 1. Create domain entity (business logic)
        task = Task(name=..., task_type=..., user_id=user_id)
        
        # 2. Save via repository (abstraction - doesn't care about database)
        created_task = await self.task_repository.create(task)
        
        # 3. Queue for background processing
        self._queue_task(created_task.id, created_task.task_type.value)
        
        return TaskResponseDTO.model_validate(created_task)
```

**Why it matters:** This orchestrates the business logic. It defines WHAT the system does, not HOW it's stored.

### 3. Infrastructure Layer (Technical Implementation)

**File: `app/infrastructure/database/repositories/task_repository.py`**
```python
class TaskRepository(ITaskRepository):
    async def create(self, task: Task) -> Task:
        # Convert domain entity to database model
        task_model = TaskModel(
            id=task.id,
            name=task.name,
            status=task.status.value,  # Convert enum to string
            ...
        )
        
        # Save to PostgreSQL
        self.session.add(task_model)
        await self.session.commit()
        
        # Convert back to domain entity
        return self._to_entity(task_model)
```

**Why it matters:** This is WHERE the data is stored. You could swap PostgreSQL for MongoDB here without changing business logic.

### 4. API Layer (HTTP Interface)

**File: `app/api/v1/routes/tasks.py`**
```python
@router.post("", response_model=TaskResponseDTO)
async def create_task(
    task_data: TaskCreateDTO,
    current_user: User = Depends(get_current_user),  # Auth check
    task_service: TaskService = Depends(get_task_service),
):
    # Call the service (use case)
    return await task_service.create_task(current_user.id, task_data)
```

**Why it matters:** This handles HTTP requests. It validates input, authenticates users, and calls the service layer.

## 🔄 Complete Flow Example

Let's trace a request from start to finish:

### User Creates a Task

```
1. HTTP Request
   POST /api/v1/tasks
   {
     "name": "Process Data",
     "task_type": "data_processing",
     "priority": "high"
   }
   ↓

2. API Route (app/api/v1/routes/tasks.py)
   - Validates request body (Pydantic)
   - Checks authentication (JWT token)
   - Extracts current user
   ↓

3. Service Layer (app/application/services/task_service.py)
   - Creates Task entity (domain)
   - Saves via repository
   - Queues task to Celery
   ↓

4. Repository (app/infrastructure/database/repositories/task_repository.py)
   - Converts Task entity → TaskModel (SQLAlchemy)
   - Saves to PostgreSQL
   - Converts back → Task entity
   ↓

5. Celery Worker (app/workers/data_processor.py)
   - Picks up task from Redis queue
   - Processes task
   - Updates task status in database
   ↓

6. Response
   {
     "id": "...",
     "name": "Process Data",
     "status": "pending",
     ...
   }
```

## 🗂️ Key Files to Explore

### Domain Layer (Start Here)
- `app/domain/entities/task.py` - Task business logic
- `app/domain/entities/user.py` - User business logic
- `app/domain/value_objects/task_status.py` - Enums

### Application Layer
- `app/application/services/task_service.py` - Task use cases
- `app/application/services/auth_service.py` - Authentication logic
- `app/application/dto/task_dto.py` - Data transfer objects

### Infrastructure Layer
- `app/infrastructure/database/models.py` - Database models
- `app/infrastructure/database/repositories/task_repository.py` - Database operations
- `app/infrastructure/queue/celery_app.py` - Celery configuration

### API Layer
- `app/api/v1/routes/tasks.py` - Task endpoints
- `app/api/v1/routes/auth.py` - Authentication endpoints
- `app/main.py` - FastAPI app setup

### Workers
- `app/workers/data_processor.py` - Background task processing
- `app/workers/email_worker.py` - Email sending

## 🧪 Testing the Flow

### 1. Start the API (after installing dependencies)
```bash
uvicorn app.main:app --reload
```

### 2. Open API Docs
```
http://localhost:8000/docs
```

### 3. Try These Steps:

**Step 1: Sign Up**
- POST `/api/v1/auth/signup`
- Body: `{"email": "test@example.com", "username": "testuser", "password": "password123"}`

**Step 2: Login**
- POST `/api/v1/auth/login`
- Body: `username=test@example.com&password=password123`
- Copy the `access_token` from response

**Step 3: Create Task**
- POST `/api/v1/tasks`
- Headers: `Authorization: Bearer YOUR_ACCESS_TOKEN`
- Body: `{"name": "Test Task", "task_type": "data_processing", "priority": "high"}`

**Step 4: Check Task Status**
- GET `/api/v1/tasks/{task_id}`
- Headers: `Authorization: Bearer YOUR_ACCESS_TOKEN`

## 💡 Key Concepts

### Dependency Injection
Services receive dependencies (repositories) instead of creating them:
```python
def get_task_service(
    task_repo: TaskRepository = Depends(get_task_repository),
) -> TaskService:
    return TaskService(task_repo)
```

### Repository Pattern
Abstraction over data storage:
```python
# Interface (what we need)
class ITaskRepository:
    async def create(self, task: Task) -> Task: ...

# Implementation (how we do it)
class TaskRepository(ITaskRepository):
    async def create(self, task: Task) -> Task:
        # PostgreSQL implementation
```

### DTOs (Data Transfer Objects)
Separate API models from domain models:
```python
# API layer uses DTOs
class TaskCreateDTO(BaseModel):
    name: str
    task_type: TaskType

# Domain layer uses entities
class Task:
    name: str
    task_type: TaskType
    # Plus business methods
```

## 🎓 Learning Path

1. **Read Domain Entities** - Understand business logic
2. **Read Services** - Understand use cases
3. **Read Repositories** - Understand data persistence
4. **Read API Routes** - Understand HTTP interface
5. **Read Workers** - Understand background processing

## 🚀 Next Steps

1. Install Docker Desktop (easiest way to run)
2. Or install PostgreSQL + Redis locally
3. Follow SETUP.md to run the project
4. Explore the API at `/docs`
5. Create tasks and watch them process!

---

**Remember:** Clean Architecture separates WHAT your app does (domain) from HOW it does it (infrastructure). This makes code testable, maintainable, and scalable!


