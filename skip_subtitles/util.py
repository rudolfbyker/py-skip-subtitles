from datetime import timedelta
from typing import Generator, Callable, Optional

from pysrt import SubRipFile, SubRipItem, SubRipTime

from ._video_skip.filter import VideoSkipFilter
from .predicates import SubtitlePredicateResult


def get_filters_from_subtitles(
    *,
    subs: SubRipFile,
    offset: timedelta,
    margin: timedelta,
    predicate: Callable[[str], Optional[SubtitlePredicateResult]],
) -> Generator[VideoSkipFilter, None, None]:
    sub: SubRipItem
    for sub in subs:
        result = predicate(sub.text_without_tags)
        if result:
            yield VideoSkipFilter(
                start=sub_to_timedelta(sub.start) + offset - margin,
                end=sub_to_timedelta(sub.end) + offset + margin,
                category=result.category,
                severity=result.severity,
                description=result.description,
                action="audio",
            )


def sub_to_timedelta(t: SubRipTime) -> timedelta:
    """
    `SubRipTime` has a `to_time` method, but we want a `to_timedelta` method, which is not available.
    `timedelta` is more appropriate for specifying movie timestamps, because `time` is limited to 24 hours.
    """
    return timedelta(
        hours=t.hours,
        minutes=t.minutes,
        seconds=t.seconds,
        milliseconds=t.milliseconds,
    )
