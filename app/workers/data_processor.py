"""Data processing worker."""

import asyncio
import json
from uuid import UUID

from app.infrastructure.queue.celery_app import celery_app
from app.infrastructure.queue.task_handlers import update_task_status
from app.domain.value_objects.task_status import TaskStatus


@celery_app.task(name="app.workers.data_processing.process_task")
def process_task(task_id: str) -> dict:
    """Process data processing task."""
    task_uuid = UUID(task_id)
    
    # Run async function
    loop = asyncio.get_event_loop()
    if loop.is_running():
        import nest_asyncio
        nest_asyncio.apply()
    
    asyncio.run(_process_data_task(task_uuid))
    
    return {"status": "completed", "task_id": task_id}


async def _process_data_task(task_id: UUID) -> None:
    """Process data task asynchronously."""
    try:
        # Update task status to running
        await update_task_status(task_id, TaskStatus.RUNNING)

        # Simulate data processing
        await asyncio.sleep(3)  # Simulate work

        # Process data (example)
        processed_data = {
            "rows_processed": 1000,
            "rows_successful": 950,
            "rows_failed": 50,
            "processing_time_seconds": 3.0,
        }

        # Update task status to completed
        await update_task_status(
            task_id,
            TaskStatus.COMPLETED,
            result=processed_data,
        )
    except Exception as e:
        # Update task status to failed
        await update_task_status(
            task_id,
            TaskStatus.FAILED,
            error_message=str(e),
        )
        raise

