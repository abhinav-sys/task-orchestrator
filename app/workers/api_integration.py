"""API integration worker."""

import asyncio
from uuid import UUID

import httpx

from app.infrastructure.queue.celery_app import celery_app
from app.infrastructure.queue.task_handlers import update_task_status
from app.domain.value_objects.task_status import TaskStatus


@celery_app.task(name="app.workers.api_integration.process_task")
def process_task(task_id: str) -> dict:
    """Process API integration task."""
    task_uuid = UUID(task_id)
    
    # Run async function
    loop = asyncio.get_event_loop()
    if loop.is_running():
        import nest_asyncio
        nest_asyncio.apply()
    
    asyncio.run(_process_api_task(task_uuid))
    
    return {"status": "completed", "task_id": task_id}


async def _process_api_task(task_id: UUID) -> None:
    """Process API task asynchronously."""
    try:
        # Update task status to running
        await update_task_status(task_id, TaskStatus.RUNNING)

        # Simulate API call
        async with httpx.AsyncClient() as client:
            # Example: Call JSONPlaceholder API
            response = await client.get("https://jsonplaceholder.typicode.com/posts/1")
            response.raise_for_status()
            data = response.json()

        # Update task status to completed
        await update_task_status(
            task_id,
            TaskStatus.COMPLETED,
            result={"api_response": data, "status_code": response.status_code},
        )
    except Exception as e:
        # Update task status to failed
        await update_task_status(
            task_id,
            TaskStatus.FAILED,
            error_message=str(e),
        )
        raise

