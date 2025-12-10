"""Simple demo script to show the project structure and basic functionality."""

import asyncio
from app.config import settings
from app.domain.entities.user import User
from app.domain.entities.task import Task
from app.domain.value_objects.task_status import TaskType, TaskPriority, TaskStatus
from app.infrastructure.security.password_handler import PasswordHandler

def demo_domain_entities():
    """Demonstrate domain entities."""
    print("=" * 60)
    print("DEMO: Domain Entities")
    print("=" * 60)
    
    # Create a user
    password_handler = PasswordHandler()
    user = User(
        email="demo@example.com",
        username="demo_user",
        hashed_password=password_handler.hash_password("password123"),
        full_name="Demo User"
    )
    print(f"\n✅ Created User: {user}")
    print(f"   - Email: {user.email}")
    print(f"   - Username: {user.username}")
    print(f"   - Active: {user.is_active}")
    
    # Create a task
    task = Task(
        name="Process Data",
        description="Process customer data",
        task_type=TaskType.DATA_PROCESSING,
        priority=TaskPriority.HIGH,
        user_id=user.id,
        parameters={"file_path": "/data/customers.csv"}
    )
    print(f"\n✅ Created Task: {task}")
    print(f"   - Name: {task.name}")
    print(f"   - Type: {task.task_type.value}")
    print(f"   - Status: {task.status.value}")
    print(f"   - Priority: {task.priority.value}")
    
    # Demonstrate task state changes
    print(f"\n📊 Task State Changes:")
    print(f"   Initial: {task.status.value}")
    
    task.start()
    print(f"   Started: {task.status.value}")
    
    task.complete({"rows_processed": 1000})
    print(f"   Completed: {task.status.value}")
    print(f"   Result: {task.result}")
    
    return user, task

def demo_config():
    """Demonstrate configuration."""
    print("\n" + "=" * 60)
    print("DEMO: Configuration")
    print("=" * 60)
    print(f"✅ App Name: {settings.app_name}")
    print(f"✅ Version: {settings.app_version}")
    print(f"✅ Environment: {settings.environment}")
    print(f"✅ Debug Mode: {settings.debug}")
    print(f"✅ Database URL: {settings.database_url[:50]}...")
    print(f"✅ Redis URL: {settings.redis_url}")

def demo_architecture():
    """Explain the architecture."""
    print("\n" + "=" * 60)
    print("DEMO: Project Architecture")
    print("=" * 60)
    print("""
🏗️ Clean Architecture Layers:

1. Domain Layer (app/domain/)
   - Entities: User, Task
   - Value Objects: TaskStatus, TaskPriority, TaskType
   - Business Logic & Rules

2. Application Layer (app/application/)
   - Services: AuthService, TaskService, UserService
   - DTOs: Data Transfer Objects
   - Use Cases

3. Infrastructure Layer (app/infrastructure/)
   - Database: SQLAlchemy models & repositories
   - Cache: Redis client
   - Queue: Celery configuration
   - Security: Password hashing, JWT

4. API Layer (app/api/)
   - Routes: REST endpoints
   - Middleware: Rate limiting, logging
   - Schemas: Request/response models

5. Workers (app/workers/)
   - Celery workers for background tasks
   - Email, Data Processing, API Integration, Reports
    """)

def main():
    """Run the demo."""
    print("\n" + "🚀" * 30)
    print("TASK ORCHESTRATOR - PROJECT DEMO")
    print("🚀" * 30)
    
    demo_config()
    demo_architecture()
    user, task = demo_domain_entities()
    
    print("\n" + "=" * 60)
    print("✅ DEMO COMPLETE!")
    print("=" * 60)
    print("""
📝 Next Steps:
1. Install all dependencies: pip install -r requirements.txt
2. Set up PostgreSQL and Redis (or use Docker)
3. Run migrations: alembic upgrade head
4. Start API: uvicorn app.main:app --reload
5. Visit: http://localhost:8000/docs

💡 To run with Docker:
   docker-compose up --build
    """)

if __name__ == "__main__":
    main()


