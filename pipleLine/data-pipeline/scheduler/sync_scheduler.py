"""
Purpose:
- ETL synchronization scheduler for automatic daily data sync.

Input:
- Pipeline job callable and scheduler timing configuration.

Output:
- Scheduled runs with retry behavior and sync history tracking.

Responsibilities:
- Schedule recurring jobs.
- Retry failed runs and capture run history/logging.

TODO implementation notes:
- Persist sync history to durable storage.
- Add alerting hooks on repeated failures.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class SyncHistoryRecord:
    started_at: datetime
    finished_at: datetime | None
    status: str
    attempt: int
    error: str | None = None


class SyncScheduler:
    def __init__(self, cron_hour: int = 2, cron_minute: int = 0, max_retries: int = 3, retry_backoff_seconds: int = 10) -> None:
        self.scheduler = BackgroundScheduler()
        self.cron_hour = cron_hour
        self.cron_minute = cron_minute
        self.max_retries = max_retries
        self.retry_backoff_seconds = retry_backoff_seconds
        self.sync_history: list[SyncHistoryRecord] = []

    def _run_with_retry(self, job_callable: Callable[[], None]) -> None:
        for attempt in range(1, self.max_retries + 1):
            start_time = datetime.now(tz=timezone.utc)
            record = SyncHistoryRecord(
                started_at=start_time,
                finished_at=None,
                status="running",
                attempt=attempt,
            )
            self.sync_history.append(record)

            try:
                LOGGER.info("Starting pipeline sync attempt=%s", attempt)
                job_callable()
                record.finished_at = datetime.now(tz=timezone.utc)
                record.status = "success"
                LOGGER.info("Pipeline sync completed successfully")
                return
            except Exception as exc:
                record.finished_at = datetime.now(tz=timezone.utc)
                record.status = "failed"
                record.error = str(exc)
                LOGGER.exception("Pipeline sync failed attempt=%s", attempt)
                if attempt >= self.max_retries:
                    raise
                time.sleep(self.retry_backoff_seconds)

    def start(self, job_callable: Callable[[], None]) -> None:
        self.scheduler.add_job(
            func=lambda: self._run_with_retry(job_callable),
            trigger="cron",
            hour=self.cron_hour,
            minute=self.cron_minute,
            id="autocare-pipeline-sync",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
        self.scheduler.start()
        LOGGER.info("SyncScheduler started at %02d:%02d", self.cron_hour, self.cron_minute)

    def stop(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=True)
            LOGGER.info("SyncScheduler stopped")
