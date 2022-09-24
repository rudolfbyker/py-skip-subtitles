from base64 import b64encode
from datetime import timedelta
from io import BytesIO
from typing import Generator, Callable, Optional

from PIL import Image
from pysrt import SubRipFile, SubRipItem, SubRipTime

from ._video_skip.filter import VideoSkipFilter
from ._predicates import SubtitlePredicateResult


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


def format_base64_data_url(
    *,
    mime_type: str,
    encoded_data: str,
) -> str:
    """
    Create a Base64 data URL.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs

    Args:
        mime_type:
            MIME content type. See https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
        encoded_data:
            Base64 encoded data.

    Returns:
        A Base64 data URL.

    Examples:
        >>> format_base64_data_url("image/jpeg", "YXNkZg==")
        'data:image/jpeg;base64,YXNkZg=='
    """
    return f"data:{mime_type};base64,{encoded_data}"


def limit_image_resolution(
    *,
    image: Image,
    max_height: int = -1,
    max_width: int = -1,
) -> Image:
    """
    Scale the image down if it's greater than the given maximum height or width. Returns a scaled copy of the image.
    """
    if max_width == -1 and max_height == -1:
        scale = 1
    elif max_width == -1:
        scale = max_width / image.width
    elif max_height == -1:
        scale = max_height / image.height
    else:
        scale = min(max_width / image.width, max_height / image.height)

    return image.resize((image.width * scale, image.height * scale))


def image_to_base64(image: Image) -> str:
    """
    Encode the image data to a base64 string.
    """
    output_buffer = BytesIO()
    image.save(output_buffer, format="JPG")
    return b64encode(output_buffer.getvalue()).decode("utf-8")
