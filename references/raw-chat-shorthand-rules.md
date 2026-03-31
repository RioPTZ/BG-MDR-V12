# raw chat shorthand rules

Use this when parsing Tún's quick quote messages.

## important shorthand patterns
- `Ti 183` should normalize to `TI183`
- missing system defaults to `Standard`
- if quantity is missing, default to `1`
- `chia đôi` means:
  - split width in half
  - change quantity to `2`
  - set note to `Trái + Phải So nan`
- `x` / `×` patterns like `2.66 x 1.70` should map to width x height
- `CK 50` or `chiết khấu 50%` should map to `discount_pct = 50`

## guardrail
Apply shorthand expansion only when it is actually supported by the text.
Do not invent special handling when the message is too incomplete.
