from __future__ import annotations

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas as pdfcanvas

from rosenkranz.load_locale import require_tutorial
from rosenkranz.themes import ThemePalette

W, H = A4
MARGIN = 26
MIN_BOTTOM = 30
COL_HASH = "#"


def fill_background(c: pdfcanvas.Canvas, palette: ThemePalette, width: float, height: float) -> None:
    c.setFillColor(palette.bg)
    c.rect(0, 0, width, height, fill=1, stroke=0)


def draw_heading(
    c: pdfcanvas.Canvas,
    text: str,
    y: float,
    palette: ThemePalette,
    margin: float,
    font_bold: str,
) -> float:
    c.setFont(font_bold, 18)
    c.setFillColor(palette.text)
    c.drawString(margin, y, text)
    y -= 14
    c.setStrokeColor(palette.accent)
    c.setLineWidth(0.8)
    c.line(margin, y, W - margin, y)
    return y - 10


def draw_table(
    c: pdfcanvas.Canvas,
    x: float,
    y_top: float,
    col_widths: list[float],
    row_heights: list[float],
    data: list[list[str]],
    palette: ThemePalette,
    font_reg: str,
    font_bold: str,
    font_size: float = 9,
    header_font_size: float = 9.5,
) -> float:
    total_w = sum(col_widths)
    total_h = sum(row_heights)
    c.setFillColor(palette.panel)
    c.rect(x, y_top - total_h, total_w, total_h, fill=1, stroke=0)
    c.setFillColor(palette.header)
    c.rect(x, y_top - row_heights[0], total_w, row_heights[0], fill=1, stroke=0)
    yy = y_top
    for r, row in enumerate(data):
        row_h = row_heights[r]
        xx = x
        for col_idx, cell in enumerate(row):
            cw = col_widths[col_idx]
            c.setStrokeColor(palette.line)
            c.setLineWidth(0.35)
            c.rect(xx, yy - row_h, cw, row_h, fill=0, stroke=1)
            name = font_bold if r == 0 else font_reg
            size = header_font_size if r == 0 else font_size
            color = palette.text if r == 0 else palette.muted
            c.setFont(name, size)
            c.setFillColor(color)
            maxw = cw - 8
            lines = simpleSplit(str(cell), name, size, maxw)
            line_h = size + 1.2
            start_y = yy - 5 - size
            if len(lines) > 1:
                start_y = yy - 4 - size
            for i, line in enumerate(lines[:3]):
                c.drawString(xx + 4, start_y - i * line_h, line)
            xx += cw
        yy -= row_h
    return y_top - total_h


def mystery_table(
    c: pdfcanvas.Canvas,
    x: float,
    y_top: float,
    title: str,
    rows: list[list[str]],
    palette: ThemePalette,
    font_reg: str,
    font_bold: str,
) -> float:
    data = [[COL_HASH, title]] + rows
    return draw_table(
        c,
        x,
        y_top,
        [18, 240],
        [18, 20, 20, 20, 20, 20],
        data,
        palette,
        font_reg,
        font_bold,
        font_size=8.8,
        header_font_size=9.7,
    )


def estimate_box_height(
    title: str,
    body: str,
    box_w: float,
    title_size: float,
    body_size: float,
    leading: float,
    font_bold: str,
    font_reg: str,
) -> float:
    title_lines = simpleSplit(title, font_bold, title_size, box_w - 14)
    body_lines: list[str] = []
    for part in body.split("\n"):
        body_lines.extend(simpleSplit(part, font_reg, body_size, box_w - 14) or [""])
    return 8 + len(title_lines) * (title_size + 1) + 3 + len(body_lines) * leading + 7


