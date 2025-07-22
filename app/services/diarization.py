
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
