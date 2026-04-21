#!/usr/bin/env python3
"""
Replace all Unsplash image URLs in guides/, projects/, and blog/ with
locally-hosted AVIF/WebP/JPEG <picture> elements.

Also fixes the malformed `photo-photo-` Unsplash URLs (double prefix bug).

Usage:
    python3 scripts/use_local_images.py
"""

from __future__ import annotations
import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
IMG_DIR = PROJECT / "assets" / "img"

# ─── Local image library ────────────────────────────────────────────────────
# Each entry: stem -> (alt_text, max_width_available)
# All these stems have been optimized by optimize_local_images.py
LOCAL_IMAGES: dict[str, str] = {
    "london-victorian-terrace":    "Victorian terraced street in inner London — typical residential housing",
    "london-house-exterior":       "London residential property exterior — period house with architectural character",
    "dormer-loft-conversion":      "Dormer loft conversion on a London Victorian terrace",
    "double-storey-extension":     "Double-storey rear extension on a London semi-detached house",
    "double-storey-extension-2":   "Two-storey side and rear extension on a London terraced house",
    "kitchen-extension":           "Open-plan kitchen extension with natural light and contemporary finishes",
    "blueprint-stationery":        "Architectural blueprints and planning drawings on a studio desk in London",
    "architect-working":           "MCIAT-chartered architectural technologist reviewing project drawings",
    "blueprint-review":            "Architect reviewing technical blueprints for a London residential project",
    "design-tools":                "Architectural design tools and technical drawings — professional studio setup",
    "planning-permission-drawings":"Planning permission drawings for a London house extension",
    "l-shaped-extension":          "L-shaped single-storey rear extension in London showing full floor plan",
    "side-extension-pitched":      "Side extension with pitched roof on a London semi-detached house",
    "rear-side-extension":         "Rear and side infill flat-roof extension on a London Victorian terrace",
    "extension-with-balcony":      "L-shaped extension with first-floor balcony on a London terraced house",
    "flat-roof-extension":         "Flat-roof rear extension on a London residential property",
    "planning-drawings-example":   "Architectural planning drawings for a London house project",
    "rear-extension-plans":        "Rear extension technical drawings and specifications for a London home",
    "architectural-detail":        "Architectural detail on a London period property — conservation-area approved",
    "extension-project-1":         "Completed house extension project in London — rear elevation",
    "extension-project-2":         "London house extension project — side elevation and roof detail",
    "extension-project-3":         "House extension in London — completed rear and side return",
    "extension-project-4":         "Residential extension project in London — finished with landscaping",
    "loft-project-1":              "Loft conversion project in London — dormer with rooflight",
    "loft-project-2":              "Loft bedroom conversion in London — vaulted ceiling and built-ins",
    "loft-project-3":              "Rear dormer loft conversion — completed London project",
    # Existing optimized families (already have proper 640/1024/1600 sets)
    "blueprint-correcting":        "MCIAT architectural technologist correcting blueprint drawings in a London studio",
    "blueprint-tablet":            "Architectural drawings reviewed on tablet — London residential project",
    "technologist-working":        "Architectural technologist at work on London residential planning drawings",
    "tools-workplace":             "Professional architectural tools and instruments on studio desk",
}

