from __future__ import annotations

import json
from pathlib import Path


def locales_dir() -> Path:
    return Path(__file__).resolve().parent / "locales"


def normalize_lang(code: str) -> str:
    c = code.strip().lower().replace("_", "-")
    aliases = {"zh": "zh-cn", "zh_cn": "zh-cn", "zh-hans": "zh-cn", "pt-br": "pt", "pt_pt": "pt"}
    return aliases.get(c, c)


def locale_filename(norm: str) -> str:
    if norm == "zh-cn":
        return "zh-CN.json"
    return f"{norm}.json"


def load_locale(lang_code: str) -> dict:
    norm = normalize_lang(lang_code)
    path = locales_dir() / locale_filename(norm)
    if not path.is_file():
        available = sorted(p.stem for p in locales_dir().glob("*.json"))
        raise SystemExit(f"Unknown locale '{lang_code}'. Available: {', '.join(available)}")
    return json.loads(path.read_text(encoding="utf-8"))


def require_tutorial(data: dict) -> dict:
    tut = data.get("tutorial")
    if not tut or not tut.get("title") or not tut.get("sections"):
        raise SystemExit("This locale file has no 'tutorial' section; cannot use --tutorial.")
    return tut


def require_full_prayers(data: dict) -> tuple[dict, dict]:
    prayers = data.get("prayers") or {}
    pater = prayers.get("pater_noster")
    ave = prayers.get("ave_maria")
    if not pater or not ave:
        raise SystemExit("Locale missing pater_noster or ave_maria; cannot use --full.")
    return pater, ave