def draw_box(
    c: pdfcanvas.Canvas,
    title: str,
    body: str,
    x: float,
    y_top: float,
    box_w: float,
    palette: ThemePalette,
    font_reg: str,
    font_bold: str,
    title_size: float = 9.6,
    body_size: float = 8.4,
    leading: float = 9.4,
) -> float:
    title_lines = simpleSplit(title, font_bold, title_size, box_w - 14)
    body_lines: list[str] = []
    for part in body.split("\n"):
        body_lines.extend(simpleSplit(part, font_reg, body_size, box_w - 14) or [""])
    h = 8 + len(title_lines) * (title_size + 1) + 3 + len(body_lines) * leading + 7
    c.setFillColor(palette.panel)
    c.roundRect(x, y_top - h, box_w, h, 5, fill=1, stroke=0)
    c.setStrokeColor(palette.line)
    c.setLineWidth(0.35)
    c.roundRect(x, y_top - h, box_w, h, 5, fill=0, stroke=1)
    yy = y_top - 8 - title_size
    c.setFillColor(palette.text)
    c.setFont(font_bold, title_size)
    for line in title_lines:
        c.drawString(x + 7, yy, line)
        yy -= title_size + 1
    yy -= 2
    c.setFillColor(palette.muted)
    c.setFont(font_reg, body_size)
    for line in body_lines:
        c.drawString(x + 7, yy, line)
        yy -= leading
    return y_top - h


def ensure_space(
    c: pdfcanvas.Canvas,
    y: float,
    needed: float,
    palette: ThemePalette,
) -> float:
    if y - needed >= MIN_BOTTOM:
        return y
    c.showPage()
    fill_background(c, palette, W, H)
    return H - MARGIN


def measure_tutorial_height(
    tutorial: dict,
    font_reg: str,
    font_bold: str,
    body_pt: float,
    section_heading_pt: float,
    body_width: float,
) -> float:
    title_lines = simpleSplit(tutorial["title"], font_bold, 18, body_width)
    used = len(title_lines) * 20 + 14 + 10 + 10
    for sec in tutorial["sections"]:
        used += len(simpleSplit(sec["heading"], font_bold, section_heading_pt, body_width)) * (
            section_heading_pt + 2
        )
        used += 4
        for part in sec["body"].split("\n"):
            used += len(simpleSplit(part, font_reg, body_pt, body_width) or [""]) * body_pt * 1.15
        used += 12
    return used


def draw_tutorial_page(
    c: pdfcanvas.Canvas,
    tutorial: dict,
    palette: ThemePalette,
    font_reg: str,
    font_bold: str,
) -> None:
    """Tutorial intro; prefers a single A4 page by shrinking body size."""
    fill_background(c, palette, W, H)
    body_width = W - 2 * MARGIN
    usable = H - MARGIN - MIN_BOTTOM
    chosen: tuple[float, float] | None = None
    for body_pt_try in (10.5, 10.0, 9.5, 9.0, 8.5, 8.0, 7.5, 7.0, 6.8):
        section_heading_pt_try = min(body_pt_try + 2.2, 12.0)
        if measure_tutorial_height(
            tutorial, font_reg, font_bold, body_pt_try, section_heading_pt_try, body_width
        ) <= usable:
            chosen = (body_pt_try, section_heading_pt_try)
            break
    if chosen:
        body_pt, section_heading_pt = chosen
        y = H - MARGIN
        y = draw_heading(c, tutorial["title"], y, palette, MARGIN, font_bold)
        y -= 10
        for sec in tutorial["sections"]:
            for line in simpleSplit(sec["heading"], font_bold, section_heading_pt, body_width):
                c.setFont(font_bold, section_heading_pt)
                c.setFillColor(palette.text)
                c.drawString(MARGIN, y, line)
                y -= section_heading_pt + 2
            y -= 4
            c.setFont(font_reg, body_pt)
            c.setFillColor(palette.muted)
            for part in sec["body"].split("\n"):
                for line in simpleSplit(part, font_reg, body_pt, body_width) or [""]:
                    c.drawString(MARGIN, y, line)
                    y -= body_pt * 1.15
            y -= 12
        return
    draw_tutorial_flow(c, tutorial, palette, font_reg, font_bold, 6.8, 9.0, body_width)


def draw_tutorial_flow(
    c: pdfcanvas.Canvas,
    tutorial: dict,
    palette: ThemePalette,
    font_reg: str,
    font_bold: str,
    body_pt: float,
    section_heading_pt: float,
    body_width: float,
) -> None:
    y = H - MARGIN
    y = draw_heading(c, tutorial["title"], y, palette, MARGIN, font_bold)
    y -= 8
    for sec in tutorial["sections"]:
        for line in simpleSplit(sec["heading"], font_bold, section_heading_pt, body_width):
            y = ensure_space(c, y, section_heading_pt + 4, palette)
            c.setFont(font_bold, section_heading_pt)
            c.setFillColor(palette.text)
            c.drawString(MARGIN, y, line)
            y -= section_heading_pt + 2
        y -= 4
        c.setFont(font_reg, body_pt)
        c.setFillColor(palette.muted)
        for part in sec["body"].split("\n"):
            for line in simpleSplit(part, font_reg, body_pt, body_width) or [""]:
                y = ensure_space(c, y, body_pt * 1.2, palette)
                c.drawString(MARGIN, y, line)
                y -= body_pt * 1.15
        y -= 10


