
from pyannote.audio import Pipeline
import torch

def diarize(audio_path, hf_token, num_speakers=None):
    """
    Perform speaker diarization on an audio file.
    Args:
        audio_path (str): Path to the audio file.
        hf_token (str): Hugging Face token for authentication.
        num_speakers (int, optional): Number of speakers to diarize. If None, the model will try to detect it automatically.
    """
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=hf_token
    )

    # indicar quantas pessoas estão a falar
    args = {"num_speakers": num_speakers} if num_speakers else {}

    diarization = pipeline(audio_path, **args)
    segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        segments.append({
            "start": turn.start,
            "end": turn.end,
            "speaker": speaker
        })
    return segments

def filter_minimum_segments(segments, min_duration=1.0):
    """
    Filter out segments shorter than the specified minimum duration.
    """
    return [seg for seg in segments if seg['end'] - seg['start'] >= min_duration]


def merge_consecutive_segments(segments, max_gap=0.5):
    """
    Merge consecutive segments of the same speaker that are separated by a gap smaller than max_gap seconds.
    """
    if not segments:
        return []
    merged = [segments[0]]
    for seg in segments[1:]:
        last = merged[-1]
        # Mesma pessoa e gap pequeno: funde
        if seg['speaker'] == last['speaker'] and seg['start'] - last['end'] <= max_gap:
            merged[-1] = {
                'start': last['start'],
                'end': seg['end'],
                'speaker': last['speaker']
            }
        else:
            merged.append(seg)
    return merged

