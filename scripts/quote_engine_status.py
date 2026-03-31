from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    base = Path('/root/.openclaw/workspace/skills/son-home-quote-image/assets')
    engine_status = json.loads((base / 'engine-status.json').read_text(encoding='utf-8'))
    workflow = json.loads((base / 'workflow-version.json').read_text(encoding='utf-8'))

    out = {
        'engine': engine_status['engine'],
        'engineVersion': engine_status['version'],
        'workflowVersion': workflow['version'],
        'phase': workflow['phase'],
        'phasesCompleted': engine_status['phasesCompleted'],
        'capabilities': engine_status['capabilities'],
        'routes': engine_status['routes'],
        'gaps': engine_status['gaps'],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
