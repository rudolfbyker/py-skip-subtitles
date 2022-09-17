import logging
import sys
from datetime import timedelta

import click
import pysrt

from ._video_skip.file import VideoSkipFile
from ._video_skip.screenshot import VideoSkipScreenshot
from .predicates import has_blasphemy
from .util import get_filters_from_subtitles


@click.command()
@click.argument(
    "subtitles",
    type=click.File("r", encoding="utf8"),
    help="Subtitles input file",
)
@click.argument(
    "screenshot",
    type=click.File("rb"),
    help="Screenshot input file",
)
@click.argument(
    "screenshot_time",
    type=float,
    help="Screenshot time, as a decimal number in seconds.",
)
@click.argument(
    "output",
    type=click.File("w", encoding="utf8"),
    help="Output file",
)
@click.option(
    "--offset",
    type=float,
    default=0,
    help="Subtitles offset",
)
@click.option(
    "--margin",
    type=float,
    default=0,
    help="Filtering margin",
)
def main(subtitles, screenshot, screenshot_time, output, offset, margin):
    """
    \b
    ░▄▀▀░█▄▀░█▒█▀▄░░░▄▀▀░█▒█░██▄░▀█▀░█░▀█▀░█▒░▒██▀░▄▀▀
    ▒▄██░█▒█░█░█▀▒▒░▒▄██░▀▄█▒█▄█░▒█▒░█░▒█▒▒█▄▄░█▄▄▒▄██
    """
    log_to_stdout()

    result = VideoSkipFile(
        filters=list(
            get_filters_from_subtitles(
                subs=pysrt.from_string(subtitles.read()),
                offset=offset,
                margin=margin,
                predicate=has_blasphemy,
            )
        ),
        serviceOffsets={
            # TODO: Allow specifying offset per service.
            "google": 0
        },
        screenshot=VideoSkipScreenshot(
            image_base64="todo read from screenshot file",
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
