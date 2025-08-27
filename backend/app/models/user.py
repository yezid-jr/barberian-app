import pymysql
import bcrypt
from app.config.database import Database

class User:
    def __init__(self):
        self.db = Database()
    
    def create_user(self, full_name, email, password=None, role_id=2):
        """Crear un nuevo usuario (role_id=2 para customer por defecto)"""
        conn = self.db.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            
            # Verificar si el email ya existe
            cursor.execute("SELECT id_user FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return {"error": "Email ya registrado"}
            
            # Hash de la contraseña si se proporciona
            password_hash = None
            if password:
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Insertar usuario
            query = "INSERT INTO users (full_name, email, password_hash, id_role) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (full_name, email, password_hash, role_id))
            conn.commit()
            
            user_id = cursor.lastrowid
            return {"id_user": user_id, "full_name": full_name, "email": email, "id_role": role_id}
            
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            conn.close()
    
    def get_user_by_email(self, email):
        """Obtener usuario por email"""
        conn = self.db.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            query = """
            SELECT u.id_user, u.full_name, u.email, u.password_hash, u.id_role, r.name as role_name
            FROM users u
            LEFT JOIN roles r ON u.id_role = r.id_role
            WHERE u.email = %s
            """
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            
            # Debug: imprimir el resultado para verificar
            if user:
                print(f"🔍 Usuario encontrado: {user}")
            else:
                print(f"❌ Usuario no encontrado para email: {email}")
                
            return user
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
        finally:
            conn.close()
    
    def verify_password(self, password, password_hash):
        """Verificar contraseña"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False