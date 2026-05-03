from __future__ import annotations

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as pdfcanvas

from rosenkranz.load_locale import get_tutorial
from rosenkranz.text_wrap import (
    body_leading,
    locale_uses_unspaced_wrap,
    stacked_line_step,
    tutorial_body_step,
    wrap_paragraph,
)
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
    *,
    unspaced_wrap: bool = False,
    wrap_width: float | None = None,
    heading_size: float = 18,
    line_gap: float = 22,
) -> float:
    mw = wrap_width if wrap_width is not None else W - 2 * margin
    c.setFont(font_bold, heading_size)
    c.setFillColor(palette.text)
    lines = wrap_paragraph(text, font_bold, heading_size, mw, unspaced=unspaced_wrap) or [text]
    yy = y
    for i, line in enumerate(lines):
        c.drawString(margin, yy, line)
        if i + 1 < len(lines):
            yy -= line_gap
    rule_y = yy - 10
    c.setStrokeColor(palette.accent)
    c.setLineWidth(0.8)
    c.line(margin, rule_y, W - margin, rule_y)
    return rule_y - 10


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
    max_cell_lines: int = 3,
    *,
    unspaced_wrap: bool = False,
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
            lines = wrap_paragraph(str(cell), name, size, maxw, unspaced=unspaced_wrap)
            cap = max(1, max_cell_lines)
            lines = lines[:cap]
            if not lines:
                lines = [""]
            line_h = stacked_line_step(size, unspaced_wrap=unspaced_wrap)
            text_h = (len(lines) - 1) * line_h + size
            pad_top = max(0, (row_h - text_h) / 2)
            start_y = yy - pad_top - size
            for i, line in enumerate(lines):
                c.drawString(xx + 4, start_y - i * line_h, line)
            xx += cw
        yy -= row_h
    return y_top - total_h


def measure_prayer_order_row_heights(
    title: str,
    steps: list[str],
    order_w: float,
    font_reg: str,
    font_bold: str,
    header_fs: float,
    body_fs: float,
    max_lines: int,
    budget: float,
    *,
    header_floor: float = 14.5,
    body_floor: float = 10.0,
    unspaced_wrap: bool = False,
) -> tuple[list[float], float, float]:
    """Row heights from wrapped text; shrink fonts until sum fits budget."""
    maxw = order_w - 8
    hfs, bfs = header_fs, body_fs
    heights: list[float] = []
    for _ in range(14):
        heights = []
        line_h_h = stacked_line_step(hfs, unspaced_wrap=unspaced_wrap, gap=1.1)
        line_h_b = stacked_line_step(bfs, unspaced_wrap=unspaced_wrap, gap=1.1)
        ht_lines = wrap_paragraph(title, font_bold, hfs, maxw, unspaced=unspaced_wrap)[:max_lines]
        if not ht_lines:
            ht_lines = [""]
        heights.append(max(header_floor, (len(ht_lines) - 1) * line_h_h + hfs + 6))
        for step in steps:
            sl = wrap_paragraph(str(step), font_reg, bfs, maxw, unspaced=unspaced_wrap)[:max_lines]
            if not sl:
                sl = [""]
            heights.append(max(body_floor, (len(sl) - 1) * line_h_b + bfs + 5))
        total = sum(heights)
        if total <= budget:
            return heights, hfs, bfs
        bfs -= 0.2
        hfs -= 0.15
        if bfs < 7.05:
            break
    return heights, hfs, bfs


