"""Task repository implementation."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.task import Task
from app.domain.value_objects.task_status import TaskStatus
from app.application.interfaces.task_repository import ITaskRepository
from app.infrastructure.database.models import TaskModel


class TaskRepository(ITaskRepository):
    """Task repository implementation."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository."""
        self.session = session

    async def create(self, task: Task) -> Task:
        """Create a new task."""
        task_model = TaskModel(
            id=task.id,
            name=task.name,
            description=task.description,
            task_type=task.task_type,
            status=task.status,
            priority=task.priority,
            user_id=task.user_id,
            parameters=task.parameters,
            result=task.result,
            error_message=task.error_message,
            retry_count=task.retry_count,
            max_retries=task.max_retries,
            started_at=task.started_at,
            completed_at=task.completed_at,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
        self.session.add(task_model)
        await self.session.commit()
        await self.session.refresh(task_model)
        return self._to_entity(task_model)

    async def get_by_id(self, task_id: UUID) -> Optional[Task]:
        """Get task by ID."""
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        task_model = result.scalar_one_or_none()
        return self._to_entity(task_model) if task_model else None

    async def get_by_user_id(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        status: Optional[TaskStatus] = None,
    ) -> List[Task]:
        """Get tasks by user ID with pagination."""
        query = select(TaskModel).where(TaskModel.user_id == user_id)

        if status:
            query = query.where(TaskModel.status == status)

        query = query.order_by(TaskModel.created_at.desc()).offset(skip).limit(limit)

        result = await self.session.execute(query)
        task_models = result.scalars().all()
        return [self._to_entity(task_model) for task_model in task_models]

    async def update(self, task: Task) -> Task:
        """Update task."""
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == task.id)
        )
        task_model = result.scalar_one_or_none()
        if not task_model:
            raise ValueError(f"Task with ID {task.id} not found")

        task_model.name = task.name
        task_model.description = task.description
        task_model.task_type = task.task_type
        task_model.status = task.status
        task_model.priority = task.priority
        task_model.parameters = task.parameters
        task_model.result = task.result
        task_model.error_message = task.error_message
        task_model.retry_count = task.retry_count
        task_model.max_retries = task.max_retries
        task_model.started_at = task.started_at
        task_model.completed_at = task.completed_at
        task_model.updated_at = task.updated_at

        await self.session.commit()
        await self.session.refresh(task_model)
        return self._to_entity(task_model)

    async def delete(self, task_id: UUID) -> bool:
        """Delete task."""
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        task_model = result.scalar_one_or_none()
        if not task_model:
            return False

        await self.session.delete(task_model)
        await self.session.commit()
        return True

    async def count_by_user_id(
        self, user_id: UUID, status: Optional[TaskStatus] = None
    ) -> int:
        """Count tasks by user ID."""
        query = select(func.count()).select_from(TaskModel).where(
            TaskModel.user_id == user_id
        )

        if status:
            query = query.where(TaskModel.status == status)

        result = await self.session.execute(query)
        return result.scalar() or 0

    def _to_entity(self, task_model: TaskModel) -> Task:
        """Convert model to entity."""
        return Task(
            id=task_model.id,
            name=task_model.name,
            description=task_model.description,
            task_type=task_model.task_type,
            status=task_model.status,
            priority=task_model.priority,
            user_id=task_model.user_id,
            parameters=task_model.parameters,
            result=task_model.result,
            error_message=task_model.error_message,
            retry_count=task_model.retry_count,
            max_retries=task_model.max_retries,
            started_at=task_model.started_at,
            completed_at=task_model.completed_at,
            created_at=task_model.created_at,
            updated_at=task_model.updated_at,
        )


