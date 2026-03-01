---
name: html-to-pdf
description: "Convert HTML presentation files to high-quality PDF. Use when: user wants to export HTML presentation to PDF, converting web-based presentations to printable format, or when HTML file should become a multi-page PDF."
---

# HTML to PDF Converter

## Overview

Converts HTML presentation files to PDF with configurable resolution and dimensions. Each `.slide` element becomes a separate PDF page. Supports viewport-based sizing and device scale factor for sharp text rendering.

## Quick Start

```bash
# Basic usage - converts presentation.html to presentation.pdf
python3 scripts/html_to_pdf.py input.html

# With custom output path
python3 scripts/html_to_pdf.py input.html -o output.pdf

# With custom viewport (for different slide sizes)
python3 scripts/html_to_pdf.py input.html --width 1920 --height 1080
```

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `--width` | 1920 | Viewport width in pixels |
| `--height` | 1080 | Viewport height in pixels |
| `--scale` | 2 | Device scale factor (1-4, higher = sharper text) |
| `--selector` | .slide | CSS selector for slide elements |
| `--wait` | 3000 | Wait time in ms for fonts to load |
| `-o` | auto | Output PDF path |

## How It Works

1. **Viewport Detection**: Uses viewport dimensions to render HTML at correct size
2. **Slide Capture**: Each element matching `--selector` becomes a PDF page
3. **High Resolution**: Uses `--scale` factor (default 2) for crisp text
4. **Image Embedding**: Screenshots are embedded as high-quality images

## HTML Requirements

The HTML should have slide elements (e.g., `<section class="slide">`):

```html
<body>
  <section class="slide">Slide 1 content</section>
  <section class="slide">Slide 2 content</section>
  <section class="slide">Slide 3 content</section>
</body>
```

## Quality Settings

- **Scale 1**: Good for small files, may have blurry text
- **Scale 2** (recommended): Sharp text, moderate file size
- **Scale 3-4**: Very sharp, larger file size

For presentations with text, use `--scale 2` or higher.
