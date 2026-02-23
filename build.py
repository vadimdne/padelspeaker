#!/usr/bin/env python3
"""
build.py — Padel Speaker website generator
Reads template.html + translations/*.json → outputs all language pages.
"""

import datetime
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "template.html"
TRANSLATIONS_DIR = ROOT / "translations"

LANGS = ["en", "es", "fr", "sv", "it", "nl", "pt"]


def render(template: str, data: dict) -> str:
    """Replace all {{key}} placeholders with values from data."""
    def replacer(m):
        key = m.group(1)
        return data.get(key, m.group(0))
    return re.sub(r"\{\{(\w+)\}\}", replacer, template)


def build():
    template = TEMPLATE.read_text(encoding="utf-8")

    for lang in LANGS:
        json_path = TRANSLATIONS_DIR / f"{lang}.json"
        if not json_path.exists():
            print(f"  [SKIP] {json_path} not found")
            continue

        data = json.loads(json_path.read_text(encoding="utf-8"))
        data["footer_copy"] = f"© {datetime.date.today().year} Cheese Wheels Apps OU"
        html = render(template, data)

        if lang == "en":
            out_path = ROOT / "index.html"
        else:
            lang_dir = ROOT / lang
            lang_dir.mkdir(exist_ok=True)
            out_path = lang_dir / "index.html"

        out_path.write_text(html, encoding="utf-8")
        print(f"  [OK]   {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    print("Building Padel Speaker website...")
    build()
    print("Done.")
