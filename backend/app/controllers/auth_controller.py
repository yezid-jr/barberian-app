from flask import request, jsonify
from app.models.user import User
from app.utils.jwt_helper import JWTHelper
# google imports
import os
from flask import jsonify
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv

load_dotenv()
user_model = User()
jwt_helper = JWTHelper()

class AuthController:
    def register(self):
        """Registro local de usuario"""
        try:
            data = request.get_json()
            
            # Validar campos requeridos
            required_fields = ['full_name', 'email', 'password']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'Campo {field} es requerido'}), 400
            
            # Crear usuario
            result = user_model.create_user(
                full_name=data['full_name'],
                email=data['email'],
                password=data['password'],
                role_id=data.get('role_id', 2)  # 2 = customer por defecto
            )
            
            if 'error' in result:
                return jsonify({'error': result['error']}), 400
            
            return jsonify({
                'message': 'Usuario registrado exitosamente',
                'user': result
            }), 201
            
        except Exception as e:
            print(f"Error en registro: {e}")
            return jsonify({'error': str(e)}), 500
    
    def login(self):
        """Login local de usuario"""
        try:
            data = request.get_json()
            
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return jsonify({'error': 'Email y contraseña son requeridos'}), 400
            
            # Buscar usuario
            user = user_model.get_user_by_email(email)
            print(f"🔍 Resultado de búsqueda de usuario: {user}")
            
            if not user:
                return jsonify({'error': 'Credenciales inválidas'}), 401
            
            # Verificar contraseña
            if not user.get('password_hash'):
                return jsonify({'error': 'Usuario registrado con Google, use login social'}), 401
            
            if not user_model.verify_password(password, user['password_hash']):
                return jsonify({'error': 'Credenciales inválidas'}), 401
            
            # Preparar datos del usuario para el token
            user_data = {
                'id_user': user['id_user'],  # Asegurar que tenga la clave correcta
                'full_name': user['full_name'],
                'email': user['email'],
                'role_name': user['role_name']
            }
            
            print(f"🔧 Datos para token: {user_data}")
            
            # Generar token
            token = jwt_helper.generate_token(user_data)
            
            return jsonify({
                'message': 'Login exitoso',
                'token': token,
                'user': {
                    'id': user['id_user'],
                    'full_name': user['full_name'],
                    'email': user['email'],
                    'role': user['role_name']
                }
            }), 200
            
        except Exception as e:
            print(f"Error en login: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500
    
    def profile(self):
        """Obtener perfil del usuario autenticado"""
        try:
            user_data = request.current_user
            return jsonify({
                'user': {
                    'id': user_data['user_id'],
                    'email': user_data['email'],
                    'role': user_data['role']
                }
            }), 200
        except Exception as e:
            print(f"Error en profile: {e}")
            return jsonify({'error': str(e)}), 500
        
    ############################
    ### Google OAuth methods ###
    ############################
    
    def google_oauth(self):
        """Manejo de autenticación con Google OAuth"""
        try:
            data = request.get_json()
            google_token = data.get('token')
            
            if not google_token:
                return jsonify({'error': 'Token de Google requerido'}), 400
            
            # Verificar token de Google
            try:
                idinfo = id_token.verify_oauth2_token(
                    google_token, 
                    requests.Request(), 
                    os.getenv('GOOGLE_CLIENT_ID')
                )
                
                # Extraer información del usuario de Google
                google_user_id = idinfo['sub']
                email = idinfo['email']
                full_name = idinfo['name']
                
                print(f"🔍 Usuario Google verificado: {email}")
                
            except ValueError as e:
                print(f"Token de Google inválido: {e}")
                return jsonify({'error': 'Token de Google inválido'}), 401
            
            # Buscar si el usuario ya existe
            existing_user = user_model.get_user_by_email(email)
            
            if existing_user:
                # Usuario existe - hacer login
                print(f"🔑 Usuario existente encontrado: {existing_user['full_name']}")
                
                # Verificar si ya está vinculado con Google
                if not self._check_google_auth_provider(existing_user['id_user'], google_user_id):
                    # Vincular cuenta existente con Google
                    self._link_google_account(existing_user['id_user'], google_user_id, google_token)
                
                user_data = {
                    'id_user': existing_user['id_user'],
                    'full_name': existing_user['full_name'],
                    'email': existing_user['email'],
                    'role_name': existing_user['role_name']
                }
                
            else:
                # Usuario no existe - registrar automáticamente
                print(f"✨ Creando nuevo usuario: {full_name}")
                
                # Crear nuevo usuario (sin password_hash para usuarios de Google)
                new_user = user_model.create_user(
                    full_name=full_name,
                    email=email,
                    password=None,  # Sin password para usuarios de Google
                    role_id=2  # Customer por defecto
                )
                
                if 'error' in new_user:
                    return jsonify({'error': new_user['error']}), 400
                
                # Crear auth_provider para Google
                auth_provider_id = self._create_google_auth_provider(google_user_id, google_token)
                
                # Vincular usuario con auth_provider
                self._link_user_auth_provider(new_user['id_user'], auth_provider_id)
                
                user_data = {
                    'id_user': new_user['id_user'],
                    'full_name': new_user['full_name'],
                    'email': new_user['email'],
                    'role_name': 'customer'  # Por defecto
                }
            
            # Generar JWT token propio
            token = jwt_helper.generate_token(user_data)
            
            return jsonify({
                'message': 'Autenticación con Google exitosa',
                'token': token,
                'user': {
                    'id': user_data['id_user'],
                    'full_name': user_data['full_name'],
                    'email': user_data['email'],
                    'role': user_data.get('role_name', 'customer')
                }
            }), 200
            
        except Exception as e:
            print(f"Error en Google OAuth: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500

    def _check_google_auth_provider(self, user_id, google_user_id):
        """Verificar si el usuario ya tiene vinculado Google"""
        conn = self.db.get_connection() if hasattr(self, 'db') else user_model.db.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            query = """
            SELECT ap.id_auth_provider 
            FROM user_auth_provider uap
            JOIN auth_provider ap ON uap.id_auth_provider = ap.id_auth_provider
            WHERE uap.id_user = %s AND ap.provider = 'google' AND ap.provider_id_google = %s
            """
            cursor.execute(query, (user_id, google_user_id))
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error checking Google auth provider: {e}")
            return False
        finally:
            conn.close()

    def _create_google_auth_provider(self, google_user_id, google_token):
        """Crear registro de auth_provider para Google"""
        conn = self.db.get_connection() if hasattr(self, 'db') else user_model.db.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO auth_provider (provider, provider_id_google, token) 
            VALUES ('google', %s, %s)
            """
            cursor.execute(query, (google_user_id, google_token))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating Google auth provider: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    def _link_google_account(self, user_id, google_user_id, google_token):
        """Vincular cuenta existente con Google"""
        # Primero crear o actualizar auth_provider
        conn = user_model.db.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            # Buscar si ya existe un auth_provider para este Google ID
            cursor.execute(
                "SELECT id_auth_provider FROM auth_provider WHERE provider = 'google' AND provider_id_google = %s",
                (google_user_id,)
            )
            auth_provider = cursor.fetchone()
            
            if auth_provider:
                # Actualizar token
                cursor.execute(
                    "UPDATE auth_provider SET token = %s WHERE id_auth_provider = %s",
                    (google_token, auth_provider['id_auth_provider'])
                )
                auth_provider_id = auth_provider['id_auth_provider']
            else:
                # Crear nuevo auth_provider
                cursor.execute(
                    "INSERT INTO auth_provider (provider, provider_id_google, token) VALUES ('google', %s, %s)",
                    (google_user_id, google_token)
                )
                auth_provider_id = cursor.lastrowid
            
            # Vincular con el usuario si no existe la relación
            cursor.execute(
                "INSERT IGNORE INTO user_auth_provider (id_user, id_auth_provider) VALUES (%s, %s)",
                (user_id, auth_provider_id)
            )
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error linking Google account: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def _link_user_auth_provider(self, user_id, auth_provider_id):
        """Vincular usuario con auth_provider"""
        conn = user_model.db.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            query = "INSERT INTO user_auth_provider (id_user, id_auth_provider) VALUES (%s, %s)"
            cursor.execute(query, (user_id, auth_provider_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error linking user auth provider: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()