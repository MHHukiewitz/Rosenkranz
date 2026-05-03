# Contributing

New and corrected translations are welcome!

## Translations

All user-visible strings live in [`rosenkranz/locales/`](rosenkranz/locales/) as JSON. Each file must keep the **same keys** so the renderer stays simple.

### Structure

- **`title`**: Main sheet heading.
- **`table`**: `column_day`, `column_mystery`, `rows` (each row: `days`, `mystery`).
- **`prayer_order`**: `title` and `steps` (compact sequence on the main sheet: cross, creed, **three Hail Marys** for faith/hope/charity, five decades pattern, Salve, closing).
- **`mysteries`**: `joyful`, `sorrowful`, `glorious`, `luminous` — each has `label` and `decades` (five strings).
- **`prayers`**: always includes `pater_noster`, `ave_maria`, `gloria` (Gloria Patri / „Ehre sei …“), `creed`, `fatima`, `salve`, `closing` (`title` + `text` each).
- **`tutorial`**: `title` and `sections` (list of `heading` + `body`). Always printed as PDF page 1; include a section with the **detailed prayer sequence** (cross, creed, three Hail Marys for faith/hope/charity, decades, Salve, closing).


### Checking your edits

Locale **`la`** is ecclesiastical Latin end-to-end (including tutorial), mostly for fun; keep keys aligned with other JSON files.

From the repo root, with the venv activated:

```bash
pip install -e .
rosenkranz-pdf --lang <code> --theme dark -o /tmp/check.pdf
rosenkranz-pdf --lang <code> --theme light -o /tmp/check-light.pdf
```

For `ru` / `ja` / `ko` / `zh-cn`, install Noto fonts first (see [README.md](README.md)).

### Accuracy

Prayer texts and mystery wording touch living faith traditions. Prefer sources recognized by the Catholic Church for your language, and note sources or reviewers in pull requests when possible.

Currently, accuracy can only be guaranteed for the German translation, as the other are generated with AI.
