from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta


@dataclass
class VideoSkipFilter:
    start: timedelta
    """
    Where to start filtering.
    """

    end: timedelta
    """
    Where to end filtering.
    """

    category: str
    """
    E.g. "profanity".
    """

    severity: int
    """
    1 or 2 or 3
    """

    action: str
    """
    E.g. "audio".
    """

    description: str
    """
    Any human-readable text.
    """

    def __str__(self) -> str:
        return f"{self.start} --> {self.end}\n{self.category} {self.action} {self.severity} ({self.description})"
