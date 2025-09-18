from flask import request, jsonify
from app import app
from .extensions import db, bcrypt
from .models import User
import jwt
from datetime import datetime, timedelta

# ---------------------------
# User Registration
# ---------------------------
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409

    # Hash password before saving
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, password=hashed_pw)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


# ---------------------------
# User Login
# ---------------------------
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        # jwt.encode() may return bytes in some versions, ensure str
        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return jsonify({'token': token})

    return jsonify({'error': 'Invalid username or password'}), 401
