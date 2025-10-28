from flask import Blueprint, request, jsonify
import hashlib
from datetime import datetime, timedelta
import jwt
import os

bp = Blueprint('auth', __name__)

# Simple in-memory user store for demo
USERS = {
    'test@example.com': {
        'password': hashlib.sha256('password123'.encode()).hexdigest(),
        'name': 'Test User'
    },
    'admin@pricehawk.com': {
        'password': hashlib.sha256('admin123'.encode()).hexdigest(),
        'name': 'Admin User'
    }
}

SECRET_KEY = os.getenv('JWT_SECRET', 'your-secret-key')

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
            
        if email in USERS:
            return jsonify({'error': 'User already exists'}), 400
            
        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Store user
        USERS[email] = {
            'password': hashed_password,
            'name': email.split('@')[0].title()
        }
        
        return jsonify({'message': 'User registered successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
            
        # Check if user exists
        if email not in USERS:
            return jsonify({'error': 'Invalid credentials'}), 401
            
        # Verify password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if USERS[email]['password'] != hashed_password:
            return jsonify({'error': 'Invalid credentials'}), 401
            
        # Generate JWT token
        token = jwt.encode({
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'access_token': token,
            'user': {
                'email': email,
                'name': USERS[email]['name']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/verify', methods=['GET'])
def verify():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No token provided'}), 401
            
        token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        email = payload['email']
        
        if email not in USERS:
            return jsonify({'error': 'User not found'}), 401
            
        return jsonify({
            'user': {
                'email': email,
                'name': USERS[email]['name']
            }
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500