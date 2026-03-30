from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

from PIL import Image, ImageDraw, ImageFont

W = 1600
BG = "#F8FCF9"
HEADER = "#EEF8F1"
HEADER_BORDER = "#DBECE0"
TABLE_HEAD = "#EDF7F0"
LINE = "#DFECE3"
TEXT = "#24312A"
SUBTLE = "#7D9186"
WHITE = "#FFFFFF"
ACCENT = "#CFE8D8"
ACCENT_BORDER = "#BFDCCB"
TOTAL_BG = "#D8ECDF"
TOTAL_BORDER = "#C7E1D1"

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size: int, bold: bool = False):
    path = FONT_BOLD if bold and Path(FONT_BOLD).exists() else FONT_REG
    if not Path(path).exists():
        return ImageFont.load_default()
    return ImageFont.truetype(path, size=size)


@dataclass
class Row:
    ma_sp: str
    he: str
    ngang: str
    cao: str
    sl: str
    klg: str
    don_gia: str
    ck: str
    sau_ck: str
    ghi_chu: str = ""


def text(draw, xy, s, f, fill=TEXT, anchor=None):
    draw.text(xy, s, font=f, fill=fill, anchor=anchor)


def rounded(draw, box, r, fill, outline=None, width=2):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def load_payload(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = [Row(**r) for r in data["rows"]]
    data["rows"] = rows
    return data


def row_height(row: Row) -> int:
    extra = max(len(row.ghi_chu) // 26, 0)
    return 64 + extra * 18


def render(data: dict, out_path: Path):
    rows: List[Row] = data["rows"]
    top = 48
    margin = 56
    header_h = 160
    summary_h = 66
    table_header_h = 54
    rows_h = sum(row_height(r) for r in rows)
    subtotal_h = 62
    total_h = 122
    bottom = 54
    H = top + header_h + 18 + summary_h + 26 + table_header_h + rows_h + subtotal_h + 28 + total_h + bottom

    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    f_title = font(42, True)
    f_summary = font(24, False)
    f_head = font(22, True)
    f_cell = font(21, False)
    f_cell_b = font(21, True)
    f_total = font(24, True)
    f_total_big = font(36, True)
    f_small = font(19, False)

    rounded(draw, (margin, top, W - margin, top + header_h), 28, HEADER, HEADER_BORDER, 3)
    text(draw, (margin + 30, top + 34), data.get("title", "BẢNG BÁO GIÁ"), f_title)
    text(draw, (margin + 30, top + 95), data.get("summary", "Bảng báo giá theo form chuẩn đã chốt"), f_summary, SUBTLE)

    sy = top + header_h + 18
    rounded(draw, (margin, sy, W - margin, sy + summary_h), 20, WHITE, HEADER_BORDER, 2)
    info = data.get("infoLine", "Báo giá được trình bày theo form chuẩn, rõ cột, dễ đọc.")
    text(draw, (margin + 24, sy + 18), info, f_summary)

    ty = sy + summary_h + 26
    cols = [
        ("Mã SP", 140),
        ("Hệ", 150),
        ("Ngang", 110),
        ("Cao", 110),
        ("SL", 80),
        ("K/lg", 120),
        ("Đơn giá", 175),
        ("CK", 90),
        ("Sau CK", 195),
        ("Ghi chú", 262),
    ]

    rounded(draw, (margin, ty, W - margin, ty + table_header_h), 14, TABLE_HEAD, LINE, 2)
    x = margin
    for name, width in cols:
        draw.line((x, ty, x, ty + table_header_h), fill=LINE, width=2)
        text(draw, (x + width / 2, ty + table_header_h / 2), name, f_head, anchor="mm")
        x += width
    draw.line((W - margin, ty, W - margin, ty + table_header_h), fill=LINE, width=2)

    cy = ty + table_header_h
    for r in rows:
        rh = row_height(r)
        draw.rectangle((margin, cy, W - margin, cy + rh), fill=WHITE, outline=LINE, width=2)
        x = margin
        vals = [r.ma_sp, r.he, r.ngang, r.cao, r.sl, r.klg, r.don_gia, r.ck, r.sau_ck, r.ghi_chu]
        for i, ((_, width), val) in enumerate(zip(cols, vals)):
            draw.line((x, cy, x, cy + rh), fill=LINE, width=2)
            if i != 9:
                text(draw, (x + width / 2, cy + rh / 2), str(val), f_cell if i not in (0, 8) else f_cell_b, anchor="mm")
            else:
                text(draw, (x + 14, cy + 18), str(val), f_small)
            x += width
        draw.line((W - margin, cy, W - margin, cy + rh), fill=LINE, width=2)
        cy += rh

    rh = subtotal_h
    draw.rectangle((margin, cy, W - margin, cy + rh), fill="#F9FCFF", outline=LINE, width=2)
    merge_w = cols[0][1] + cols[1][1]
    text(draw, (margin + merge_w / 2, cy + rh / 2), "Cộng tiền hàng", f_head, anchor="mm")

    x = margin + merge_w
    remainder = cols[2:]
    vals = ["", "", "", "", "", "", data.get("subtotalText", data.get("totalText", "")), ""]
    for (_, width), val in zip(remainder, vals):
        draw.line((x, cy, x, cy + rh), fill=LINE, width=2)
        if val:
            text(draw, (x + width / 2, cy + rh / 2), str(val), f_cell_b, anchor="mm")
        x += width
    draw.line((W - margin, cy, W - margin, cy + rh), fill=LINE, width=2)

    by = cy + rh + 28
    rounded(draw, (margin, by, W - margin, by + total_h), 24, TOTAL_BG, TOTAL_BORDER, 3)
    text(draw, (margin + 28, by + 22), "THÀNH TIỀN SAU CHIẾT KHẤU", f_total)
    text(draw, (W - margin - 28, by + 66), data.get("totalText", ""), f_total_big, anchor="ra")
    note = data.get("footerNote", "Form mặc định: bảng rõ cột, subtotal lấy từ cột Sau CK, phối màu mint pastel.")
    text(draw, (margin + 28, by + 86), note, f_small, SUBTLE)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    return out_path


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python3 scripts/render_quote_card.py <input.json> <output.png>")
        raise SystemExit(2)
    data = load_payload(Path(sys.argv[1]))
    out = render(data, Path(sys.argv[2]))
    print(out)