# ─── Page → images mapping ───────────────────────────────────────────────────
# Listed in order: first image on page gets index 0, second gets 1, etc.
PAGE_IMAGES: dict[str, list[str]] = {
    # projects/
    "side-return-camden":             ["kitchen-extension", "london-victorian-terrace", "blueprint-review", "design-tools", "architect-working"],
    "dormer-loft-hackney":            ["dormer-loft-conversion", "london-house-exterior", "blueprint-review", "design-tools", "architect-working", "dormer-loft-conversion"],
    "double-storey-wandsworth":       ["double-storey-extension", "london-house-exterior", "blueprint-review", "design-tools", "architect-working"],
    "garage-conversion-ealing":       ["blueprint-stationery", "london-victorian-terrace", "design-tools", "blueprint-review", "architect-working"],
    "hmo-conversion-hackney":         ["london-house-exterior", "london-victorian-terrace", "architect-working", "design-tools", "blueprint-review"],
    "mansard-islington":              ["architectural-detail", "london-house-exterior", "blueprint-review", "design-tools", "architect-working"],
    "planning-regs-southwark":        ["planning-permission-drawings", "design-tools", "blueprint-review", "architect-working", "london-house-exterior"],
    "basement-dig-kensington":        ["design-tools", "london-house-exterior", "blueprint-review", "architect-working", "planning-permission-drawings"],
    "rear-dormer-lewisham":           ["dormer-loft-conversion", "london-victorian-terrace", "blueprint-review", "architect-working", "design-tools"],
    "wraparound-extension-wandsworth":["l-shaped-extension", "london-house-exterior", "blueprint-review", "design-tools", "architect-working"],
    # projects/index.html
    "projects-index":                 ["london-house-exterior", "dormer-loft-conversion", "double-storey-extension", "kitchen-extension", "architectural-detail"],
    # guides/
    "extensions-guide":               ["double-storey-extension", "l-shaped-extension", "rear-side-extension", "blueprint-review", "side-extension-pitched"],
    "lofts-guide":                     ["dormer-loft-conversion", "blueprint-stationery", "blueprint-review", "design-tools"],
    "planning-guide":                  ["planning-permission-drawings", "design-tools", "blueprint-review", "architect-working"],
    "victorian-terrace-guide":         ["london-victorian-terrace", "blueprint-review", "architect-working"],
    "georgian-townhouse-guide":        ["london-house-exterior", "blueprint-review", "planning-permission-drawings"],
    "1930s-semi-guide":                ["london-victorian-terrace", "double-storey-extension", "blueprint-review"],
    "modern-flat-guide":               ["architect-working", "blueprint-stationery", "design-tools"],
    "edwardian-semi-guide":            ["london-victorian-terrace", "double-storey-extension", "architect-working"],
}

# Unsplash photo-ID → local image stem (for direct mapping)
UNSPLASH_MAP: dict[str, str] = {
    "1600585154340-be6161a56a0c": "dormer-loft-conversion",      # loft bedroom
    "1568454537842-d933259bb258": "london-victorian-terrace",     # London Victorian
    "1503387762-592deb58ef4e":    "blueprint-review",              # blueprints on desk
    "1600607687939-ce8a6c25118c": "dormer-loft-conversion",       # loft beams
    "1600607687644-aac4c3eac7f4": "kitchen-extension",            # kitchen extension
    "1600566753190-17f0baa2a6c3": "double-storey-extension",      # rear extension
    "1600210492493-0946911123ea": "dormer-loft-conversion",       # velux/rooflight
    "1592595896616-c37162298647": "london-victorian-terrace",     # terrace
    "1513694203232-719a280e022f": "architectural-detail",          # mansard roofs
    "1600607687644-c7171b42498f": "design-tools",                  # basement/tools
    "1486718448742-163732cd1544": "london-house-exterior",         # modern arch
    "1513635269975-59663e0ac1ad": "london-victorian-terrace",      # Victorian street
    "1605146768851-eda79da39897": "london-victorian-terrace",      # conservation
    "1551038247-3d9af20df552":    "london-house-exterior",          # Georgian
    "1520986606214-8b456906c813": "london-house-exterior",          # Georgian townhouse
    "1541888946425-d81bb19240f5": "design-tools",                   # construction
    "1590644365607-1c0f865b5c09": "blueprint-review",               # construction drawings
    "1558346490-a72e53ae2d4f":    "double-storey-extension",        # extension under const
    "1564013799919-ab600027ffc6": "london-house-exterior",           # Victorian house
    "1597216729923-2e36dfb60ecc": "london-victorian-terrace",        # party wall terrace
    "1556909114-f6e7ad7d3136":    "kitchen-extension",               # kitchen island
    "1600585154526-990dced4db0d": "kitchen-extension",               # kitchen diner
    "1484154218962-a197022b5858": "architect-working",               # architect tablet
    "1581094794329-c8112a89af12": "design-tools",                    # structural steel
    "1504307651254-35680f356dfd": "blueprint-review",                # structural drawings
    "1517022812141-23620dba5c23": "blueprint-stationery",            # technical overlay
}


