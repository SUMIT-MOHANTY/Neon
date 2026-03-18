import os
import logging
from flask import Flask, render_template, send_from_directory, abort

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# Routes
@app.route('/')
def index():
    """Serve the landing page"""
    try:
        logger.info("Serving index page")
        return render_template('index.html')
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
    logger.warning("404 error - resource not found")
    return {"error": "Not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    logger.error("500 error - internal server error")
    return {"error": "Internal server error"}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    logger.info(f"Starting Flask server on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
