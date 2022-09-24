import logging
import sys
from datetime import timedelta

import click
import pysrt
from PIL import Image

from ._video_skip.file import VideoSkipFile
from ._video_skip.screenshot import VideoSkipScreenshot
from ._predicates import has_blasphemy
from ._util import (
    get_filters_from_subtitles,
    format_base64_data_url,
    image_to_base64,
    limit_image_resolution,
)


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
    help="Subtitles offset. Use this when the subtitles file does not align perfectly with the streaming service.",
)
@click.option(
    "--margin",
    type=float,
    default=0,
    help="Filtering margin",
)
def main(subtitles, screenshot, screenshot_time, output, subs_offset, margin):
    """
    \b
    ░▄▀▀░█▄▀░█▒█▀▄░░░▄▀▀░█▒█░██▄░▀█▀░█░▀█▀░█▒░▒██▀░▄▀▀
    ▒▄██░█▒█░█░█▀▒▒░▒▄██░▀▄█▒█▄█░▒█▒░█░▒█▒▒█▄▄░█▄▄▒▄██

    SUBTITLES: Subtitles input file.
    SCREENSHOT: File containing screenshot, for synchronization.
    SCREENSHOT_TIME: The timestamp of the screenshot, as a decimal number, in seconds.
    OUTPUT: Output file, to be used with VideoSkip.
    """
    log_to_stdout()

    result = VideoSkipFile(
        filters=list(
            get_filters_from_subtitles(
                subs=pysrt.from_string(subtitles.read()),
                offset=subs_offset,
                margin=margin,
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


def log_to_stdout():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)


if __name__ == "__main__":
    main()
