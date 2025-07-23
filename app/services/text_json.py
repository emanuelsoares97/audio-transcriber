import json
import re

def text_to_json(text):
    """
    Converte um texto formatado em JSON.
    O texto deve conter linhas no formato:
    'Speaker [start_time - end_time]: text'
    """

    # Regex mais flexível, aceita SPEAKER_01, Speaker 1, etc.
    pattern = r'(\w+)\s*\[(\d+\.\d+)s\s*-\s*(\d+\.\d+)s\]:\s*(.+)'
    matches = re.findall(pattern, text)

    results = []
    for match in matches:
        speaker, start, end, spoken_text = match
        results.append({
            'speaker': speaker,
            'start_time': float(start),
            'end_time': float(end),
            'text': spoken_text.strip()
        })

    return json.dumps(results, ensure_ascii=False, indent=4)

import json

def save_json_to_file(data, filename):
    if isinstance(data, str):
        # Já está em string JSON, guarda diretamente
        with open(filename, "w", encoding="utf-8") as f:
            f.write(data)
    else:
        # É objeto Python (lista ou dict), transforma em JSON
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
