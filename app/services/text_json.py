import json
import os
import uuid

def save_json_to_file(data, outdir=None):
    """
    Save a dictionary to a JSON file in the specified directory.
    If no directory is specified, it uses the current working directory.
    """
    filename = f"{uuid.uuid4().hex}_transcript.json"
    outpath = os.path.join(outdir, filename)
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return outpath
