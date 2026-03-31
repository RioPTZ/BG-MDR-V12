from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CODE_PAT = re.compile(r'\b([A-Z]{1,4}\s*\d{2,5}(?:\s*/\s*\d+)?)\b', re.I)
DIM_PAT_1 = re.compile(r'(?:rộng|ngang|n)\s*[:=]?\s*(\d+[\.,]?\d*)\s*(?:m)?', re.I)
DIM_PAT_2 = re.compile(r'(?:cao|c)\s*[:=]?\s*(\d+[\.,]?\d*)\s*(?:m)?', re.I)
X_PAT = re.compile(r'(\d+[\.,]?\d*)\s*[x×]\s*(\d+[\.,]?\d*)', re.I)
QTY_PAT = re.compile(r'(\d+)\s*(?:bộ|bo|cái|cai)', re.I)
CK_PAT = re.compile(r'(?:chiết\s*khấu|ck)\s*[:=]?\s*(\d+[\.,]?\d*)\s*%?', re.I)
SYS_PAT = re.compile(r'\b(Standard|Slim|Square|Premier|Lumera|Avalon|Vista|Prime|Masteri|Cordless|Top-Down|Day-Night)\b', re.I)


def to_float(s: str | None):
    if not s:
        return None
    return float(s.replace(',', '.'))


def main() -> None:
    if len(sys.argv) != 3:
        print('Usage: python3 chat_to_structured.py <chat.txt> <structured.json>')
        raise SystemExit(2)

    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    text = src.read_text(encoding='utf-8').strip()

    code = None
    m = CODE_PAT.search(text.upper())
    if m:
        code = re.sub(r'\s+', '', m.group(1).upper())

    width = None
    height = None
    mx = X_PAT.search(text)
    if mx:
        width = to_float(mx.group(1))
        height = to_float(mx.group(2))

    if width is None:
        m = DIM_PAT_1.search(text)
        if m:
            width = to_float(m.group(1))
    if height is None:
        m = DIM_PAT_2.search(text)
        if m:
            height = to_float(m.group(1))

    qty = 1
    m = QTY_PAT.search(text)
    if m:
        qty = int(m.group(1))

    discount = None
    m = CK_PAT.search(text)
    if m:
        discount = to_float(m.group(1))

    system = 'Standard'
    m = SYS_PAT.search(text)
    if m:
        system = m.group(1)

    structured = {
        'code': code or '',
        'system': system,
        'width_m': width,
        'height_m': height,
        'qty': qty,
        'discount_pct': discount,
        '_chat_preprocessor': {
            'source': 'raw-chat',
            'rawText': text
        }
    }

    out.write_text(json.dumps(structured, ensure_ascii=False, indent=2), encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()
