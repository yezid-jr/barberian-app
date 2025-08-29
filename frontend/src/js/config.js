const CONFIG = {
    // Base URL of the backend API
    API_BASE_URL: 'http://localhost:5000',

    // Google OAuth Configuration
    GOOGLE_CLIENT_ID: '1033444850049-2gi6ql4t81u2i635bjpqqg1gucp98ps2.apps.googleusercontent.com',

    // All available API endpoints
    ENDPOINTS: {
        AUTH: {
            REGISTER: '/auth/register', // User registration
            LOGIN: '/auth/login',       // User login
            PROFILE: '/auth/profile',    // Get user profile (requires token)
            GOOGLE_VERIFY: '/auth/google/verify'  // Google OAuth verification
        }
    },

    // Keys for localStorage session management
    STORAGE: {
        TOKEN_KEY: 'barberian_token', // Stores JWT token
        USER_KEY: 'barberian_user'    // Stores user information
    }
};

export default CONFIG;
