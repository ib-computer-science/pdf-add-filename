# pdf_add_filename.py - stamps the PDF filename at the top of its first page
# Copyright (C) 2026  pdf-add-filename contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import argparse
import os
import sys


NAMED_COLORS = {
    "red":     (1.0, 0.0, 0.0),
    "green":   (0.0, 0.502, 0.0),
    "blue":    (0.0, 0.0, 1.0),
    "black":   (0.0, 0.0, 0.0),
    "white":   (1.0, 1.0, 1.0),
    "yellow":  (1.0, 1.0, 0.0),
    "orange":  (1.0, 0.647, 0.0),
    "purple":  (0.502, 0.0, 0.502),
    "cyan":    (0.0, 1.0, 1.0),
    "magenta": (1.0, 0.0, 1.0),
    "gray":    (0.502, 0.502, 0.502),
}


def parse_color(color_str):
    """Return an (r, g, b) tuple with components in [0, 1].

    Accepts:
      - named colors: red, green, blue, black, ...
      - hex strings: #rrggbb or rrggbb
    """
    s = color_str.strip().lower()
    if s in NAMED_COLORS:
        return NAMED_COLORS[s]
    hex_str = s.lstrip("#")
    if len(hex_str) == 6:
        try:
            r = int(hex_str[0:2], 16) / 255
            g = int(hex_str[2:4], 16) / 255
            b = int(hex_str[4:6], 16) / 255
            return (r, g, b)
        except ValueError:
            pass
    raise ValueError(
        f"Unrecognised color '{color_str}'. "
        "Use a named color (red, blue, …) or a hex value (#rrggbb)."
    )


def parse_margin(margin_str):
    """Return margin in PDF points (1 pt = 1/72 in).

    Accepted units: cm, mm, in, pt.
    """
    s = margin_str.strip().lower()
    multiplier = 0
    try:
        if s.endswith("cm"):
            multiplier = 28.3465
        if s.endswith("mm"):
            multiplier = 2.83465
        if s.endswith("in"):
            multiplier = 72.0
        if s.endswith("pt"):
            multiplier = 1

        if multiplier:
            numerical_part = float(s[:-2])
            return multiplier * numerical_part
    except ValueError:
        raise ValueError(f"Cannot parse margin '{margin_str}'. Examples: 1cm, 10mm, 0.5in, 28pt")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Add the name of the input PDF file as centered text "
            "at the top of its first page and write the result to OUTPUT."
        )
    )
    parser.add_argument("input",  help="Input PDF file")
    parser.add_argument("output", help="Output PDF file")
    parser.add_argument(
        "--color",
        default="red",
        metavar="COLOR",
        help="Text color — named (red, blue, …) or hex (#rrggbb). Default: red",
    )
    parser.add_argument(
        "--margin",
        default="1cm",
        metavar="MARGIN",
        help="Distance from top of page. Units: cm, mm, in, pt. Default: 1cm",
    )
    parser.add_argument(
        "--font-size",
        type=float,
        default=12.0,
        metavar="PT",
        help="Font size in points. Default: 12",
    )

    args = parser.parse_args()

    # --- validate dependencies -----------------------------------------------
    try:
        import fitz  # PyMuPDF
    except ImportError:
        sys.exit(
            "Error: PyMuPDF is not installed."
        )

    # --- validate arguments ---------------------------------------------------
    if not os.path.isfile(args.input):
        sys.exit(f"Error: input file not found: {args.input}")

    try:
        color = parse_color(args.color)
    except ValueError as exc:
        sys.exit(f"Error: {exc}")

    try:
        margin_pt = parse_margin(args.margin)
    except ValueError as exc:
        sys.exit(f"Error: {exc}")

    if args.font_size <= 0:
        sys.exit("Error: --font-size must be a positive number")

    font_size = args.font_size
    filename = os.path.basename(args.input)

    # --- open PDF and annotate ------------------------------------------------
    try:
        doc = fitz.open(args.input)
    except Exception as exc:
        sys.exit(f"Error opening '{args.input}': {exc}")

    if doc.page_count == 0:
        sys.exit("Error: the PDF contains no pages")

    page       = doc[0]
    page_width = page.rect.width   # points

    # Measure text width so we can centre it.
    font       = fitz.Font("helv")
    text_width = font.text_length(filename, fontsize=font_size)

    # x: left edge of text for horizontal centring (clamp to 0 so it is never off-page)
    x = max((page_width - text_width) / 2, 0)

    # y: baseline position.
    # insert_text() uses the baseline, and the ascender is ~ascender_ratio * font_size
    # above the baseline.  We want the top of the rendered text to sit at margin_pt.
    ascender_ratio = font.ascender   # typically ~0.72 for Helvetica
    y = margin_pt + ascender_ratio * font_size

    page.insert_text(
        (x, y),
        filename,
        fontname="helv",
        fontsize=font_size,
        color=color,
    )

    # --- save output ----------------------------------------------------------
    try:
        doc.save(args.output)
    except Exception as exc:
        sys.exit(f"Error saving '{args.output}': {exc}")

    doc.close()


main()