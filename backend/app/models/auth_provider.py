import pymysql
from app.config.database import Database
from app.models.user import User

class AuthProvider:
    def __init__(self):
        self.db = Database()
        self.user_model = User()
    
    def create_auth_provider(self, provider, provider_id_google=None, token=None):
        """Crear registro de proveedor de autenticación"""
        conn = self.db.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            
            query = "INSERT INTO auth_provider (provider, provider_id_google, token) VALUES (%s, %s, %s)"
            cursor.execute(query, (provider, provider_id_google, token))
            conn.commit()
            
            auth_provider_id = cursor.lastrowid
            return auth_provider_id
            
        except Exception as e:
            conn.rollback()
            print(f"Error creating auth provider: {e}")
            return None
        finally:
            conn.close()
    
    def link_user_to_provider(self, user_id, auth_provider_id):
        """Vincular usuario con proveedor de autenticación"""
        conn = self.db.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            query = "INSERT INTO user_auth_provider (id_user, id_auth_provider) VALUES (%s, %s)"
            cursor.execute(query, (user_id, auth_provider_id))
            conn.commit()
            
            return True
            
        except Exception as e:
            conn.rollback()
            print(f"Error linking user to provider: {e}")
            return False
        finally:
            conn.close()
    
    def find_user_by_google_id(self, google_id):
        """Encontrar usuario por Google ID"""
        conn = self.db.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            
            query = """
            SELECT u.id_user, u.full_name, u.email, u.id_role, r.name as role_name
            FROM users u
            JOIN user_auth_provider uap ON u.id_user = uap.id_user
            JOIN auth_provider ap ON uap.id_auth_provider = ap.id_auth_provider
            LEFT JOIN roles r ON u.id_role = r.id_role
            WHERE ap.provider = 'google' AND ap.provider_id_google = %s
            """
            
            cursor.execute(query, (google_id,))
            return cursor.fetchone()
            
        except Exception as e:
            print(f"Error finding user by Google ID: {e}")
            return None
        finally:
            conn.close()
    
    def create_google_user(self, google_user_info):
        """Crear usuario desde información de Google"""
        try:
            # 1. Crear usuario
            user_result = self.user_model.create_user(
                full_name=google_user_info.get('name', ''),
                email=google_user_info.get('email', ''),
                password=None,  # Sin contraseña para usuarios de Google
                role_id=2  # Customer por defecto
            )
            
            if 'error' in user_result:
                # Si el usuario ya existe por email, intentar vincularlo
                existing_user = self.user_model.get_user_by_email(google_user_info.get('email'))
                if existing_user:
                    user_id = existing_user['id_user']
                else:
                    return {"error": user_result['error']}
            else:
                user_id = user_result['id_user']
            
            # 2. Crear proveedor de autenticación
            auth_provider_id = self.create_auth_provider(
                provider='google',
                provider_id_google=google_user_info.get('sub', ''),  # Google User ID
                token=google_user_info.get('access_token', '')
            )
            
            if not auth_provider_id:
                return {"error": "Error creando proveedor de autenticación"}
            
            # 3. Vincular usuario con proveedor
            if not self.link_user_to_provider(user_id, auth_provider_id):
                return {"error": "Error vinculando usuario con proveedor"}
            
            # 4. Retornar datos del usuario
            user_data = self.user_model.get_user_by_email(google_user_info.get('email'))
            return user_data
            
        except Exception as e:
            print(f"Error creating Google user: {e}")
            return {"error": str(e)}