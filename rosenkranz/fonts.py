from __future__ import annotations

import os
from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

REGULAR_NAME = "RosKr-Regular"
BOLD_NAME = "RosKr-Bold"

LOCALE_SCRIPT_GROUPS = {
    "ja": "cjk",
    "ko": "cjk",
    "zh-cn": "cjk",
    "ru": "cyrillic",
}

_CANDIDATES = {
    "cjk_ja": [
        ("NotoSansJP-Regular.otf", "NotoSansJP-Bold.otf"),
        ("NotoSansJP-Regular.ttf", "NotoSansJP-Bold.ttf"),
    ],
    "cjk_ko": [
        ("NotoSansKR-Regular.otf", "NotoSansKR-Bold.otf"),
        ("NotoSansKR-Regular.ttf", "NotoSansKR-Bold.ttf"),
    ],
    "cjk_zh": [
        ("NotoSansSC-Regular.otf", "NotoSansSC-Bold.otf"),
        ("NotoSansSC-Regular.ttf", "NotoSansSC-Bold.ttf"),
    ],
    "latin": [
        ("NotoSans-Regular.ttf", "NotoSans-Bold.ttf"),
        ("NotoSans-Regular.otf", "NotoSans-Bold.otf"),
    ],
}


def _font_search_roots() -> list[Path]:
    roots: list[Path] = []
    env = os.environ.get("ROSENKRANZ_FONT_DIR", "").strip()
    if env:
        roots.append(Path(env))
    roots.append(Path(__file__).resolve().parent / "fonts")
    roots.append(Path.home() / ".local" / "share" / "rosenkranz" / "fonts")
    return roots


def _find_pair(reg_file: str, bold_file: str) -> tuple[Path | None, Path | None]:
    for root in _font_search_roots():
        if not root.is_dir():
            continue
        reg = root / reg_file
        bold = root / bold_file
        if reg.is_file():
            bold_path = bold if bold.is_file() else None
            return reg, bold_path
    return None, None


def _pick_candidates(locale_norm: str) -> list[tuple[str, str]]:
    if locale_norm == "ja":
        return _CANDIDATES["cjk_ja"]
    if locale_norm == "ko":
        return _CANDIDATES["cjk_ko"]
    if locale_norm == "zh-cn":
        return _CANDIDATES["cjk_zh"]
    out = list(_CANDIDATES["latin"])
    return out


def register_fonts_for_locale(locale_norm: str) -> tuple[str, str]:
    """Register TrueType/OpenType fonts and return (regular_font_name, bold_font_name)."""
    group = LOCALE_SCRIPT_GROUPS.get(locale_norm)
    candidates = _pick_candidates(locale_norm)
    reg_path: Path | None = None
    bold_path: Path | None = None
    for reg_file, bold_file in candidates:
        reg_path, bold_path = _find_pair(reg_file, bold_file)
        if reg_path:
            break
    if group == "cjk" or group == "cyrillic":
        if reg_path is None:
            msg = (
                f"No font files found for locale '{locale_norm}'. "
                f"Install Noto Sans (see README) under one of: "
                + ", ".join(str(p) for p in _font_search_roots())
            )
            raise SystemExit(msg)
        pdfmetrics.registerFont(TTFont(REGULAR_NAME, str(reg_path)))
        if bold_path:
            pdfmetrics.registerFont(TTFont(BOLD_NAME, str(bold_path)))
        else:
            pdfmetrics.registerFont(TTFont(BOLD_NAME, str(reg_path)))
        return REGULAR_NAME, BOLD_NAME
    if reg_path:
        pdfmetrics.registerFont(TTFont(REGULAR_NAME, str(reg_path)))
        if bold_path:
            pdfmetrics.registerFont(TTFont(BOLD_NAME, str(bold_path)))
        else:
            pdfmetrics.registerFont(TTFont(BOLD_NAME, str(reg_path)))
        return REGULAR_NAME, BOLD_NAME
    return "Helvetica", "Helvetica-Bold"
