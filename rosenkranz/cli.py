from __future__ import annotations

import argparse
from pathlib import Path

from rosenkranz.fonts import register_fonts_for_locale
from rosenkranz.load_locale import load_locale, normalize_lang, require_full_prayers, require_tutorial
from rosenkranz.render import render_pdf
from rosenkranz.themes import ThemeName, get_theme


def default_output_path(lang: str, theme: ThemeName, full: bool, tutorial: bool) -> Path:
    slug = normalize_lang(lang).replace("-", "")
    parts = ["rosenkranz", slug, theme]
    if full:
        parts.append("full")
    if tutorial:
        parts.append("tutorial")
    return Path("_".join(parts) + ".pdf")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Generate a Rosary cheat-sheet PDF (Rosenkranz) in multiple languages.",
    )
    p.add_argument(
        "--lang",
        default="de",
        help="Locale code: de, en, es, fr, pl, ru, ja, ko, zh-cn, pt (default: de)",
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
        help="Output PDF path (default: rosenkranz_<lang>_<theme>.pdf, with _full / _tutorial if set)",
    )
    p.add_argument(
        "--full",
        action="store_true",
        help="Include Our Father and Hail Mary on the main sheet",
    )
    p.add_argument(
        "--tutorial",
        action="store_true",
        help="Prepend an introductory page (what / what you need / purpose)",
    )
    return p


def main() -> None:
    args = build_parser().parse_args()
    lang_norm = normalize_lang(args.lang)
    data = load_locale(args.lang)
    if args.full:
        require_full_prayers(data)
    if args.tutorial:
        require_tutorial(data)
    font_reg, font_bold = register_fonts_for_locale(lang_norm)
    palette = get_theme(args.theme)
    out = Path(args.output) if args.output else default_output_path(args.lang, args.theme, args.full, args.tutorial)
    render_pdf(
        str(out),
        data,
        palette,
        font_reg,
        font_bold,
        full=args.full,
        tutorial=args.tutorial,
    )
