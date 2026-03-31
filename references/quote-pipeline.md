# quote pipeline

Use this as the end-to-end operational flow for SON Home quote work.

## 1. intake
Collect from user input or image:
- product code
- system
- width
- height
- quantity
- discount
- note if any

## 2. extract
If the source is an image:
- inspect layout first
- for handwritten / messy images: Gemini Flash first
- local OCR as cross-check / fallback
- if Tún confirms the Gemini read, continue with it

## 3. resolve pricing
- locate workbook
- choose correct sheet
- resolve code through `Mã vải` / code range
- choose correct price column for system

## 4. calculate
- apply height minimum 1m rule
- apply minimum billed 1m² rule
- multiply by quantity
- apply discount

## 5. build payload
Create structured JSON for render.
Payload must include:
- rows
- subtotalText
- totalText
- title
- summary
- infoLine

## 6. validate
Run:
`python3 scripts/validate_quote_payload.py <payload.json>`

Do not render if validation fails.

## 7. render
Run the render script with the validated payload.

## 8. verify
Read `references/quote-verification-checklist.md`.
Do a final pass on:
- math
- layout
- subtotal row rules
- direct-send readiness

## 9. deliver
Send image directly to Telegram when possible.
Report completion clearly.
