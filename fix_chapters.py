#!/usr/bin/env python3
from __future__ import annotations
import argparse, re, shutil, sys
from pathlib import Path

# ── configuration ──────────────────────────────────────────────────────────────
OEBPS_DIR     = Path("OEBPS")
BACKUP_SUFFIX = ".bak"
FILE_RANGE    = range(1, 29)                 # 1-28 inclusive
SCRIPT_NAME   = "fix_chapters.py"

# ── helpers ────────────────────────────────────────────────────────────────────
echo   = lambda m: (print(m), sys.stdout.flush())
read   = lambda p: p.read_text("utf-8", errors="ignore")
write  = lambda p, t: p.write_text(t, "utf-8")

def backup(src: Path) -> None:
    bak = src.with_suffix(src.suffix + BACKUP_SUFFIX)
    if not bak.exists():
        shutil.copy2(src, bak)
        echo(f"  ↳ backup → {bak.name}")

def _sp(a: str) -> str:               # ensure a leading space
    return a if a.startswith(" ") else f" {a.lstrip()}"

# ── regex pre-compiles (global) ────────────────────────────────────────────────
RE_DATA  = re.compile(r"\bdata-epub-type=")
RE_ROLE  = re.compile(r'role="document"')
RE_HTML  = re.compile(r"<html[^>]*>", re.I)
RE_BQ    = re.compile(r"<blockquote(?![^>]*class=)")
RE_SVG   = re.compile(r"<svg(?![^>]*aria-hidden)")

P_RE       = re.compile(r"<p[^>]*>.*?</p>", re.S)
STAR       = re.compile(r"[\u2605\u2606]\s*")
QUIZ_SEC   = re.compile(r"<(section|div)([^>]*quiz[^>]*)>", re.I)
QUIZ_LST   = re.compile(r"<(ul|ol)(?=[^>]*quiz)[^>]*>", re.I)
ROI_TAB    = re.compile(r"<table[^>]*>(?=.*ROI)", re.S | re.I)
PLACE_URL  = re.compile(r'href="https?://[^"]*(example|placeholder)[^"]*"')
AI_TERM    = re.compile(r"Beauty\s*Genius\s*AI", re.I)
HELP_TEL   = re.compile(r"tel:[\d-]{7,14}")
ASSESS_SEC = re.compile(r"<(section|div)([^>]*(assessment|worksheet)[^>]*)>", re.I)
CURL_TXT   = re.compile(r"\b([123])([abc])\b")
SUP_NUM    = re.compile(r"(<sup>)(\d+)(</sup>)")
CONC_H1    = re.compile(r"<h1[^>]*>\s*Conclusion\s*</h1>", re.I)

# ── shared transforms ──────────────────────────────────────────────────────────
def ensure_ns(m: re.Match[str]) -> str:
    tag = m.group(0)
    return tag if "xmlns:epub" in tag else tag[:-1] + ' xmlns:epub="http://www.idpf.org/2007/ops">'

def elevate(levels: tuple[str, ...], dest: str, t: str) -> str:
    pat = fr"<(/?)h({'|'.join(levels)})(?=[\s>])"
    return re.sub(pat, lambda m: f"<{m.group(1)}h{dest}", t)

def baseline(t: str) -> str:
    t = RE_DATA.sub("epub:type=", t)
    t = RE_ROLE.sub('role="doc-chapter"', t)
    t = RE_HTML.sub(ensure_ns, t, 1)
    t = RE_BQ.sub('<blockquote class="styled-quote"', t)
    t = RE_SVG.sub('<svg aria-hidden="true"', t)
    return t

# ── file-specific transforms ───────────────────────────────────────────────────
def file20(t: str) -> str:
    dups = P_RE.findall(t)[:2]
    if len(dups) == 2 and dups[0] == dups[1]:
        t = t.replace(dups[1], "", 1)
    return t

def file21(t: str) -> str:
    return STAR.sub("⭐ ", t)

