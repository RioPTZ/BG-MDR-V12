# son home quote brain

This is the compact decision core for SON Home quote work.

## mission
Turn messy quote requests into correct, verified, directly delivered quote images with minimal back-and-forth.

## priority order
1. correct code / code range
2. correct dimensions
3. correct quantity
4. correct system
5. correct math
6. correct render form
7. direct Telegram delivery

## default decisions
- if system is missing: use `Standard`
- if quantity is missing and nothing suggests otherwise: use `1`
- if no valid note exists: keep `Ghi chú` blank
- if title is not specified: do not include `SON HOME`
- if user says `báo giá`: produce image quote by default

## image-reading decision tree

### case 1: clean text input
- parse directly
- confirm only if a critical field is missing

### case 2: handwritten / messy image
- inspect layout first
- Gemini Flash first
- local OCR second
- if Gemini output is plausible and Tún confirms it, continue without re-asking
- if still ambiguous, ask for only the missing fields

### case 3: sample-follow request
- treat latest approved sample as strongest visual source
- check master sample registry before improvising any style

## pricing decision tree
- locate workbook
- choose product family sheet
- resolve code through `Mã vải` / code range
- choose system column
- do not price by nearby product name if code range is known
- if sheet or system column is unclear, ask before finalizing

## math rules
- if height < 1m, bill height as 1m minimum
- if billed area still < 1m², bill 1m² minimum
- multiply by quantity after one-unit billed area is stable
- subtotal row must reflect sum of `Sau CK`, not a separate retail multiplication shortcut

## render rules
- wide horizontal layout
- very light mint pastel palette
- dimensions shown in mm
- subtotal row merges first 2 cells
- subtotal row leaves `Đơn giá` blank
- `Sau CK` must always show a value

## delivery rules
- render is not the end
- task is only complete when image is sent back in Telegram when possible
- clearly report completion

## failure rules
- if not sure, pause and ask
- if tool output is weak, say it is weak
- if impossible, say it clearly
