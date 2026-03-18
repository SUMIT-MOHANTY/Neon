set -e

echo "  Validating test environment..."

# Check Python
python3 --version || { echo " Python not found"; exit 1; }

# Install dependencies
python3 -m pip install -r requirements.txt

# Verify test files exist
if [ ! -f "tests/__init__.py" ]; then
    python3 run_tests.py
fi

echo " Environment validation complete"
