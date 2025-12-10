"""Task repository interface."""

from typing import List, Optional
from uuid import UUID

from app.domain.entities.task import Task
from app.domain.value_objects.task_status import TaskStatus, TaskPriority, TaskType


class ITaskRepository:
    """Task repository interface."""

    async def create(self, task: Task) -> Task:
        """Create a new task."""
        raise NotImplementedError

    async def get_by_id(self, task_id: UUID) -> Optional[Task]:
        """Get task by ID."""
        raise NotImplementedError

    async def get_by_user_id(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        status: Optional[TaskStatus] = None,
    ) -> List[Task]:
        """Get tasks by user ID with pagination."""
        raise NotImplementedError

    async def update(self, task: Task) -> Task:
        """Update task."""
        raise NotImplementedError

    async def delete(self, task_id: UUID) -> bool:
        """Delete task."""
        raise NotImplementedError

    async def count_by_user_id(
        self, user_id: UUID, status: Optional[TaskStatus] = None
    ) -> int:
        """Count tasks by user ID."""
        raise NotImplementedError

