"""Task DTOs."""

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel

from app.domain.value_objects.task_status import TaskPriority, TaskStatus, TaskType


class TaskCreateDTO(BaseModel):
    """DTO for creating a task."""

    name: str
    description: Optional[str] = None
    task_type: TaskType
    priority: TaskPriority = TaskPriority.MEDIUM
    parameters: Dict[str, Any] = {}
    max_retries: int = 3


class TaskUpdateDTO(BaseModel):
    """DTO for updating a task."""

    name: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None


class TaskResponseDTO(BaseModel):
    """DTO for task response."""

    id: UUID
    name: str
    description: Optional[str]
    task_type: TaskType
    status: TaskStatus
    priority: TaskPriority
    user_id: UUID
    parameters: Dict[str, Any]
    result: Optional[Dict[str, Any]]
    error_message: Optional[str]
    retry_count: int
    max_retries: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class TaskListResponseDTO(BaseModel):
    """DTO for paginated task list response."""

    items: list[TaskResponseDTO]
    total: int
    page: int
    page_size: int
    total_pages: int

