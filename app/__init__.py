import os
from flask import Flask
from .extensions import db, migrate, bcrypt, login_manager
from .models import File, User
from .auth.routes import auth_bp
from .storage.routes import storage_bp
from .api.routes import api_bp
from .admin.routes import admin_bp

# Define storage folder and make sure it exists
STORAGE_FOLDER = os.path.join(os.path.dirname(__file__), "..", "storage")
os.makedirs(STORAGE_FOLDER, exist_ok=True)

def create_app(config=None):
    # Initialize Flask app
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # App configuration
    app.config['SECRET_KEY'] = "ultra-secret-v5"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pcloud_v5.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['STORAGE_FOLDER'] = STORAGE_FOLDER

    # Initialize extensions
    db.init_app(app)              # SQLAlchemy: DB models & queries
    migrate.init_app(app, db)     # Flask-Migrate: create/update tables
    bcrypt.init_app(app)          # Flask-Bcrypt: Password hashing
    login_manager.init_app(app)   # Flask-Login: User login/session

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(storage_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


