"""Task status and related enums."""

from enum import Enum


class TaskStatus(str, Enum):
    """Task status enumeration."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Task priority enumeration."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskType(str, Enum):
    """Task type enumeration."""

    EMAIL = "email"
    DATA_PROCESSING = "data_processing"
    API_INTEGRATION = "api_integration"
    REPORT_GENERATION = "report_generation"


