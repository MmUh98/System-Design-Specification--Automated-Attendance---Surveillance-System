"""Module 1 - DataIngestion: acquires frames from camera / file sources."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator, Optional

from .schemas import Frame


class BaseDataIngestion(ABC):
    """Contract for every frame source (RTSP, USB, video file)."""

    @abstractmethod
    def connect(self) -> bool:
        """Open the source. Returns True on success; retries are internal."""

    @abstractmethod
    def read_frame(self, timeout_s: float = 2.0) -> Optional[Frame]:
        """Return the next Frame, or None on timeout / end of stream."""

    @abstractmethod
    def is_connected(self) -> bool:
        """True while the stream is healthy."""

    @abstractmethod
    def release(self) -> None:
        """Free sockets, decoders and buffers."""

    def frames(self) -> Iterator[Frame]:
        """Generator wrapper: yields frames until the stream ends."""
        while self.is_connected():
            frame = self.read_frame()
            if frame is not None:
                yield frame


class RTSPDataIngestion(BaseDataIngestion):
    """RTSP/H.264 ingestion with frame skipping and auto-reconnect."""

    def __init__(self, camera_id: str, rtsp_url: str,
                 target_fps: int = 15, max_retries: int = 5,
                 queue_size: int = 4) -> None:
        self.camera_id = camera_id
        self.rtsp_url = rtsp_url
        self.target_fps = target_fps
        self.max_retries = max_retries
        self.queue_size = queue_size   # small queue -> drop stale frames

    def connect(self) -> bool:
        raise NotImplementedError

    def read_frame(self, timeout_s: float = 2.0) -> Optional[Frame]:
        raise NotImplementedError

    def is_connected(self) -> bool:
        raise NotImplementedError

    def release(self) -> None:
        raise NotImplementedError
