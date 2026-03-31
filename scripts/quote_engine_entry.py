from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run_json(cmd: list[str]) -> dict:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def main() -> None:
    if len(sys.argv) not in {3, 4}:
        print('Usage: python3 quote_engine_entry.py <routing-input.json> <output-base-name> [structured-input.json]')
        raise SystemExit(2)

    routing_input = Path(sys.argv[1]).resolve()
    output_base = sys.argv[2]
    structured_input = Path(sys.argv[3]).resolve() if len(sys.argv) == 4 else None

    router = Path('/root/.openclaw/workspace/skills/son-home-quote-image/scripts/route_quote_workflow.py')
    operator = Path('/root/.openclaw/workspace/skills/son-home-quote-image/scripts/quote_operator.py')

    route_result = run_json(['python3', str(router), str(routing_input)])
    route = route_result['route']

    out = {
        'route': route,
        'executed': False,
    }

    if route == 'operator-fast-path':
        if structured_input is None:
            out['error'] = 'structured input required for operator-fast-path'
            print(json.dumps(out, ensure_ascii=False, indent=2))
            raise SystemExit(1)
        op_result = run_json(['python3', str(operator), str(structured_input), output_base])
        out['executed'] = True
        out['result'] = op_result

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
