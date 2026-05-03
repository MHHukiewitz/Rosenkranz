from __future__ import annotations

import argparse
from pathlib import Path

from rosenkranz.fonts import register_fonts_for_locale
from rosenkranz.load_locale import load_locale, normalize_lang
from rosenkranz.render import render_pdf
from rosenkranz.themes import ThemeName, get_theme


def default_output_path(lang: str, theme: ThemeName) -> Path:
    slug = normalize_lang(lang).replace("-", "")
    return Path(f"rosenkranz_{slug}_{theme}.pdf")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Generate a Rosary cheat-sheet PDF (Rosenkranz) in multiple languages.",
    )
    p.add_argument(
        "--lang",
        default="de",
        help="Locale code: de, en, es, fr, pl, ru, ja, ko, zh-cn, pt, la (default: de)",
    )
    p.add_argument(
        "--theme",
        choices=("light", "dark"),
        default="dark",
        help="Color theme (default: dark)",
    )
    p.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output PDF path (default: rosenkranz_<lang>_<theme>.pdf)",
    )
    return p


def main() -> None:
    args = build_parser().parse_args()
    lang_norm = normalize_lang(args.lang)
    data = load_locale(args.lang)
    font_reg, font_bold = register_fonts_for_locale(lang_norm)
    palette = get_theme(args.theme)
    out = Path(args.output) if args.output else default_output_path(args.lang, args.theme)
    render_pdf(str(out), data, palette, font_reg, font_bold, locale_norm=lang_norm)
