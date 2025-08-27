from functools import wraps
from flask import request, jsonify
from app.utils.jwt_helper import JWTHelper

jwt_helper = JWTHelper()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get the token from the request headers
        token = request.headers.get('Authorization')
        
        # If no token is provided, return error
        if not token:
            return jsonify({'error': 'Missing token'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            # Verify and decode token
            data = jwt_helper.verify_token(token)
            
            # If token is invalid or expired, return error
            if 'error' in data:
                return jsonify({'error': data['error']}), 401
                
            # Attach current user info to the request object
            request.current_user = data
        except Exception as e:
            # Catch unexpected token errors
            return jsonify({'error': 'Invalid token'}), 401
        
        # Proceed to the protected route
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get the token from the request headers
        token = request.headers.get('Authorization')
        
        # If no token is provided, return error
        if not token:
            return jsonify({'error': 'Missing token'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            # Verify and decode token
            data = jwt_helper.verify_token(token)
            
            # If token is invalid or expired, return error
            if 'error' in data:
                return jsonify({'error': data['error']}), 401
            
            # Check if the user has admin role
            if data.get('role') != 'admin':
                return jsonify({'error': 'Access denied - Admin role required'}), 403
                
            # Attach current user info to the request object
            request.current_user = data
        except Exception as e:
            # Catch unexpected token errors
            return jsonify({'error': 'Invalid token'}), 401
        
        # Proceed to the admin-only route
        return f(*args, **kwargs)
    return decorated
