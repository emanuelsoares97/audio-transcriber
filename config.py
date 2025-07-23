import os
from dotenv import load_dotenv

load_dotenv()


BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.join(BASEDIR, "uploads"))
    OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", os.path.join(BASEDIR, "outputs"))
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", None)
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
