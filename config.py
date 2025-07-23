import os
from dotenv import load_dotenv

load_dotenv()


ROOTDIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    # Usa caminhos absolutos para as pastas uploads e outputs, dentro da raiz do projeto
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.join(ROOTDIR, "uploads"))
    OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", os.path.join(ROOTDIR, "outputs"))
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", None)
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
