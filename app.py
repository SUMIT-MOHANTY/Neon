"""
Satya Landing Page Flask Application
Serves static assets with proper security headers
"""

from flask import Flask, render_template, request
import os

def create_app() -> Flask:
    """Create and configure Flask application"""
    app = Flask(__name__)

    # Prevent caching during development
    if os.environ.get('FLASK_ENV') == 'development':
        @app.after_request
        def after_request(response):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response

    return app

app = create_app()

@app.route('/')
def index():
    """Serve the landing page with dynamic context"""
    context = {
        "page_title": "Satya - Landing Page"
    }
    return render_template('index.html', **context)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with consistent template"""
    return render_template('index.html', page_title="Page Not Found - Satya"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors gracefully"""
    return render_template('index.html', page_title="Error - Satya"), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
