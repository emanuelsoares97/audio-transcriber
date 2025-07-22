speaker-transcribe/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── audio_extractor.py      # Extrai áudio do vídeo/áudio
│   │   ├── diarization.py          # Core da pyannote
│   │   ├── transcription.py        # Core do Whisper
│   │   ├── pdf_generator.py        # Gera PDFs
│   ├── static/
│   └── templates/
│
├── uploads/                       # Ficheiros carregados pelo user
├── outputs/                       # PDFs finais e outros resultados
│
├── tests/                         # Testes unitários
│   └── test_services.py
│
├── requirements.txt               # Dependências do projeto
├── config.py                      # Configurações globais
├── run.py                         # Arquivo principal
└── README.md
