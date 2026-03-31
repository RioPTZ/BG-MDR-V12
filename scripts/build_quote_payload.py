from __future__ import annotations

import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


def money(v: Decimal) -> str:
    return f"{int(v):,}".replace(',', '.') + ' đ'


def qint(v: Decimal) -> Decimal:
    return v.quantize(Decimal('1'), rounding=ROUND_HALF_UP)


def build_row(item: dict, default_system: str) -> tuple[dict, Decimal, Decimal]:
    code = item['code']
    system = item.get('system') or default_system or 'Standard'
    width_m = Decimal(str(item['width_m']))
    height_m = Decimal(str(item['height_m']))
    qty = Decimal(str(item.get('qty', 1)))
    unit_price = Decimal(str(item['unit_price']))
    discount_pct = Decimal(str(item['discount_pct']))
    note = item.get('note', '')

    bill_h = height_m if height_m >= 1 else Decimal('1')
    area_one = width_m * bill_h
    if area_one < 1:
        area_one = Decimal('1')
    area_total = area_one * qty
    subtotal = qint(area_total * unit_price)
    after = qint(subtotal * (Decimal('100') - discount_pct) / Decimal('100'))

    width_mm = str(qint(width_m * Decimal('1000')))
    height_mm = str(qint(height_m * Decimal('1000')))

    row = {
        'ma_sp': code,
        'he': system,
        'ngang': width_mm,
        'cao': height_mm,
        'sl': str(qty.normalize()),
        'klg': f"{area_total.normalize()} m²",
        'don_gia': money(unit_price),
        'ck': f"{discount_pct.normalize()}%",
        'sau_ck': money(after),
        'ghi_chu': note,
    }
    return row, area_total, after


def main() -> None:
    if len(sys.argv) != 3:
        print('Usage: python3 build_quote_payload.py <input.json> <output.json>')
        raise SystemExit(2)

    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    data = json.loads(src.read_text(encoding='utf-8'))

    default_system = data.get('system') or 'Standard'
    items = data.get('items') or [
        {
            'code': data['code'],
            'system': data.get('system'),
            'width_m': data['width_m'],
            'height_m': data['height_m'],
            'qty': data.get('qty', 1),
            'unit_price': data['unit_price'],
            'discount_pct': data['discount_pct'],
            'note': data.get('note', ''),
        }
    ]

    rows = []
    total_after = Decimal('0')
    total_area = Decimal('0')
    first_code = items[0]['code']
    first_group = items[0].get('group_name') or data.get('group_name', '')
    first_discount = Decimal(str(items[0]['discount_pct']))

    for item in items:
        row, area_total, after = build_row(item, default_system)
        rows.append(row)
        total_area += area_total
        total_after += after

    payload = {
        'title': data.get('title', 'BÁO GIÁ RÈM'),
        'summary': data.get('summary') or f"Mã {first_code} · {first_group} · Hệ {default_system} · Chiết khấu {first_discount}%",
        'infoLine': data.get('infoLine') or f"{len(rows)} dòng · tổng khối lượng tính giá {total_area.normalize()} m².",
        'rows': rows,
        'subtotalText': money(total_after),
        'totalText': money(total_after),
        'footerNote': data.get('footer_note', ''),
    }

    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()
