from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)


def run_json(cmd: list[str]) -> dict:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def maybe_resolve_price(structured: dict) -> dict:
    if 'unit_price' in structured:
        return structured
    workbook = structured.get('workbook_path')
    code = structured.get('code')
    system = structured.get('system', 'Standard')
    if not (workbook and code):
        return structured

    resolver = Path('/root/.openclaw/workspace/skills/son-home-quote-image/scripts/resolve_workbook_price.py')
    result = run_json(['python3', str(resolver), workbook, code, system])
    candidates = result.get('candidates', [])
    if len(candidates) == 1 and candidates[0].get('priceCandidate') is not None:
        structured = dict(structured)
        structured['unit_price'] = candidates[0]['priceCandidate']
        structured['_resolver'] = {
            'sheet': candidates[0].get('sheet'),
            'rowIndex': candidates[0].get('rowIndex'),
            'matchedText': candidates[0].get('matchedText'),
            'systemColumn': candidates[0].get('systemColumn')
        }
    else:
        structured = dict(structured)
        structured['_resolver_result'] = result
    return structured


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

    structured = json.loads(structured_input.read_text(encoding='utf-8'))
    structured = maybe_resolve_price(structured)
    if 'unit_price' not in structured and 'items' not in structured:
        out = {
            'payload': None,
            'image': None,
            'workflowVersion': cfg.get('activeWorkflowVersion'),
            'directDeliveryPreferred': cfg.get('directDeliveryPreferred', True),
            'executed': False,
            'reason': 'unit_price_missing_after_resolver',
            'resolver': structured.get('_resolver_result')
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    resolved_input = out_dir / f'{base}.resolved-input.json'
    resolved_input.write_text(json.dumps(structured, ensure_ascii=False, indent=2), encoding='utf-8')

    build_script = Path('/root/.openclaw/workspace/skills/son-home-quote-image/scripts/build_quote_payload.py')
    validate_script = Path('/root/.openclaw/workspace/skills/son-home-quote-image/scripts/validate_quote_payload.py')
    render_script = Path(cfg['rendererScript']).resolve()

    run(['python3', str(build_script), str(resolved_input), str(payload)])
    run(['python3', str(validate_script), str(payload)])
    run(['python3', str(render_script), str(payload), str(image)])

    result = {
        'payload': str(payload),
        'image': str(image),
        'workflowVersion': cfg.get('activeWorkflowVersion'),
        'directDeliveryPreferred': cfg.get('directDeliveryPreferred', True),
        'executed': True,
        'resolvedInput': str(resolved_input),
        'resolver': structured.get('_resolver')
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