def mystery_table(
    c: pdfcanvas.Canvas,
    x: float,
    y_top: float,
    title: str,
    rows: list[list[str]],
    palette: ThemePalette,
    font_reg: str,
    font_bold: str,
    *,
    unspaced_wrap: bool = False,
) -> float:
    data = [[COL_HASH, title]] + rows
    return draw_table(
        c,
        x,
        y_top,
        [15.5, 241.5],
        [12.8, 17.05, 17.05, 17.05, 17.05, 17.05],
        data,
        palette,
        font_reg,
        font_bold,
        font_size=7.95,
        header_font_size=8.55,
        max_cell_lines=3,
        unspaced_wrap=unspaced_wrap,
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
    *,
    unspaced_wrap: bool = False,
) -> float:
    inner = box_w - 14
    title_lines = wrap_paragraph(title, font_bold, title_size, inner, unspaced=unspaced_wrap) or [""]
    body_lines: list[str] = []
    for part in body.split("\n"):
        body_lines.extend(wrap_paragraph(part, font_reg, body_size, inner, unspaced=unspaced_wrap) or [""])
    ld = body_leading(body_size, leading, unspaced_wrap=unspaced_wrap)
    return 8 + len(title_lines) * (title_size + 1) + 3 + len(body_lines) * ld + 7


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
    *,
    unspaced_wrap: bool = False,
) -> float:
    inner = box_w - 14
    title_lines = wrap_paragraph(title, font_bold, title_size, inner, unspaced=unspaced_wrap) or [""]
    body_lines: list[str] = []
    for part in body.split("\n"):
        body_lines.extend(wrap_paragraph(part, font_reg, body_size, inner, unspaced=unspaced_wrap) or [""])
    ld = body_leading(body_size, leading, unspaced_wrap=unspaced_wrap)
    h = 8 + len(title_lines) * (title_size + 1) + 3 + len(body_lines) * ld + 7
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
        yy -= ld
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
    *,
    unspaced_wrap: bool = False,
) -> float:
    title_lines = wrap_paragraph(tutorial["title"], font_bold, 18, body_width, unspaced=unspaced_wrap) or [""]
    used = len(title_lines) * 20 + 14 + 10 + 10
    for sec in tutorial["sections"]:
        used += len(
            wrap_paragraph(sec["heading"], font_bold, section_heading_pt, body_width, unspaced=unspaced_wrap)
            or [""]
        ) * (section_heading_pt + 2)
        used += 4
        body_step = tutorial_body_step(body_pt, unspaced_wrap=unspaced_wrap)
        for part in sec["body"].split("\n"):
            used += len(wrap_paragraph(part, font_reg, body_pt, body_width, unspaced=unspaced_wrap) or [""]) * body_step
        used += 12
    return used


def draw_tutorial_page(
    c: pdfcanvas.Canvas,
    tutorial: dict,
    palette: ThemePalette,
    font_reg: str,
    font_bold: str,
    *,
    unspaced_wrap: bool = False,
) -> None:
    """Tutorial intro; prefers a single A4 page by shrinking body size."""
    fill_background(c, palette, W, H)
    body_width = W - 2 * MARGIN
    usable = H - MARGIN - MIN_BOTTOM
    chosen: tuple[float, float] | None = None
    for body_pt_try in (10.5, 10.0, 9.5, 9.0, 8.5, 8.0, 7.5, 7.0, 6.8):
        section_heading_pt_try = min(body_pt_try + 2.2, 12.0)
        if measure_tutorial_height(
            tutorial,
            font_reg,
            font_bold,
            body_pt_try,
            section_heading_pt_try,
            body_width,
            unspaced_wrap=unspaced_wrap,
        ) <= usable:
            chosen = (body_pt_try, section_heading_pt_try)
            break
    if chosen:
        body_pt, section_heading_pt = chosen
        y = H - MARGIN
        y = draw_heading(
            c, tutorial["title"], y, palette, MARGIN, font_bold, unspaced_wrap=unspaced_wrap, wrap_width=body_width
        )
        y -= 10
        for sec in tutorial["sections"]:
            for line in wrap_paragraph(
                sec["heading"], font_bold, section_heading_pt, body_width, unspaced=unspaced_wrap
            ) or [""]:
                c.setFont(font_bold, section_heading_pt)
                c.setFillColor(palette.text)
                c.drawString(MARGIN, y, line)
                y -= section_heading_pt + 2
            y -= 4
            c.setFont(font_reg, body_pt)
            c.setFillColor(palette.muted)
            body_step = tutorial_body_step(body_pt, unspaced_wrap=unspaced_wrap)
            for part in sec["body"].split("\n"):
                for line in wrap_paragraph(part, font_reg, body_pt, body_width, unspaced=unspaced_wrap) or [""]:
                    c.drawString(MARGIN, y, line)
                    y -= body_step
            y -= 12
        return
    draw_tutorial_flow(
        c, tutorial, palette, font_reg, font_bold, 6.8, 9.0, body_width, unspaced_wrap=unspaced_wrap
    )


