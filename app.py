#
# PASTE THIS ENTIRE CODE INTO: app.py
#
import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.config import config
from backend.extensions import db, bcrypt
from backend.init_db import create_sample_data
from backend.models import Book, User # Import User model for token_required

# --- THIS DECORATOR IS MOVED HERE FOR BETTER STRUCTURE ---
from functools import wraps
import jwt
from flask import request, jsonify

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try:
            # Use the app's secret key for decoding
            secret_key = app.config.get('SECRET_KEY')
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except Exception as e:
            return jsonify({'message' : 'Token is invalid!', 'error': str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated
# --- END OF DECORATOR ---

# Determine the config name from the environment variable
config_name = os.environ.get('FLASK_ENV', 'default')

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config[config_name])

# Initialize extensions with the app
db.init_app(app)
bcrypt.init_app(app)
CORS(app)  # Enable CORS for frontend integration

# Import routes after app and db are initialized to avoid circular imports
from backend import routes, auth_routes

# --- STATIC FILE SERVING ROUTES ---
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
    # This is a simple way; for high performance, Apache/Nginx should handle this.
    return send_from_directory('.', filename)
# --- END OF STATIC FILE SERVING ---

if __name__ == '__main__':
    # This block runs only when you execute "python app.py" locally
    with app.app_context():
        db.create_all()  # Create database tables
        # Add sample data if the database is empty
        if not Book.query.first():
            print("Database is empty, creating sample data...")
            create_sample_data()
            print("Sample data created.")
    
    app.run(debug=True, host='0.0.0.0', port=5001)