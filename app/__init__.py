from flask import Flask
from config import Config
from .extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.admin import admin_bp
    from .routes.manager import manager_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(manager_bp, url_prefix="/manager")

    with app.app_context():
        db.create_all()

    return app
