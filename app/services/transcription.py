from pydub import AudioSegment
import whisper
import tempfile
import os

# Carregar modelo Whisper
model = whisper.load_model("large") # ou medium/large, etc

def transcribe_segments(audio_path, segments, language='pt'):
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
