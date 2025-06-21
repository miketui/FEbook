#!/usr/bin/env bash
set -euo pipefail

FIXER_PATH="fix_chapters.py"
NODE_MAJOR=18

echo "💾  Updating apt lists…"
apt-get update -y

echo "📦  Installing system libraries…"
apt-get install -y --no-install-recommends \
  ca-certificates libfontconfig1 bzip2 curl gnupg python3

if ! command -v node >/dev/null; then
  curl -fsSL "https://deb.nodesource.com/setup_${NODE_MAJOR}.x" | bash -
  apt-get install -y --no-install-recommends nodejs
fi

npm install -g chalk@4 html-lint

HTML_LINT_REAL="$(command -v html-lint)"
NODE_GLOBAL=$(npm root -g)
MODULE_TEMP="${NODE_GLOBAL}/html-lint/temp"
mkdir -p "${MODULE_TEMP}"

cat >/usr/local/bin/html-lint-safe <<EOF
#!/usr/bin/env bash
set -euo pipefail
mkdir -p "${MODULE_TEMP}"
exec "${HTML_LINT_REAL}" "\$@"
EOF
chmod +x /usr/local/bin/html-lint-safe

if [[ ! -f "${FIXER_PATH}" ]]; then
  echo "❌  ${FIXER_PATH} not found – commit it or update FIXER_PATH" >&2
  exit 1
fi

echo "🛠️  Running ${FIXER_PATH}…"
python3 "${FIXER_PATH}"

echo "🔍  Running html-lint on all XHTML chapters…"
shopt -s nullglob
FILES=(OEBPS/*.xhtml)
if (( ${#FILES[@]} == 0 )); then
  echo "⚠️  No XHTML files found in OEBPS/" >&2
  exit 1
fi

for f in "${FILES[@]}"; do
  echo "→ $f"
  html-lint-safe "$f"
done

echo "✅  All chapters fixed and passed html-lint."