def draw_tutorial_flow(
    c: pdfcanvas.Canvas,
    tutorial: dict,
    palette: ThemePalette,
    font_reg: str,
    font_bold: str,
    body_pt: float,
    section_heading_pt: float,
    body_width: float,
    *,
    unspaced_wrap: bool = False,
) -> None:
    y = H - MARGIN
    y = draw_heading(
        c, tutorial["title"], y, palette, MARGIN, font_bold, unspaced_wrap=unspaced_wrap, wrap_width=body_width
    )
    y -= 8
    for sec in tutorial["sections"]:
        for line in wrap_paragraph(
            sec["heading"], font_bold, section_heading_pt, body_width, unspaced=unspaced_wrap
        ) or [""]:
            y = ensure_space(c, y, section_heading_pt + 4, palette)
            c.setFont(font_bold, section_heading_pt)
            c.setFillColor(palette.text)
            c.drawString(MARGIN, y, line)
            y -= section_heading_pt + 2
        y -= 4
        c.setFont(font_reg, body_pt)
        c.setFillColor(palette.muted)
        body_step = tutorial_body_step(body_pt, unspaced_wrap=unspaced_wrap)
        for part in sec["body"].split("\n"):
            for line in wrap_paragraph(part, font_reg, body_pt, body_width, unspaced=unspaced_wrap) or [""]:
                y = ensure_space(c, y, body_step * 1.05, palette)
                c.drawString(MARGIN, y, line)
                y -= body_step
        y -= 10


