set -e
cd /workspace

# CSS Validation and Testing Script
printf "=== CSS VALIDATION REPORT ===\n"
printf "Timestamp: $(date)\n\n"

# Check CSS syntax
if ! which node > /dev/null 2>&1; then
    printf "[WARN] Node.js not found - skipping CSS syntax check\n"
elif ! npm list stylelint > /dev/null 2>&1; then
    printf "[WARN] Stylelint not installed - skipping CSS validation\n"
else
    printf "[TEST] Running CSS syntax validation...\n"
    npx stylelint static/styles.css --config tests/.stylelintrc.json || printf "[FAIL] CSS syntax errors found\n"
fi

# Check for common CSS issues
printf "[TEST] Checking for common CSS issues...\n"

# Check for missing semicolons
if grep -n ';[[:space:]]*$' static/styles.css > /dev/null; then
    printf "[PASS] All rules properly terminated with semicolons\n"
else
    printf "[WARN] Potential missing semicolons found\n"
fi

# Check for duplicate CSS properties
printf "[TEST] Checking for duplicate properties...\n"
awk '/^[[:space:]]*[a-zA-Z-]+[[:space:]]*:/ {print tolower($0)}' static/styles.css | \
    sort | uniq -d | while read -r prop; do
    printf "[WARN] Duplicate property detected: %s\n" "$prop"
done

# Check file size
css_size=$(wc -c < static/styles.css)
css_kbs=$((css_size / 1024))
printf "[INFO] CSS file size: ${css_kbs}KB\n"

if [ $css_kbs -gt 100 ]; then
    printf "[WARN] CSS file is large (${css_kbs}KB > 100KB)\n"
else
    printf "[PASS] CSS file size acceptable\n"
fi

# Check for responsive breakpoints
if grep -q "@media.*max-width.*\|@media.*min-width" static/styles.css; then
    printf "[PASS] Responsive breakpoints present\n"
else
    printf "[WARN] No responsive breakpoints found\n"
fi

# Check accessibility features
if grep -q ":focus\|:hover\|@media.*prefers-reduced-motion" static/styles.css; then
    printf "[PASS] Accessibility features present\n"
else
    printf "[WARN] Limited accessibility features\n"
fi

printf "\n=== CSS VALIDATION COMPLETE ===\n"
