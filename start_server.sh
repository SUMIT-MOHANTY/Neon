set -e
cd "$(dirname "$0")"

# Create basic landing page if it doesn't exist
if [ ! -d "landing-page" ]; then
    mkdir -p landing-page/static
    cat > landing-page/index.html <<'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div class="container">
        <h1>Welcome to Our Landing Page</h1>
        <p>This is served by our minimal Flask server.</p>
    </div>
</body>
</html>
HTML

    cat > landing-page/static/style.css <<'CSS'
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f5f5f5;
}
.container {
    max-width: 800px;
    margin: 100px auto;
    text-align: center;
    padding: 40px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
h1 {
    color: #333;
    margin-bottom: 20px;
}
p {
    color: #666;
    font-size: 18px;
}
CSS
fi

# Install dependencies if needed
if ! python3 -c "import flask" > /dev/null 2>&1; then
    echo "Installing Flask..."
    pip install -r requirements.txt
fi

# Start the server
export FLASK_ENV=production
python3 server.py
