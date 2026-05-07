// config.js - Dynamic API configuration for production
const getApiBaseUrl = () => {
    // Check if we're in production (Netlify or any non-localhost domain)
    const hostname = window.location.hostname;
    
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        // Local development
        return 'http://localhost:8000/api';
    }
    
    // Production - REPLACE WITH YOUR RENDER BACKEND URL
    // After deploying backend to Render, update this URL
    return 'https://muscle-forge-api.onrender.com/api';
};

const getBackendBaseUrl = () => {
    const hostname = window.location.hostname;
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return 'http://localhost:8000';
    }
    return 'https://muscle-forge-api.onrender.com';
};

// Set global variables
window.API_BASE_URL = getApiBaseUrl();
window.BACKEND_BASE_URL = getBackendBaseUrl();

console.log('🌐 Environment:', window.location.hostname);
console.log('🔗 API URL:', window.API_BASE_URL);
console.log('🖼️ Backend URL:', window.BACKEND_BASE_URL);
