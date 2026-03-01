# HTML to PDF

Convert HTML presentation files to high-quality PDF. Each slide element becomes a separate PDF page, with configurable viewport and scale for sharp text and images.

## Requirements

- **Python 3.8+**
- **Playwright** (Chromium) for headless rendering
- **pypdf** and **reportlab** for PDF assembly

Install dependencies:

```bash
pip install playwright pypdf reportlab
playwright install chromium
```

## Quick Start

```bash
# Convert presentation.html → presentation.pdf
python3 scripts/html_to_pdf.py input.html

# Custom output path
python3 scripts/html_to_pdf.py input.html -o output.pdf

# Custom viewport (e.g. 16:9 slides)
python3 scripts/html_to_pdf.py input.html --width 1920 --height 1080
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-o`, `--output` | (input name).pdf | Output PDF path |
| `--width` | 1920 | Viewport width (px) |
| `--height` | 1080 | Viewport height (px) |
| `--scale` | 2 | Device scale factor 1–4 (higher = sharper) |
| `--selector` | `.slide` | CSS selector for slide elements |
| `--wait` | 3000 | Wait time in ms before capture |

## HTML Format

Use elements that match the slide selector (default: `.slide`):

```html
<body>
  <section class="slide">Slide 1</section>
  <section class="slide">Slide 2</section>
  <section class="slide">Slide 3</section>
</body>
```

If no elements match the selector, the whole page is captured as a single PDF page.

## Quality

- **Scale 1**: Smaller files; text may look soft.
- **Scale 2** (default): Good balance of sharpness and file size.
- **Scale 3–4**: Very sharp, larger files.

Use `--scale 2` or higher for text-heavy slides.

## How It Works

1. Opens the HTML file in a headless Chromium viewport.
2. Waits for fonts and layout (`--wait` ms).
3. Finds all elements matching `--selector`.
4. Captures each as a PNG at viewport size × scale, then embeds as a PDF page.

Output is a multi-page PDF with one page per slide.
