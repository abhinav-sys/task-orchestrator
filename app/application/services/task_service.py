"""Task service."""

from typing import List, Optional
from uuid import UUID

from app.domain.entities.task import Task
from app.domain.exceptions.domain_exceptions import (
    TaskNotFoundError,
    TaskCannotBeCancelledError,
    InsufficientPermissionsError,
)
from app.domain.value_objects.task_status import TaskStatus
from app.application.dto.task_dto import (
    TaskCreateDTO,
    TaskUpdateDTO,
    TaskResponseDTO,
    TaskListResponseDTO,
)
from app.application.interfaces.task_repository import ITaskRepository
from app.infrastructure.queue.celery_app import celery_app


class TaskService:
    """Task service."""

    def __init__(self, task_repository: ITaskRepository) -> None:
        """Initialize task service."""
        self.task_repository = task_repository

    async def create_task(
        self, user_id: UUID, task_data: TaskCreateDTO
    ) -> TaskResponseDTO:
        """Create a new task."""
        task = Task(
            name=task_data.name,
            description=task_data.description,
            task_type=task_data.task_type,
            priority=task_data.priority,
            user_id=user_id,
            parameters=task_data.parameters,
            max_retries=task_data.max_retries,
        )

        created_task = await self.task_repository.create(task)

        # Queue task for execution
        self._queue_task(created_task.id, created_task.task_type.value)

        return TaskResponseDTO.model_validate(created_task)

    async def get_task_by_id(
        self, task_id: UUID, user_id: Optional[UUID] = None
    ) -> TaskResponseDTO:
        """Get task by ID."""
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        # Check permissions
        if user_id and task.user_id != user_id:
            raise InsufficientPermissionsError(
                "You don't have permission to access this task"
            )

        return TaskResponseDTO.model_validate(task)

    async def get_user_tasks(
        self,
        user_id: UUID,
        page: int = 1,
        page_size: int = 20,
        status: Optional[TaskStatus] = None,
    ) -> TaskListResponseDTO:
        """Get tasks for a user with pagination."""
        skip = (page - 1) * page_size
        tasks = await self.task_repository.get_by_user_id(
            user_id, skip=skip, limit=page_size, status=status
        )
        total = await self.task_repository.count_by_user_id(user_id, status=status)

        total_pages = (total + page_size - 1) // page_size

        return TaskListResponseDTO(
            items=[TaskResponseDTO.model_validate(task) for task in tasks],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    async def update_task(
        self, task_id: UUID, task_data: TaskUpdateDTO, user_id: UUID
    ) -> TaskResponseDTO:
        """Update task."""
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        # Check permissions
        if task.user_id != user_id:
            raise InsufficientPermissionsError(
                "You don't have permission to update this task"
            )

        # Check if task can be updated
        if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            raise TaskCannotBeCancelledError(
                f"Cannot update task with status {task.status.value}"
            )

        # Update fields
        if task_data.name is not None:
            task.name = task_data.name
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.priority is not None:
            task.priority = task_data.priority

        updated_task = await self.task_repository.update(task)
        return TaskResponseDTO.model_validate(updated_task)

    async def cancel_task(self, task_id: UUID, user_id: UUID) -> TaskResponseDTO:
        """Cancel a task."""
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        # Check permissions
        if task.user_id != user_id:
            raise InsufficientPermissionsError(
                "You don't have permission to cancel this task"
            )

        # Check if task can be cancelled
        if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
            raise TaskCannotBeCancelledError(
                f"Cannot cancel task with status {task.status.value}"
            )

        task.status = TaskStatus.CANCELLED
        updated_task = await self.task_repository.update(task)

        return TaskResponseDTO.model_validate(updated_task)

    async def delete_task(self, task_id: UUID, user_id: UUID) -> bool:
        """Delete task."""
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        # Check permissions
        if task.user_id != user_id:
            raise InsufficientPermissionsError(
                "You don't have permission to delete this task"
            )

        return await self.task_repository.delete(task_id)

    def _queue_task(self, task_id: UUID, task_type: str) -> None:
        """Queue task for execution."""
        # Map task types to worker task names
        worker_map = {
            "email": "app.workers.email_worker.process_task",
            "data_processing": "app.workers.data_processing.process_task",
            "api_integration": "app.workers.api_integration.process_task",
            "report_generation": "app.workers.report_generation.process_task",
        }
        
        task_name = worker_map.get(task_type, "app.workers.data_processing.process_task")
        celery_app.send_task(
            task_name,
            args=[str(task_id)],
            task_id=str(task_id),
        )

