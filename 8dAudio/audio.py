import subprocess
from pydub import AudioSegment
import numpy as np


def extract_audio(mp4_file, output_audio_file):
    command = f"ffmpeg -i {mp4_file} -q:a 0 -map a {output_audio_file}"
    subprocess.call(command, shell=True)


def apply_8d_effect(audio_file):
    sound = AudioSegment.from_file(audio_file)
    samples = np.array(sound.get_array_of_samples())

    left_channel = samples[::2] * np.sin(np.linspace(0, np.pi, len(samples) // 2))
    right_channel = samples[1::2] * np.cos(np.linspace(0, np.pi, len(samples) // 2))

    new_samples = np.empty((left_channel.size + right_channel.size,), dtype=left_channel.dtype)
    new_samples[0::2] = left_channel
    new_samples[1::2] = right_channel

    new_sound = AudioSegment(
        new_samples.tobytes(),
        frame_rate=sound.frame_rate,
        sample_width=sound.sample_width,
        channels=2
    )

    return new_sound


def combine_audio_video(video_file, audio_file, output_file):
    command = f"ffmpeg -i {video_file} -i {audio_file} -c:v copy -map 0:v:0 -map 1:a:0 {output_file}"
    subprocess.call(command, shell=True)


# Main process
mp4_file = 'FE!N.mp4.mp4'
audio_file = 'output.mp3'
output_audio_file = '8d_output.mp3'
final_output_file = 'final_output.mp4'

extract_audio(mp4_file, audio_file)
new_sound = apply_8d_effect(audio_file)
new_sound.export(output_audio_file, format='mp3')
combine_audio_video(mp4_file, output_audio_file, final_output_file)

