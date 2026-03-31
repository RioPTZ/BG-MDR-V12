from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_ROW_KEYS = [
    'ma_sp', 'he', 'ngang', 'cao', 'sl', 'klg', 'don_gia', 'ck', 'sau_ck', 'ghi_chu'
]


def fail(msg: str) -> None:
    print(f'INVALID: {msg}')
    raise SystemExit(1)


def main() -> None:
    if len(sys.argv) != 2:
        print('Usage: python3 validate_quote_payload.py <payload.json>')
        raise SystemExit(2)

    path = Path(sys.argv[1])
    if not path.exists():
        fail('payload file not found')

    data = json.loads(path.read_text(encoding='utf-8'))

    if 'rows' not in data or not isinstance(data['rows'], list) or not data['rows']:
        fail('rows must be a non-empty list')

    for idx, row in enumerate(data['rows'], start=1):
        for key in REQUIRED_ROW_KEYS:
            if key not in row:
                fail(f'row {idx} missing key: {key}')
        if not str(row['sau_ck']).strip():
            fail(f'row {idx} has blank sau_ck')

    if not str(data.get('totalText', '')).strip():
        fail('totalText must not be blank')

    if not str(data.get('subtotalText', '')).strip():
        fail('subtotalText must not be blank')

    print('VALID')


if __name__ == '__main__':
    main()