# ─── Helpers ─────────────────────────────────────────────────────────────────

def rel_prefix(html_path: Path) -> str:
    """Return relative path prefix from html_path to project root assets/img/."""
    depth = len(html_path.relative_to(PROJECT).parts) - 1  # -1 for the file itself
    if depth == 0:
        return "assets/img/"
    return "../" * depth + "assets/img/"


def available_widths(stem: str) -> list[int]:
    """Return sorted list of widths that exist for this image stem."""
    widths = []
    for w in [640, 1024, 1600]:
        if (IMG_DIR / f"{stem}-{w}.avif").exists():
            widths.append(w)
    return widths if widths else [1600]


def picture_html(stem: str, alt: str, prefix: str, *, sizes: str = "(max-width:640px) 640px,(max-width:1024px) 1024px,1600px") -> str:
    """Build a responsive <picture> element for a local image stem."""
    widths = available_widths(stem)

    def srcset(ext: str) -> str:
        parts = []
        for w in widths:
            fname = f"{stem}-{w}.{ext}"
            if (IMG_DIR / fname).exists():
                parts.append(f"{prefix}{fname} {w}w")
        return ", ".join(parts) if parts else f"{prefix}{stem}-{widths[-1]}.{ext}"

    fallback_w = widths[-1]
    return (
        f'<picture>\n'
        f'    <source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}" />\n'
        f'    <source type="image/webp" srcset="{srcset("webp")}" sizes="{sizes}" />\n'
        f'    <img src="{prefix}{stem}-{fallback_w}.jpg" alt="{alt}"\n'
        f'         loading="lazy" width="{fallback_w}" height="{int(fallback_w * 9 / 16)}"\n'
        f'         style="width:100%;height:100%;object-fit:cover;display:block;" />\n'
        f'  </picture>'
    )


def get_page_key(html_path: Path) -> str:
    """Return the page key for PAGE_IMAGES lookup."""
    stem = html_path.stem  # e.g. "dormer-loft-hackney"
    parts = html_path.relative_to(PROJECT).parts

    # projects/index.html
    if "projects" in parts and stem == "index":
        return "projects-index"

    # guides/extensions/index.html
    if "guides" in parts:
        parent = parts[-2]  # directory containing the index.html
        if stem == "index":
            mappings = {
                "extensions": "extensions-guide",
                "lofts": "lofts-guide",
                "planning": "planning-guide",
                "victorian-terrace": "victorian-terrace-guide",
                "georgian-townhouse": "georgian-townhouse-guide",
                "1930s-semi": "1930s-semi-guide",
                "modern-flat": "modern-flat-guide",
                "edwardian-semi": "edwardian-semi-guide",
            }
            return mappings.get(parent, stem)
    return stem


UNSPLASH_IMG_RE = re.compile(
    r'<img\s[^>]*src=["\']https://images\.unsplash\.com/(?:photo-)?(?:photo-)?([A-Za-z0-9_\-]+)\?[^"\']*["\'][^>]*>',
    re.DOTALL | re.IGNORECASE,
)