def file22(t: str) -> str:
    t = QUIZ_SEC.sub(lambda m: f"<{m.group(1)}{_sp(m.group(2))} role=\"doc-quiz\">", t)
    t = QUIZ_LST.sub(lambda m: f"<{m.group(1)} class=\"quiz-list\">", t)
    return elevate(("4", "5", "6"), "3", t)

def file23(t: str) -> str:
    t = ROI_TAB.sub(lambda m: m.group(0).replace("<table", '<table class="roi-table" role="table"'), t)
    return PLACE_URL.sub('href="#"', t)

def file25(t: str) -> str:
    t = AI_TERM.sub("Beauty Genius AI", t)
    return elevate(("5", "6"), "4", t)

def file26(t: str) -> str:
    t = HELP_TEL.sub("tel:+18002738255", t)
    return ASSESS_SEC.sub(lambda m: f"<{m.group(1)}{_sp(m.group(2))} role=\"doc-assessment\">", t)

def file27(t: str) -> str:
    t = CURL_TXT.sub(lambda m: m.group(1) + m.group(2).upper(), t)
    n = 1
    def renum(m: re.Match[str]) -> str:
        nonlocal n
        r = f"{m.group(1)}{n}{m.group(3)}"
        n += 1
        return r
    return SUP_NUM.sub(renum, t)

def file28(t: str) -> str:
    if not CONC_H1.search(t):
        body = t.find("<body")
        idx  = t.find(">", body) + 1
        t = t[:idx] + "\n<h1>Conclusion</h1>" + t[idx:]
    seen = False
    return CONC_H1.sub(lambda m: m.group(0) if not (seen := True) else "", t)

TRANSFORMS = {
    "20-": file20,
    "21-": file21,
    "22-": file22,
    "23-": file23,
    "25-": file25,
    "26-": file26,
    "27-": file27,
    "28-": file28,
}

# ── processing ────────────────────────────────────────────────────────────────
def process(p: Path, dry: bool) -> None:
    echo(f"• {p.name}")
    backup(p)
    src = read(p)
    out = baseline(src)
    for pre, fn in TRANSFORMS.items():
        if p.name.startswith(pre):
            out = fn(out)
            break
    if out == src:
        echo("  ↳ no changes")
    elif dry:
        echo("  ↳ would write (dry-run)")
    else:
        write(p, out)

def rename_conclusion(dry: bool) -> None:
    old, new = OEBPS_DIR / "28Conclusion.xhtml", OEBPS_DIR / "28-Conclusion.xhtml"
    if old.exists() and not new.exists():
        echo("• renaming 28Conclusion.xhtml → 28-Conclusion.xhtml")
        if not dry:
            old.rename(new)

def targets() -> list[Path]:
    return sorted(
        [p for p in OEBPS_DIR.glob("*.xhtml")
         if re.match(r"(\d+)-", p.name)
         and int(p.name.split("-", 1)[0]) in FILE_RANGE],
        key=lambda p: int(p.name.split("-", 1)[0])
    )

def self_test() -> None:
    s = '<html><body><h4>x</h4><blockquote>q</blockquote><svg></svg></body></html>'
    assert 'styled-quote' in baseline(s)
    assert 'aria-hidden'  in baseline(s)
    assert elevate(("4",), "3", s).count("<h3") == 1
    assert file21("★ ☆ ") == "⭐ ⭐ "
    echo("Self-test passed ✓")

# ── CLI ────────────────────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(prog=SCRIPT_NAME,
        description="Losslessly fix EPUB XHTML files 1-28 in OEBPS/")
    ap.add_argument("--dry-run",   action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        self_test(); return
    if not OEBPS_DIR.is_dir():
        echo("❌  OEBPS directory not found"); sys.exit(1)

    rename_conclusion(args.dry_run)
    for f in targets():
        process(f, args.dry_run)
    echo("✅  Fixes complete – run EPUBCheck for final validation.")

if __name__ == "__main__":
    main()
