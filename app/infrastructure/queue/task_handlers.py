"""Task handlers for Celery."""

from typing import Any, Dict
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.base import AsyncSessionLocal
from app.infrastructure.database.repositories.task_repository import TaskRepository
from app.domain.value_objects.task_status import TaskStatus


async def update_task_status(
    task_id: UUID,
    status: TaskStatus,
    result: Dict[str, Any] | None = None,
    error_message: str | None = None,
) -> None:
    """Update task status in database."""
    async with AsyncSessionLocal() as session:
        task_repo = TaskRepository(session)
        task = await task_repo.get_by_id(task_id)
        if not task:
            return

        if status == TaskStatus.RUNNING:
            task.start()
        elif status == TaskStatus.COMPLETED:
            task.complete(result)
        elif status == TaskStatus.FAILED:
            task.fail(error_message or "Task failed")

        await task_repo.update(task)


