# image reading workflow for quote inputs

Use this when Tún sends a measurement photo/screenshot and wants a quote generated from the image.

## goal

Extract these fields reliably before pricing:
- product code or code prefix
- `N` = width (`Ngang`)
- `C` = height (`Cao`)
- quantity / number of sets
- side notes like `kéo trái`, `kéo phải`, `so nan với nhau`

## default assumptions

For Tún's measurement images unless the image clearly shows otherwise:
- `N` means `Ngang`
- `C` means `Cao`
- comma decimals like `1,53` are meter values
- fragments like `x2`, `x3`, `x4` usually indicate quantity
- if no quantity is shown anywhere, default to `SL = 1`

## upgraded workflow

### 1. identify the image pattern before OCR
Look at the image as a form, not as random text.
First decide which pattern it most likely is:
- one line item
- multiple line items
- left / right split
- handwritten note with scattered fields
- screenshot of a previous quote card

Never treat every number on the image as a measurement candidate.

### 2. map likely field zones
Before reading text, decide where each field probably lives:
- code zone
- `N` zone
- `C` zone
- `SL` zone
- notes zone

If the image is dense, mentally split it into top / middle / bottom and left / center / right.

### 3. preprocess before OCR
Do not OCR the raw image only once.
Run lightweight preprocessing first:
- enlarge image or crop 2x to 6x
- convert to grayscale
- increase contrast
- sharpen
- autocontrast
- threshold black/white when handwriting is faint
- deskew if the photo is tilted

### 4. vision-first for handwritten images
For handwritten / messy measurement photos from Tún, do not rely on local OCR first.
Run **Gemini Flash vision** early to get a structured best-guess extraction of:
- `mã`
- `N`
- `C`
- `SL`
- `ghi chú`

Rules:
- ask Gemini to answer briefly and only with extraction fields
- treat Gemini as a strong first-pass reader for handwriting, not blind truth
- if Gemini output is plausible and Tún confirms it, proceed with that result
- if Gemini output is implausible, use local OCR + layout evidence to challenge it instead of pricing blindly

### 4. OCR in layers, not one pass
Use OCR as helper only.
Run it in this order:
1. full image pass
2. region passes: top / middle / bottom / left / right / center
3. tight crop passes around likely `N`, `C`, code, and quantity zones
4. retry with different OCR modes if needed

Preferred local helper:
- after the Gemini Flash pass, run `scripts/extract_quote_ocr.py <image_path>` for cross-check / fallback
- this uses `paddleocr-light` as the primary OCR engine and keeps Tesseract as fallback
- use PaddleOCR light especially for rendered quote screenshots, dense tables, and as a verifier for handwriting reads

Recommended fallback variations when using raw Tesseract manually:
- `psm 6`
- `psm 7`
- `psm 11`
- `eng`
- `vie+eng`

### 5. anchor every value to a nearby label
Only accept a number if it is tied to context.
Examples:
- a number near `N` is a width candidate
- a number near `C` is a height candidate
- a number near `x` or `SL` is a quantity candidate
- a code-like token near the product/code area is a code candidate

Loose numbers without anchors are weak evidence only.

### 6. normalize candidates before deciding
Normalize OCR output before comparison:
- convert likely decimal separators consistently
- fix common OCR confusions like `O` ↔ `0`, `I` ↔ `1`, `S` ↔ `5` only when context supports it
- remove stray punctuation
- treat `0.745`, `0,745`, and `745` carefully based on field meaning
- for display, dimensions later become mm, but extraction should first stay in meters

### 7. score confidence, then choose
For each extracted field, assign a simple confidence level:

#### high confidence
- value is visible in the image
- OCR agrees across multiple passes
- value is anchored to the correct nearby label
- value is plausible for curtain dimensions / quantity

#### medium confidence
- value is readable but slightly messy
- anchor is present but weak
- OCR outputs differ slightly but point to the same number

#### low confidence
- only one noisy OCR pass produced it
- no clear label anchor
- value conflicts with layout or business plausibility

Only finalize automatically when key fields are high confidence, or when medium confidence is supported by strong layout evidence.

### 8. apply business plausibility filters
Before finalizing, reject values that do not make business sense:
- width and height should be realistic curtain sizes
- quantity should usually be a small integer
- line totals / prices are not size candidates
- screenshot text from old quote cards should not override handwritten source values unless the user is clearly referencing the rendered quote
- if multiple values conflict, prefer the one with the strongest anchor + plausibility + repeat OCR agreement

### 9. apply operator rules after extraction
After dimensions are stable, then apply Tún's rules:
- if Tún says `chia đôi`, split `Ngang` in half
- convert `1 bộ` into `2 bộ`
- default note becomes `Trái + Phải So nan`
- example: `2.66 x 1.70 x 1 bộ` becomes `1.33 x 1.70 x 2 bộ`
- if no quantity is shown, use `SL = 1`

### 10. only then resolve pricing
After image fields are stable:
- resolve the product code through the workbook `Mã vải` column / code range
- never sort price by `Tên vải`
- use the correct system column
- apply area rules and discount rules

## decision rule: when to finalize vs ask

### finalize directly when
- code is clear enough
- `N` and `C` are high confidence
- quantity is visible or safely defaults to `1`
- no critical conflict remains

### ask Tún when
- more than one plausible `N/C` pair remains
- the code is ambiguous across different ranges
- quantity is unclear and the image suggests something other than `1`
- notes materially affect production but are unreadable

## hard rules

- never guess dimensions just because OCR produced a number
- never choose price by nearby product name if the code range is known
- never let a noisy OCR string outrank clear layout evidence
- if the image is still ambiguous after visual reading + preprocessing + multi-pass OCR + plausibility checks, ask for only the missing fields

## fallback question format

When the image still cannot be read safely, ask in the shortest possible format:

```text
Anh chốt giúp em đúng 1 dòng: N ... / C ... / SL ...
```

If the code is also unclear:

```text
Anh chốt giúp em: mã ... / N ... / C ... / SL ...
```

## operator checklist before rendering

Silently confirm:
- code resolved by `Mã vải` range, not product name
- `N` and `C` were anchored to labels or strong layout evidence
- quantity defaults to `1` only when not shown
- `chia đôi` rule applied only when Tún explicitly says so
- note is kept only when actually supported by the input
- if confidence is not good enough, ask one short question instead of rendering a risky quote

## practical priority order

When time is limited, prioritize accuracy in this order:
1. correct code / code range
2. correct `N`
3. correct `C`
4. correct quantity
5. note / production remark

The quote must not be rendered until the first 4 are stable enough.
