"""Validate HTML/EPUB structure for compliance."""
import sys
from pathlib import Path
from bs4 import BeautifulSoup


def validate_html(file: Path) -> list[str]:
    errors = []
    soup = BeautifulSoup(file.read_text(encoding='utf-8'), 'lxml')
    if not soup.find('title'):
        errors.append('Missing <title> element')
    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_files.py <html_file>")
        return
    file = Path(sys.argv[1])
    errors = validate_html(file)
    if errors:
        print('\n'.join(errors))
    else:
        print(f"{file} valid")


if __name__ == "__main__":
    main()
