from flask import request, jsonify
from app.models.user import User
from app.utils.jwt_helper import JWTHelper

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