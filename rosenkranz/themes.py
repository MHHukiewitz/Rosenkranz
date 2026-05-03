from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from reportlab.lib import colors

ThemeName = Literal["light", "dark"]


@dataclass(frozen=True)
class ThemePalette:
    bg: colors.Color
    panel: colors.Color
    header: colors.Color
    text: colors.Color
    muted: colors.Color
    line: colors.Color
    accent: colors.Color


THEMES: dict[ThemeName, ThemePalette] = {
    "dark": ThemePalette(
        bg=colors.HexColor("#202124"),
        panel=colors.HexColor("#2B2C2F"),
        header=colors.HexColor("#3A3B3F"),
        text=colors.HexColor("#E8E3DA"),
        muted=colors.HexColor("#D1CBC2"),
        line=colors.HexColor("#6F6F72"),
        accent=colors.HexColor("#C9B99A"),
    ),
    "light": ThemePalette(
        bg=colors.HexColor("#F5F3EF"),
        panel=colors.HexColor("#FFFFFF"),
        header=colors.HexColor("#E8E4DC"),
        text=colors.HexColor("#1C1B19"),
        muted=colors.HexColor("#4A4845"),
        line=colors.HexColor("#B8B4AC"),
        accent=colors.HexColor("#7A5C3E"),
    ),
}


def get_theme(name: ThemeName) -> ThemePalette:
    return THEMES[name]
