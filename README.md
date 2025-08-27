estructura
para instalar librerias de python en el requirement:
``bash
pip install -r requirements.txt
``

barberian-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── routes/
│   │   └── utils/
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── js/
│   │   ├── styles/
│   │   └── pages/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── database/
│   └── barbarian-db.sql
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
