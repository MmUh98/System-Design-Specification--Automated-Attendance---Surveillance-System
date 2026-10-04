"""Shared data contracts passed between pipeline modules."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

import numpy as np


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class Frame:
    """Raw frame produced by DataIngestion."""
    frame_id: int
    camera_id: str
    timestamp_utc: float              # UNIX epoch seconds
    image: np.ndarray                 # HxWx3, uint8, BGR
    source_resolution: Tuple[int, int]  # (width, height)


@dataclass(frozen=True)
class PreprocessedFrame:
    """Model-ready tensor plus metadata needed to map boxes back."""
    frame: Frame
    tensor: np.ndarray                # 1x3xHxW, float32, normalised
    scale: float                      # resize ratio applied
    pad: Tuple[int, int]              # (pad_x, pad_y) from letterboxing


@dataclass(frozen=True)
class BoundingBox:
    x_min: float
    y_min: float
    x_max: float
    y_max: float                      # pixel coords in ORIGINAL frame space


@dataclass(frozen=True)
class Detection:
    label: str
    confidence: float                 # 0.0 - 1.0
    box: BoundingBox
    identity: Optional[str] = None    # filled when face recognition matches


@dataclass
class InferenceResult:
    frame_id: int
    camera_id: str
    timestamp_utc: float
    detections: List[Detection] = field(default_factory=list)
    inference_ms: float = 0.0


@dataclass(frozen=True)
class Alert:
    alert_id: str
    camera_id: str
    timestamp_utc: float
    rule_name: str
    severity: Severity
    message: str
    detections: Tuple[Detection, ...] = ()
    snapshot_path: Optional[str] = None


@dataclass(frozen=True)
class AttendanceRecord:
    person_id: str
    camera_id: str
    timestamp_utc: float
    confidence: float
    session_id: str
    synced: bool = False


Metrics = Dict[str, float]
