import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class JWTHelper:
    def __init__(self):
        self.secret_key = os.getenv('JWT_SECRET_KEY')
        self.algorithm = os.getenv('JWT_ALGORITHM', 'HS256')
    
    def generate_token(self, user_data):
        """Generar token JWT"""
        try:
            payload = {
                'user_id': user_data['id_user'],  # Asegurar que coincida con el campo de la DB
                'email': user_data['email'],
                'role': user_data.get('role_name', 'customer'),
                'exp': datetime.utcnow() + timedelta(hours=24),
                'iat': datetime.utcnow()
            }
            
            print(f"🔧 Payload para JWT: {payload}")
            
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return token
            
        except Exception as e:
            print(f"Error generando token: {e}")
            raise e
    
    def verify_token(self, token):
        """Verificar y decodificar token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            print(f"🔧 Token decodificado: {payload}")
            return payload
        except jwt.ExpiredSignatureError:
            return {"error": "Token expirado"}
        except jwt.InvalidTokenError as e:
            print(f"Token inválido: {e}")
            return {"error": "Token inválido"}