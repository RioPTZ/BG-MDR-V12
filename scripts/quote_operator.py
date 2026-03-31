from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    if len(sys.argv) not in {3, 4}:
        print('Usage: python3 quote_operator.py <structured-input.json> <output-base-name> [defaults.json]')
        raise SystemExit(2)

    structured_input = Path(sys.argv[1]).resolve()
    base = sys.argv[2]
    defaults = Path(sys.argv[3]).resolve() if len(sys.argv) == 4 else Path('/root/.openclaw/workspace/skills/son-home-quote-image/assets/operator/defaults.json')

    cfg = json.loads(defaults.read_text(encoding='utf-8'))
    out_dir = Path(cfg['outputDir']).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = out_dir / f'{base}.json'
    image = out_dir / f'{base}.png'

    build_script = Path('/root/.openclaw/workspace/skills/son-home-quote-image/scripts/build_quote_payload.py')
    validate_script = Path('/root/.openclaw/workspace/skills/son-home-quote-image/scripts/validate_quote_payload.py')
    render_script = Path(cfg['rendererScript']).resolve()

    run(['python3', str(build_script), str(structured_input), str(payload)])
    run(['python3', str(validate_script), str(payload)])
    run(['python3', str(render_script), str(payload), str(image)])

    result = {
        'payload': str(payload),
        'image': str(image),
        'workflowVersion': cfg.get('activeWorkflowVersion'),
        'directDeliveryPreferred': cfg.get('directDeliveryPreferred', True),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
