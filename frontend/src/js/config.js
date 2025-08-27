const CONFIG = {
    // Base URL of the backend API
    API_BASE_URL: 'http://localhost:5000',

    // All available API endpoints
    ENDPOINTS: {
        AUTH: {
            REGISTER: '/auth/register', // User registration
            LOGIN: '/auth/login',       // User login
            PROFILE: '/auth/profile'    // Get user profile (requires token)
        }
    },

    // Keys for localStorage session management
    STORAGE: {
        TOKEN_KEY: 'barberian_token', // Stores JWT token
        USER_KEY: 'barberian_user'    // Stores user information
    }
};

export default CONFIG;
