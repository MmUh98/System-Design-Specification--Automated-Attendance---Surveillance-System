"""Module 3 - ModelInferenceEngine: runs the detector and post-processes output."""
from __future__ import annotations

from typing import List, Optional, Sequence

import numpy as np

from .schemas import Detection, InferenceResult, Metrics, PreprocessedFrame


class ModelInferenceEngine:
    """Wraps an ONNX / TensorRT model behind a hardware-agnostic API."""

    def __init__(self, model_path: str, labels: Sequence[str],
                 device: str = "cuda:0", conf_threshold: float = 0.5,
                 iou_threshold: float = 0.45, use_fp16: bool = True) -> None:
        self.model_path = model_path
        self.labels = list(labels)
        self.device = device
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.use_fp16 = use_fp16
        self._session: Optional[object] = None

    def load_model(self) -> None:
        """Load weights, build runtime session, validate input shape."""
        raise NotImplementedError

    def warmup(self, runs: int = 3) -> None:
        """Dummy passes so the first real frame is not slow."""
        raise NotImplementedError

    def infer(self, item: PreprocessedFrame) -> InferenceResult:
        """Single-frame inference -> post-processed InferenceResult."""
        raise NotImplementedError

    def infer_batch(self, items: Sequence[PreprocessedFrame]) -> List[InferenceResult]:
        """Batched inference for multi-camera deployments."""
        raise NotImplementedError

    def postprocess(self, raw_output: np.ndarray, item: PreprocessedFrame) -> List[Detection]:
        """Decode raw tensor, apply confidence filter + NMS, restore coordinates."""
        raise NotImplementedError

    def get_metrics(self) -> Metrics:
        """Rolling stats: mean_latency_ms, p95_latency_ms, fps, gpu_mem_mb."""
        raise NotImplementedError

    def unload(self) -> None:
        raise NotImplementedError
