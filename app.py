from flask import Flask, render_template, send_from_directory
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    """Serve the index.html template"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving index: {e}")
        return f"Error: {str(e)}", 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "flask-app"}, 200

@app.errorhandler(404)
def not_found(error):
    return {"error": "Not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    return {"error": "Internal server error"}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() != 'false'
    logger.info(f"Starting Flask app on port {port} (debug: {debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)
