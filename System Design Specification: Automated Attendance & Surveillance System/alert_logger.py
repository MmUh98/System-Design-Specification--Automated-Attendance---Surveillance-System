"""Module 4 - AlertLogger: rule evaluation, persistence and notification."""
from __future__ import annotations

from typing import Callable, List, Optional, Sequence

from .schemas import Alert, AttendanceRecord, InferenceResult, Severity


class AlertRule:
    """A named predicate over an InferenceResult."""

    def __init__(self, name: str, severity: Severity,
                 predicate: Callable[[InferenceResult], bool],
                 cooldown_s: float = 30.0) -> None:
        self.name = name
        self.severity = severity
        self.predicate = predicate
        self.cooldown_s = cooldown_s   # suppress duplicate alerts


class AlertLogger:
    """Turns inference results into logs, attendance rows and alerts."""

    def __init__(self, db_url: str, rules: Sequence[AlertRule],
                 notifier_endpoints: Sequence[str] = (),
                 snapshot_dir: str = "./snapshots",
                 retention_days: int = 30) -> None:
        self.db_url = db_url
        self.rules = list(rules)
        self.notifier_endpoints = list(notifier_endpoints)
        self.snapshot_dir = snapshot_dir
        self.retention_days = retention_days

    def log_event(self, result: InferenceResult) -> None:
        """Persist every inference result (batched writes)."""
        raise NotImplementedError

    def evaluate(self, result: InferenceResult) -> List[Alert]:
        """Apply rules + cooldowns; return newly raised alerts."""
        raise NotImplementedError

    def dispatch_alert(self, alert: Alert) -> bool:
        """Push to dashboard / SMS / email / webhook. True if delivered."""
        raise NotImplementedError

    def log_attendance(self, record: AttendanceRecord) -> bool:
        """Insert once per person per session; False if duplicate."""
        raise NotImplementedError

    def sync_pending(self, max_batch: int = 100) -> int:
        """Upload unsynced rows to central DB. Returns number synced."""
        raise NotImplementedError

    def save_snapshot(self, result: InferenceResult) -> Optional[str]:
        """Write annotated frame to disk and return its path."""
        raise NotImplementedError

    def purge_expired(self) -> int:
        """Delete data older than retention_days. Returns rows removed."""
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError
