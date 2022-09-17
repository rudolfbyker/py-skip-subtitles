from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta


@dataclass
class VideoSkipScreenshot:
    image_base64: str

    timestamp: timedelta

    description: str

    def __str__(self) -> str:
        return f"{self.timestamp}\n{self.description}"
