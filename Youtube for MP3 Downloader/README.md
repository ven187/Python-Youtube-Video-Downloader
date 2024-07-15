# YouTube to MP3 Converter

This Python script downloads a video from YouTube and converts it to MP3 format using `yt_dlp` and `ffmpeg`. It also adds metadata such as title, artist, album, date, genre, track number, and description to the MP3 file.

## Features

- **Download:** Downloads the best audio quality available from YouTube (`bestaudio` option).
- **Conversion:** Converts the downloaded video to MP3 format with a specified bitrate (default: `320k`).
- **Metadata:** Sets MP3 metadata including title, artist, album, release date (year), genre, track number, and description (if available).
- **Cleanup:** Cleans up special characters from the video title for file naming.
- **Timestamp:** Sets the MP3 file's timestamp to the time of download.
- **Deletion:** Optionally deletes the original video file (webm format).

## Prerequisites

Before running the script, make sure you have the following installed:

- Python 3.x
- `yt_dlp` library for downloading YouTube videos
- `mutagen` library for adding metadata to MP3 files
- `ffmpeg` installed and added to PATH for audio conversion. You can download ffmpeg from [ffmpeg.org](https://ffmpeg.org/download.html).

## Usage

Run the script with a YouTube video URL as an argument:

```bash
python script.py <video_url>
