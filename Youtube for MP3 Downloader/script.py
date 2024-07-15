import yt_dlp
import os
import subprocess
import sys
import re
import time
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, COMM, TRCK

def clean_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_audio(url, output_path='new_path', bitrate='320k'):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        video_ext = info_dict.get('ext', 'webm')  # Default to webm if ext is not found
        video_title = clean_filename(video_title)
        ydl.download([url])

    video_path = f'{output_path}/{video_title}.{video_ext}'
    mp3_path = f'{output_path}/{video_title}.mp3'

    try:
        # Perform ffmpeg conversion
        subprocess.run(['ffmpeg', '-i', video_path, '-b:a', bitrate, mp3_path], check=True)

        # Set the file's timestamp to the download time
        current_time = time.time()
        os.utime(mp3_path, (current_time, current_time))

        # Add metadata
        audio = EasyID3(mp3_path)
        audio['title'] = info_dict.get('title', video_title)
        if 'artist' in info_dict:
            audio['artist'] = info_dict['artist']
        if 'album' in info_dict:
            audio['album'] = info_dict['album']
        if 'upload_date' in info_dict:
            audio['date'] = info_dict['upload_date'][:4]  # Year information
        if 'genre' in info_dict:
            audio['genre'] = info_dict['genre']
        if 'track_number' in info_dict:
            audio['tracknumber'] = str(info_dict['track_number'])
        audio.save()

        # Use ID3 to add a comment
        if 'description' in info_dict:
            id3_audio = ID3(mp3_path)
            id3_audio.add(COMM(encoding=3, lang='eng', desc='desc', text=info_dict['description']))
            id3_audio.save()

        # Delete operation (if you want to delete the webm file)
        os.remove(video_path)

        print("Successfully converted and cleaned up.")
        return mp3_path

    except subprocess.CalledProcessError as e:
        print(f"ffmpeg conversion process failed. Error output: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <video_url>")
        sys.exit(1)

    video_url = sys.argv[1]
    output_file = download_audio(video_url)

    if output_file:
        print(f'Downloaded MP3 file: {output_file}')
    else:
        print('Operation failed.')