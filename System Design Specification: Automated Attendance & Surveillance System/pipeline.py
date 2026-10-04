"""Orchestrator wiring the four modules together."""
from __future__ import annotations

from .alert_logger import AlertLogger
from .data_ingestion import BaseDataIngestion
from .image_preprocessor import ImagePreprocessor
from .model_inference_engine import ModelInferenceEngine


class VisionPipeline:
    def __init__(self, ingestion: BaseDataIngestion,
                 preprocessor: ImagePreprocessor,
                 engine: ModelInferenceEngine,
                 logger: AlertLogger) -> None:
        self.ingestion = ingestion
        self.preprocessor = preprocessor
        self.engine = engine
        self.logger = logger

    def run(self) -> None:
        """Main loop: ingest -> preprocess -> infer -> log/alert."""
        self.engine.load_model()
        self.engine.warmup()
        if not self.ingestion.connect():
            raise RuntimeError("Unable to open video source")
        try:
            for frame in self.ingestion.frames():
                prepared = self.preprocessor.process(frame)
                result = self.engine.infer(prepared)
                self.logger.log_event(result)
                for alert in self.logger.evaluate(result):
                    self.logger.dispatch_alert(alert)
        finally:
            self.ingestion.release()
            self.logger.close()
