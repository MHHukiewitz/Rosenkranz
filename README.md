# Rosenkranz - Rosary Cheat Sheet

CLI that builds a **Rosary cheat sheet**: page 1 is a short **tutorial** (what it is, what you need, purpose, **full prayer sequence** including the three Hail Marys for faith, hope, and charity); page 2 has weekday → mystery set, compact **Gebetsfolge**, mystery tables, **Our Father**, **Hail Mary**, **Glory Be** (kleine Doxologie), Creed, Fatima prayer, Latin *Salve Regina*, and closing prayer. **Light/dark** themes and **eleven locales** (including ecclesiastical **Latin** for fun).

## Setup

Use a virtual environment (recommended on macOS/Homebrew Python):

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

Dependency: [ReportLab](https://www.reportlab.com/).

## Usage

```bash
rosenkranz-pdf --lang en --theme dark -o rosary.pdf
python -m rosenkranz --lang de --theme light
```

- **`--lang`**: `de`, `en`, `es`, `fr`, `pl`, `ru`, `ja`, `ko`, `zh-cn`, `pt`, `la` (Latin; aliases: `zh` → `zh-cn`).
- **`--theme`**: `light` or `dark`.
- **`-o` / `--output`**: output path (default: `rosenkranz_<lang>_<theme>.pdf`).

## Fonts (Russian, Japanese, Korean, Chinese)

Built-in PDF fonts do **not** cover Cyrillic or CJK glyphs. For **`ru`**, **`ja`**, **`ko`**, and **`zh-cn`**, install **Noto Sans** files into either:

- [`rosenkranz/fonts/`](rosenkranz/fonts/) inside this repo (directory may be empty until you add files), or  
- `~/.local/share/rosenkranz/fonts/`, or  
- any directory pointed to by **`ROSENKRANZ_FONT_DIR`**.

ReportLab’s `TTFont` loader does **not** support the usual **noto-cjk `.otf`** files (CFF outlines). Prefer the variable **TTF** builds below, or static **`.ttf`** subsets.

Expected names (Regular + Bold pairs; bold may fall back to regular):

| Locale | Regular | Bold |
|--------|---------|------|
| `ru` | `NotoSans-Regular.ttf` | `NotoSans-Bold.ttf` |
| `ja` | `NotoSansCJKjp-VF.ttf` or `NotoSansJP-Regular.ttf` | matching Bold or same VF |
| `ko` | `NotoSansCJKkr-VF.ttf` or `NotoSansKR-Regular.ttf` | matching Bold or same VF |
| `zh-cn` | `NotoSansCJKsc-VF.ttf` or `NotoSansSC-Regular.ttf` | matching Bold or same VF |

CI downloads **`NotoSansCJK{jp,kr,sc}-VF.ttf`** from [noto-cjk `Sans/Variable/TTF`](https://github.com/notofonts/noto-cjk/tree/main/Sans/Variable/TTF). Older **`NotoSansCJK*-Regular.otf`** names remain as fallbacks but often fail at runtime with ReportLab.

Download from [Google Fonts](https://fonts.google.com/) or the [noto-fonts](https://github.com/notofonts/noto-fonts) project. Noto fonts are licensed under the **OFL**.

European Latin locales may use the same **Noto Sans** pair for full Unicode coverage (e.g. Polish diacritics); if those files are absent, the tool falls back to Helvetica.

## Legacy script

[`main.py`](main.py) delegates to the same CLI:

```bash
python main.py --lang en --theme dark
```

## Prebuilt PDFs (CI)

On every push to **`main`** that does not only touch `dist/`, [`.github/workflows/build-pdfs.yml`](.github/workflows/build-pdfs.yml) regenerates PDFs for **all locales**, each in **`dist/<lang>/`**, as **`rosenkranz_<lang>_dark.pdf`** and **`rosenkranz_<lang>_light.pdf`**. Results are committed with **`[skip ci]`** so the job does not run again on that commit. The same folder is also attached as a workflow **artifact** (`rosenkranz-pdfs`).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
