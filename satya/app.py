"""
Flask application for serving the landing page and static assets.
Root route / renders templates/index.html.
"""

import logging
import os
from flask import Flask, render_template, Response

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Absolute path guarantees consistent behaviour regardless of CWD
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
logger.info("Static folder path: %s", STATIC_DIR)

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/static")
logger.info("Flask app instantiated")

@app.route("/", methods=["GET"])
def index() -> Response:
    """Serve the landing page using Jinja template."""
    try:
        logger.info("GET /")
        response = render_template("index.html")
        logger.debug("Template rendered successfully.")
        return response
    except Exception as exc:
        logger.error("Template rendering failed: %s", exc, exc_info=True)
        return "Internal Server Error", 500

if __name__ == "__main__":
    # For dev convenience; gunicorn in production
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
