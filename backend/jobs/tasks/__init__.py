"""Celery tasks for background job processing."""

from jobs.tasks.gap_detection import gap_detection_task
from jobs.tasks.question_generation import question_generation_task
from jobs.tasks.vector_sync import vector_sync_task
from jobs.tasks.proposal_generation import proposal_generation_task
from jobs.tasks.proposal_application import proposal_application_task

__all__ = [
    "gap_detection_task",
    "question_generation_task",
    "vector_sync_task",
    "proposal_generation_task",
    "proposal_application_task",
]
