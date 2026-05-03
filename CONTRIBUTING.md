# Contributing

## Translations

All user-visible strings live in [`rosenkranz/locales/`](rosenkranz/locales/) as JSON. Each file must keep the **same keys** so the renderer stays simple.

### Structure

- **`title`**: Main sheet heading.
- **`table`**: `column_day`, `column_mystery`, `rows` (each row: `days`, `mystery`).
- **`mysteries`**: `joyful`, `sorrowful`, `glorious`, `luminous` — each has `label` and `decades` (five strings).
- **`prayers`**: `creed`, `fatima`, `salve`, `closing` (`title` + `text`); optional for PDF unless `--full`: `pater_noster`, `ave_maria`.
- **`tutorial`**: `title` and `sections` (list of `heading` + `body`). Required for `--tutorial` to work.

### Liturgical note

The body of **`prayers.salve`** is kept in **Latin** in every locale; only the box **`title`** is localized.

### Checking your edits

From the repo root, with the venv activated:

```bash
pip install -e .
rosenkranz-pdf --lang <code> --theme dark -o /tmp/check.pdf
rosenkranz-pdf --lang <code> --theme light --full --tutorial -o /tmp/check-all.pdf
```

For `ru` / `ja` / `ko` / `zh-cn`, install Noto fonts first (see [README.md](README.md)).

### Accuracy

Prayer texts and mystery wording touch living faith traditions. Prefer sources recognized by the Catholic Church for your language, and note sources or reviewers in pull requests when possible.
