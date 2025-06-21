#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# CONFIG
###############################################################################
FIXER_PATH="fix_chapters.py"    # relative to repo root
NODE_MAJOR=18
PHANTOM_VER=2.1.1
###############################################################################

echo "💾  Updating apt lists…"
apt-get update -y

echo "📦  Installing system libraries…"
apt-get install -y --no-install-recommends \
  ca-certificates libfontconfig1 bzip2 curl gnupg python3

# ── libssl1.1 for PhantomJS (use old-releases mirror) ─────────────────────────
if ! dpkg -s libssl1.1 >/dev/null 2>&1; then
  echo "⬇️  Installing legacy libssl1.1 for PhantomJS…"
  curl -fsSL https://old-releases.ubuntu.com/ubuntu/pool/main/o/openssl1.1/libssl1.1_1.1.1f-1ubuntu2.16_amd64.deb -o /tmp/libssl1.1.deb
  apt-get install -y /tmp/libssl1.1.deb
  rm /tmp/libssl1.1.deb
fi

# ── Node.js + html-lint + chalk@4 ─────────────────────────────────────────────
if ! command -v node >/dev/null; then
  curl -fsSL "https://deb.nodesource.com/setup_${NODE_MAJOR}.x" | bash -
  apt-get install -y --no-install-recommends nodejs
fi

npm install -g chalk@4 html-lint

# ── html-lint wrapper that creates the **module** temp dir ────────────────────
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
echo "✔️  html-lint wrapper installed → html-lint-safe"

# ── PhantomJS 2.1.1 ───────────────────────────────────────────────────────────
TMPDIR=$(mktemp -d)
curl -L --fail \
  "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-${PHANTOM_VER}-linux-x86_64.tar.bz2" \
  -o "${TMPDIR}/phantomjs.tar.bz2"

tar -xjf "${TMPDIR}/phantomjs.tar.bz2" -C "${TMPDIR}"
install -Dm755 "${TMPDIR}/phantomjs-${PHANTOM_VER}-linux-x86_64/bin/phantomjs" \
  /usr/local/bin/phantomjs
rm -rf "${TMPDIR}"
echo "✔️  PhantomJS ready: $(phantomjs --version)"

# ── Run the Python fixer ──────────────────────────────────────────────────────
if [[ ! -f "${FIXER_PATH}" ]]; then
  echo "❌  ${FIXER_PATH} not found – commit it or update FIXER_PATH" >&2
  exit 1
fi

echo "🛠️  Running ${FIXER_PATH}…"
python3 "${FIXER_PATH}"

# ── Lint every XHTML file ─────────────────────────────────────────────────────
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
