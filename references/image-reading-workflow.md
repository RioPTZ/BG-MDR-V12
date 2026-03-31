# image reading workflow for quote inputs

Use this when the quote source is a handwritten note, measurement photo, or messy screenshot.

## priority order
1. visually inspect the layout first
2. run **Gemini Flash vision** for a structured best-guess read
3. run local OCR as cross-check / fallback
4. apply plausibility checks before pricing
5. if the operator confirms the Gemini read, proceed without re-asking basic fields

## extract only these fields
- product code
- `N` = width
- `C` = height
- `SL` = quantity
- notes

## Gemini Flash guidance
- ask for a short, structured extraction only
- do not ask Gemini to explain the whole image when all you need is quote data
- treat Gemini as strong handwriting support, not blind truth
- if its output conflicts with layout or workbook code ranges, verify before pricing

## local OCR guidance
- use local OCR after Gemini, not instead of Gemini, for handwritten photos
- use it to verify numbers, labels, and code fragments
- keep OCR as fallback when Gemini is unavailable

## decision rule
- if Gemini output is plausible and operator-confirmed, use it
- if Gemini and OCR disagree, prefer the result that best matches layout evidence and workbook code ranges
- if neither is reliable, ask for only the missing fields in one short line
