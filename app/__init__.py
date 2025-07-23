from flask import Flask, app
import os
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.DevelopmentConfig)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)

    from app.routes import bp
    app.register_blueprint(bp)

    return app

