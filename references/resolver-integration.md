# resolver integration

Use this when the engine should turn code + system + workbook into a price candidate before payload building.

## purpose
Connect the workbook price resolver into the operator path so structured input no longer always needs a manual `unit_price`.

## fast-path idea
If structured input has:
- code
- system (or default Standard)
- workbook path
- width
- height
- qty
- discount

then the engine may resolve `unit_price` automatically before build -> validate -> render.

## guardrail
If resolver returns zero or multiple weak candidates, do not pretend certainty.
Return the resolver result for review instead of forcing a quote.
