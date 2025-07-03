"""Merge numbered XHTML files into a plain-text DOCX manuscript."""

import subprocess
from pathlib import Path

from bs4 import BeautifulSoup

OEBPS_DIR = Path("OEBPS")
OUTPUT = Path("manuscript.docx")
PAGE_BREAK = "\n\\newpage\n"


def collect_chapters(limit: int = 44) -> list[Path]:
    """Return XHTML files starting with digits, sorted numerically."""
    files = [p for p in OEBPS_DIR.glob("*.xhtml") if p.name[0].isdigit()]
    return sorted(files)[:limit]


def strip_tags(path: Path) -> str:
    """Return plain text from an XHTML file."""
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")
    return soup.get_text()


def combine_files(files: list[Path], temp_path: Path) -> None:
    """Write concatenated plain text with page breaks to *temp_path*."""
    with temp_path.open("w", encoding="utf-8") as out:
        for i, f in enumerate(files):
            out.write(strip_tags(f))
            if i < len(files) - 1:
                out.write(PAGE_BREAK)


def main():
    files = collect_chapters()
    if not files:
        print("No XHTML files found.")
        return
    temp = Path("/tmp/combined.txt")
    combine_files(files, temp)
    try:
        subprocess.run([
            "pandoc",
            str(temp),
            "-o",
            str(OUTPUT),
        ], check=True)
        print(f"Created {OUTPUT}")
    finally:
        if temp.exists():
            temp.unlink()


if __name__ == "__main__":
    main()
