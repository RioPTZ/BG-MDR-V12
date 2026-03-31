from __future__ import annotations

import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


def money(v: Decimal) -> str:
    return f"{int(v):,}".replace(',', '.') + ' đ'


def qint(v: Decimal) -> Decimal:
    return v.quantize(Decimal('1'), rounding=ROUND_HALF_UP)


def main() -> None:
    if len(sys.argv) != 3:
        print('Usage: python3 build_quote_payload.py <input.json> <output.json>')
        raise SystemExit(2)

    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    data = json.loads(src.read_text(encoding='utf-8'))

    code = data['code']
    system = data.get('system') or 'Standard'
    width_m = Decimal(str(data['width_m']))
    height_m = Decimal(str(data['height_m']))
    qty = Decimal(str(data.get('qty', 1)))
    unit_price = Decimal(str(data['unit_price']))
    discount_pct = Decimal(str(data['discount_pct']))
    group_name = data.get('group_name', '')
    note = data.get('note', '')
    footer_note = data.get('footer_note', '')

    bill_h = height_m if height_m >= 1 else Decimal('1')
    area_one = width_m * bill_h
    if area_one < 1:
        area_one = Decimal('1')
    area_total = area_one * qty
    subtotal = qint(area_total * unit_price)
    after = qint(subtotal * (Decimal('100') - discount_pct) / Decimal('100'))

    width_mm = str(qint(width_m * Decimal('1000')))
    height_mm = str(qint(height_m * Decimal('1000')))

    payload = {
        'title': data.get('title', 'BÁO GIÁ RÈM'),
        'summary': data.get('summary') or f"Mã {code} · {group_name} · Hệ {system} · Chiết khấu {discount_pct}%",
        'infoLine': data.get('infoLine') or f"Khổ thực tế {width_mm} x {height_mm} mm · {qty} bộ · tính giá theo {area_total.normalize()} m².",
        'rows': [
            {
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
        ],
        'subtotalText': money(after),
        'totalText': money(after),
        'footerNote': footer_note,
    }

    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()
