from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = "auth.login"

    # Import models
    from app.models import User

    # Register blueprints
    from app.auth import auth
    from app.dashboard import dashboard
    from app.uploads import uploads
    from app.routes import main

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(uploads)

    return app