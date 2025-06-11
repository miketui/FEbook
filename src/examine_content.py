"""Analyze raw text files for potential issues."""
import sys
from pathlib import Path


def examine_directory(input_dir: Path) -> None:
    for file in input_dir.glob('*.txt'):
        text = file.read_text(encoding='utf-8')
        word_count = len(text.split())
        print(f"File: {file.name} -> {word_count} words")


def main():
    if len(sys.argv) < 2:
        print("Usage: python examine_content.py <input_dir>")
        return
    examine_directory(Path(sys.argv[1]))


if __name__ == "__main__":
    main()
