# input confidence rubric

Use this to score whether quote input is safe enough to finalize.

## fields to score
- code
- width
- height
- quantity
- system
- note

## levels

### high
- clearly visible or explicitly typed by user
- consistent across layout, Gemini, and/or OCR
- plausible for workbook mapping and curtain sizing

### medium
- mostly readable but slightly noisy
- one source is weak but another source supports it
- plausible enough to proceed if the user confirms or if other fields are strong

### low
- only one weak source produced it
- conflicts with layout or workbook mapping
- implausible size / code / quantity

## decision rule
- finalize automatically only when core fields are high, or high enough after user confirmation
- ask short follow-up when more than one core field remains medium/low
- if user explicitly confirms a plausible Gemini read, upgrade that path and proceed
