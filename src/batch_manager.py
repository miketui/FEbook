import json
import re
import sys
from pathlib import Path
from typing import Tuple

from bs4 import BeautifulSoup

TEMPLATE_FILE = Path('templates/chapter_template.xhtml')
RAW_DIR = Path('blue')
OUTPUT_DIR = Path('output')
EXTRACT_DIR = OUTPUT_DIR / 'extracted'
STRUCTURED_DIR = OUTPUT_DIR / 'structured'
CLEAN_DIR = OUTPUT_DIR / 'clean'

# Mapping of source filenames to target word counts
WORD_COUNTS = {
    '9-Chapter-I-Unveiling-Your-Creative-Odyssey.xhtml': 4097,
    '10-Chapter-II-Refining-Your-Creative-Toolkit.xhtml': 3339,
    '11-Chapter-III-Reigniting-Your-Creative-Fire.xhtml': 2574,
    '13-Chapter-IV-The-Art-of-Networking-in-Freelance-Hairstyling.xhtml': 4541,
    '14-Chapter-V-Cultivating-Creative-Excellence-Through-Mentorship.xhtml': 5365,
    '15-Chapter-VI-Mastering-the-Business-of-Hairstyling.xhtml': 4637,
    '16-Chapter-VII-Embracing-Wellness-and-Self-Care.xhtml': 4710,
    '17-Chapter-VIII-Advancing-Skills-Through-Continuous-Education.xhtml': 5872,
    '19-Chapter-IX-Stepping-Into-Leadership.xhtml': 5439,
    '20-Chapter-X-Crafting-Enduring-Legacies.xhtml': 5968,
    '21-Chapter-XI-Advanced-Digital-Strategies-for-Freelance-Hairstylists.xhtml': 5592,
    '22-Chapter-XII-Financial-Wisdom-Building-Sustainable-Ventures.xhtml': 5545,
    '23-Chapter-XIII-Embracing-Ethics-and-Sustainability-in-Hairstyling.xhtml': 6740,
    '25-Chapter-XIV-The-Impact-of-AI-on-the-Beauty-Industry.xhtml': 6095,
    '26-Chapter-XV-Cultivating-Resilience-and-Well-Being-in-Hairstyling.xhtml': 3948,
    '27-Chapter-XVI-Tresses-and-Textures-Embracing-Diversity-in-Hairstyling.xhtml': 3806,
}

SVG_PATTERN = re.compile(r'<svg[\s\S]*?</svg>|</?(?:path|circle|rect)[^>]*>', re.IGNORECASE)


def extract_text(chapter_file: Path) -> Tuple[Path, Path]:
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    soup = BeautifulSoup(chapter_file.read_text(encoding='utf-8'), 'lxml')
    text = soup.get_text(separator=' ')
    txt_path = EXTRACT_DIR / f'{chapter_file.stem}.txt'
    json_path = EXTRACT_DIR / f'{chapter_file.stem}.json'
    txt_path.write_text(text, encoding='utf-8')
    json_path.write_text(json.dumps({'source_word_count': len(text.split())}, indent=2), encoding='utf-8')
    return txt_path, json_path


def build_structure(raw_txt: Path, output_file: Path) -> Path:
    STRUCTURED_DIR.mkdir(parents=True, exist_ok=True)
    template = TEMPLATE_FILE.read_text(encoding='utf-8')
    content = raw_txt.read_text(encoding='utf-8')
    html = template.replace('{{CONTENT}}', content)
    output_file.write_text(html, encoding='utf-8')
    return output_file


def remove_svg(html_file: Path) -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    html = html_file.read_text(encoding='utf-8')
    cleaned = SVG_PATTERN.sub('', html)
    cleaned_file = CLEAN_DIR / html_file.name
    cleaned_file.write_text(cleaned, encoding='utf-8')


def qa_check(cleaned_file: Path, raw_txt: Path, expected_words: int) -> Tuple[bool, list]:
    errors = []
    soup = BeautifulSoup(cleaned_file.read_text(encoding='utf-8'), 'lxml')
    if soup.find('svg'):
        errors.append('SVG element found')
    text = soup.get_text(separator=' ').split()
    if len(text) != expected_words:
        errors.append(f'Word count mismatch: expected {expected_words}, got {len(text)}')
    raw_text = raw_txt.read_text(encoding='utf-8').split()
    if text[: len(raw_text)] != raw_text:
        errors.append('Content mismatch with source')
    return not errors, errors


def process_chapter(chapter_filename: str) -> None:
    source_file = RAW_DIR / chapter_filename
    if not source_file.exists():
        print(f'Source not found: {source_file}')
        return
    raw_txt, raw_json = extract_text(source_file)
    structured = STRUCTURED_DIR / chapter_filename
    build_structure(raw_txt, structured)
    remove_svg(structured)
    cleaned_file = CLEAN_DIR / chapter_filename
    expected = WORD_COUNTS.get(chapter_filename, 0)
    success, errs = qa_check(cleaned_file, raw_txt, expected)
    report = CLEAN_DIR / f'{chapter_filename}.report.json'
    report.write_text(json.dumps({'status': 'SUCCESS' if success else 'FAILURE', 'errors': errs}, indent=2), encoding='utf-8')
    if success:
        print(f'{chapter_filename} processed successfully')
    else:
        print(f'QA failed for {chapter_filename}: {errs}')


def main():
    RAW_DIR.mkdir(exist_ok=True)
    chapters = list(WORD_COUNTS.keys())
    for chapter in chapters:
        process_chapter(chapter)


if __name__ == '__main__':
    main()
