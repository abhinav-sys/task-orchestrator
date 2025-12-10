"""Report generation worker."""

import asyncio
from uuid import UUID

from app.infrastructure.queue.celery_app import celery_app
from app.infrastructure.queue.task_handlers import update_task_status
from app.domain.value_objects.task_status import TaskStatus


@celery_app.task(name="app.workers.report_generation.process_task")
def process_task(task_id: str) -> dict:
    """Process report generation task."""
    task_uuid = UUID(task_id)
    
    # Run async function
    loop = asyncio.get_event_loop()
    if loop.is_running():
        import nest_asyncio
        nest_asyncio.apply()
    
    asyncio.run(_process_report_task(task_uuid))
    
    return {"status": "completed", "task_id": task_id}


async def _process_report_task(task_id: UUID) -> None:
    """Process report task asynchronously."""
    try:
        # Update task status to running
        await update_task_status(task_id, TaskStatus.RUNNING)

        # Simulate report generation
        await asyncio.sleep(5)  # Simulate work

        # Generate report (example)
        report_data = {
            "report_id": f"RPT-{task_id}",
            "pages": 25,
            "sections": 5,
            "generated_at": "2024-01-01T00:00:00Z",
            "file_path": f"/reports/{task_id}.pdf",
        }

        # Update task status to completed
        await update_task_status(
            task_id,
            TaskStatus.COMPLETED,
            result=report_data,
        )
    except Exception as e:
        # Update task status to failed
        await update_task_status(
            task_id,
            TaskStatus.FAILED,
            error_message=str(e),
        )
        raise


