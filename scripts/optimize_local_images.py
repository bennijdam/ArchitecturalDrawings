#!/usr/bin/env python3
"""
Convert all raw/unoptimized images in assets/img/ to AVIF + WebP + JPEG
at 640 / 1024 / 1600 px widths with semantic output names.

Pillow with AVIF support required (pip install Pillow).

Usage:
    python3 scripts/optimize_local_images.py
"""

from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageOps

PROJECT = Path(__file__).resolve().parent.parent
IMG_DIR = PROJECT / "assets" / "img"
WIDTHS = [640, 1024, 1600]

# source_filename → output_stem
# Output files will be: <stem>-640.avif, <stem>-640.webp, <stem>-640.jpg etc.
CONVERSIONS: dict[str, str] = {
    "iStock-481645322.jpg":                     "london-victorian-terrace",
    "Dormer-loft-converison-by-Ridgeline-Lofts-Ltd.jpeg": "dormer-loft-conversion",
    "double-storey.jpg":                        "double-storey-extension",
    "Home_Hub_Group_Double_Storey_Extension.jpg": "double-storey-extension-2",
    "Double-Story-Extension.png":               "double-storey-extension-3",
    "l-shaped-mansard-loft-conversion.jpg":     "mansard-loft-conversion",
    "kitchen-2-1-e1722852896192.jpg":           "kitchen-extension",
    "istock-loft-conversion-bedroom.jpg":       "loft-bedroom",
    "crop-tablet-stationery-blueprint.jpg":     "blueprint-stationery",
    "female-working-environment-projects.jpg":  "architect-working",
    "from-hand-correcting-blueprint.jpg":       "blueprint-review",
    "image-engineering-objects-workplace-top-view-construction-concept-engineering-tools-vintage-tone-retro-filter-effect-soft-focus-selective-focus.jpg": "design-tools",
    "A-planning-permission-drawings-house-extension-building-control-12345-1-1024x810.png": "planning-permission-drawings",
    "JPL_42-Foxcote-Rd-Pic4_l-shaped_white-bckgd.jpg": "l-shaped-extension",
    "Large-Side-pitched-roof.jpg":              "side-extension-pitched",
    "Small-Rear-flat-roof-Small-side-infill-pitched-roof.jpg": "rear-side-extension",
    "L-shaped-with-balcony-.jpg":               "extension-with-balcony",
    "over-structure-extension.jpg":             "over-structure-extension",
    "roof B.JPG":                               "flat-roof-extension",
    "tewrw-1536x1080.jpg":                      "planning-drawings-example",
    "42-e1727686687513.jpg":                    "rear-extension-plans",
    "1-1-1024x630.jpg":                         "extension-project-1",
    "25-1024x720.jpg":                          "extension-project-2",
    "35-1024x720.jpg":                          "extension-project-3",
    "5-1024x720.jpg":                           "extension-project-4",
    "5-1024x720 (1).jpg":                       "extension-project-5",
    "hq720.jpg":                                "loft-project-1",
    "hq720 (1).jpg":                            "loft-project-2",
    "hq720 (2).jpg":                            "loft-project-3",
    "L-shaped.jpg":                             "l-shaped-extension-2",
    "L5odLHQXhpjJJKvQM77s4R.jpg":              "london-house-exterior",
    "3885b3c6f3c84826b54d10e9a3218250.jpeg":    "architectural-detail",
    "Screen-Shot-2018-11-20-at-1.54.10-PM-300x237.png": "extension-diagram",
    "Types-of-Mansard-Roof.webp":              "mansard-roof-types",
}


def resize_and_save(img: Image.Image, out_path: Path, width: int, fmt: str, quality: int) -> None:
    h = int(img.height * width / img.width)
    resized = img.resize((width, h), Image.LANCZOS)
    if fmt == "JPEG" and resized.mode in ("RGBA", "P", "LA"):
        bg = Image.new("RGB", resized.size, (255, 255, 255))
        if resized.mode == "P":
            resized = resized.convert("RGBA")
        bg.paste(resized, mask=resized.split()[-1] if resized.mode in ("RGBA", "LA") else None)
        resized = bg
    elif fmt in ("AVIF", "WEBP") and resized.mode == "P":
        resized = resized.convert("RGBA")
    try:
        save_kwargs: dict = {"quality": quality, "optimize": True}
        if fmt == "AVIF":
            save_kwargs = {"quality": quality}
        resized.save(out_path, format=fmt, **save_kwargs)
    except Exception as e:
        print(f"    [!] Failed {out_path.name}: {e}")


def process(src_name: str, stem: str) -> bool:
    src = IMG_DIR / src_name
    if not src.exists():
        print(f"  [MISS] {src_name}")
        return False

    try:
        img = Image.open(src)
        img = ImageOps.exif_transpose(img)
    except Exception as e:
        print(f"  [ERR]  {src_name}: {e}")
        return False

    # Skip if too small (skip width < 640)
    if img.width < 640:
        print(f"  [SKIP] {src_name} — too small ({img.width}px wide)")
        return False

    print(f"  [CONV] {src_name} ({img.width}x{img.height}) -> {stem}")

    for w in WIDTHS:
        if img.width < w:
            continue
        resize_and_save(img, IMG_DIR / f"{stem}-{w}.avif", w, "AVIF", 60)
        resize_and_save(img, IMG_DIR / f"{stem}-{w}.webp", w, "WEBP", 80)
        resize_and_save(img, IMG_DIR / f"{stem}-{w}.jpg",  w, "JPEG", 85)
        print(f"    OK {w}px avif/webp/jpg")

    return True


def main() -> None:
    print("=== Local image optimization ===\n")
    done = 0
    for src_name, stem in CONVERSIONS.items():
        if process(src_name, stem):
            done += 1
    print(f"\n=== Done. {done}/{len(CONVERSIONS)} images converted. ===")
    print("New files in assets/img/ - update HTML to use <picture> tags.")


if __name__ == "__main__":
    main()
