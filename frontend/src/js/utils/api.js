import CONFIG from '../config.js';

class API {
    constructor() {
        // Base URL for backend API
        this.baseURL = CONFIG.API_BASE_URL;
    }

    // =============================
    // TOKEN MANAGEMENT
    // =============================

    // Get token from localStorage
    getToken() {
        return localStorage.getItem(CONFIG.STORAGE.TOKEN_KEY);
    }

    // Save token in localStorage
    saveToken(token) {
        localStorage.setItem(CONFIG.STORAGE.TOKEN_KEY, token);
    }

    // Remove token and user info from localStorage
    removeToken() {
        localStorage.removeItem(CONFIG.STORAGE.TOKEN_KEY);
        localStorage.removeItem(CONFIG.STORAGE.USER_KEY);
    }

    // =============================
    // HEADERS MANAGEMENT
    // =============================

    // Set request headers
    // includeAuth = true → adds Authorization header
    getHeaders(includeAuth = false) {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (includeAuth) {
            const token = this.getToken();
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
        }

        return headers;
    }

    // =============================
    // GENERIC REQUEST METHOD
    // =============================

    // Universal fetch wrapper
    // Handles: GET, POST, PUT, DELETE
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        try {
            const response = await fetch(url, {
                headers: this.getHeaders(options.includeAuth),
                ...options
            });

            const data = await response.json();

            // If response is not OK → throw error
            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }

            return data; // return success response
        } catch (error) {
            console.error('API Error:', error);
            console.log('Endpoint:', endpoint);
            console.log('Options:', options);
            console.log(error.message);
            throw error; // re-throw to handle outside
        }
    }

    // =============================
    // AUTHENTICATION METHODS
    // =============================

    // Register new user
    async register(userData) {
        return this.request(CONFIG.ENDPOINTS.AUTH.REGISTER, {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    // Login existing user
    async login(credentials) {
        return this.request(CONFIG.ENDPOINTS.AUTH.LOGIN, {
            method: 'POST',
            body: JSON.stringify(credentials)
        });
    }

    // Get authenticated user profile
    async getProfile() {
        return this.request(CONFIG.ENDPOINTS.AUTH.PROFILE, {
            method: 'GET',
            includeAuth: true
        });
    }

    // Verify Google OAuth token
    async googleLogin(googleToken) {
        return this.request(CONFIG.ENDPOINTS.AUTH.GOOGLE_VERIFY, {
            method: 'POST',
            body: JSON.stringify({ token: googleToken })
        });
    }
}

// =============================
// EXPORT SINGLETON
// =============================
// Export a single API instance for use across the app
export default new API();
