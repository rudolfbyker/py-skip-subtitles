from datetime import timedelta

import click
import pysrt
from PIL import Image

from ._logging import log_to_stdout
from ._predicates import has_blasphemy
from ._util import (
    get_filters_from_subtitles,
    format_base64_data_url,
    image_to_base64,
    limit_image_resolution,
)
from ._video_skip.file import VideoSkipFile
from ._video_skip.screenshot import VideoSkipScreenshot


@click.command()
@click.argument(
    "subtitles",
    type=click.File("r", encoding="utf8"),
)
@click.argument(
    "screenshot",
    type=click.File("rb"),
)
@click.argument(
    "screenshot_time",
    type=float,
)
@click.argument(
    "output",
    type=click.File("w", encoding="utf8"),
)
@click.option(
    "--subs-offset",
    type=float,
    default=0,
    help="Subtitles offset, as a decimal number of seconds. "
    "Use this when the subtitles file does not align perfectly with the streaming service.",
)
@click.option(
    "--margin",
    type=float,
    default=0,
    help="Filtering margin, as a decimal number of seconds. This is how long before the start of the filtered "
    "subtitles to start muting, and how long to keep muting afterwards.",
)
def main(
    subtitles,
    screenshot,
    screenshot_time: float,
    output,
    subs_offset: float,
    margin: float,
):
    """
    \b
    ░▄▀▀░█▄▀░█▒█▀▄░░░▄▀▀░█▒█░██▄░▀█▀░█░▀█▀░█▒░▒██▀░▄▀▀
    ▒▄██░█▒█░█░█▀▒▒░▒▄██░▀▄█▒█▄█░▒█▒░█░▒█▒▒█▄▄░█▄▄▒▄██

    SUBTITLES: Subtitles input file.
    SCREENSHOT: File containing screenshot, for synchronization.
    SCREENSHOT_TIME: The timestamp of the screenshot, as a decimal number of seconds.
    OUTPUT: Output file, to be used with VideoSkip.
    """
    log_to_stdout()

    result = VideoSkipFile(
        filters=list(
            get_filters_from_subtitles(
                subs=pysrt.from_string(subtitles.read()),
                offset=timedelta(seconds=subs_offset),
                margin=timedelta(seconds=margin),
                predicate=has_blasphemy,
            )
        ),
        serviceOffsets={
            # TODO: Allow specifying offset per service.
            "google": 0
        },
        screenshot=VideoSkipScreenshot(
            image_base64=format_base64_data_url(
                mime_type="image/jpeg",
                encoded_data=image_to_base64(
                    limit_image_resolution(
                        image=Image.open(screenshot),
                        max_height=240,
                    )
                ),
            ),
            timestamp=timedelta(seconds=screenshot_time),
            description="screenshot",
        ),
    )

    output.write(str(result))
