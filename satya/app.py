from flask import Flask, render_template, abort
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def landing():
    """
    Serves the landing page
    Returns: rendered index.html (200 OK)
    Errors: 500 on template failure
    """
    try:
        return render_template('index.html')
    except Exception:
        abort(500)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
