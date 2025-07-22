from moviepy import VideoFileClip, AudioFileClip
import os

def extract_audio(input_path, output_path=None, output_format="wav"):
    #valida o tipo de ficheiro
    ext = os.path.splitext(input_path)[1].lower()
    if ext in ['.mp4', '.avi', '.mov', '.mkv']:
        video = VideoFileClip(input_path)
        audio = video.audio
    elif ext in ['.mp3', '.wav', '.flac']:
        audio = AudioFileClip(input_path)
    else:
        raise ValueError("Unsupported audio format. Supported formats are: .mp4, .avi, .mov, .mkv, .mp3, .wav, .flac")

    if not output_path:
        base = os.path.splitext(os.path.basename(input_path))[0]
        output_path = f"{base}_extracted.{output_format}"

    #exporta no formado desejado

    audio.write_audiofile(output_path)

    return output_path