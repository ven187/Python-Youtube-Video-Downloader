import subprocess
import sys
import os

def download_video(video_url, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    command = f'yt-dlp -o "{output_directory}/%(title)s.%(ext)s" {video_url} -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'

    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Video successfully downloaded and saved to {output_directory}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while downloading the video: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <video_url>")
        sys.exit(1)

    video_url = sys.argv[1]
    output_directory = "downloads"

    download_video(video_url, output_directory)
