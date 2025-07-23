from pydub import AudioSegment
import whisper
import tempfile
import os

# Carregar modelo Whisper
model = None

def get_model():
    global model
    if model is None:
        import whisper
        model = whisper.load_model("large")
    return model


def transcribe_segments(audio_path, segments, language='pt'):
    """
    Transcreve segmentos de áudio utilizando o modelo Whisper.

    Args:
        audio_path (str): Caminho para o ficheiro de áudio.
        segments (list): Lista de segmentos a serem transcritos.
        language (str): Idioma da transcrição.

    Returns:
        list: Resultados da transcrição.
    """
    
    model = get_model()

    audio = AudioSegment.from_wav(audio_path)
    results = []
    for seg in segments:
        start_ms = int(seg['start'] * 1000)
        end_ms = int(seg['end'] * 1000)
        # Extrai o segmento
        segment_audio = audio[start_ms:end_ms]
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio_file:
            segment_audio.export(temp_audio_file.name, format='wav')
            temp_path = temp_audio_file.name
        # Transcreve segmento
        try:
            result = model.transcribe(temp_path, fp16=False, language=language)
            text = result.get('text', '').strip()
        except Exception as e:
            text = f'Erro: {e}'
        results.append({
            'start': seg['start'],
            'end': seg['end'],
            'speaker': seg['speaker'],
            'text': text
        })
        # Limpa ficheiro temporário
        os.remove(temp_path)

    return results
