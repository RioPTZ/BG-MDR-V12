from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    base = Path('/root/.openclaw/workspace/skills/son-home-quote-image/assets')
    roadmap = json.loads((base / 'upgrade-roadmap.json').read_text(encoding='utf-8'))
    status = json.loads((base / 'engine-status.json').read_text(encoding='utf-8'))

    gaps = set(status.get('gaps', []))
    priorities = roadmap.get('priorities', [])

    out = {
        'engine': roadmap['engine'],
        'roadmapVersion': roadmap['roadmapVersion'],
        'recommendedNext': priorities[:3],
        'knownGaps': list(gaps),
        'allPriorities': priorities,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
