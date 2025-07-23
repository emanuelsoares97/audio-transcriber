from flask import render_template, request, jsonify, send_from_directory, Blueprint, current_app, send_file
import os
import uuid

from app.services.audio_extractor import extract_audio
from app.services.diarization import diarize, filter_minimum_segments, merge_consecutive_segments
from app.services.transcription import transcribe_segments
from app.services.text_json import save_json_to_file

bp = Blueprint('main', __name__)

# Página principal 
@bp.route("/")
def index():
    return render_template("index.html")

# Upload endpoint 
@bp.route("/api/upload", methods=["POST"])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Nenhum ficheiro enviado"}), 400
        file = request.files['file']
        if file.filename == "":
            return jsonify({"error": "Ficheiro sem nome"}), 400

        extension = os.path.splitext(file.filename)[1]
        unique_name = f"{uuid.uuid4().hex}{extension}"
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_name)
        file.save(save_path)

        return jsonify({"message": "Ficheiro carregado com sucesso!", "file_path": save_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Process endpoint 
@bp.route("/api/process", methods=["POST"])
def process():
    try:
        data = request.get_json()
        if not data or 'file_path' not in data:
            return jsonify({"error": "No file path provided"}), 400
        file_path = data['file_path']
        hf_token = data.get('hf_token', os.getenv("HUGGINGFACE_TOKEN"))
        num_speakers = int(data.get('num_speakers', 2))
        language = data.get('language', "pt")

        audio_wav_path = extract_audio(file_path)
        segments = diarize(audio_wav_path, hf_token, num_speakers=num_speakers)
        segments = filter_minimum_segments(segments, min_duration=1.0)
        segments = merge_consecutive_segments(segments, max_gap=0.5)
        transcript = transcribe_segments(audio_wav_path, segments, language=language)
        output_json_path = save_json_to_file(transcript, outdir=current_app.config["OUTPUT_FOLDER"])
        rel_json_path = os.path.relpath(output_json_path, start=current_app.config["OUTPUT_FOLDER"])

        return jsonify({
            "message": "Processamento concluído!",
            "segments": transcript,
            "output_json": f"/outputs/{rel_json_path}"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/outputs/<path:filename>')
def download_output(filename):
    folder = current_app.config["OUTPUT_FOLDER"]
    # Normaliza o separador para o SO
    file_path = os.path.join(folder, filename.replace("/", os.sep).replace("\\", os.sep))
    print("DEBUG file_path:", file_path)
    if not os.path.exists(file_path):
        return "NÃO EXISTE", 404
    return send_file(file_path, as_attachment=True)

