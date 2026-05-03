# Rosenkranz PDF

Small CLI that builds a **one-page Rosary cheat sheet** (weekday → mystery set, four sets of five decade blurbs, Creed, Fatima prayer, Latin *Salve Regina*, closing prayer). Optional **tutorial page**, **light/dark** themes, and **ten locales**.

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

- **`--lang`**: `de`, `en`, `es`, `fr`, `pl`, `ru`, `ja`, `ko`, `zh-cn`, `pt` (aliases: `zh` → `zh-cn`).
- **`--theme`**: `light` or `dark`.
- **`-o` / `--output`**: output path. If omitted: `rosenkranz_<lang><theme>.pdf`, with `_full` and/or `_tutorial` in the name when those flags are set.
- **`--full`**: adds **Our Father** and **Hail Mary** on the main sheet (for people who want the text in front of them).
- **`--tutorial`**: prepends an **intro page** (what the Rosary is, what you need, what it is for) in the chosen language.

Examples:

```bash
rosenkranz-pdf --lang es --theme dark --full -o rosary_es.pdf
rosenkranz-pdf --lang fr --tutorial --theme light
```

## Fonts (Russian, Japanese, Korean, Chinese)

Built-in PDF fonts do **not** cover Cyrillic or CJK glyphs. For **`ru`**, **`ja`**, **`ko`**, and **`zh-cn`**, install **Noto Sans** TTF/OTF files into either:

- [`rosenkranz/fonts/`](rosenkranz/fonts/) inside this repo (directory may be empty until you add files), or  
- `~/.local/share/rosenkranz/fonts/`, or  
- any directory pointed to by **`ROSENKRANZ_FONT_DIR`**.

Expected file names (Regular + Bold pairs):

| Locale | Regular | Bold |
|--------|---------|------|
| `ru` | `NotoSans-Regular.ttf` | `NotoSans-Bold.ttf` |
| `ja` | `NotoSansJP-Regular.ttf` (or `.otf`) | `NotoSansJP-Bold.ttf` |
| `ko` | `NotoSansKR-Regular.ttf` | `NotoSansKR-Bold.ttf` |
| `zh-cn` | `NotoSansSC-Regular.ttf` | `NotoSansSC-Bold.ttf` |

Download from [Google Fonts](https://fonts.google.com/) or the [noto-fonts](https://github.com/notofonts/noto-fonts) project. Noto fonts are licensed under the **OFL**.

European Latin locales may use the same **Noto Sans** pair for full Unicode coverage (e.g. Polish diacritics); if those files are absent, the tool falls back to Helvetica.

## Legacy script

[`main.py`](main.py) delegates to the same CLI:

```bash
python main.py --lang en --theme dark
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
