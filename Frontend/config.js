// config.js - Dynamic API configuration
// This file determines which API URL to use based on environment

const getApiBaseUrl = () => {
    // Check if we're in production (Netlify)
    if (window.location.hostname !== 'localhost' && 
        window.location.hostname !== '127.0.0.1') {
        // Use your Render backend URL (replace with your actual Render URL)
        return 'https://muscle-forge-api.onrender.com/api';
    }
    // Local development
    return 'http://localhost:8000/api';
};

// Export for use in other files
window.API_BASE_URL = getApiBaseUrl();
console.log('🌐 API URL:', window.API_BASE_URL);
