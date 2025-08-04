from moviepy import VideoFileClip, AudioFileClip
import os

def extract_audio(input_path, output_path=None, output_format="wav", uploads_folder=None):
    """Extract audio from a video or audio file and save it in the specified format.
    Args:
        input_path (str): Path to the input video or audio file.
        output_path (str, optional): Path to save the extracted audio file. If None, it will be saved in the uploads folder.
        output_format (str): Format of the output audio file (default is "wav").
        uploads_folder (str, optional): Folder where the extracted audio will be saved if output_path is not specified.
    """
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
        if uploads_folder is None:
            raise ValueError("uploads_folder tem de ser passado explicitamente!")
        os.makedirs(uploads_folder, exist_ok=True)
        output_path = os.path.join(uploads_folder, f"{base}_extracted.{output_format}")

    print("Saving extracted audio to:", output_path)
    audio.write_audiofile(output_path)
    return output_path