def process_file(html_path: Path, page_images: list[str]) -> int:
    """Replace all Unsplash img tags. Returns count of replacements."""
    try:
        html = html_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  [!] read error {html_path}: {e}")
        return 0

    prefix = rel_prefix(html_path)
    img_index = [0]  # mutable for closure

    def replace_img(m: re.Match) -> str:
        photo_id = m.group(1)
        # Determine local stem
        stem = None
        if page_images and img_index[0] < len(page_images):
            stem = page_images[img_index[0]]
        elif photo_id in UNSPLASH_MAP:
            stem = UNSPLASH_MAP[photo_id]
        else:
            stem = page_images[0] if page_images else "london-house-exterior"
        img_index[0] += 1

        alt = LOCAL_IMAGES.get(stem, "London residential architecture")
        return picture_html(stem, alt, prefix)

    new_html, count = UNSPLASH_IMG_RE.subn(replace_img, html)
    if count:
        html_path.write_text(new_html, encoding="utf-8")
    return count


def main() -> None:
    print("=== Replace Unsplash with local images ===\n")
    total = 0

    dirs = ["projects", "guides"]
    for dir_name in dirs:
        base = PROJECT / dir_name
        if not base.exists():
            continue
        for html_path in sorted(base.rglob("*.html")):
            page_key = get_page_key(html_path)
            page_imgs = PAGE_IMAGES.get(page_key, list(UNSPLASH_MAP.values())[:5])
            count = process_file(html_path, page_imgs)
            rel = html_path.relative_to(PROJECT).as_posix()
            if count:
                print(f"  [OK] {rel} — {count} image(s) replaced")
                total += count
            else:
                # Check if file has Unsplash at all
                txt = html_path.read_text(encoding="utf-8")
                if "images.unsplash.com" in txt:
                    print(f"  [!!] {rel} — has Unsplash but not replaced (check regex)")

    print(f"\n=== guides/ + projects/: {total} Unsplash images replaced ===\n")

    # ─── Blog pages ─────────────────────────────────────────────────────────
    blog_total = 0
    blog_base = PROJECT / "blog"
    if blog_base.exists():
        # Blog images: map by topic keyword in filename
        BLOG_IMG_MAP = {
            "loft": ["dormer-loft-conversion", "blueprint-review", "design-tools"],
            "extension": ["double-storey-extension", "l-shaped-extension", "blueprint-review"],
            "mansard": ["architectural-detail", "london-house-exterior", "blueprint-review"],
            "planning": ["planning-permission-drawings", "blueprint-review", "design-tools"],
            "building": ["blueprint-review", "design-tools", "architect-working"],
            "kitchen": ["kitchen-extension", "double-storey-extension", "blueprint-review"],
            "basement": ["design-tools", "blueprint-review", "london-house-exterior"],
            "party-wall": ["london-victorian-terrace", "blueprint-review", "design-tools"],
            "conservation": ["london-house-exterior", "london-victorian-terrace", "blueprint-review"],
            "permitted": ["planning-permission-drawings", "blueprint-review", "design-tools"],
            "cost": ["planning-permission-drawings", "blueprint-review", "design-tools"],
            "victorian": ["london-victorian-terrace", "blueprint-review", "architect-working"],
            "georgian": ["london-house-exterior", "blueprint-review", "architect-working"],
            "1930": ["london-victorian-terrace", "double-storey-extension", "blueprint-review"],
            "edwardian": ["london-victorian-terrace", "architect-working", "blueprint-review"],
        }

        def blog_imgs(stem: str) -> list[str]:
            s = stem.lower()
            for kw, imgs in BLOG_IMG_MAP.items():
                if kw in s:
                    return imgs
            return ["london-house-exterior", "blueprint-review", "design-tools"]

        for html_path in sorted(blog_base.rglob("*.html")):
            page_imgs = blog_imgs(html_path.stem)
            count = process_file(html_path, page_imgs)
            if count:
                rel = html_path.relative_to(PROJECT).as_posix()
                print(f"  [OK] {rel} — {count} replaced")
                blog_total += count

    print(f"=== blog/: {blog_total} Unsplash images replaced ===")
    print(f"\n=== Total: {total + blog_total} images replaced across all pages ===")


if __name__ == "__main__":
    main()
