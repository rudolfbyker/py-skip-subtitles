from dataclasses import dataclass
from typing import Optional


@dataclass
class SubtitlePredicateResult:
    category: str
    severity: int
    description: str


def has_blasphemy(txt: str) -> Optional[SubtitlePredicateResult]:
    words = [
        "god",
        "jesus",
        "christ",
        "lord",
    ]
    if any((w.casefold() in txt.casefold() for w in words)):
        return SubtitlePredicateResult(
            category="profanity",
            severity=3,
            description="blasphemy auto-detected from subtitles",
        )
