from __future__ import annotations

import json
from dataclasses import dataclass
from typing import List, Dict

from .filter import VideoSkipFilter
from .screenshot import VideoSkipScreenshot


@dataclass
class VideoSkipFile:
    screenshot: VideoSkipScreenshot
    filters: List[VideoSkipFilter]
    service_offsets: Dict[str, float]

    def __str__(self) -> str:
        filters = "\n\n".join(str(s) for s in self.filters)
        return (
            f"{self.screenshot}\n\n"
            f"{filters}\n\n"
            f"{json.dumps(self.service_offsets)}\n\n"
            f"{self.screenshot.image_base64}"
        )
