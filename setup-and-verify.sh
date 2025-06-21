#!/usr/bin/env bash
set -euo pipefail

# ─── CONFIG ───────────────────────────────────────────────────────────────────
FIXER_PATH="fix_chapters.py"    # path to your Python fixer
NODE_MAJOR=18                   # Node.js LTS major
# ──────────────────────────────────────────────────────────────────────────────

echo "💾 Updating apt lists…"
apt-get update -y

echo "📦 Installing system libraries…"
apt-get install -y --no-install-recommends \
  ca-certificates libfontconfig1 bzip2 curl gnupg python3

# ─── Node.js ──────────────────────────────────────────────────────────────────
if ! command -v node >/dev/null; then
  echo "⬇️ Installing Node.js ${NODE_MAJOR} LTS…"
  curl -fsSL "https://deb.nodesource.com/setup_${NODE_MAJOR}.x" | bash -
  apt-get install -y --no-install-recommends nodejs
fi

# ─── NPM tools ────────────────────────────────────────────────────────────────
# Use --unsafe-perm to address EACCES issues for phantomjs-prebuilt
# Downgrade chalk to version 4 to avoid ERR_REQUIRE_ESM errors
echo "⬇️ Installing html-lint, chalk@4, and phantomjs-prebuilt…"
npm install -g html-lint chalk@4 phantomjs-prebuilt --unsafe-perm

# Wrap html-lint so it always has a temp/ directory to write into
HTML_LINT_REAL="$(command -v html-lint)"
NODE_GLOBAL="$(npm root -g)"
MODULE_TEMP="${NODE_GLOBAL}/html-lint/temp"
mkdir -p "${MODULE_TEMP}"

cat >/usr/local/bin/html-lint-safe <<EOF
#!/usr/bin/env bash
set -euo pipefail
# Create a 'temp' directory in the current working directory if it doesn't exist
# This is crucial as html-lint seems to look for 'temp/saved.html' relative to where it's executed.
mkdir -p temp
exec "${HTML_LINT_REAL}" "\$@"
EOF
chmod +x /usr/local/bin/html-lint-safe
echo "✔️ html-lint wrapper installed → html-lint-safe"

# ─── Run your Python fixer ────────────────────────────────────────────────────
if [[ ! -f "${FIXER_PATH}" ]]; then
  echo "❌ ${FIXER_PATH} not found – commit it or update FIXER_PATH" >&2
  exit 1
fi

echo "🛠️ Running ${FIXER_PATH}…"
python3 "${FIXER_PATH}"

# ─── Lint every XHTML chapter ─────────────────────────────────────────────────
echo "🔍 Linting all OEBPS/*.xhtml with html-lint-safe…"
shopt -s nullglob
FILES=(OEBPS/*.xhtml)
if (( ${#FILES[@]} == 0 )); then
  echo "⚠️ No XHTML files found in OEBPS/" >&2
  exit 1
fi

for f in "${FILES[@]}"; do
  echo "→ $f"
  html-lint-safe "$f"
done

echo "✅ All chapters fixed & passed html-lint."
