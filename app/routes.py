from flask import render_template, request, jsonify, send_from_directory, Blueprint, current_app, send_file, url_for
import os
import uuid

from app.services.audio_extractor import extract_audio
from app.services.diarization import diarize, filter_minimum_segments, merge_consecutive_segments
from app.services.transcription import transcribe_segments
from app.services.text_json import save_json_to_file
from app.services.text_pdf import export_segments_to_pdf

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

        audio_wav_path = extract_audio(
    file_path,
    uploads_folder=current_app.config["UPLOAD_FOLDER"]
)

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
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500



@bp.route('/outputs/<path:filename>', methods=['GET'])
def download_output(filename):
    folder = current_app.config["OUTPUT_FOLDER"]

    file_path = os.path.join(folder, filename.replace("/", os.sep).replace("\\", os.sep))
    if not os.path.exists(file_path):
        return "NÃO EXISTE", 404
    return send_file(file_path, as_attachment=True)



@bp.route('/api/export/pdf', methods=['GET'])
def export_pdf_endpoint():
    data = request.json
    segments = data.get("segments")
    if not segments:
        return jsonify({"error": "Sem segmentos de transcrição."}), 400

    filename = f"{uuid.uuid4().hex}_transcript.pdf"
    output_folder = current_app.config["OUTPUT_FOLDER"]
    pdf_path = os.path.join(output_folder, filename)
    export_segments_to_pdf(segments, pdf_path)
    return jsonify({"pdf_url": url_for('.download_output', filename=filename)}), 200

@bp.route('/clean', methods=['POST'])
def limpar_uploads_outputs():
    folders = [
        current_app.config["UPLOAD_FOLDER"],
        current_app.config["OUTPUT_FOLDER"]
    ]
    deleted = []
    for folder in folders:
        for fname in os.listdir(folder):
            fpath = os.path.join(folder, fname)
            if os.path.isfile(fpath):
                try:
                    os.remove(fpath)
                    deleted.append(fpath)
                except Exception as e:
                    print(f"Erro ao apagar {fpath}: {e}")
    return jsonify({"mensagem": "Limpeza feita", "apagados": deleted}), 200