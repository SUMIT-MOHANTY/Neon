import os
import logging
from flask import Flask, render_template, send_from_directory, abort, request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

""" Satya Landing Page Flask Application
Serves static assets with proper security headers """

def create_app() -> Flask:
    """Create and configure Flask application"""
    app = Flask(__name__, static_folder='static', template_folder='templates')

    # Prevent caching during development
    if os.environ.get('FLASK_ENV') == 'development':
        @app.after_request
        def after_request(response):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response

    # Routes
    @app.route('/')
    def index():
        """Serve the landing page with dynamic context"""
        try:
            logger.info("Serving index page")
            context = {
                "page_title": "Satya - Landing Page"
            }
            return render_template('index.html', **context)
        except Exception as e:
            logger.error(f"Error serving index: {e}")
            abort(500)

    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return {"status": "healthy", "service": "flask-app"}, 200

    @app.route('/static/<path:filename>')
    def static_files(filename):
        """Serve static files safely"""
        try:
            return send_from_directory('static', filename)
        except FileNotFoundError:
            logger.warning(f"Static file not found: {filename}")
            abort(404)
        except Exception as e:
            logger.error(f"Error serving static file {filename}: {e}")
            abort(500)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors with consistent template"""
        logger.warning("404 error - resource not found")
        return render_template('index.html', page_title="Page Not Found - Satya"), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors gracefully"""
        logger.error("500 error - internal server error")
        return render_template('index.html', page_title="Error - Satya"), 500

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    logger.info(f"Starting Flask server on 0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
