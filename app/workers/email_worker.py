"""Email worker for sending emails."""

import asyncio
from uuid import UUID

from app.infrastructure.queue.celery_app import celery_app
from app.infrastructure.queue.task_handlers import update_task_status
from app.domain.value_objects.task_status import TaskStatus


@celery_app.task(name="app.workers.email_worker.process_task")
def process_task(task_id: str) -> dict:
    """Process email task."""
    task_uuid = UUID(task_id)
    
    # Run async function
    loop = asyncio.get_event_loop()
    if loop.is_running():
        import nest_asyncio
        nest_asyncio.apply()
    
    asyncio.run(_process_email_task(task_uuid))
    
    return {"status": "completed", "task_id": task_id}


async def _process_email_task(task_id: UUID) -> None:
    """Process email task asynchronously."""
    try:
        # Update task status to running
        await update_task_status(task_id, TaskStatus.RUNNING)

        # Simulate email sending
        await asyncio.sleep(2)  # Simulate work

        # Update task status to completed
        await update_task_status(
            task_id,
            TaskStatus.COMPLETED,
            result={"message": "Email sent successfully", "recipient": "user@example.com"},
        )
    except Exception as e:
        # Update task status to failed
        await update_task_status(
            task_id,
            TaskStatus.FAILED,
            error_message=str(e),
        )
        raise

