# quote verification checklist

Use this reference right before finalizing a SON Home quote.

## A. source check
- workbook found and readable
- correct sheet selected
- code resolved through `Mã vải` / code range
- correct price column selected for the applied system

## B. input check
- `Mã SP` is stable enough
- `Ngang` is stable enough
- `Cao` is stable enough
- `SL` is visible or safely defaulted to `1`
- `Ghi chú` is only kept if truly supported

## C. image-reading check
- if image is handwritten / messy, Gemini Flash was tried first
- local OCR used only as cross-check / fallback
- if Gemini was implausible, it was challenged before pricing
- if Tún confirmed the Gemini read, proceed without asking the same fields again

## D. math check
- height-under-1m rule applied
- minimum-1m² rule applied
- quantity multiplication applied correctly
- discount applied correctly
- final `Sau CK` values are correct
- `Cộng tiền hàng` equals sum of `Sau CK`

## E. render check
- latest approved layout/sample respected
- mint pastel palette respected
- `Ngang` and `Cao` shown in mm
- `Đơn giá` blank on subtotal row
- `Sau CK` cell is never blank
- final total block is present
- no `SON HOME` in title unless requested

## F. delivery check
- image successfully rendered
- image sent directly to Telegram when possible
- final reply clearly states completion
