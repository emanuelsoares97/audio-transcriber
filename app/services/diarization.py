
from pyannote.audio import Pipeline
import torch

def diarize(audio_path, hf_token, num_speakers=None):
    """
    Executa a diarização num ficheiro de áudio e retorna os resultados.

    Args:
        audio_path (str): Caminho para o ficheiro de áudio mono (16kHz).
        hf_token (str): Access token do HuggingFace.
        num_speakers (int, opcional): Se souber quantos locutores há.

    Returns:
        list of dict: Lista com início, fim e label do locutor para cada segmento.
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
    Remove segmentos abaixo de uma duração mínima (em segundos).
    """
    return [seg for seg in segments if seg['end'] - seg['start'] >= min_duration]


def merge_consecutive_segments(segments, max_gap=0.5):
    """
    Junta segmentos consecutivos do mesmo locutor separados por menos do que max_gap segundos.
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

