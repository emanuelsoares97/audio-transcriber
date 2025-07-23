# Audio Transcriber

Aplicação web para transcrição automática de áudio com separação por locutor, baseada no modelo OpenAI Whisper. Interface moderna, responsiva e com tudo automatizado no backend.

---

## Funcionalidades

- Upload de ficheiros áudio (MP3, WAV, MP4, etc)
- Transcrição automática com Whisper large (alta qualidade)
- Diarização: organiza por locutor
- Exportação dos resultados em JSON e PDF

---

## Tecnologias

- Python 3.9+
- Flask (API backend)
- OpenAI Whisper
- MoviePy (extração de áudio de vídeos)
- JavaScript (lógica frontend)
- Bootstrap (UI)
- reportlab (para geração de PDF)

---

## Como correr localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/emanuelsoares97/speaker-transcribe.git
cd speaker-transcribe
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate    # No Windows: venv\Scripts\activate
```

### 3. Instalar as dependências

Se tiveres o ficheiro `requirements.txt`:

```bash
pip install -r requirements.txt
```

Ou instala manualmente:

```bash
pip install flask openai-whisper moviepy reportlab python-dotenv
```

### 4. Instalar o ffmpeg (obrigatório)

- No Windows: baixar em https://ffmpeg.org/download.html  
- No Linux:

```bash
sudo apt install ffmpeg
```

### 5. Executar a aplicação

```bash
python run.py
```

A aplicação ficará disponível em `http://127.0.0.1:5000`

---

## Como usar

- Acede à página
- Faz upload do ficheiro de áudio ou vídeo
- Após o processamento, os resultados são apresentados por locutor
- É possível fazer download dos resultados em JSON e PDF

---

## Limpeza automática

Inclui um script para remover ficheiros antigos nas pastas `uploads/` e `outputs/`.

- Pode ser configurado para correr via cron ou manualmente
- Por padrão, apaga todos os ficheiros com mais de 1 hora

---

## Estrutura do projeto

```
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
```

---  
**Desenvolvido por [Emanuel Soares](https://github.com/emanuelsoares97)**
