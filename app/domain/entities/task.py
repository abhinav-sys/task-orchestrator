"""Task entity."""

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.domain.value_objects.task_status import TaskStatus, TaskPriority, TaskType


class Task(BaseModel):
    """Task domain entity."""

    id: UUID = Field(default_factory=uuid4)
    name: str
    description: Optional[str] = None
    task_type: TaskType
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    user_id: UUID
    parameters: Dict[str, Any] = Field(default_factory=dict)
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic config."""

        from_attributes = True
        json_encoders = {UUID: str, datetime: lambda v: v.isoformat()}

    def start(self) -> None:
        """Mark task as started."""
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def complete(self, result: Optional[Dict[str, Any]] = None) -> None:
        """Mark task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.result = result
        self.updated_at = datetime.utcnow()

    def fail(self, error_message: str) -> None:
        """Mark task as failed."""
        self.status = TaskStatus.FAILED
        self.error_message = error_message
        self.completed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def can_retry(self) -> bool:
        """Check if task can be retried."""
        return self.retry_count < self.max_retries and self.status == TaskStatus.FAILED

    def increment_retry(self) -> None:
        """Increment retry count."""
        self.retry_count += 1
        self.status = TaskStatus.PENDING
        self.error_message = None
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        """String representation."""
        return f"<Task {self.name} [{self.status.value}]>"

