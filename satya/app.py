from flask import Flask, render_template, abort
import traceback

app = Flask(__name__)

@app.route('/', methods=['GET'])
def landing_page():
    try:
        return render_template('index.html'), 200
    except Exception as e:
        # generic 500 with stack
        return traceback.format_exc(), 500, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(debug=False)
