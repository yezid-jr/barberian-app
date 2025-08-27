import os
import requests
from flask import request, jsonify, redirect
from dotenv import load_dotenv

from app.models.auth_provider import AuthProvider
from app.utils.jwt_helper import JWTHelper

load_dotenv()

auth_provider_model = AuthProvider()
jwt_helper = JWTHelper()

class GoogleAuthController:
    def __init__(self):
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
        
        # Verificar que las credenciales estén configuradas
        if not self.client_id:
            print("⚠️ GOOGLE_CLIENT_ID no configurado")
        if not self.client_secret:
            print("⚠️ GOOGLE_CLIENT_SECRET no configurado")
        if not self.redirect_uri:
            print("⚠️ GOOGLE_REDIRECT_URI no configurado")
    
    def get_google_login_url(self):
        """Generar URL de login de Google"""
        try:
            if not all([self.client_id, self.client_secret, self.redirect_uri]):
                return jsonify({'error': 'Google OAuth no está configurado correctamente'}), 500
            
            # URL de autorización de Google
            base_url = "https://accounts.google.com/o/oauth2/v2/auth"
            params = {
                'client_id': self.client_id,
                'redirect_uri': self.redirect_uri,
                'scope': 'openid email profile',
                'response_type': 'code',
                'access_type': 'offline',
                'prompt': 'consent'
            }
            
            # Construir URL
            param_string = '&'.join([f"{k}={v}" for k, v in params.items()])
            authorization_url = f"{base_url}?{param_string}"
            
            return jsonify({
                'authorization_url': authorization_url,
                'client_id': self.client_id  # Para usar en el frontend también
            }), 200
            
        except Exception as e:
            print(f"Error generating Google login URL: {e}")
            return jsonify({'error': str(e)}), 500
    
    def handle_google_callback(self):
        """Manejar callback de Google OAuth"""
        try:
            if not all([self.client_id, self.client_secret, self.redirect_uri]):
                return redirect('http://localhost:3000?error=Google OAuth no configurado')
            
            # Obtener código de autorización
            code = request.args.get('code')
            error = request.args.get('error')
            
            if error:
                return redirect(f'http://localhost:3000?error=Google OAuth error: {error}')
            
            if not code:
                return redirect('http://localhost:3000?error=Código de autorización no encontrado')
            
            # Intercambiar código por token
            token_url = "https://oauth2.googleapis.com/token"
            token_data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': self.redirect_uri
            }
            
            token_response = requests.post(token_url, data=token_data)
            token_json = token_response.json()
            
            if 'error' in token_json:
                return redirect(f'http://localhost:3000?error=Error obteniendo token: {token_json["error"]}')
            
            access_token = token_json.get('access_token')
            id_token = token_json.get('id_token')
            
            # Obtener información del usuario
            user_info_url = f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}"
            user_response = requests.get(user_info_url)
            user_info = user_response.json()
            
            # Buscar o crear usuario
            google_id = user_info.get('id')
            user = auth_provider_model.find_user_by_google_id(google_id)
            
            if not user:
                # Crear nuevo usuario
                user = auth_provider_model.create_google_user({
                    'sub': google_id,
                    'name': user_info.get('name', ''),
                    'email': user_info.get('email', ''),
                    'access_token': access_token
                })
                
                if 'error' in user:
                    return redirect(f'http://localhost:3000?error={user["error"]}')
            
            # Generar JWT token
            jwt_token = jwt_helper.generate_token(user)
            
            # Redirigir al frontend con el token
            return redirect(f'http://localhost:3000?token={jwt_token}&provider=google&email={user["email"]}')
            
        except Exception as e:
            print(f"Error in Google callback: {e}")
            return redirect(f'http://localhost:3000?error=Error de autenticación con Google')
    
    def verify_google_token_frontend(self):
        """Verificar token de Google enviado desde el frontend (Google Sign-In API)"""
        try:
            data = request.get_json()
            credential = data.get('credential')  # Token JWT de Google
            
            if not credential:
                return jsonify({'error': 'Credential de Google requerido'}), 400
            
            # Verificar token con Google
            verify_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={credential}"
            response = requests.get(verify_url)
            
            if response.status_code != 200:
                return jsonify({'error': 'Token de Google inválido'}), 401
            
            user_info = response.json()
            
            # Verificar que el token sea para nuestra aplicación
            if user_info.get('aud') != self.client_id:
                return jsonify({'error': 'Token no es para esta aplicación'}), 401
            
            # Buscar o crear usuario
            google_id = user_info.get('sub')
            user = auth_provider_model.find_user_by_google_id(google_id)
            
            if not user:
                # Crear nuevo usuario
                user = auth_provider_model.create_google_user({
                    'sub': google_id,
                    'name': user_info.get('name', ''),
                    'email': user_info.get('email', ''),
                    'access_token': credential
                })
                
                if 'error' in user:
                    return jsonify({'error': user['error']}), 400
            
            # Generar JWT token
            jwt_token = jwt_helper.generate_token(user)
            
            return jsonify({
                'message': 'Login con Google exitoso',
                'token': jwt_token,
                'user': {
                    'id': user['id_user'],
                    'full_name': user['full_name'],
                    'email': user['email'],
                    'role': user['role_name']
                }
            }), 200
            
        except Exception as e:
            print(f"Error verifying Google token: {e}")
            return jsonify({'error': str(e)}), 500