def render_pdf(
    output_path: str,
    data: dict,
    palette: ThemePalette,
    font_reg: str,
    font_bold: str,
    *,
    full: bool,
    tutorial: bool,
) -> None:
    c = pdfcanvas.Canvas(output_path, pagesize=A4)
    if tutorial:
        draw_tutorial_page(c, require_tutorial(data), palette, font_reg, font_bold)
        c.showPage()

    fill_background(c, palette, W, H)
    y = H - MARGIN

    y = draw_heading(c, data["title"], y, palette, MARGIN, font_bold)

    tbl = data["table"]
    days_header = [tbl["column_day"], tbl["column_mystery"]]
    day_rows = [[r["days"], r["mystery"]] for r in tbl["rows"]]
    days_data = [days_header] + day_rows
    y = (
        draw_table(
            c,
            MARGIN,
            y,
            [145, 170],
            [17, 17, 17, 17, 17],
            days_data,
            palette,
            font_reg,
            font_bold,
            font_size=9.3,
            header_font_size=9.8,
        )
        - 11
    )

    my = data["mysteries"]
    freuden = [[str(i + 1), t] for i, t in enumerate(my["joyful"]["decades"])]
    schmerz = [[str(i + 1), t] for i, t in enumerate(my["sorrowful"]["decades"])]
    glor = [[str(i + 1), t] for i, t in enumerate(my["glorious"]["decades"])]
    licht = [[str(i + 1), t] for i, t in enumerate(my["luminous"]["decades"])]

    left = MARGIN
    right = W / 2 + 5
    block_y = y
    bottom1 = mystery_table(c, left, block_y, my["joyful"]["label"], freuden, palette, font_reg, font_bold)
    bottom2 = mystery_table(c, right, block_y, my["sorrowful"]["label"], schmerz, palette, font_reg, font_bold)
    block_y2 = min(bottom1, bottom2) - 9
    bottom3 = mystery_table(c, left, block_y2, my["glorious"]["label"], glor, palette, font_reg, font_bold)
    bottom4 = mystery_table(c, right, block_y2, my["luminous"]["label"], licht, palette, font_reg, font_bold)
    y = min(bottom3, bottom4) - 12

    prayers = data["prayers"]
    box_w = W - 2 * MARGIN

    if full:
        pater = prayers["pater_noster"]
        ave = prayers["ave_maria"]
        for title_key, body_key, ts, bs, ld in [
            (pater["title"], pater["text"], 10.0, 8.9, 10.0),
            (ave["title"], ave["text"], 10.0, 8.9, 10.0),
        ]:
            h = estimate_box_height(title_key, body_key, box_w, ts, bs, ld, font_bold, font_reg)
            y = ensure_space(c, y, h + 10, palette)
            y = draw_box(c, title_key, body_key, MARGIN, y, box_w, palette, font_reg, font_bold, ts, bs, ld) - 7

    prayer_boxes = [
        (prayers["creed"]["title"], prayers["creed"]["text"], 10.0, 8.9, 10.1),
        (prayers["fatima"]["title"], prayers["fatima"]["text"], 10.0, 9.2, 10.2),
        (prayers["salve"]["title"], prayers["salve"]["text"], 10.0, 8.9, 10.0),
        (prayers["closing"]["title"], prayers["closing"]["text"], 10.0, 8.9, 10.0),
    ]

    for idx, (ptitle, pbody, ts, bs, ld) in enumerate(prayer_boxes):
        h = estimate_box_height(ptitle, pbody, box_w, ts, bs, ld, font_bold, font_reg)
        gap = 7 if idx < len(prayer_boxes) - 1 else 0
        y = ensure_space(c, y, h + gap + 8, palette)
        y = draw_box(c, ptitle, pbody, MARGIN, y, box_w, palette, font_reg, font_bold, ts, bs, ld) - gap

    c.save()
