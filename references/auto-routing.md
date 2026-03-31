# auto routing

Use this to choose the best quote workflow path before execution.

## route selection order
1. identify input source: text or image
2. identify line count: single-line or multi-line
3. estimate ambiguity: low / medium / high
4. decide whether structured input is already ready
5. choose one route only

## preferred routes

### text single-line
Use when the user typed a clear one-line request.
Path:
- resolve pricing
- build payload
- validate
- render
- deliver

### text multi-line
Use when the request clearly contains multiple actual line items.
Path:
- resolve each line
- build multi-line payload
- validate
- render
- deliver

### image handwriting
Use when the request comes from a handwritten or messy image.
Path:
- inspect layout
- Gemini first
- OCR cross-check
- confidence score
- finalize or ask-back

### operator fast path
Use only when the structured input is already resolved and safe.
Path:
- `quote_operator.py`

### ask-back path
Use when ambiguity is still too high.
Ask only for the missing critical fields.

## guardrail
Auto-routing is for choosing the safest fast path.
It is not permission to skip verification.
