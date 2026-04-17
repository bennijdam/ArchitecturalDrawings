#!/usr/bin/env python3
"""Replace IMAGE PLACEHOLDER divs in project pages with UK Unsplash images."""
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
PROJECTS_DIR = SCRIPT_DIR / "projects"

# Unsplash image IDs for different content types
IMAGE_MAPPING = {
    "before": "photo-1568454537842-d933259bb258",  # London street/house
    "after": "photo-1600566753190-17f0baa2a6c3",  # Modern extension
    "complete": "photo-1600566753190-17f0baa2a6c3",  # Modern extension
    "finished": "photo-1600566753190-17f0baa2a6c3",  # Modern extension
    "floor plan": "photo-1503387762-592deb58ef4e",  # Blueprint on desk
    "drawing": "photo-1503387762-592deb58ef4e",  # Blueprint on desk
    "plans": "photo-1503387762-592deb58ef4e",  # Blueprint on desk
    "loft": "photo-1600585154340-be6161a56a0c",  # Loft bedroom
    "dormer": "photo-1600585154340-be6161a56a0c",  # Loft bedroom
    "mansard": "photo-1513694203232-719a280e022f",  # Mansard roofs
    "basement": "photo-1600607687644-c7171b42498f",  # Basement conversion
    "default": "photo-1513635269975-59663e0ac1ad",  # London terrace
}

# Per-project hero image mapping
HERO_IMAGES = {
    "side-return-camden": "photo-1600607687644-aac4c3eac7f4",
    "dormer-loft-hackney": "photo-1600607687939-ce8a6c25118c",
    "double-storey-wandsworth": "photo-1600566753190-17f0baa2a6c3",
    "garage-conversion-ealing": "photo-1600210492493-0946911123ea",
    "hmo-conversion-hackney": "photo-1592595896616-c37162298647",
    "mansard-islington": "photo-1513694203232-719a280e022f",
    "planning-regs-southwark": "photo-1503387762-592deb58ef4e",
    "basement-dig-kensington": "photo-1600607687644-c7171b42498f",
    "rear-dormer-lewisham": "photo-1600585154340-be6161a56a0c",
    "wraparound-extension-wandsworth": "photo-1600607687644-aac4c3eac7f4",
}

def get_image_id(slug, placeholder_text):
    """Determine Unsplash image ID based on slug and placeholder context."""
    text_lower = placeholder_text.lower() if placeholder_text else ""

    # Check for specific keywords in placeholder text
    for key, img_id in IMAGE_MAPPING.items():
        if key in text_lower:
            return img_id

    # Fallback: use project-specific hero or default
    return HERO_IMAGES.get(slug, IMAGE_MAPPING["default"])

def get_alt_text(image_id):
    """Generate descriptive alt text based on image type."""
    alt_map = {
        "photo-1568454537842-d933259bb258": "London house exterior before renovation",
        "photo-1600566753190-17f0baa2a6c3": "Modern extension after completion",
        "photo-1503387762-592deb58ef4e": "Architectural plans and blueprints",
        "photo-1600585154340-be6161a56a0c": "Loft bedroom conversion",
        "photo-1513694203232-719a280e022f": "Mansard roof exterior",
        "photo-1600607687644-c7171b42498f": "Basement conversion with natural light",
        "photo-1513635269975-59663e0ac1ad": "London Victorian terrace house",
        "photo-1600607687644-aac4c3eac7f4": "Modern kitchen extension",
        "photo-1600607687939-ce8a6c25118c": "Loft conversion with exposed beams",
        "photo-1600210492493-0946911123ea": "Converted garage space",
        "photo-1592595896616-c37162298647": "Residential Victorian terrace",
    }
    return alt_map.get(image_id, "Architectural project example")

def replace_placeholders(filepath, slug):
    """Replace IMAGE PLACEHOLDER divs with Unsplash image tags."""
    content = filepath.read_text(encoding="utf-8")
    original_content = content

    # Find all divs with background:var(--bg-2) containing IMAGE PLACEHOLDER text
    # Pattern: <div style="...background:var(--bg-2)...">...<p>IMAGE PLACEHOLDER — description</p>...</div>
    pattern = r'<div\s+style="[^"]*background:\s*var\(--bg-2\)[^"]*"[^>]*>.*?<p[^>]*>IMAGE PLACEHOLDER([^<]*)</p>.*?</div>'

    replaced_count = 0

    def replace_match(match):
        nonlocal replaced_count
        placeholder_div = match.group()
        placeholder_text = match.group(1)  # Captures " — description text"

        # Determine which image to use based on context
        image_id = get_image_id(slug, placeholder_text)
        alt_text = get_alt_text(image_id)

        # Build replacement HTML
        replacement = f'''<div style="border-radius: var(--r-lg); overflow: hidden; aspect-ratio: 16/9; margin: 32px 0;">
  <img src="https://images.unsplash.com/photo-{image_id}?auto=format&fit=crop&w=1600&q=75"
       alt="{alt_text}" loading="lazy" width="1600" height="900"
       style="width:100%;height:100%;object-fit:cover;display:block;" />
</div>'''

        replaced_count += 1
        return replacement

    # Use DOTALL flag to make . match newlines
    content = re.sub(pattern, replace_match, content, flags=re.DOTALL)

    if content != original_content:
        filepath.write_text(content, encoding="utf-8")
        return replaced_count
    return 0

# Process all project pages
project_files = [
    "side-return-camden.html",
    "dormer-loft-hackney.html",
    "double-storey-wandsworth.html",
    "garage-conversion-ealing.html",
    "hmo-conversion-hackney.html",
    "mansard-islington.html",
    "planning-regs-southwark.html",
    "basement-dig-kensington.html",
    "rear-dormer-lewisham.html",
    "wraparound-extension-wandsworth.html",
]

total_replaced = 0
for filename in project_files:
    filepath = PROJECTS_DIR / filename
    if filepath.exists():
        slug = filename.replace(".html", "")
        replaced = replace_placeholders(filepath, slug)
        if replaced > 0:
            print(f"[OK] {filename} — replaced {replaced} placeholder(s)")
            total_replaced += replaced
    else:
        print(f"[SKIP] {filename} — file not found")

print(f"\n[OK] Processed {len(project_files)} project pages — replaced {total_replaced} placeholder(s) total")
