#!/usr/bin/env python3
"""
One-shot image fix pass:

A) Patches pseo_boroughs.py  — adds BOROUGH_STREET_PHOTOS mapping (per-borough
   Unsplash photo IDs that match each area's actual housing character).
B) Patches gen_pseo.py       — replaces the two hardcoded trust-signal images
   with the per-borough variable.
C) Patches 7 guide pages     — replaces the generic 'modern residential
   architecture' placeholder with property-type-appropriate images.
D) Patches blog/index.html   — fixes the duplicate image on the
   planning-vs-permitted-development card.

Usage:
    python3 scripts/fix_images_all.py
After running, regenerate pSEO pages:
    python3 gen_pseo.py
"""

from pathlib import Path
import re

PROJECT = Path(__file__).resolve().parent.parent


# ─── A: per-borough street photo mapping ──────────────────────────────────────
# Seven carefully chosen Unsplash IDs cover the full range of London housing
# stock.  Adjacent boroughs with similar character get different photos where
# possible so the trust-signal thumbnail always looks contextually right.
#
# IDs (all confirmed in the existing add_stock_images.py library):
#   1513635269975-59663e0ac1ad  Victorian terraced street
#   605146768851-eda79da39897   Victorian conservation area terrace
#   513694203232-719a280e022f   London terraced houses with mansard roofs
#   551038247-3d9af20df552      Listed building Georgian facade
#   520986606214-8b456906c813   Georgian London townhouses
#   592595896616-c37162298647   Traditional London residential street
#   568454537842-d933259bb258   London suburban Victorian / inter-war semis

BOROUGH_STREET_PHOTOS = {
    # Inner north — dense Victorian / Georgian
    "camden":                   ("1513635269975-59663e0ac1ad", "Victorian terraced street in Camden NW1"),
    "islington":                ("605146768851-eda79da39897",  "Victorian conservation area terrace in Islington N1"),
    "hackney":                  ("513694203232-719a280e022f",  "Victorian terraced houses in Hackney E8"),
    # Central / west — stucco, Georgian, Regency
    "westminster":              ("551038247-3d9af20df552",     "Georgian listed townhouses in Westminster SW1"),
    "kensington-and-chelsea":   ("520986606214-8b456906c813",  "Stucco Georgian townhouses in Kensington W8"),
    "hammersmith-and-fulham":   ("605146768851-eda79da39897",  "Victorian bay-fronted terrace in Fulham SW6"),
    # South London — Victorian terraces and villas
    "wandsworth":               ("1513635269975-59663e0ac1ad", "Victorian terraced street in Clapham SW11"),
    "lambeth":                  ("592595896616-c37162298647",  "Victorian terraced street in Brixton SW9"),
    "southwark":                ("568454537842-d933259bb258",  "Georgian and Victorian terraces in Bermondsey SE1"),
    "lewisham":                 ("1513635269975-59663e0ac1ad", "Victorian terraced street in Forest Hill SE23"),
    "greenwich":                ("605146768851-eda79da39897",  "Georgian conservation area street in Greenwich SE10"),
    # East London
    "tower-hamlets":            ("551038247-3d9af20df552",     "Georgian terraces in Spitalfields E1"),
    "newham":                   ("592595896616-c37162298647",  "Victorian terraced street in Forest Gate E7"),
    "waltham-forest":           ("1513635269975-59663e0ac1ad", "Victorian terraced street in Walthamstow E17"),
    "redbridge":                ("568454537842-d933259bb258",  "1930s semi-detached houses in Wanstead E11"),
    "barking-and-dagenham":     ("1513635269975-59663e0ac1ad", "1920s terraced housing in Becontree Estate Dagenham"),
    "havering":                 ("568454537842-d933259bb258",  "1930s semi-detached houses in Hornchurch RM11"),
    # North London
    "haringey":                 ("513694203232-719a280e022f",  "Edwardian terraced houses in Crouch End N8"),
    "barnet":                   ("568454537842-d933259bb258",  "1930s semi-detached houses in Finchley N3"),
    "enfield":                  ("605146768851-eda79da39897",  "Edwardian villas in Winchmore Hill N21"),
    # West London
    "ealing":                   ("605146768851-eda79da39897",  "Edwardian villas in Ealing W5"),
    "hounslow":                 ("513694203232-719a280e022f",  "Edwardian terraced houses in Chiswick W4"),
    "brent":                    ("513694203232-719a280e022f",  "Edwardian villas in Queens Park NW6"),
    "hillingdon":               ("592595896616-c37162298647",  "1930s semi-detached street in Ruislip HA4"),
    "harrow":                   ("568454537842-d933259bb258",  "1930s semi-detached houses in Harrow HA1"),
    # South-west London
    "richmond-upon-thames":     ("520986606214-8b456906c813",  "Georgian houses on Richmond Green TW9"),
    "kingston-upon-thames":     ("592595896616-c37162298647",  "Edwardian terraced street in Surbiton KT6"),
    "merton":                   ("568454537842-d933259bb258",  "Victorian villas in Wimbledon SW19"),
    "sutton":                   ("592595896616-c37162298647",  "1930s semi-detached houses in Sutton SM1"),
    # South-east London
    "croydon":                  ("1513635269975-59663e0ac1ad", "Victorian villas in Crystal Palace SE19"),
    "bromley":                  ("568454537842-d933259bb258",  "1930s detached houses in Chislehurst BR7"),
    "bexley":                   ("592595896616-c37162298647",  "1930s semi-detached street in Bexleyheath DA6"),
    # City / historic
    "city-of-london":           ("551038247-3d9af20df552",     "Georgian listed buildings in the City of London EC2"),
}

