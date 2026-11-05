#!/usr/bin/env python3
"""Place ordered, unchanged raster sources in a PDF and write an export receipt."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

MAX_PAGE_HEIGHT = 14400.0  # PDF's conventional 200-inch page boundary.
MARGIN = 18.0
GAP = 12.0
PAPERS = {"A4": A4, "Letter": letter}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_source(path: Path) -> dict:
    raw = path.read_bytes()
    with warnings.catch_warnings():
        warnings.simplefilter("error", Image.DecompressionBombWarning)
        with Image.open(io.BytesIO(raw)) as image:
            if getattr(image, "n_frames", 1) != 1:
                raise ValueError(f"Multi-frame input is unsupported: {path}")
            image.load()
            width, height = image.size
            if width < 1 or height < 1:
                raise ValueError(f"Invalid image dimensions: {path}")
            image_format = image.format
    return {"path": str(path.resolve()), "sha256": digest(raw),
            "pixelWidth": width, "pixelHeight": height,
            "format": image_format, "bytes": len(raw), "raw": raw}


def layout(sources: list[dict], mode: str, paper: str) -> list[dict]:
    width, height = PAPERS[paper]
    inner_width = width - 2 * MARGIN
    if mode == "page" and len(sources) != 1:
        raise ValueError("--format page requires exactly one image; use pdf or long for several.")
    if mode == "long":
        heights = [inner_width * s["pixelHeight"] / s["pixelWidth"] for s in sources]
        height = 2 * MARGIN + sum(heights) + GAP * (len(sources) - 1)
        if not math.isfinite(height) or height > MAX_PAGE_HEIGHT:
            raise ValueError(f"Long page exceeds {MAX_PAGE_HEIGHT:g} points; use --format pdf or split the inputs.")
        y = height - MARGIN
        placements = []
        for index, scaled_height in enumerate(heights):
            y -= scaled_height
            placements.append({"sourceIndex": index, "x": MARGIN, "y": y,
                               "width": inner_width, "height": scaled_height})
            y -= GAP
        return [{"widthPoints": width, "heightPoints": height, "images": placements}]
    pages = []
    for index, source in enumerate(sources):
        scale = min(inner_width / source["pixelWidth"], (height - 2 * MARGIN) / source["pixelHeight"])
        placed_width, placed_height = source["pixelWidth"] * scale, source["pixelHeight"] * scale
        pages.append({"widthPoints": width, "heightPoints": height, "images": [
            {"sourceIndex": index, "x": (width - placed_width) / 2,
             "y": (height - placed_height) / 2, "width": placed_width, "height": placed_height}]})
    return pages


def export(images: list[Path], mode: str, paper: str, output: Path) -> dict:
    if output.suffix.lower() != ".pdf":
        raise ValueError("--output must end in .pdf; every format exports a PDF.")
    receipt_path = output.with_suffix(".receipt.json")
    if output.exists() or receipt_path.exists():
        raise ValueError("Output PDF or receipt already exists; choose a new filename.")
    sources = [read_source(path) for path in images]
    if not sources:
        raise ValueError("At least one source image is required.")
    pages = layout(sources, mode, paper)
    buffer = io.BytesIO()
    document = canvas.Canvas(buffer, pagesize=(pages[0]["widthPoints"], pages[0]["heightPoints"]), pageCompression=1)
    document.setTitle(output.stem)
    for page in pages:
        document.setPageSize((page["widthPoints"], page["heightPoints"]))
        for placed in page["images"]:
            source = sources[placed["sourceIndex"]]
            document.drawImage(ImageReader(io.BytesIO(source["raw"])), placed["x"], placed["y"],
                               width=placed["width"], height=placed["height"], mask="auto")
        document.showPage()
    document.save()
    pdf_bytes = buffer.getvalue()
    receipt = {"schemaVersion": 1, "createdAt": datetime.now(timezone.utc).isoformat(),
               "format": mode, "paper": paper, "pageCount": len(pages),
               "output": {"path": str(output.resolve()), "bytes": len(pdf_bytes), "sha256": digest(pdf_bytes)},
               "sources": [{k: v for k, v in source.items() if k != "raw"} for source in sources],
               "pages": pages, "sourceFilesModified": False,
               "notes": "Raster-backed PDF, no crop. Source pixel orientation retained; no EXIF rotation. Not searchable or layered text."}
    receipt_bytes = (json.dumps(receipt, indent=2) + "\n").encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation protects both paths even if a file appears after preflight.
    created = []
    try:
        for path, data in [(output, pdf_bytes), (receipt_path, receipt_bytes)]:
            with path.open("xb") as handle:
                created.append(path)
                handle.write(data)
    except Exception:
        for path in reversed(created):
            path.unlink(missing_ok=True)
        raise
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", nargs="+", type=Path, help="Ordered local raster image paths; no glob sorting is performed.")
    parser.add_argument("--format", choices=["page", "long", "pdf"], default="pdf", dest="mode")
    parser.add_argument("--paper", choices=list(PAPERS), default="A4")
    parser.add_argument("--output", type=Path, required=True, help="New .pdf path; a .receipt.json sibling is also created.")
    args = parser.parse_args(argv)
    try:
        receipt = export(args.images, args.mode, args.paper, args.output)
    except (OSError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps({"output": receipt["output"]["path"], "receipt": str(args.output.with_suffix('.receipt.json').resolve()), "pages": receipt["pageCount"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
