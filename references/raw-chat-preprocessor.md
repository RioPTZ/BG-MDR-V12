# raw chat preprocessor

Use this to bridge raw chat text into engine-friendly structured input candidates.

## goal
Given a rough chat message like:
- `Ti 183 rộng 1,55 cao 1,8 chiết khấu 50%`
- `CB1243 0.99 x 1.0 CK 50%`

extract a best-effort structured input candidate for the quote engine.

## expected extraction targets
- code
- width_m
- height_m
- qty
- discount_pct
- system if explicitly present
- note if obviously present

## guardrail
This is only a preprocessor.
It should normalize rough chat into a candidate structure, not pretend to be final truth when the message is ambiguous.
