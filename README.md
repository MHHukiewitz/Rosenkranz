# Rosenkranz – Rosary Cheat Sheet

CLI that builds a printable **Rosary cheat sheet** (two pages: tutorial, then the compact reference).

## What’s in the PDF

**Page 1 — Tutorial**  
What the Rosary is, what you need, why people pray it, and the **full prayer sequence** (including the three Hail Marys for faith, hope, and charity).

**Page 2 — Cheat sheet**  
Weekday → mystery set and a narrow **prayer-order** column, then **Creed** and **Hail Mary**, the four mystery tables (joyful, sorrowful, glorious, luminous), then **Our Father**, **Glory Be**, Fatima prayer, **Salve Regina**, and the closing Rosary prayer.

**Languages & themes**  
Eleven locales: `de`, `en`, `es`, `fr`, `pl`, `ru`, `pt`, `ja`, `ko`, `zh-cn`, `la`.  
Prayer texts follow each locale; **ecclesiastical Latin** is reserved for **`la`** (including *Salve Regina*). **`light`** and **`dark`** themes.

**Japanese & Chinese layout**  
For **`ja`** and **`zh-cn`**, lines wrap between glyphs (no reliance on spaces). Line spacing is tuned so stacked lines stay readable.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

Requires Python **≥ 3.10** and [ReportLab](https://www.reportlab.com/) **≥ 4** (see [`pyproject.toml`](pyproject.toml)).

## Usage

```bash
rosenkranz-pdf --lang en --theme dark -o rosary.pdf
python -m rosenkranz --lang de --theme light
python -m rosenkranz --lang zh-cn --theme dark -o out/zh.pdf
```

| Option | Meaning |
|--------|---------|
| **`--lang`** | `de` (default), `en`, `es`, `fr`, `pl`, `ru`, `pt`, `ja`, `ko`, `zh-cn`, `la`. Aliases: `zh`, `zh-hans` → `zh-cn`; `pt-br` → `pt`. |
| **`--theme`** | `light` or `dark`. |
| **`-o` / `--output`** | Output path; default `rosenkranz_<lang>_<theme>.pdf` (`zh-cn` → `rosenkranz_zh-cn_…`). |

[`main.py`](main.py) calls the same entry point: `python main.py --lang en --theme dark`.

## Fonts (Cyrillic & CJK)

Helvetica cannot render Cyrillic or CJK. For **`ru`**, **`ja`**, **`ko`**, and **`zh-cn`**, place **Noto Sans** files in one of:

- [`rosenkranz/fonts/`](rosenkranz/fonts/) (often empty in git; add files locally),  
- `~/.local/share/rosenkranz/fonts/`, or  
- a directory set in **`ROSENKRANZ_FONT_DIR`**.

ReportLab’s `TTFont` **does not load** typical **noto-cjk `.otf`** (CFF outlines). Use **variable TTF** or **`.ttf`** subsets instead.

| Locale | Regular | Bold |
|--------|---------|------|
| `ru` | `NotoSans-Regular.ttf` | `NotoSans-Bold.ttf` |
| `ja` | `NotoSansCJKjp-VF.ttf` or `NotoSansJP-Regular.ttf` | bold file or same VF |
| `ko` | `NotoSansCJKkr-VF.ttf` or `NotoSansKR-Regular.ttf` | bold file or same VF |
| `zh-cn` | `NotoSansCJKsc-VF.ttf` or `NotoSansSC-Regular.ttf` | bold file or same VF |

Latin and most European text can use the same **`NotoSans-{Regular,Bold}.ttf`** pair; without them, the tool falls back to Helvetica (fine for many Latin-only locales, not for `ru` / CJK).

Noto fonts are **OFL**-licensed ([Noto](https://github.com/notofonts/noto-fonts), [Noto CJK](https://github.com/notofonts/noto-cjk)).

## Prebuilt PDFs

Ready-made files live under **`dist/<lang>/`**:

- `rosenkranz_<lang>_dark.pdf`
- `rosenkranz_<lang>_light.pdf`

On pushes to **`main`** that change files **outside** `dist/`, [`.github/workflows/build-pdfs.yml`](.github/workflows/build-pdfs.yml) reinstalls the package, downloads Noto (Latin + CJK variable TTFs), rebuilds all PDFs, uploads the **`dist/`** tree as artifact **`rosenkranz-pdfs`**, and commits updates under **`dist/`** with **`[skip ci]`** so that commit does not retrigger the workflow.

## Contributing

Locales live in [`rosenkranz/locales/*.json`](rosenkranz/locales/). See [CONTRIBUTING.md](CONTRIBUTING.md).
