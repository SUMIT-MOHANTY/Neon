"""
Minimal Flask server to serve the landing page.
"""
import os
from flask import Flask, send_from_directory, request, jsonify
from pathlib import Path

# Create Flask app
app = Flask(__name__, static_folder=None)

# Determine paths based on environment
LANDING_PAGE_DIR = os.path.abspath('landing-page')
STATIC_DIR = os.path.join(LANDING_PAGE_DIR, 'static')

@app.route('/')
def serve_landing_page():
    """Serve the main landing page index.html"""
    index_path = os.path.join(LANDING_PAGE_DIR, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(LANDING_PAGE_DIR, 'index.html')
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Landing Page Coming Soon</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .coming-soon { color: #666; font-size: 24px; }
        </style>
    </head>
    <body>
        <div class="coming-soon">Landing page is being prepared...</div>
    </body>
    </html>
    """, 404

@app.route('/<path:filepath>')
def serve_static_files(filepath):
    """Serve static files from the landing page directory"""
    # Prevent path traversal attacks
    filepath = filepath.replace('..', '')

    # Check if file exists in landing page directory
    full_path = os.path.join(LANDING_PAGE_DIR, filepath)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return send_from_directory(LANDING_PAGE_DIR, filepath)

    # Check in static subdirectory
    static_full_path = os.path.join(STATIC_DIR, filepath)
    if os.path.exists(static_full_path) and os.path.isfile(static_full_path):
        return send_from_directory(STATIC_DIR, filepath)

    return "File not found", 404

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({"status": "healthy", "service": "landing-page-server"})

@app.errorhandler(404)
def not_found(e):
    """Handle 404s gracefully"""
    return jsonify({"error": "Not found", "path": request.path}), 404

@app.errorhandler(500)
def server_error(e):
    """Handle server errors gracefully"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'

    print(f"Starting Flask server on port {port}")
    print(f"Serving landing page from: {LANDING_PAGE_DIR}")

    app.run(host='0.0.0.0', port=port, debug=debug)
