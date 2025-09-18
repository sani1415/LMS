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
config_name = os.environ.get('FLASK_ENV', 'development_mysql')  # Default to MySQL now
app.config.from_object(config[config_name])

# Import models first to get db instance

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
CORS(app)  # Enable CORS for frontend integration

# Import routes after extensions are initialized
from backend.routes import *
from backend.auth_routes import *

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

# Import init_db for sample data
from backend.init_db import create_sample_data

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
        # Add sample data if database is empty
        from backend.models import Book
        if not Book.query.first():
            create_sample_data()
    
    app.run(debug=True, host='0.0.0.0', port=5001)
