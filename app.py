from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from backend.extensions import db, bcrypt
from datetime import datetime
import os
from backend.config import config

# Initialize Flask app
app = Flask(__name__)

# Configuration
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", "localhost")
db_name = os.getenv("DB_NAME")

if db_user and db_pass and db_name:
    # Use cPanel MySQL credentials
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")  # required for JWT
    print(f"✅ Using cPanel database: {db_name} as {db_user}@{db_host}")
else:
    # Fall back to config.py (development)
    config_name = os.environ.get('FLASK_ENV', 'development_mysql')
    app.config.from_object(config[config_name])
    print(f"⚠️ Using fallback config: {config_name}")


# Import models first to get db instance

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
CORS(app)  # Enable CORS for frontend integration

# Serve the main application
@app.route('/')
def serve_main_app():
    """Serve the main Library Management System application"""
    return send_from_directory('.', 'index.html')

@app.route('/favicon.ico')
def favicon():
    return ''

@app.route('/<path:filename>')
def serve_static_files(filename):
    """Serve static files (CSS, JS, images)"""
    return send_from_directory('.', filename)

from functools import wraps
import jwt
from backend.models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Import routes after db initialization
from backend.routes import *
from backend.auth_routes import *
from backend.init_db import create_sample_data

# Initialize database for both local and cPanel deployment
def init_app_database():
    """Initialize database tables and create admin user if needed"""
    try:
        db.create_all()  # Create database tables
        
        # Create admin user if no users exist
        from backend.models import User, Book
        if not User.query.first():
            admin_user = User(username='admin', password='admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Admin user created: admin/admin123")
        
        # Add sample data if database is empty
        if not Book.query.first():
            create_sample_data()
            print("✅ Sample data created")
            
    except Exception as e:
        print(f"Database initialization error: {e}")

# Initialize database when app starts (works for both local and cPanel)
with app.app_context():
    init_app_database()

if __name__ == '__main__':
    # Only run Flask dev server locally, not on cPanel
    app.run(debug=True, host='0.0.0.0', port=5001)
