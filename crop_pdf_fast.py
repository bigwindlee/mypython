#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fast cropping of a PDF by pages and optional top/bottom percentages.
Uses pikepdf (qpdf backend) for better performance on large PDFs.

Examples:
  1) From page 3 to the end:
     python crop_pdf_fast.py -i in.pdf -o out.pdf -s 3

  2) From page 2 to the end, keeping only the bottom 40% of page 2:
     python crop_pdf_fast.py -i in.pdf -o out.pdf -s 2 -b 40

  3) From page 1 to page 5, keeping only the top 30% of page 5:
     python crop_pdf_fast.py -i in.pdf -o out.pdf -s 1 -e 5 -t 30
"""

import argparse
import sys
from pathlib import Path

try:
    import pikepdf
except ImportError:
    print("Error: You must install 'pikepdf' first.")
    print("       e.g. pip install pikepdf")
    sys.exit(1)


def parse_args() -> argparse.Namespace:
    # add_help=True ensures -h / --help is available
    parser = argparse.ArgumentParser(
        description=(
            "截取 PDF 指定页范围，并可选择只保留起始页的底部百分比、"
            "终止页的顶部百分比。\n"
            "页面编号为 1-based（第一页是 1）。"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=True,
        epilog=(
            "参数说明：\n"
            "  -i, --input              必选，被截取的 PDF 文件路径\n"
            "  -o, --output             必选，截取后输出的 PDF 文件路径\n"
            "  -s, --start-page         可选，起始页编号（1-based），缺省为 1\n"
            "  -b, --start-bottom-pct   可选，起始页保留底部百分比，例如 40 表示保留底部 40%%\n"
            "  -e, --end-page           可选，终止页编号（1-based），缺省为最后一页\n"
            "  -t, --end-top-pct        可选，终止页保留顶部百分比，例如 40 表示保留顶部 40%%\n"
            "  -h, --help               打印此帮助信息并退出\n\n"
            "依赖关系：\n"
            "  - 如果未指定 --start-page，则不得指定 --start-bottom-pct\n"
            "  - 如果未指定 --end-page，则不得指定 --end-top-pct\n"
            "  - 若起始页和终止页相同，目前不支持同时指定\n"
            "    --start-bottom-pct 和 --end-top-pct\n\n"
            "示例：\n"
            "  1) 从第 3 页到最后一页：\n"
            "     python crop_pdf_fast.py -i in.pdf -o out.pdf -s 3\n\n"
            "  2) 从第 2 页到底部 40%，再到最后一页：\n"
            "     python crop_pdf_fast.py -i in.pdf -o out.pdf -s 2 -b 40\n\n"
            "  3) 从第 1 页到第 5 页，且只保留第 5 页顶部 30%：\n"
            "     python crop_pdf_fast.py -i in.pdf -o out.pdf -s 1 -e 5 -t 30\n"
        ),
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input PDF file path",
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output PDF file path",
    )
    parser.add_argument(
        "-s", "--start-page",
        type=int,
        help="Start page number (1-based), default is 1",
    )
    parser.add_argument(
        "-b", "--start-bottom-pct",
        type=float,
        help="Bottom percentage to keep on start page (0-100]",
    )
    parser.add_argument(
        "-e", "--end-page",
        type=int,
        help="End page number (1-based), default is last page",
    )
    parser.add_argument(
        "-t", "--end-top-pct",
        type=float,
        help="Top percentage to keep on end page (0-100]",
    )

    # If no arguments are provided at all, show help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    # Dependency checks
    if args.start_page is None and args.start_bottom_pct is not None:
        parser.error(
            "If --start-page is not specified, "
            "--start-bottom-pct/-b must not be provided."
        )

    if args.end_page is None and args.end_top_pct is not None:
        parser.error(
            "If --end-page is not specified, "
            "--end-top-pct/-t must not be provided."
        )

    return args


def validate_percent(name: str, value: float) -> None:
    """Validate percentage value is in (0, 100]."""
    if value <= 0.0 or value > 100.0:
        raise ValueError(f"{name} must be in (0, 100], got {value}")


def main() -> None:
    args = parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    # Check input file existence
    if not in_path.is_file():
        print(f"Error: input PDF does not exist: {in_path}")
        sys.exit(1)

    try:
        pdf = pikepdf.open(str(in_path))
    except Exception as e:
        print(f"Error: failed to open input PDF: {e}")
        sys.exit(1)

    num_pages = len(pdf.pages)
    if num_pages == 0:
        print("Error: input PDF has no pages.")
        pdf.close()
        sys.exit(1)

    # Determine start_page and end_page (1-based)
    start_page = args.start_page if args.start_page is not None else 1
    end_page = args.end_page if args.end_page is not None else num_pages

    # Basic page range validation
    if start_page < 1 or start_page > num_pages:
        print(f"Error: start_page must be in [1, {num_pages}], got {start_page}")
        pdf.close()
        sys.exit(1)

    if end_page < 1 or end_page > num_pages:
        print(f"Error: end_page must be in [1, {num_pages}], got {end_page}")
        pdf.close()
        sys.exit(1)

    if start_page > end_page:
        print(f"Error: start_page ({start_page}) cannot be greater than end_page ({end_page}).")
        pdf.close()
        sys.exit(1)

    start_bottom_pct = args.start_bottom_pct
    end_top_pct = args.end_top_pct

    if start_bottom_pct is not None:
        validate_percent("start_bottom_pct", start_bottom_pct)
    if end_top_pct is not None:
        validate_percent("end_top_pct", end_top_pct)

    if start_page == end_page and start_bottom_pct is not None and end_top_pct is not None:
        print(
            "Error: start_page and end_page are the same, "
            "but both --start-bottom-pct/-b and --end-top-pct/-t are specified.\n"
            "Currently this case is not supported to avoid ambiguity."
        )
        pdf.close()
        sys.exit(1)

    new_pdf = pikepdf.Pdf.new()

    # Convert to zero-based indices
    start_idx = start_page - 1
    end_idx = end_page - 1

    for i in range(start_idx, end_idx + 1):
        page = pdf.pages[i]

        # In pikepdf, the attribute is MediaBox (capital M, B)
        media = page.MediaBox
        x0, y0, x1, y1 = [float(v) for v in media]
        height = y1 - y0

        new_x0 = x0
        new_y0 = y0
        new_x1 = x1
        new_y1 = y1

        # Apply bottom percent cropping on start page
        if i == start_idx and start_bottom_pct is not None:
            new_y1 = y0 + height * (start_bottom_pct / 100.0)

        # Apply top percent cropping on end page
        if i == end_idx and end_top_pct is not None:
            new_y0 = y1 - height * (end_top_pct / 100.0)

        if new_y1 <= new_y0:
            print(
                f"Error: invalid crop region on page {i + 1}: "
                f"new_y0={new_y0}, new_y1={new_y1}. Check your percentages."
            )
            pdf.close()
            new_pdf.close()
            sys.exit(1)

        page.MediaBox = [new_x0, new_y0, new_x1, new_y1]
        page.CropBox = [new_x0, new_y0, new_x1, new_y1]

        new_pdf.pages.append(page)

    try:
        new_pdf.save(str(out_path))
    except Exception as e:
        print(f"Error: failed to write output PDF: {e}")
        pdf.close()
        new_pdf.close()
        sys.exit(1)

    pdf.close()
    new_pdf.close()

    print(
        f"Success: extracted pages {start_page} to {end_page} "
        f"from '{in_path}' to '{out_path}'."
    )
    if start_bottom_pct is not None:
        print(f"  - Start page {start_page} bottom {start_bottom_pct}% kept.")
    if end_top_pct is not None:
        print(f"  - End page {end_page} top {end_top_pct}% kept.")


if __name__ == "__main__":
    main()
