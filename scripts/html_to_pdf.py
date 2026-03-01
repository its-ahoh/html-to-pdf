#!/usr/bin/env python3
"""
HTML to PDF Converter

Converts HTML presentation files to PDF with configurable resolution and dimensions.
Supports slide-based HTML presentations where each .slide element becomes a PDF page.
"""

import argparse
import io
import os
from pathlib import Path

from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def get_slide_dimensions(page, slide):
    """Get the dimensions of a slide element."""
    return page.evaluate('''(slide) => {
        const rect = slide.getBoundingClientRect();
        return {
            x: rect.x,
            y: rect.y,
            width: rect.width,
            height: rect.height
        };
    }''', slide)


def convert_html_to_pdf(
    html_path: str,
    output_path: str = None,
    viewport_width: int = 1920,
    viewport_height: int = 1080,
    device_scale_factor: int = 2,
    slide_selector: str = ".slide",
    wait_time: int = 3000,
):
    """
    Convert HTML file to PDF.

    Args:
        html_path: Path to the input HTML file
        output_path: Path for output PDF (default: same name as HTML with .pdf)
        viewport_width: Viewport width in pixels
        viewport_height: Viewport height in pixels
        device_scale_factor: Device scale factor for higher resolution (1-4)
        slide_selector: CSS selector for slide elements
        wait_time: Milliseconds to wait for page load
    """
    html_path = Path(html_path)
    if output_path is None:
        output_path = html_path.with_suffix(".pdf")
    else:
        output_path = Path(output_path)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": viewport_width, "height": viewport_height},
            device_scale_factor=device_scale_factor,
        )
        page.goto(f"file://{html_path.resolve()}", wait_until="networkidle")
        page.wait_for_timeout(wait_time)

        slides = page.query_selector_all(slide_selector)
        print(f"Found {len(slides)} slides")

        if len(slides) == 0:
            print("No slides found. Capturing entire page as single PDF page.")
            pdf_data = page.pdf(
                print_background=True,
                format="Letter",
                landscape=True,
            )
            with open(output_path, "wb") as f:
                f.write(pdf_data)
        else:
            writer = PdfWriter()

            # Calculate capture dimensions based on device_scale_factor
            capture_width = viewport_width * device_scale_factor
            capture_height = viewport_height * device_scale_factor

            for i, slide in enumerate(slides):
                slide.scroll_into_view_if_needed()
                page.wait_for_timeout(300)

                # Get slide bounding box
                slide_bbox = get_slide_dimensions(page, slide)
                print(f"Slide {i+1}: {slide_bbox['width']}x{slide_bbox['height']}")

                # Capture screenshot
                clip = {
                    "x": slide_bbox["x"] * device_scale_factor,
                    "y": slide_bbox["y"] * device_scale_factor,
                    "width": capture_width,
                    "height": capture_height,
                }
                img_data = page.screenshot(clip=clip, type="png", full_page=False)

                # Create PDF page with image
                pdf_width = viewport_width
                pdf_height = viewport_height

                c = io.BytesIO()
                cv = canvas.Canvas(c, pagesize=(pdf_width, pdf_height))
                cv.drawImage(ImageReader(io.BytesIO(img_data)), 0, 0,
                           width=pdf_width, height=pdf_height)
                cv.save()

                c.seek(0)
                temp_reader = PdfReader(c)
                writer.add_page(temp_reader.pages[0])

                print(f"  -> Page {i+1} created")

            with open(output_path, "wb") as f:
                writer.write(f)

        browser.close()

    size = os.path.getsize(output_path)
    print(f"Done! Output: {output_path}")
    print(f"Size: {size / 1024 / 1024:.1f} MB")


def main():
    parser = argparse.ArgumentParser(description="Convert HTML to PDF")
    parser.add_argument("input", help="Input HTML file path")
    parser.add_argument("-o", "--output", help="Output PDF file path")
    parser.add_argument("--width", type=int, default=1920,
                       help="Viewport width (default: 1920)")
    parser.add_argument("--height", type=int, default=1080,
                       help="Viewport height (default: 1080)")
    parser.add_argument("--scale", type=int, default=2,
                       help="Device scale factor 1-4 (default: 2)")
    parser.add_argument("--selector", default=".slide",
                       help="CSS selector for slides (default: .slide)")
    parser.add_argument("--wait", type=int, default=3000,
                       help="Wait time in ms for page load (default: 3000)")

    args = parser.parse_args()

    convert_html_to_pdf(
        html_path=args.input,
        output_path=args.output,
        viewport_width=args.width,
        viewport_height=args.height,
        device_scale_factor=args.scale,
        slide_selector=args.selector,
        wait_time=args.wait,
    )


if __name__ == "__main__":
    main()
