# Setup notes

## Python dependency

This packaged skill expects Pillow for image rendering:

```bash
python3 -m pip install pillow
```

## Quick render test

Use the bundled sample payload:

```bash
python3 scripts/render_quote_card.py assets/sample-payload.json out.png
```

If the environment does not have the DejaVu fonts used by default, the script falls back to the default PIL font.

## Integration advice

- Keep workbook lookup logic separate from rendering.
- Build a JSON payload first, then render the image.
- Send the output image using the target bot's own media-send workflow.
- If the new bot uses a different platform, do not hardcode Telegram-specific message syntax into the pricing core.
