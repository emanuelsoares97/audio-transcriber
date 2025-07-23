from flask import Flask, request, jsonify
from app.services.audio_extractor import extract_audio
from app.services.diarization import diarize, filter_minimum_segments, merge_consecutive_segments
from app.services.transcription import transcribe_segments
from app.services.text_json import text_to_json
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/api/upload", methods=["POST"])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Nenhum ficheiro enviado"}), 400

        file = request.files['file']

        if file.filename == "":
            return jsonify({"error": "Ficheiro sem nome"}), 400

        # Gera um nome único antes de guardar
        extension = os.path.splitext(file.filename)[1]  # mantém a extensão original
        unique_name = f"{uuid.uuid4().hex}{extension}"
        save_path = os.path.join(UPLOAD_FOLDER, unique_name)

        file.save(save_path)

        return jsonify({"message": "Ficheiro carregado com sucesso!", "file_path": save_path}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/process", methods=["POST"])
def process():
    try:
        data = request.get_json()
        if not data or 'file_path' not in data:
            return jsonify({"error": "No file path provided"}), 400
        
        file_path = data['file_path']
        hf_token = data.get('hf_token', os.getenv("HUGGINGFACE_TOKEN"))  # fallback para .env
        num_speakers = int(data.get('num_speakers', 2))
        language = data.get('language', "pt")
        
        # Extração de áudio
        audio_wav_path = extract_audio(file_path)
        
        # Diarização
        segments = diarize(audio_wav_path, hf_token, num_speakers=num_speakers)

        # Filtra e funde segmentos
        segments = filter_minimum_segments(segments, min_duration=1.0)
        segments = merge_consecutive_segments(segments, max_gap=0.5)

        # Transcrição
        transcript = transcribe_segments(audio_wav_path, segments, language=language)
        
        # Exporta para JSON - pode gerar uid ou job_id se quiseres
        output_json_path = text_to_json(transcript)

        return jsonify({
            "message": "Processamento concluído!",
            "segments": transcript,
            "output_json": output_json_path
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/api/result/<job_id>", methods=["GET"])
def result(job_id):
    # Devolve ficheiro JSON/PDF
    ...
