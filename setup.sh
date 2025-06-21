#!/usr/bin/env bash
set -euo pipefail

echo "💾  Updating apt lists…"
apt-get update -y

echo "📦  Installing system packages…"
apt-get install -y --no-install-recommends \
  ca-certificates \
  libfontconfig1 \
  bzip2 \
  curl \
  gnupg

# ── Node.js 18 LTS ─────────────────────────────────────────────────────────────
if ! command -v node &>/dev/null; then
  echo "⬇️  Installing Node.js 18 LTS…"
  curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
  apt-get install -y --no-install-recommends nodejs
fi

# ── html-lint + CommonJS-compatible chalk ──────────────────────────────────────
echo "⬇️  Installing chalk@4 and html-lint…"
npm install -g chalk@4 html-lint

# defensive check
if ! command -v html-lint &>/dev/null; then
  echo "❌  html-lint installation failed" >&2
  exit 1
fi

# create a wrapper that guarantees the temp folder exists
HTML_LINT_REAL="$(command -v html-lint)"
cat >/usr/local/bin/html-lint-safe <<'WRAP'
#!/usr/bin/env bash
set -euo pipefail
DIR="$(pwd)"
mkdir -p "$DIR/temp"
exec '"'"$HTML_LINT_REAL"'"' "$@"
WRAP
chmod +x /usr/local/bin/html-lint-safe

echo "✔️  html-lint ready (wrapper: html-lint-safe)"

# ── PhantomJS (for other tools) ────────────────────────────────────────────────
PHANTOM_VER="2.1.1"
PHANTOM_URL="https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-${PHANTOM_VER}-linux-x86_64.tar.bz2"
TMPDIR="$(mktemp -d)"

echo "🕶️  Downloading PhantomJS ${PHANTOM_VER}…"
curl -L --fail "$PHANTOM_URL" -o "${TMPDIR}/phantomjs.tar.bz2"

echo "📦  Extracting PhantomJS…"
tar -xjf "${TMPDIR}/phantomjs.tar.bz2" -C "${TMPDIR}"
install -Dm755 "${TMPDIR}/phantomjs-${PHANTOM_VER}-linux-x86_64/bin/phantomjs" /usr/local/bin/phantomjs

if ! command -v phantomjs &>/dev/null; then
  echo "❌  PhantomJS install failed" >&2
  exit 1
fi
echo "✔️  PhantomJS installed: $(phantomjs --version)"

rm -rf "${TMPDIR}"
echo "✅  Environment ready: use \`html-lint-safe <file>\` (or npx with chalk@4) without crashes."
