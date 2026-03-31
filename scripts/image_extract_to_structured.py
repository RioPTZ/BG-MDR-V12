from __future__ import annotations

import json
import sys
from pathlib import Path


def parse_num(v, default=None):
    if v is None:
        return default
    if isinstance(v, (int, float)):
        return v
    s = str(v).strip().replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return default


def main() -> None:
    if len(sys.argv) != 3:
        print('Usage: python3 image_extract_to_structured.py <extraction.json> <structured-output.json>')
        raise SystemExit(2)

    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    data = json.loads(src.read_text(encoding='utf-8'))

    structured = {
        'code': data.get('code') or data.get('ma') or '',
        'system': data.get('system') or 'Standard',
        'width_m': parse_num(data.get('width_m', data.get('ngang_m', data.get('width')))),
        'height_m': parse_num(data.get('height_m', data.get('cao_m', data.get('height')))),
        'qty': parse_num(data.get('qty', data.get('sl')), 1),
        'discount_pct': parse_num(data.get('discount_pct', data.get('ck'))),
        'note': data.get('note', data.get('ghi_chu', '')),
        'group_name': data.get('group_name', ''),
        'workbook_path': data.get('workbook_path', ''),
        '_bridge': {
            'source': 'image-extraction',
            'requiresReview': bool(data.get('requires_review', False))
        }
    }

    out.write_text(json.dumps(structured, ensure_ascii=False, indent=2), encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()
