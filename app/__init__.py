from flask import Flask, send_from_directory
from backend_server.config import Config
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os


mail = Mail()
db = SQLAlchemy()


def create_app():
    from .models import User, NewsPost, TestResult
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)
    CORS(app, supports_credentials=True)

    from backend_server.app.routes.auth_routes import auth_bp
    from backend_server.app.routes.news_routes import news_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(news_bp)

    @app.route('/static/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(os.path.join(app.root_path, 'static/uploads'), filename)

    with app.app_context():
        from . import models

    return app
