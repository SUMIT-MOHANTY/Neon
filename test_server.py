import requests
import time
import subprocess
import signal
import os

def test_server():
    # Start the server
    os.environ['FLASK_ENV'] = 'development'
    server_process = subprocess.Popen(['python3', 'server.py'])

    # Wait for server to start
    time.sleep(2)

    try:
        # Test health endpoint
        response = requests.get('http://localhost:5000/health')
        assert response.status_code == 200
        print("[CHECK] PASS: Health endpoint working")

        # Test landing page
        response = requests.get('http://localhost:5000/')
        assert response.status_code == 200
        print("[CHECK] PASS: Landing page serving")

        # Test static file serving
        response = requests.get('http://localhost:5000/static/style.css')
        if response.status_code == 200:
            print("[CHECK] PASS: Static files serving")
        else:
            print("[CHECK] FAIL: Static files not found (expected)")

    except requests.exceptions.ConnectionError:
        print("[CHECK] FAIL: Server not responding")

    finally:
        # Clean up
        server_process.send_signal(signal.SIGTERM)
        server_process.wait()

if __name__ == '__main__':
    test_server()
