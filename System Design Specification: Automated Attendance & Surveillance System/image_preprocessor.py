"""Module 2 - ImagePreprocessor: converts raw frames into model tensors."""
from __future__ import annotations

from typing import Sequence, Tuple

import numpy as np

from .schemas import BoundingBox, Frame, PreprocessedFrame


class ImagePreprocessor:
    """Letterbox-resize, colour-convert and normalise frames."""

    def __init__(self, target_size: Tuple[int, int] = (640, 640),
                 mean: Sequence[float] = (0.0, 0.0, 0.0),
                 std: Sequence[float] = (1.0, 1.0, 1.0),
                 bgr_to_rgb: bool = True) -> None:
        self.target_size = target_size   # (width, height)
        self.mean = np.asarray(mean, dtype=np.float32)
        self.std = np.asarray(std, dtype=np.float32)
        self.bgr_to_rgb = bgr_to_rgb

    def process(self, frame: Frame) -> PreprocessedFrame:
        """Full pipeline: letterbox -> colour -> normalise -> NCHW tensor."""
        raise NotImplementedError

    def letterbox(self, image: np.ndarray) -> Tuple[np.ndarray, float, Tuple[int, int]]:
        """Aspect-preserving resize + padding. Returns (image, scale, (pad_x, pad_y))."""
        raise NotImplementedError

    def normalize(self, image: np.ndarray) -> np.ndarray:
        """uint8 HxWx3 -> float32 HxWx3 scaled to [0,1] then (x-mean)/std."""
        raise NotImplementedError

    def to_tensor(self, image: np.ndarray) -> np.ndarray:
        """HxWx3 -> 1x3xHxW contiguous float32."""
        raise NotImplementedError

    def restore_box(self, box: BoundingBox, scale: float,
                    pad: Tuple[int, int]) -> BoundingBox:
        """Map model-space box back to original frame coordinates."""
        raise NotImplementedError
