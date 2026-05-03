"""Line wrapping for PDF text: ReportLab ``simpleSplit`` only breaks on spaces."""

from __future__ import annotations

from reportlab.lib.textsplit import dumbSplit, getCharWidths
from reportlab.lib.utils import simpleSplit

# Locales where body text is mostly unspaced (Han/Kana). ``simpleSplit`` leaves one long line.
# Korean is omitted: hangul text usually contains spaces; unspaced glyph-splitting breaks Latin badly.
LOCALES_UNSPACED_WRAP = frozenset({"ja", "zh-cn"})


def locale_uses_unspaced_wrap(locale_norm: str) -> bool:
    return locale_norm in LOCALES_UNSPACED_WRAP


def body_leading(body_size: float, leading: float, *, unspaced_wrap: bool) -> float:
    """CJK fonts need more baseline gap than Latin or adjacent lines look merged."""
    if not unspaced_wrap:
        return leading
    return max(leading, body_size + 3.0)


def tutorial_body_step(body_pt: float, *, unspaced_wrap: bool) -> float:
    step = body_pt * 1.15
    if unspaced_wrap:
        step = max(step, body_pt + 3.0)
    return step


def stacked_line_step(font_size: float, *, unspaced_wrap: bool = False, gap: float = 1.12) -> float:
    """Vertical distance between baselines for stacked wrapped lines in tables."""
    lh = font_size + gap
    if unspaced_wrap:
        lh = max(lh, font_size + 3.0)
    return lh


def wrap_paragraph(
    text: str,
    font_name: str,
    font_size: float,
    max_width: float,
    *,
    unspaced: bool,
) -> list[str]:
    """Wrap a single paragraph (no embedded newlines) to fit ``max_width``."""
    if not unspaced:
        return simpleSplit(text, font_name, font_size, max_width)
    if not text:
        return []
    # Slightly narrow: VF metrics vs PDF drawing can disagree by a fraction of a point.
    eff_w = max(1.0, float(max_width) - 2.0)
    widths = getCharWidths(text, font_name, font_size)
    rows = dumbSplit(text, widths, eff_w)
    lines = [frag.strip() for (_, frag) in rows if frag.strip()]
    return lines
