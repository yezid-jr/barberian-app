estructura
para instalar librerias de python en el requirement:
``bash
pip install -r requirements.txt
``

barberian-app/
├── backend/
│   ├── app/
│   │   ├── config/
│   │   │   ├── __pycache__/
│   │   │   └── database.py
│   │   ├── controllers/
│   │   │   ├── __pycache__/
│   │   │   └── auth_controller.py
│   │   ├── models/
│   │   │   ├── __pycache__/
│   │   │   ├── auth_provider.py
│   │   │   └── user.py
│   │   ├── routes/
│   │   │   ├── __pycache__/
│   │   │   ├── auth_routes.py
│   │   │   └── general_routes.py
│   │   └── utils/
│   │       ├── __pycache__/
│   │       ├── auth_decorator.py
│   │       └── jwt_helper.py
│   ├── venv/
│   ├── .env
│   ├── requirements.txt
│   └── main.py
├── database/
│   └──barbarian-db.sql
├── frontend/
│   ├── node_modules/
│   ├── src/
│   │   ├── assets/
│   │   ├── js/
│   │   │   ├── utils
│   │   │   │   └── api.js
│   │   │   ├── config.js
│   │   │   └── main.js
│   │   ├── styles/
│   │   │   └── main.css
│   │   └── pages/
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.js
└── README.md

para verificar que todo funciona
# Terminal 1 - Backend
cd backend
pip install -r requirements.txt
python main.py

# Terminal 2 - Frontend (nueva terminal)
cd frontend
npm install
npm run dev






# CONFIG.js Documentation  

This file centralizes all the **frontend configuration** for the project, making it easier to manage API endpoints and storage keys in one place.  

---

## 🔗 API Base URL  
API_BASE_URL: 'http://localhost:5000'  
- Defines the backend server URL.  
- Change this when moving from local development to production.  

---

## 📌 Endpoints  
ENDPOINTS: {
  AUTH: {
    REGISTER: '/auth/register',
    LOGIN: '/auth/login',
    PROFILE: '/auth/profile'
  }
}

- REGISTER → POST /auth/register → Creates a new user.  
- LOGIN → POST /auth/login → Authenticates a user and returns a token.  
- PROFILE → GET /auth/profile → Retrieves the authenticated user profile (requires JWT).  

---

## 💾 Storage Keys  
STORAGE: {
  TOKEN_KEY: 'barberian_token',
  USER_KEY: 'barberian_user'
}

- TOKEN_KEY → Stores the JWT token in localStorage.  
- USER_KEY → Stores the authenticated user information in localStorage.  

---

## 🚀 Usage Example  

import CONFIG from './CONFIG.js';

# Login request
fetch(CONFIG.API_BASE_URL + CONFIG.ENDPOINTS.AUTH.LOGIN, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
})
.then(res => res.json())
.then(data => {
  localStorage.setItem(CONFIG.STORAGE.TOKEN_KEY, data.token);
});

---

auth google
auth_provider.py
