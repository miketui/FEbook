"""Combine numbered XHTML files into a Markdown manuscript."""

import re
from pathlib import Path

from bs4 import BeautifulSoup

OEBPS_DIR = Path("OEBPS")
OUTPUT = Path("manuscript.md")
PAGE_BREAK = "\n\\newpage\n"


def collect_chapters(limit: int = 44) -> list[Path]:
    """Return sorted XHTML chapter files."""
    files = [
        p
        for p in OEBPS_DIR.glob("*.xhtml")
        if p.name[0].isdigit() and not p.name.endswith(".bak")
    ]
    return sorted(
        files,
        key=lambda p: int(re.match(r"(\d+)", p.name).group(1)),
    )[:limit]


def strip_tags(path: Path) -> str:
    """Return plain text from XHTML file."""
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")
    return soup.get_text()


def combine(files: list[Path], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8") as out:
        for i, f in enumerate(files):
            out.write(strip_tags(f))
            if i < len(files) - 1:
                out.write(PAGE_BREAK)


def main() -> None:
    files = collect_chapters()
    if not files:
        print("No chapters found")
        return
    combine(files, OUTPUT)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
