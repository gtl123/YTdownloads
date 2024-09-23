from pytubefix import YouTube
import subprocess
import os

def download_video_audio(url):
    # Create YouTube object
    yt = YouTube(url)

    # Get the highest resolution video stream
    video_stream = yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc().first()
    video_path = video_stream.download(filename='video.mp4')

    # Get the highest quality audio stream
    audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
    audio_path = audio_stream.download(filename='audio.mp4')

    # Merge video and audio using ffmpeg
    output_path = f'{yt.title}.mp4'
    subprocess.run(['ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'copy', output_path])

    # Clean up temporary files
    os.remove(video_path)
    os.remove(audio_path)

    print(f'Video and audio merged successfully into {output_path}')




# Example usage
download_video_audio("https://www.youtube.com/watch?v=3aVhXHkbzJA")
