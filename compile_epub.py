#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re
import shutil
import sys
from pathlib import Path

OEBPS_DIR = Path("OEBPS")
BACKUP_SUFFIX = ".bak"
CHAPTER_RANGE = range(1, 29)

def echo(msg: str) -> None:
    print(msg)
    try:
        sys.stdout.flush()
    except Exception:
        pass

def backup(path: Path) -> None:
    bak = path.with_suffix(path.suffix + BACKUP_SUFFIX)
    if not bak.exists():
        shutil.copy2(path, bak)
        echo(f"  ↳ backup → {bak.name}")

read = lambda p: p.read_text("utf-8", errors="ignore")
write = lambda p, t: p.write_text(t, "utf-8")

RE_DATA = re.compile(r"\bdata-epub-type=")
RE_ROLE = re.compile(r"role=\"document\"")
RE_HTML = re.compile(r"<html[^>]*>", re.I)
RE_BQ = re.compile(r"<blockquote(?![^>]*class=)")
RE_SVG = re.compile(r"<svg(?![^>]*aria-hidden)")


def _map(levels: tuple[str, ...], to: str, text: str) -> str:
    pat = fr"<(\/?)h({'|'.join(levels)})(?=[\s>])"
    return re.sub(pat, lambda m: f"<{m.group(1)}h{to}", text)

def _ensure_ns(match: re.Match[str]) -> str:
    tag = match.group(0)
    if "xmlns:epub" in tag:
        return tag
    return tag[:-1] + " xmlns:epub=\"http://www.idpf.org/2007/ops\">"

def common(txt: str) -> str:
    txt = RE_DATA.sub("epub:type=", txt)
    txt = RE_ROLE.sub("role=\"doc-chapter\"", txt)
    txt = RE_HTML.sub(_ensure_ns, txt, 1)
    txt = RE_BQ.sub("<blockquote class=\"styled-quote\"", txt)
    txt = RE_SVG.sub("<svg aria-hidden=\"true\"", txt)
    return txt

P_RE = re.compile(r"<p[^>]*>.*?</p>", re.S)
STAR = re.compile(r"[★☆]\s*")
QUIZ_SEC = re.compile(r"<(section|div)([^>]*quiz[^>]*)>", re.I)
QUIZ_LIST = re.compile(r"<(ul|ol)(?=[^>]*quiz)[^>]*>", re.I)
ROI_TAB = re.compile(r"<table[^>]*>(?=.*ROI)", re.S | re.I)
PLACE_URL = re.compile(r"href=\"https?://(www\.)?(example|placeholder)[^\"]*\"")
AI_TERM = re.compile(r"Beauty\s*Genius\s*AI", re.I)
HELP = re.compile(r"tel:[\d-]{7,14}")
ASSESS = re.compile(r"<(section|div)([^>]*(assessment|worksheet)[^>]*)>", re.I)
CURL = re.compile(r"\b([123])([abc])\b")
SUP = re.compile(r"(<sup>)(\d+)(</sup>)")
CONC = re.compile(r"<h1[^>]*>\s*Conclusion\s*</h1>", re.I)

def ch20(t: str) -> str:
    paras = P_RE.findall(t)[:2]
    if len(paras) == 2 and paras[0] == paras[1]:
        t = t.replace(paras[1], "", 1)
    return t

def ch21(t: str) -> str:
    return STAR.sub("⭐ ", t)

def ch22(t: str) -> str:
    t = QUIZ_SEC.sub(lambda m: f"<{m.group(1)}{m.group(2)} role=\"doc-quiz\">", t)
    t = QUIZ_LIST.sub(lambda m: f"<{m.group(1)} class=\"quiz-list\">", t)
    return _map(("4", "5", "6"), "3", t)

def ch23(t: str) -> str:
    t = ROI_TAB.sub(lambda m: m.group(0).replace("<table", "<table class=\"roi-table\" role=\"table\""), t)
    return PLACE_URL.sub("href=\"#\"", t)

def ch25(t: str) -> str:
    t = AI_TERM.sub("Beauty Genius AI", t)
    return _map(("5", "6"), "4", t)

def ch26(t: str) -> str:
    t = HELP.sub("tel:+18002738255", t)
    return ASSESS.sub(lambda m: f"<{m.group(1)}{m.group(2)} role=\"doc-assessment\">", t)

def ch27(t: str) -> str:
    t = CURL.sub(lambda m: m.group(1) + m.group(2).upper(), t)
    counter = 1
    def repl(m: re.Match[str]) -> str:
        nonlocal counter
        rep = f"{m.group(1)}{counter}{m.group(3)}"
        counter += 1
        return rep
    return SUP.sub(repl, t)

def ch28(t: str) -> str:
    if not CONC.search(t):
        body_idx = t.find("<body")
        insert = t.find('>', body_idx) + 1
        t = t[:insert] + "\n<h1>Conclusion</h1>" + t[insert:]
    first = True
    def keep(m: re.Match[str]) -> str:
        nonlocal first
        if first:
            first = False
            return m.group(0)
        return ""
    return CONC.sub(keep, t)

TRANS = {
    "20-": ch20,
    "21-": ch21,
    "22-": ch22,
    "23-": ch23,
    "25-": ch25,
    "26-": ch26,
    "27-": ch27,
    "28-": ch28,
}

def process(path: Path, *, dry: bool) -> None:
    echo(f"• {path.name}")
    backup(path)
    original = read(path)
    modified = common(original)
    for prefix, fn in TRANS.items():
        if path.name.startswith(prefix):
            modified = fn(modified)
            break
    if modified == original:
        echo("  ↳ no changes")
        return
    if dry:
        echo("  ↳ would write (dry-run)")
    else:
        write(path, modified)

rename_conc = lambda: (OEBPS_DIR / "28Conclusion.xhtml").rename(OEBPS_DIR / "28-Conclusion.xhtml") if (OEBPS_DIR / "28Conclusion.xhtml").exists() else None

def targets() -> list[Path]:
    return sorted(
        [p for p in OEBPS_DIR.glob("*.xhtml") if re.match(r"(\d+)-", p.name) and int(p.name.split("-", 1)[0]) in CHAPTER_RANGE],
        key=lambda p: int(p.name.split("-", 1)[0])
    )

def self_test() -> None:
    sample = "<html><body><h4>Title</h4><blockquote>Hi</blockquote><svg></svg></body></html>"
    assert "styled-quote" in common(sample)
    assert "aria-hidden" in common(sample)
    assert _map(("4",), "3", sample).count("<h3") == 1
    assert ch21("★ ☆ ") == "⭐ ⭐ ", "Star normalisation failed"
    echo("Self‑test passed ✔")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fix EPUB XHTML chapters 1‑28 losslessly")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        sys.exit()

    if not OEBPS_DIR.is_dir():
        echo("Error: OEBPS directory not found")
        sys.exit(1)

    rename_conc()
    files = targets()
    if not files:
        echo("No target XHTML files found")
        sys.exit(0)

    for f in files:
        process(f, dry=args.dry_run)

    echo("Done. Validate with EPUBCheck for complete assurance.")
