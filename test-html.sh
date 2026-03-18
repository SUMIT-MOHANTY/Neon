set -e
cd /workspace

echo "=== HTML Validation Test ==="
echo "Running basic HTML structure validation..."

# Check if required files exist
test_files=(
    "templates/index.html"
    "static/css/main.css"
    "static/js/app.js"
    "static/images"
)

all_pass=true
for file in "${test_files[@]}"; do
    if [[ -e "$file" ]]; then
        echo "[PASS] $file exists"
    else
        echo "[FAIL] $file missing"
        all_pass=false
    fi
done

# Validate HTML syntax (basic check for major tags)
if grep -q '<!DOCTYPE html>' templates/index.html; then
    echo "[PASS] DOCTYPE declaration found"
else
    echo "[FAIL] Missing DOCTYPE"
    all_pass=false
fi

if grep -q '<header>' templates/index.html; then
    echo "[PASS] Semantic header tag found"
else
    echo "[FAIL] Missing header tag"
    all_pass=false
fi

if grep -q '<main>' templates/index.html; then
    echo "[PASS] Semantic main tag found"
else
    echo "[FAIL] Missing main tag"
    all_pass=false
fi

if grep -q '<footer>' templates/index.html; then
    echo "[PASS] Semantic footer tag found"
else
    echo "[FAIL] Missing footer tag"
    all_pass=false
fi

# Check for required meta tags
meta_tags=("viewport" "description")
for tag in "${meta_tags[@]}"; do
    if grep -q "name=\"$tag\"" templates/index.html; then
        echo "[PASS] Meta $tag tag found"
    else
        echo "[FAIL] Missing meta $tag tag"
        all_pass=false
    fi
done

echo ""
if [[ "$all_pass" == true ]]; then
    echo " All validation tests PASSED"
else
    echo " Some validation tests FAILED"
    exit 1
fi
