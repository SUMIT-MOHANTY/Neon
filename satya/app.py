import logging
import os
import traceback
from flask import Flask, render_template, abort

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
logger.info("Static folder path: %s", STATIC_DIR)

app = Flask(
    __name__,
    template_folder="templates",
    static_folder=STATIC_DIR,
    static_url_path="/static",
)
logger.info("Flask app instantiated")

@app.route('/', methods=['GET'])
def landing_page():
    """Serve the landing page using Jinja template."""
    try:
        logger.info("GET /")
        response = render_template('index.html')
        logger.debug("Template rendered successfully.")
        return response, 200
    except Exception as e:
        logger.error("Template rendering failed: %s", e, exc_info=True)
        return traceback.format_exc(), 500, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
