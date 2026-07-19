"""
Purpose:
- Backward-compatible scheduler module.

Input:
- ETL job callable.

Output:
- Delegated scheduling behavior from sync_scheduler.

Responsibilities:
- Preserve old import path compatibility.

TODO implementation notes:
- Remove this adapter after full import migration to sync_scheduler.
"""

from scheduler.sync_scheduler import SyncScheduler

PipelineScheduler = SyncScheduler

__all__ = ["SyncScheduler", "PipelineScheduler"]

 