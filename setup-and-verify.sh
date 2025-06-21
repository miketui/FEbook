#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# CONFIG – change only if you move the fixer script
###############################################################################
FIXER_PATH="fix_chapters.py"        # relative to repo root
###############################################################################

echo "💾  Updating apt lists…"
apt-get update -y

echo "📦  Installing system packages…"
apt-get install -y --no-install-recommends \
  ca-certificates libfontconfig1 bzip2 curl gnupg python3

###############################################################################
# Node 18 LTS  +  chalk@4  +  html-lint
###############################################################################
if ! command -v node >/dev/null; then
  echo "⬇️  Installing Node.js 18 LTS…"
  curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
  apt-get install -y --no-install-recommends nodejs
fi

npm install -g chalk@4 html-lint

# wrapper guaranteeing a writable temp/ folder
HTML_LINT_REAL="$(command -v html-lint)"
cat >/usr/local/bin/html-lint-safe <<'WRAP'
#!/usr/bin/env bash
set -euo pipefail
mkdir -p "$(pwd)/temp"
exec '"'"$HTML_LINT_REAL"'"' "$@"
WRAP
chmod +x /usr/local/bin/html-lint-safe

###############################################################################
# PhantomJS 2.1.1
###############################################################################
PHANTOM_VER="2.1.1"
TMPDIR="$(mktemp -d)"
curl -L --fail \
  "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-${PHANTOM_VER}-linux-x86_64.tar.bz2" \
  -o "${TMPDIR}/phantomjs.tar.bz2"
tar -xjf "${TMPDIR}/phantomjs.tar.bz2" -C "$TMPDIR"
install -Dm755 "${TMPDIR}/phantomjs-${PHANTOM_VER}-linux-x86_64/bin/phantomjs" \
  /usr/local/bin/phantomjs
rm -rf "$TMPDIR"

###############################################################################
# Run the chapter-fixing Python script
###############################################################################
if [[ ! -f "$FIXER_PATH" ]]; then
  echo "❌  Cannot locate $FIXER_PATH – make sure it’s committed at that path." >&2
  exit 1
fi

echo "🛠️  Running $FIXER_PATH…"
python3 "$FIXER_PATH"

###############################################################################
# html-lint verification (all XHTML files under OEBPS/)
###############################################################################
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
