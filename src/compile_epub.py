"""Assemble an EPUB from validated HTML files."""
import sys
from pathlib import Path
from ebooklib import epub


def compile_epub(output_path: Path, html_files: list[Path], metadata: dict):
    book = epub.EpubBook()
    book.set_identifier(metadata.get('id', 'id'))
    book.set_title(metadata.get('title', 'Untitled'))
    book.set_language(metadata.get('language', 'en'))

    for html_file in html_files:
        chapter = epub.EpubHtml(title=html_file.stem, file_name=html_file.name)
        # Use raw bytes to avoid lxml parser errors with XML declarations
        chapter.content = html_file.read_bytes()
        book.add_item(chapter)

    book.toc = [epub.Link(f.name, f.stem, f.stem) for f in html_files]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(str(output_path), book)
    print(f"EPUB written to {output_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python compile_epub.py <output_epub> <html_files...>")
        return
    output = Path(sys.argv[1])
    html_files = [Path(p) for p in sys.argv[2:]]
    compile_epub(output, html_files, {'title': 'My Book'})


if __name__ == "__main__":
    main()