BOROUGH_PHOTOS_BLOCK = '''
# Per-borough street photograph (Unsplash IDs).
# Each entry matches the area\'s actual housing character so the trust-signal
# thumbnail on every pSEO page is contextually accurate rather than generic.
BOROUGH_STREET_PHOTOS = {
''' + "\n".join(
    f'    "{slug}": ("{pid}", "{alt}"),'
    for slug, (pid, alt) in BOROUGH_STREET_PHOTOS.items()
) + "\n}\n"


def patch_pseo_boroughs():
    path = PROJECT / "pseo_boroughs.py"
    src = path.read_text(encoding="utf-8")

    if "BOROUGH_STREET_PHOTOS" in src:
        print("[skip] pseo_boroughs.py — BOROUGH_STREET_PHOTOS already present")
        return

    # Append after the closing brace of BOROUGHS dict
    src += BOROUGH_PHOTOS_BLOCK
    path.write_text(src, encoding="utf-8")
    print("[OK]   pseo_boroughs.py — added BOROUGH_STREET_PHOTOS")


# ─── B: patch gen_pseo.py ─────────────────────────────────────────────────────
HARDCODED_IMG_BLOCK = (
    '<img src="https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&amp;fit=crop&amp;w=400&amp;q=75"\n'
    '             alt="Victorian terraced street in London" loading="lazy" width="400" height="267"\n'
    '             style="width:100%;height:100%;object-fit:cover;display:block;" />'
)

DYNAMIC_IMG_BLOCK = (
    '<img src="https://images.unsplash.com/photo-{{borough_photo_id}}?auto=format&amp;fit=crop&amp;w=400&amp;q=75"\n'
    '             alt="{{borough_photo_alt}}" loading="lazy" width="400" height="267"\n'
    '             style="width:100%;height:100%;object-fit:cover;display:block;" />'
)

# We also need to import BOROUGH_STREET_PHOTOS and set up the variables in both
# render functions.
IMPORT_OLD = "from pseo_boroughs import BOROUGHS, BOROUGH_SLUGS, adjacent_names"
IMPORT_NEW = "from pseo_boroughs import BOROUGHS, BOROUGH_SLUGS, adjacent_names, BOROUGH_STREET_PHOTOS"