def render_pdf(
    output_path: str,
    data: dict,
    palette: ThemePalette,
    font_reg: str,
    font_bold: str,
    *,
    locale_norm: str = "de",
) -> None:
    uw = locale_uses_unspaced_wrap(locale_norm)
    c = pdfcanvas.Canvas(output_path, pagesize=A4)
    draw_tutorial_page(c, get_tutorial(data), palette, font_reg, font_bold, unspaced_wrap=uw)
    c.showPage()

    fill_background(c, palette, W, H)
    y = H - MARGIN

    heading_width = W - 2 * MARGIN
    y = draw_heading(c, data["title"], y, palette, MARGIN, font_bold, unspaced_wrap=uw, wrap_width=heading_width)

    tbl = data["table"]
    po = data["prayer_order"]
    days_header = [tbl["column_day"], tbl["column_mystery"]]
    day_rows = [[r["days"], r["mystery"]] for r in tbl["rows"]]
    days_data = [days_header] + day_rows
    day_col_w = [108, 122]
    gap_tables = 8
    days_total_w = sum(day_col_w)
    order_x = MARGIN + days_total_w + gap_tables
    order_w = W - MARGIN - order_x
    row_h = 17
    days_row_heights = [row_h] * 5
    days_total_h = sum(days_row_heights)
    y_top_row = y
    bottom_days = draw_table(
        c,
        MARGIN,
        y_top_row,
        day_col_w,
        days_row_heights,
        days_data,
        palette,
        font_reg,
        font_bold,
        font_size=9.1,
        header_font_size=9.6,
        unspaced_wrap=uw,
    )
    steps = po["steps"]
    order_row_heights, order_hfs, order_bfs = measure_prayer_order_row_heights(
        po["title"],
        steps,
        order_w,
        font_reg,
        font_bold,
        9.35,
        8.05,
        5,
        float(days_total_h),
        unspaced_wrap=uw,
    )
    order_data = [[po["title"]]] + [[s] for s in steps]
    bottom_order = draw_table(
        c,
        order_x,
        y_top_row,
        [order_w],
        order_row_heights,
        order_data,
        palette,
        font_reg,
        font_bold,
        font_size=order_bfs,
        header_font_size=order_hfs,
        max_cell_lines=5,
        unspaced_wrap=uw,
    )
    y = min(bottom_days, bottom_order) - 6

    my = data["mysteries"]
    freuden = [[str(i + 1), t] for i, t in enumerate(my["joyful"]["decades"])]
    schmerz = [[str(i + 1), t] for i, t in enumerate(my["sorrowful"]["decades"])]
    glor = [[str(i + 1), t] for i, t in enumerate(my["glorious"]["decades"])]
    licht = [[str(i + 1), t] for i, t in enumerate(my["luminous"]["decades"])]

    left = MARGIN
    right = W / 2 + 5
    block_y = y
    bottom1 = mystery_table(
        c, left, block_y, my["joyful"]["label"], freuden, palette, font_reg, font_bold, unspaced_wrap=uw
    )
    bottom2 = mystery_table(
        c, right, block_y, my["sorrowful"]["label"], schmerz, palette, font_reg, font_bold, unspaced_wrap=uw
    )
    block_y2 = min(bottom1, bottom2) - 5
    bottom3 = mystery_table(
        c, left, block_y2, my["glorious"]["label"], glor, palette, font_reg, font_bold, unspaced_wrap=uw
    )
    bottom4 = mystery_table(
        c, right, block_y2, my["luminous"]["label"], licht, palette, font_reg, font_bold, unspaced_wrap=uw
    )
    y = min(bottom3, bottom4) - 7

    prayers = data["prayers"]
    box_w = W - 2 * MARGIN

    pater = prayers["pater_noster"]
    ave = prayers["ave_maria"]
    gloria = prayers["gloria"]
    for title_key, body_key, ts, bs, ld in [
        (pater["title"], pater["text"], 9.85, 8.65, 9.55),
        (ave["title"], ave["text"], 9.85, 8.65, 9.55),
        (gloria["title"], gloria["text"], 9.85, 8.65, 9.35),
    ]:
        h = estimate_box_height(title_key, body_key, box_w, ts, bs, ld, font_bold, font_reg, unspaced_wrap=uw)
        y = ensure_space(c, y, h + 8, palette)
        y = (
            draw_box(
                c, title_key, body_key, MARGIN, y, box_w, palette, font_reg, font_bold, ts, bs, ld, unspaced_wrap=uw
            )
            - 5
        )

    prayer_boxes = [
        (prayers["creed"]["title"], prayers["creed"]["text"], 9.85, 8.65, 9.55),
        (prayers["fatima"]["title"], prayers["fatima"]["text"], 9.85, 8.75, 9.65),
        (prayers["salve"]["title"], prayers["salve"]["text"], 9.85, 8.65, 9.45),
        (prayers["closing"]["title"], prayers["closing"]["text"], 9.85, 8.65, 9.45),
    ]

    for idx, (ptitle, pbody, ts, bs, ld) in enumerate(prayer_boxes):
        h = estimate_box_height(ptitle, pbody, box_w, ts, bs, ld, font_bold, font_reg, unspaced_wrap=uw)
        gap = 5 if idx < len(prayer_boxes) - 1 else 0
        y = ensure_space(c, y, h + gap + 6, palette)
        y = draw_box(c, ptitle, pbody, MARGIN, y, box_w, palette, font_reg, font_bold, ts, bs, ld, unspaced_wrap=uw) - gap

    c.save()
