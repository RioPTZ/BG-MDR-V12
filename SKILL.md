---
name: son-home-quote-packaged
description: Create SON Home curtain quote images from workbook-driven pricing rules, render them in the approved horizontal quote-card format, and prepare portable quote workflows for other bots or agents. Use when handling SON Home curtain quotes, pricing lookups from Vol 12-style Excel workbooks, quote-card rendering, discount calculations, or packaging the SON Home quote process for reuse.
---

# SON Home Quote Packaged

Workflow version reference: `assets/workflow-version.json`
Default operator config: `assets/operator/defaults.json`
Structured input schema: `assets/schema/structured-input.schema.json`
Routing rules: `assets/router/routing-rules.json`

## Overview

Use this skill to calculate SON Home curtain quotes from the pricing workbook, apply the approved business rules, and render a clean quote image card.

Read `references/son-home-quote-brain.md` for the compact decision core when handling messy inputs or when you want the shortest reliable mental model for quote work.

This packaged version is meant to be reusable by other bots, so keep the workflow portable: price lookup, area calculation, totals, and image render should not depend on hidden chat context.

## Core workflow

1. Read the user quote inputs.
2. Identify product family, code, system, size, quantity, and discount.
3. Find the correct sheet and price column in the workbook.
4. Apply SON Home area rules exactly.
5. Calculate line totals and after-discount totals.
6. Build a render payload JSON.
7. Validate the payload.
8. Render the quote card image in the approved layout.
9. Return or send the generated image.

Read `references/quote-pipeline.md` for the full end-to-end operational flow.

If the workbook mapping is ambiguous, stop and ask instead of guessing.

## Required pricing behavior

### Price source
- Use the Vol 12 pricing workbook or the newest workbook explicitly provided by the operator.
- Match the correct sheet for the product family.
- Resolve requested codes through the workbook's **`Mã vải` column / code range**, not through the nearby product-name column.
- For example, a code like `IS362` must be matched to the range that contains it (such as `IS 361 - IS 366`) before reading price columns.
- Match the correct system column.
- Do not guess when a code range or system is unclear.

### Default system rule
- If the user explicitly provides the system, use it.
- If no system is provided, default to `Standard`.
- Only ask back if the surrounding context strongly suggests another system.

### Required quote inputs
Minimum fields:
- product code
- width
- height
- quantity
- discount
- system

## Reading quote input from images

When quote input comes from a handwritten or messy measurement image:
- first use **Gemini Flash vision** to extract only: product code, `N`, `C`, `SL`, and notes
- then use local OCR only as a cross-check / fallback, not as the only reader
- if Gemini produces a plausible read and the operator confirms it, continue with pricing instead of asking the same basic fields again
- if Gemini output is implausible, challenge it with layout evidence + OCR before pricing
- for handwritten photos, do not skip the Gemini step and jump straight into local OCR-only questioning

Read `references/image-reading-workflow.md` for the detailed workflow when packaging or reusing this skill on another bot/runtime.

## Area calculation rules

These rules are mandatory.

### Height minimum for billing
- If height is under 1 meter, round the billed height up to 1 meter before calculating area.

### Minimum billed area
- After height rounding, if billed area is still under 1 square meter, bill 1 square meter minimum.

### Quantity rule
- Calculate billed area for one unit first, then multiply by quantity unless the workbook explicitly requires another method.

## Quote card format rules

Use the approved SON Home quote image structure.

### Visual direction
- Keep the quote card in a wide horizontal format.
- Active master sample registry: `assets/master-samples/registry.json`
- Use the soft mint pastel palette, not the old blue palette.
- Keep the layout clean, bright, calm, and easy to scan.
- Do not include `SON HOME` in the title unless explicitly requested.

### Required table columns
Use these columns exactly:
- `Mã SP`
- `Hệ`
- `Ngang`
- `Cao`
- `SL`
- `K/lg`
- `Đơn giá`
- `CK`
- `Sau CK`
- `Ghi chú`

### Dimension display
- Display width and height in `mm` inside the rendered quote table.
- Keep calculations in meters internally.

### Totals rules
- Include a `Cộng tiền hàng` row.
- Merge the first two cells on that subtotal row.
- Keep `Đơn giá` blank on that subtotal row.
- `Cộng tiền hàng` must equal the sum of the `Sau CK` column.
- `Sau CK` must always show a number.
- Include a highlighted final block: `THÀNH TIỀN SAU CHIẾT KHẤU`.

## Notes behavior

- Leave `Ghi chú` blank if no valid note is provided.
- Keep notes short and practical.
- Notes like `cùng chiều cao so nan với nhau` should only remain when the listed rows truly share that same condition.

## Portable packaging guidance

When adapting this skill for another bot:
- keep workbook path configurable
- keep render input JSON-based when possible
- keep send/delivery logic separate from pricing logic
- avoid platform-specific message syntax inside the pricing core

## Files in this package

### scripts/render_quote_card.py
Use this script to render a quote-card PNG from an input JSON payload.

### scripts/build_quote_payload.py
Use this to build a final render payload JSON from resolved structured inputs.

### scripts/quote_operator.py
Use this for semi-automatic operator mode: structured input -> build -> validate -> render.

### scripts/score_quote_input.py
Use this for a quick finalize/review/ask recommendation from field confidence levels before operator execution.

### scripts/route_quote_workflow.py
Use this to choose the best workflow path before execution: text single-line, text multi-line, image-handwriting, operator-fast-path, or ask-back.

### scripts/quote_engine_entry.py
Use this as the single main entrypoint to the quote engine: route first, then execute only when fast-path is safe.

### scripts/validate_quote_payload.py
Use this before rendering to catch blank totals, blank `Sau CK`, or missing row fields.

### scripts/run_quote_render_pipeline.sh
Use this shell wrapper to run validation first, then render in one small flow.

Expected usage:
```bash
python3 scripts/render_quote_card.py assets/sample-payload.json out.png
```

### assets/sample-payload.json
Use this bundled sample payload to test the render path quickly before wiring the skill into another bot.

### references/son-home-quote-brain.md
Use this as the decision-core reference: defaults, priority order, image-reading decisions, pricing decisions, render rules, and delivery rules.

### references/operator-mode.md
Use this when speed matters and ambiguity is already resolved; it explains the shortest safe operator flow.

### references/input-confidence-rubric.md
Use this when image-derived or OCR-derived fields feel uncertain and you want a compact scoring rubric.

### references/auto-routing.md
Use this to choose the safest and fastest execution route before doing quote work.

### references/super-entrypoint.md
Use this as the top-level entry into the quote engine when you want one main command to orchestrate routing + safe execution.

### references/vol12-notes.md
Use this reference for quick workbook structure recall: product families, system groups, and helpful notes about Vol 12.

### references/setup-notes.md
Read this when setting up the skill on another machine or bot runtime.

## Quality check before finishing

Before returning a quote:
- verify the correct sheet
- verify the correct code match through `Mã vải` / code range
- verify the correct system price column
- verify billed area rules
- verify discount math
- verify subtotal and final total
- verify the quote image keeps the approved table structure
- verify the image is actually generated
