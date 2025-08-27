from flask import Blueprint, jsonify, request
from app.utils.auth_decorator import token_required

# Blueprint for general routes
general_bp = Blueprint('general', __name__)

# Public route: API home info
@general_bp.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Barberian API running correctly",
        "version": "1.0.0",
        "endpoints": {
            "auth": {
                "register": "POST /auth/register",
                "login": "POST /auth/login", 
                "profile": "GET /auth/profile (requires token)"
            }
        }
    })

# Public route: health check
@general_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "database": "connected"
    })

# Protected example route (requires token)
@general_bp.route('/protected', methods=['GET'])
@token_required
def protected_route():
    return jsonify({
        "message": "This is a protected route",
        "user": request.current_user  # Injected from decorator
    })
