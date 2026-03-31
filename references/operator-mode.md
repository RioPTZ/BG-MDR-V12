# operator mode

Use this when quote work should move fast with minimum friction.

## goal
Take resolved structured inputs and run the shortest safe path to a ready-to-send quote image.

## inputs expected
- code
- width_m
- height_m
- qty
- unit_price
- discount_pct
- optional: system, group_name, note, footer_note, title, summary, infoLine

## operator flow
1. prepare structured input JSON
2. run quote orchestrator script
3. inspect generated image if needed
4. send directly to Telegram

## rule
Operator mode is for speed after important ambiguity has already been resolved.
Do not use it to skip uncertainty.