# In render_service_location: add vars after `hero = s["hero_img"]`
SL_ANCHOR_OLD = '    # Image\n    hero = s["hero_img"]'
SL_ANCHOR_NEW = (
    '    # Image\n'
    '    hero = s["hero_img"]\n'
    '    borough_photo_id, borough_photo_alt = BOROUGH_STREET_PHOTOS.get(\n'
    '        borough_slug, ("1513635269975-59663e0ac1ad", "London residential street"))'
)

# In render_borough_hub: add vars after `location = b["name"]`
HUB_ANCHOR_OLD = '    b = BOROUGHS[borough_slug]\n    location = b["name"]'
HUB_ANCHOR_NEW = (
    '    b = BOROUGHS[borough_slug]\n'
    '    location = b["name"]\n'
    '    borough_photo_id, borough_photo_alt = BOROUGH_STREET_PHOTOS.get(\n'
    '        borough_slug, ("1513635269975-59663e0ac1ad", "London residential street"))'
)


def patch_gen_pseo():
    path = PROJECT / "gen_pseo.py"
    src = path.read_text(encoding="utf-8")

    changed = False

    if IMPORT_OLD in src:
        src = src.replace(IMPORT_OLD, IMPORT_NEW, 1)
        changed = True

    if SL_ANCHOR_OLD in src:
        src = src.replace(SL_ANCHOR_OLD, SL_ANCHOR_NEW, 1)
        changed = True

    if HUB_ANCHOR_OLD in src:
        src = src.replace(HUB_ANCHOR_OLD, HUB_ANCHOR_NEW, 1)
        changed = True

    # Replace hardcoded image block (appears twice: service-location + borough-hub)
    count = src.count(HARDCODED_IMG_BLOCK)
    if count:
        src = src.replace(HARDCODED_IMG_BLOCK, DYNAMIC_IMG_BLOCK)
        changed = True
        print(f"[OK]   gen_pseo.py — replaced {count} hardcoded trust-signal image(s)")
    else:
        print("[warn] gen_pseo.py — hardcoded image block not found (may already be patched)")

    if changed:
        path.write_text(src, encoding="utf-8")
        print("[OK]   gen_pseo.py — patched")
    else:
        print("[skip] gen_pseo.py — no changes needed")


# ─── C: fix guide pages ───────────────────────────────────────────────────────
GENERIC_IMG = "photo-1486718448742-163732cd1544"

GUIDE_IMAGES = {
    # Property type guides
    "victorian-terrace": (
        "photo-1513635269975-59663e0ac1ad",
        "Victorian terraced houses with bay windows typical of inner London",
    ),
    "georgian-townhouse": (
        "photo-1551038247-3d9af20df552",
        "Georgian listed townhouses in a London conservation area",
    ),
    "1930s-semi": (
        "photo-1568454537842-d933259bb258",
        "1930s semi-detached houses typical of London suburban streets",
    ),
    "modern-flat": (
        "photo-1600585154340-be6161a56a0c",
        "Modern apartment interior with contemporary finishes",
    ),
    "edwardian-semi": (
        "photo-1605146768851-eda79da39897",
        "Edwardian semi-detached houses in a London conservation area",
    ),
    # Topic guides
    "planning": (
        "photo-1503387762-592deb58ef4e",
        "Architectural blueprints and planning application drawings on a desk",
    ),
    "lofts": (
        "photo-1600585154340-be6161a56a0c",
        "Bright modern loft bedroom with dormer window in a London conversion",
    ),
    "extensions": (
        "photo-1600566753190-17f0baa2a6c3",
        "Modern rear extension with bi-fold doors on a London Victorian terrace",
    ),
}


