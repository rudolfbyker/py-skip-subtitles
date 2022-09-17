# Skip subtitles

A Python library and CLI to generate skip files from subtitle files.

This allows you to automatically filter unwanted words (e.g. blasphemy) from movies, without having to build the 
filters manually.

## Supported inputs

- `.srt` subtitles

Contribute a PR if you need more.

## Supported outputs

- `.skp` file for VideoSkip.

Contribute a PR if you need more.

## Features

- Automatically generate a skip file from a subtitle file.
  - Specify which words you want to mute.
  - Specify an offset for the timings in the subtitle file.
  - Specify a time margin to mute extra time before and after the filtered line. 
    This helps when the offset is not very accurate.

## Limitations

- Since subtitles are timed per line, it can only mute whole lines.
- It cannot detect homonyms and homographs.
- It cannot detect acceptable uses of words where the acceptability is contextual, e.g. names of God.
