from datetime import timedelta

from flask import Flask
from backend.models.base import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from backend.models.admin import Admin
from flask_jwt_extended.exceptions import JWTExtendedException
from werkzeug.exceptions import Unauthorized
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask import jsonify
from dotenv import load_dotenv
import os

from backend.models.base import db
from backend.models.admin import Admin

load_dotenv()
jwt = JWTManager()


def register_jwt_handlers(app):
    @app.errorhandler(JWTExtendedException)
    def handle_jwt_error(e):
        return jsonify({"message": str(e)}), 401

    @app.errorhandler(Unauthorized)
    def handle_unauthorized(e):
        return jsonify({"message": "Unauthorized"}), 401

    @app.errorhandler(NoAuthorizationError)
    def handle_no_auth_error(e):
        # if token is missing during preflight OPTIONS
        return jsonify({"message": "Missing Authorization Header"}), 401


def create_app():
    app = Flask(__name__)
    app.config.from_object('backend.config.Config')

    app.url_map.strict_slashes = False
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_COOKIE_SECURE"] = False  # Not using cookies anyway
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["JWT_ERROR_MESSAGE_KEY"] = "message"
    app.config["PROPAGATE_EXCEPTIONS"] = True

    register_jwt_handlers(app)

    db.init_app(app)
    jwt.init_app(app)
    if os.environ.get("FLASK_ENV") == "production":
        app.config["JWT_COOKIE_SECURE"] = True
        origin = os.environ.get("ORIGIN", "")
        CORS(app, origins=[origin], supports_credentials=True)
    else:
        CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"], supports_credentials=True)


    from backend.models import admin, session, patient, diagnosis, sample

    # Create tables in dev
    if app.config['DEBUG']:
        with app.app_context():
            db.create_all()

    # Register blueprints
    from backend.routes.auth import auth_bp
    from backend.routes.patients import patients_bp
    from backend.routes.diagnoses import diagnosis_bp
    from backend.routes.samples import samples_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(patients_bp, url_prefix='/api/patients')
    app.register_blueprint(diagnosis_bp, url_prefix='/api/diagnoses')
    app.register_blueprint(samples_bp, url_prefix='/api/samples')

    return app
