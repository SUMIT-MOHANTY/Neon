set -e

# Basic validation script for the landing page
echo "=== VALIDATION TESTS ==="
echo "Testing Flask app import..."
python -c "from app import app; print(' Flask app imports successfully')"

echo "Testing template rendering..."
python -c "
from app import app
with app.app_context():
    from flask import render_template
    html = render_template('index.html', page_title='Test')
    assert 'Satya' in html
    assert 'static/' in html
    print(' Template renders correctly')"

echo "Testing static file existence..."
test -f static/css/styles.css && echo " styles.css exists"
test -f static/img/logo.png && echo " logo.png exists"
test -f templates/index.html && echo " index.html exists"

echo "=== ALL TESTS PASSED ==="
