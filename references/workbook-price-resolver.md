# workbook price resolver

Use this when the engine needs to move from product code to workbook sheet / code range / candidate price values with less manual searching.

## goal
Given:
- workbook path
- product code
- system hint

Return:
- candidate sheet
- candidate code range row
- row values for inspection
- best-effort unit price candidate if a matching system column can be recognized

## rules
- code matching must prioritize `Mã vải` / code range behavior
- do not trust nearby product-name text over code range
- if multiple candidates remain, return them instead of pretending certainty
- resolver reduces manual glue; it does not remove the need for final verification
