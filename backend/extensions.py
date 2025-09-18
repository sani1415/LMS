import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def init_app(app):
    """Initialize extensions and configure the database using env vars"""
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    name = os.getenv("DB_NAME")

    if not all([user, password, name]):
        raise RuntimeError("❌ Missing database environment variables. Please set DB_USER, DB_PASSWORD, DB_NAME in cPanel.")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{user}:{password}@{host}/{name}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    bcrypt.init_app(app)
