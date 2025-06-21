#!/usr/bin/env bash
set -euo pipefail

#── prerequisites ───────────────────────────────────────────────────────────────
apt-get update -y
apt-get install -y --no-install-recommends \
  ca-certificates libfontconfig1 bzip2 curl gnupg python3 python3-pip

#── Node.js (18 LTS) ────────────────────────────────────────────────────────────
if ! command -v node &>/dev/null; then
  curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
  apt-get install -y --no-install-recommends nodejs
fi

#── html-lint & compatible chalk (CJS) ──────────────────────────────────────────
npm install -g chalk@4 html-lint

# Wrapper to ensure html-lint has a writable temp directory
HTML_LINT_REAL="$(command -v html-lint)"
cat >/usr/local/bin/html-lint-safe <<EOF
#!/usr/bin/env bash
set -euo pipefail
mkdir -p "\$(pwd)/temp"
exec "$HTML_LINT_REAL" "\$@"
EOF
chmod +x /usr/local/bin/html-lint-safe

#── PhantomJS ──────────────────────────────────────────────────────────────────
PHANTOM_VER=2.1.1
TMPDIR="$(mktemp -d)"
curl -L --fail \
  "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-${PHANTOM_VER}-linux-x86_64.tar.bz2" \
  -o "${TMPDIR}/phantomjs.tar.bz2"
tar -xjf "${TMPDIR}/phantomjs.tar.bz2" -C "$TMPDIR"
install -Dm755 "${TMPDIR}/phantomjs-${PHANTOM_VER}-linux-x86_64/bin/phantomjs" /usr/local/bin/phantomjs
rm -rf "$TMPDIR"

#── Python chapter fixes ────────────────────────────────────────────────────────
python3 fix_chapters.py

#── Lint verification ──────────────────────────────────────────────────────────
echo "🔍  Running html-lint on all XHTML chapters…"
for f in OEBPS/*.xhtml; do
  echo "→ $f"
  html-lint-safe "$f"
done

echo "✅  All chapters passed html-lint and were updated successfully."
