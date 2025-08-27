from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Import database configuration
from app.config.database import Database

# Import blueprints (modular routes)
from app.routes.auth_routes import auth_bp
from app.routes.general_routes import general_bp

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

def create_app():
    app = Flask(__name__)
    
    # Enable CORS (Cross-Origin Resource Sharing)
    # Allow requests from frontend running on localhost:3000
    CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])
    
    # App configuration
    # Secret key for signing JWT tokens
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
    # Test database connection at startup
    db = Database()
    if db.test_connection():
        print("🚀 Server started successfully")
    else:
        print("⚠️ Server started but with DB issues")
    
    # Register blueprints
    # Each blueprint handles a specific set of routes
    app.register_blueprint(general_bp)
    app.register_blueprint(auth_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    
    # Console messages for easier debugging
    print(f"🌐 Server running at: http://localhost:{port}")
    print(f"📋 Available endpoints:")
    print(f"   GET  /              - General info")
    print(f"   POST /auth/register - Register new user")
    print(f"   POST /auth/login    - User login") 
    print(f"   GET  /auth/profile  - User profile (token required)")
    
    # Start Flask server
    app.run(host='0.0.0.0', port=port, debug=True)
