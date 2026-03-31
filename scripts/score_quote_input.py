from __future__ import annotations

import json
import sys
from pathlib import Path

CORE = ['code', 'width', 'height', 'qty']


def norm_level(v: str) -> str:
    v = (v or '').strip().lower()
    if v in {'high', 'medium', 'low'}:
        return v
    return 'low'


def main() -> None:
    if len(sys.argv) != 2:
        print('Usage: python3 score_quote_input.py <confidence.json>')
        raise SystemExit(2)

    data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    fields = data.get('fields', {})
    levels = {k: norm_level(fields.get(k, 'low')) for k in ['code', 'width', 'height', 'qty', 'system', 'note']}

    core_bad = [k for k in CORE if levels[k] == 'low']
    core_medium = [k for k in CORE if levels[k] == 'medium']

    if not core_bad and len(core_medium) <= 1:
        decision = 'finalize'
    elif core_bad:
        decision = 'ask'
    else:
        decision = 'review'

    print(json.dumps({'levels': levels, 'decision': decision}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
