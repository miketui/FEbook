# FEbook

This repository contains EPUB source files and scripts for processing them.

## Combining XHTML chapters

Run `python3 combine_xhtml_to_docx.py` to build `manuscript.docx` from the numbered XHTML files in `OEBPS/`. The script strips HTML tags, concatenates the chapter text with page breaks, and relies on Pandoc to create the DOCX. Ensure you have run `setup_environment.sh` so that Pandoc is installed.

If you prefer a plain-text result, run `python3 combine_xhtml_to_markdown.py` to generate `manuscript.md`. This script merges the same XHTML chapters into a Markdown file, inserting `\newpage` markers between chapters.
