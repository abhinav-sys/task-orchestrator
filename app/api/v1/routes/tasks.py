"""Task routes."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.application.dto.task_dto import (
    TaskCreateDTO,
    TaskUpdateDTO,
    TaskResponseDTO,
    TaskListResponseDTO,
)
from app.application.services.task_service import TaskService
from app.dependencies import get_task_service
from app.api.v1.routes.auth import get_current_user
from app.domain.entities.user import User
from app.domain.exceptions.domain_exceptions import (
    TaskNotFoundError,
    TaskCannotBeCancelledError,
    InsufficientPermissionsError,
)
from app.domain.value_objects.task_status import TaskStatus

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreateDTO,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
):
    """Create a new task."""
    return await task_service.create_task(current_user.id, task_data)


@router.get("", response_model=TaskListResponseDTO)
async def get_tasks(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[TaskStatus] = None,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
):
    """Get user's tasks with pagination."""
    return await task_service.get_user_tasks(
        current_user.id, page=page, page_size=page_size, status=status
    )


@router.get("/{task_id}", response_model=TaskResponseDTO)
async def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
):
    """Get task by ID."""
    try:
        from uuid import UUID
        return await task_service.get_task_by_id(UUID(task_id), current_user.id)
    except (TaskNotFoundError, InsufficientPermissionsError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if isinstance(e, TaskNotFoundError) else status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format",
        )


@router.put("/{task_id}", response_model=TaskResponseDTO)
async def update_task(
    task_id: str,
    task_data: TaskUpdateDTO,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
):
    """Update task."""
    try:
        from uuid import UUID
        return await task_service.update_task(UUID(task_id), task_data, current_user.id)
    except (TaskNotFoundError, TaskCannotBeCancelledError, InsufficientPermissionsError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if isinstance(e, TaskNotFoundError) else status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format",
        )


@router.post("/{task_id}/cancel", response_model=TaskResponseDTO)
async def cancel_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
):
    """Cancel a task."""
    try:
        from uuid import UUID
        return await task_service.cancel_task(UUID(task_id), current_user.id)
    except (TaskNotFoundError, TaskCannotBeCancelledError, InsufficientPermissionsError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if isinstance(e, TaskNotFoundError) else status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format",
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
):
    """Delete task."""
    try:
        from uuid import UUID
        deleted = await task_service.delete_task(UUID(task_id), current_user.id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
    except (TaskNotFoundError, InsufficientPermissionsError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if isinstance(e, TaskNotFoundError) else status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format",
        )