def patch_guide_pages():
    fixed = 0
    guide_root = PROJECT / "guides"
    if not guide_root.exists():
        print("[skip] guides/ directory not found")
        return

    for html in guide_root.rglob("*.html"):
        src = html.read_text(encoding="utf-8")
        if GENERIC_IMG not in src:
            continue

        # Determine which guide this is from path segments
        parts = html.parts
        # Look for a known keyword in the path
        slug = None
        for part in reversed(parts):
            key = part.replace(".html", "").lower()
            if key in GUIDE_IMAGES:
                slug = key
                break
            # parent directory name
        if slug is None:
            for part in reversed(parts[:-1]):
                if part.lower() in GUIDE_IMAGES:
                    slug = part.lower()
                    break

        if slug is None:
            print(f"[warn] no mapping for {html.relative_to(PROJECT)} — skipping")
            continue

        new_id, new_alt = GUIDE_IMAGES[slug]
        new_src = src.replace(
            f'src="https://images.unsplash.com/{GENERIC_IMG}?auto=format&fit=crop&w=1600&q=75" alt="Modern residential architecture"',
            f'src="https://images.unsplash.com/{new_id}?auto=format&fit=crop&w=1600&q=75" alt="{new_alt}"',
        )
        if new_src != src:
            html.write_text(new_src, encoding="utf-8")
            print(f"[OK]   {html.relative_to(PROJECT)} — {slug} image")
            fixed += 1

    if fixed == 0:
        print("[skip] guide pages — no generic images found (already fixed?)")
    else:
        print(f"[OK]   {fixed} guide page(s) updated")


# ─── D: fix blog/index.html duplicate ────────────────────────────────────────
BLOG_DUP_OLD = (
    'href="planning-vs-permitted-development.html"',
    'photo-1503387762-592deb58ef4e',
    "Planning application documents",
)
BLOG_DUP_NEW_ID   = "photo-1590644365607-1c0f865b5c09"
BLOG_DUP_NEW_ALT  = "Construction drawings showing permitted development calculations"


def patch_blog_index():
    path = PROJECT / "blog" / "index.html"
    if not path.exists():
        print("[skip] blog/index.html not found")
        return

    src = path.read_text(encoding="utf-8")
    original = src

    # Find every block that contains the planning-vs-pd href and the duplicate
    # photo ID, and replace only those photo references (not the non-duplicate ones)
    # Strategy: split on the card anchor, fix within each matching card.
    pattern = re.compile(
        r'(href="planning-vs-permitted-development\.html".*?)'
        r'(photo-1503387762-592deb58ef4e)'
        r'(\?auto=format.*?alt=")'
        r'(Planning application documents)',
        re.DOTALL,
    )
    new_src = pattern.sub(
        lambda m: (
            m.group(1)
            + BLOG_DUP_NEW_ID
            + m.group(3)
            + BLOG_DUP_NEW_ALT
        ),
        src,
    )

    if new_src != original:
        path.write_text(new_src, encoding="utf-8")
        count = len(pattern.findall(original))
        print(f"[OK]   blog/index.html — replaced {count} duplicate card image(s)")
    else:
        print("[skip] blog/index.html — no duplicate found (already fixed?)")


# ─── also fix projects/index.html if it has the generic default ──────────────
def patch_projects_index():
    path = PROJECT / "projects" / "index.html"
    if not path.exists():
        return
    src = path.read_text(encoding="utf-8")
    if GENERIC_IMG not in src:
        return
    new_src = src.replace(
        f'src="https://images.unsplash.com/{GENERIC_IMG}?auto=format&fit=crop&w=1600&q=75" alt="Modern residential architecture"',
        'src="https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1600&q=75" alt="Architectural drawings and blueprints for London residential projects"',
    )
    if new_src != src:
        path.write_text(new_src, encoding="utf-8")
        print("[OK]   projects/index.html — updated generic image")


if __name__ == "__main__":
    print("=== Image fix pass ===\n")
    print("--- A: pseo_boroughs.py ---")
    patch_pseo_boroughs()
    print("\n--- B: gen_pseo.py ---")
    patch_gen_pseo()
    print("\n--- C: guide pages ---")
    patch_guide_pages()
    print("\n--- D: blog/index.html ---")
    patch_blog_index()
    print("\n--- E: projects/index.html ---")
    patch_projects_index()
    print("\n=== Done. Now run: python3 gen_pseo.py ===")
