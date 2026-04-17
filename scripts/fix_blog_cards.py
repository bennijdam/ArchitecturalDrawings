#!/usr/bin/env python3
"""Replace IMAGE PLACEHOLDER divs in blog/index.html card-img with Unsplash images."""
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent

# Unsplash image mapping for blog hub cards (link -> (image ID, alt text))
BLOG_CARD_IMAGES = {
    "planning-permission-london.html": ("photo-1503387762-592deb58ef4e", "Planning application drawings and blueprints"),
    "building-regulations-explained.html": ("photo-1541888946425-d81bb19240f5", "Building control site inspection"),
    "architect-vs-architectural-technologist.html": ("photo-1484154218962-a197022b5858", "Architect working with digital tablet"),
    "planning-vs-permitted-development.html": ("photo-1503387762-592deb58ef4e", "Planning application documents"),
    "planning-drawings-cost-london.html": ("photo-1504307651254-35680f356dfd", "Structural drawing on desk"),
    "extension-cost-guide-london.html": ("photo-1600566753190-17f0baa2a6c3", "Modern home extension"),
    "loft-vs-mansard.html": ("photo-1600585154340-be6161a56a0c", "Loft bedroom conversion"),
}

def fix_blog_index():
    """Replace blog card IMAGE PLACEHOLDER divs with Unsplash image tags."""
    filepath = SCRIPT_DIR / "blog" / "index.html"
    content = filepath.read_text(encoding="utf-8")
    original_content = content

    replaced_count = 0

    for link, (image_id, alt_text) in BLOG_CARD_IMAGES.items():
        # Pattern: find <a href="LINK" ...> ... <div class="card-img"><p>IMAGE PLACEHOLDER...</p></div>
        # We'll match from href to the closing </a>

        # Build a pattern that finds the specific href and its card-img div
        # Using a simpler approach: find the href line, then find the next card-img with IMAGE PLACEHOLDER

        lines = content.split('\n')
        result_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]
            result_lines.append(line)

            # Check if this line has the href we're looking for
            if f'href="{link}"' in line:
                # Now look for the next <div class="card-img"> with IMAGE PLACEHOLDER
                j = i + 1
                found_card = False

                while j < len(lines) and j < i + 20:  # Search next 20 lines max
                    next_line = lines[j]

                    if '<div class="card-img">' in next_line and j + 1 < len(lines):
                        # Check if the next line has IMAGE PLACEHOLDER
                        next_next_line = lines[j + 1]
                        if 'IMAGE PLACEHOLDER' in next_next_line:
                            # Found it! Replace the card-img div and its content
                            new_card_img = f'        <div class="card-img"><img src="https://images.unsplash.com/photo-{image_id}?auto=format&fit=crop&w=600&q=75" alt="{alt_text}" width="600" height="200" style="width:100%;height:100%;object-fit:cover;display:block;" /></div>'
                            result_lines.append(new_card_img)

                            # Skip the old <div class="card-img">, <p>IMAGE PLACEHOLDER...</p>, and closing </div>
                            j += 3  # Skip <div>, <p>IMAGE PLACEHOLDER</p>, </div>
                            found_card = True
                            replaced_count += 1
                            break

                    if '</a>' in next_line and not found_card:
                        # We've reached the end of the card link without finding card-img
                        break

                    if not found_card:
                        result_lines.append(next_line)

                    j += 1

                # Continue from where we left off
                i = j - 1  # -1 because we'll increment at the end

            i += 1

        content = '\n'.join(result_lines)

    if content != original_content:
        filepath.write_text(content, encoding="utf-8")
        print(f"[OK] blog/index.html — replaced {replaced_count} card image(s)")
        return replaced_count
    else:
        print("[SKIP] blog/index.html — no changes made")
        return 0

if __name__ == "__main__":
    fix_blog_index()
