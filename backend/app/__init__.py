import os
from dotenv import load_dotenv
from flask import Flask, send_from_directory
from app.config import Config
from app.extensions import db, jwt, bcrypt, cors

# Load .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)

    # Initialize extensions
    db.init_app(flask_app)
    jwt.init_app(flask_app)
    bcrypt.init_app(flask_app)
    cors.init_app(flask_app, origins=Config.CORS_ORIGINS, supports_credentials=True)
    # socketio.init_app(flask_app, cors_allowed_origins="*", async_mode="eventlet") # Removed for Vercel

    # Ensure upload directory exists
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    # Serve uploaded files
    @flask_app.route("/uploads/<path:filename>")
    def serve_upload(filename):
        return send_from_directory(Config.UPLOAD_FOLDER, filename)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.posts import posts_bp
    from app.routes.chat import chat_bp
    from app.routes.stories import stories_bp
    from app.routes.friends import friends_bp
    from app.routes.news import news_bp
    from app.routes.features import features_bp
    from app.routes.admin import admin_bp

    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(posts_bp)
    flask_app.register_blueprint(chat_bp)
    flask_app.register_blueprint(stories_bp)
    flask_app.register_blueprint(friends_bp)
    flask_app.register_blueprint(news_bp)
    flask_app.register_blueprint(features_bp)
    flask_app.register_blueprint(admin_bp)

    # Register socket events
    # from app.sockets import events  # noqa: F401 # Removed for Vercel

    # Create tables
    with flask_app.app_context():
        from app import models  # noqa: F401
        db.create_all()

        # Create default admin user if none exists
        from app.models.user import User
        if not User.query.filter_by(is_admin=True).first():
            admin_user = User(
                username="admin",
                email="admin@matebook.com",
                password_hash=bcrypt.generate_password_hash("admin123").decode("utf-8"),
                is_admin=True,
                is_verified=True,
                bio="Platform Administrator",
            )
            db.session.add(admin_user)
            db.session.commit()

        # Seed default challenges
        from app.models.challenge import Challenge
        defaults = [
            ("\U0001f4f8 Photo Challenge", "Share a photo that represents your day!", "photo"),
            ("\U0001f64f Gratitude Post", "Share 3 things you're grateful for today.", "gratitude"),
            ("\U0001f3a8 Creative Challenge", "Draw, design, or create something unique today!", "creative"),
            ("\U0001f4aa Fitness Check-in", "Share your workout or healthy meal today!", "fitness"),
        ]
        for title, desc, ctype in defaults:
            if not Challenge.query.filter_by(title=title).first():
                db.session.add(Challenge(title=title, description=desc, challenge_type=ctype))
        db.session.commit()

    return flask_app
