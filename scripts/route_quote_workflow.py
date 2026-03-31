from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        print('Usage: python3 route_quote_workflow.py <routing-input.json>')
        raise SystemExit(2)

    data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    source = data.get('source', 'text')
    lines = int(data.get('lines', 1))
    ambiguity = data.get('ambiguity', 'medium')
    handwriting = bool(data.get('handwriting_likely', False))
    structured_ready = bool(data.get('structured_input_ready', False))
    core_missing = bool(data.get('core_fields_missing', False))

    if core_missing or ambiguity == 'high':
        route = 'ask-back'
    elif structured_ready and ambiguity == 'low':
        route = 'operator-fast-path'
    elif source == 'image' and handwriting:
        route = 'image-handwriting'
    elif source == 'text' and lines > 1 and ambiguity == 'low':
        route = 'text-multi-line'
    elif source == 'text' and lines == 1 and ambiguity == 'low':
        route = 'text-single-line'
    else:
        route = 'review'

    print(json.dumps({'route': route}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
