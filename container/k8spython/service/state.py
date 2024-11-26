from dataclasses import dataclass
from datetime import datetime

from k8spython.config import EventConfig

import logging

logger = logging.getLogger(__name__)



@dataclass
class Events:
    config: EventConfig
    lastTime: datetime
    # If time is after lastTime then subtract one from chunkCount (if greater than 0). Then schedule for
    chunkCount: int

    def updateChunk(self, time: datetime) -> int:
        if self.lastTime < time:
            if self.chunkCount > 0:
                self.chunkCount -= 1
                self.lastTime = time + self.config.chunkDuration
                logger.info(f"Chunks remaining {self.chunkCount}{" FULL" if self.chunkCount>self.config.maxChunks else ""}")
                return self.config.chunkDuration.total_seconds()
            else:
                return self.config.checkTime.total_seconds()
        else:
            return self.config.checkTime.total_seconds()

    def addChunks(self, chunks: int) -> int:
        self.chunkCount+=chunks
        return self.chunkCount

    def spareCapacity(self) -> bool:
        return self.chunkCount <= self.config.maxChunks
