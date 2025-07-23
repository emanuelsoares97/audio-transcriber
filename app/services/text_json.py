import json
import os
import uuid

def save_json_to_file(data, outdir="outputs"):
    """
    Guarda uma lista (ou dict) em ficheiro JSON no diretório especificado.
    Retorna o caminho do ficheiro criado.
    """
    filename = f"{uuid.uuid4().hex}_transcript.json"
    outpath = os.path.join(outdir, filename)
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return outpath
