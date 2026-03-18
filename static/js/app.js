/**
 * NexaTech Application Core JavaScript
 * Handles frontend application logic, state management, and utilities
 */

(function() {
    'use strict';

    // Configuration object
    const Config = {
        API_BASE_URL: window.location.origin + '/api',
        LOCAL_STORAGE_KEYS: {
            USER_PREFERENCES: 'nexatech_user_prefs',
            SESSION_DATA: 'nexatech_session'
        },
        LOGGING_ENABLED: true,
        PERFORMANCE_MONITORING: true
    };

    // Utility object for common functions
    const Utils = {
        // Debounce function for performance optimization
        debounce: function(func, delay) {
            let timeoutId;
            return function(...args) {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => func.apply(this, args), delay);
            };
        },

        // Validate email address
        validateEmail: function(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        },

        // Store user preferences
        storeUserPreference: function(key, value) {
            try {
                localStorage.setItem(Config.LOCAL_STORAGE_KEYS.USER_PREFERENCES + '_' + key, JSON.stringify(value));
                return true;
            } catch (e) {
                console.warn('Failed to store user preference:', e);
                return false;
            }
        },

        // Retrieve user preferences
        getUserPreference: function(key, defaultValue = null) {
            try {
                const value = localStorage.getItem(Config.LOCAL_STORAGE_KEYS.USER_PREFERENCES + '_' + key);
                return value ? JSON.parse(value) : defaultValue;
            } catch (e) {
                console.warn('Failed to retrieve user preference:', e);
                return defaultValue;
            }
        }
    };

    // API wrapper
    const API = {
        get: async function(endpoint, params = {}) {
            try {
                const url = new URL(endpoint, Config.API_BASE_URL);
                Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

                const response = await fetch(url, {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json' }
                });

                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                return await response.json();

            } catch (error) {
                logger.error('API GET error:', error);
                throw error;
            }
        },

        post: async function(endpoint, data = {}) {
            try {
                const response = await fetch(`${Config.API_BASE_URL}${endpoint}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                return await response.json();

            } catch (error) {
                logger.error('API POST error:', error);
                throw error;
            }
        }
    };

    // Logger utility
    const logger = {
        info: function(message, data = null) {
            if (Config.LOGGING_ENABLED) {
                console.info(`[NexaTech Info] ${message}`, data);
                if (window.pageMonitor) {
                    window.pageMonitor.log(message, 'INFO');
                }
            }
        },

        error: function(message, error) {
            console.error(`[NexaTech Error] ${message}`, error);
            if (window.pageMonitor) {
                window.pageMonitor.reportError(error, message);
            }
        },

        debug: function(message, data) {
            if (Config.LOGGING_ENABLED && window.location.hostname === 'localhost') {
                console.debug(`[NexaTech Debug] ${message}`, data);
            }
        }
    };

    // Initialize application
    const init = function() {
        logger.info('NexaTech Application initializing...');

        // Load user preferences
        loadUserPreferences();

        // Setup event listeners
        setupEventListeners();

        // Check browser compatibility
        checkBrowserCompatibility();

        logger.info('NexaTech Application initialized successfully');
    };

    // Load user preferences
    const loadUserPreferences = function() {
        const savedTheme = Utils.getUserPreference('theme', 'light');
        document.documentElement.setAttribute('data-theme', savedTheme);
    };

    // Setup event listeners
    const setupEventListeners = function() {
        // Listen for theme toggle
        document.addEventListener('themeToggle', Utils.debounce(function(e) {
            Utils.storeUserPreference('theme', e.detail.theme);
            document.documentElement.setAttribute('data-theme', e.detail.theme);
        }, 250));

        // Listen for form submissions
        document.addEventListener('submit', function(e) {
            if (e.target.classList.contains('needs-validation')) {
                handleFormValidation(e);
            }
        });
    };

    // Check browser compatibility
    const checkBrowserCompatibility = function() {
        const requiredFeatures = [
            { name: 'Fetch API', test: () => 'fetch' in window },
            { name: 'Local Storage', test: () => 'Storage' in window && 'localStorage' in window },
            { name: 'Intersection Observer', test: () => 'IntersectionObserver' in window },
            { name: 'Promises', test: () => 'Promise' in window }
        ];

        const unsupported = requiredFeatures.filter(feature => !feature.test());

        if (unsupported.length > 0) {
            logger.warn('Browser compatibility issues:', unsupported.map(f => f.name));
            const unsupportedMessage = `Your browser lacks support for: ${unsupported.map(f => f.name).join(', ')}`;

            // Show compatibility banner
            const banner = document.createElement('div');
            banner.className = 'alert alert-warning alert-dismissible fade show';
            banner.innerHTML = `
                ${unsupportedMessage}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;

            const header = document.querySelector('header');
            if (header) {
                header.parentNode.insertBefore(banner, header.nextSibling);
            }
        }
    };

    // Handle form validation
    const handleFormValidation = function(event) {
        const form = event.target;

        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }

        form.classList.add('was-validated');
    };

    // Performance monitoring
    if (Config.PERFORMANCE_MONITORING && 'PerformanceObserver' in window) {
        const observer = new PerformanceObserver((list) => {
            list.getEntries().forEach(entry => {
                if (entry.entryType === 'largest-contentful-paint' && entry.startTime < 5000) {
                    logger.debug('LCP performance:', entry.startTime);
                }
            });
        });

        observer.observe({ entryTypes: ['largest-contentful-paint'] });
    }

    // Expose public API
    window.NexaTech = {
        Utils,
        API,
        logger,
        Config
    };

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    logger.info('NexaTech Application core loaded');

})();
