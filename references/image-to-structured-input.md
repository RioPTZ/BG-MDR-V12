# image to structured input

Use this to bridge image-reading output into engine-ready structured input.

## goal
Turn an image-derived extraction result into a normalized structured input JSON that the quote engine can use.

## expected image extraction fields
- code
- width_m
- height_m
- qty
- system (optional)
- discount_pct
- note (optional)
- workbook_path (optional but strongly preferred)

## rule
This bridge normalizes fields.
It does not claim image extraction is correct by itself.
Use confidence scoring and user confirmation when the image path is still ambiguous.
