from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import AuthController
from app.utils.auth_decorator import token_required, admin_required

# Crear blueprint para rutas de autenticación
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_controller = AuthController()

# Rutas públicas (no requieren autenticación)
@auth_bp.route('/register', methods=['POST'])
def register():
    return auth_controller.register()

@auth_bp.route('/login', methods=['POST'])
def login():
    return auth_controller.login()

# Rutas protegidas (requieren token)
@auth_bp.route('/profile', methods=['GET'])
@token_required
def profile():
    return auth_controller.profile()

# Ruta solo para admin
@auth_bp.route('/admin/test', methods=['GET'])
@admin_required
def admin_test():
    return jsonify({"message": "Acceso de admin exitoso", "user": request.current_user})

# Rutas de Google OAuth (temporalmente deshabilitadas)
@auth_bp.route('/google/url', methods=['GET'])
def google_login_url():
    return jsonify({"error": "Google OAuth no configurado aún"}), 501

@auth_bp.route('/google/callback', methods=['GET'])
def google_callback():
    return jsonify({"error": "Google OAuth no configurado aún"}), 501

@auth_bp.route('/google/verify', methods=['POST'])
def google_verify():
    return jsonify({"error": "Google OAuth no configurado aún"}), 501