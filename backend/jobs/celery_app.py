"""
Celery application configuration for background job processing.
"""

import logging

from celery import Celery, signals

from shared.config.settings import settings

logger = logging.getLogger(__name__)

# Create Celery app
celery_app = Celery(
    "alejandria",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["jobs.tasks"],
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    # Retry strategy with exponential backoff
    task_default_retry_delay=60,  # 1 minute initial
    task_max_retries=5,
    task_acks_late=True,  # Ack only after successful completion
    # Worker configuration
    worker_prefetch_multiplier=1,  # Process one task at a time
    worker_disable_rate_limits=True,
    # Celery Beat schedule for periodic tasks
    beat_schedule={
        "proposal-generation-every-30-minutes": {
            "task": "proposal_generation",
            "schedule": 30.0 * 60,  # 30 minutes
        },
    },
)

# celery_once configuration for distributed locks (must be set separately)
celery_app.conf.ONCE = {
    "backend": "celery_once.backends.redis.Redis",
    "settings": {
        "url": settings.redis_url,
    },
}


# Celery signal handlers for structured logging
@signals.task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, **kwargs):
    logger.info(f"Task started: {task.name}[{task_id}]")


@signals.task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, retval=None, **kwargs):
    logger.info(f"Task completed: {task.name}[{task_id}]")


@signals.task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, **kwargs):
    logger.error(f"Task failed: {task.name}[{task_id}] - {exception}")
