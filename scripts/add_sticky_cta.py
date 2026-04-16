#!/usr/bin/env python3
"""
Adds a sticky CTA bar and exit-intent modal to all public HTML pages.

- Sticky CTA: fixed bottom bar, shows after 400px scroll, dismissable per session.
- Exit-intent modal: fires once per session on desktop when mouse leaves viewport top.
- Skips portal/, api/, node_modules/ directories.
- Skips files that already contain the <!-- STICKY-CTA --> marker.
- All CSS/JS is self-contained within the injected snippet.
"""

from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {"portal", "api", "node_modules", ".git"}
MARKER = "<!-- STICKY-CTA -->"

SNIPPET = r'''<!-- STICKY-CTA -->
<style>
/* ===== Sticky CTA Bar ===== */
.sticky-cta-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 80;
  background: rgba(14, 17, 22, 0.95);
  border-top: 2px solid var(--accent, #C8664A);
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  transform: translateY(100%);
  transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
  font-family: 'Manrope', sans-serif;
}
.sticky-cta-bar.visible { transform: translateY(0); }
.sticky-cta-bar-text {
  color: rgba(250, 250, 247, 0.9);
  font-size: 0.95rem;
  font-weight: 500;
  letter-spacing: -0.01em;
}
.sticky-cta-bar-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--accent, #C8664A);
  color: #fff;
  font-family: 'Manrope', sans-serif;
  font-size: 0.88rem;
  font-weight: 700;
  padding: 10px 22px;
  border-radius: var(--r-md, 16px);
  border: none;
  cursor: pointer;
  text-decoration: none;
  white-space: nowrap;
  transition: background 0.2s, transform 0.2s;
}
.sticky-cta-bar-btn:hover {
  background: var(--accent-deep, #9D4A32);
  transform: translateY(-1px);
}
.sticky-cta-bar-close {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: rgba(250, 250, 247, 0.5);
  font-size: 1.3rem;
  cursor: pointer;
  padding: 4px 8px;
  line-height: 1;
  transition: color 0.2s;
}
.sticky-cta-bar-close:hover { color: #fff; }
@media (max-width: 640px) {
  .sticky-cta-bar {
    flex-direction: column;
    gap: 10px;
    padding: 14px 48px 14px 16px;
    text-align: center;
  }
  .sticky-cta-bar-text { font-size: 0.88rem; }
}

/* ===== Exit-Intent Modal ===== */
.exit-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(14, 17, 22, 0.6);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}
.exit-overlay.active {
  opacity: 1;
  pointer-events: auto;
}
.exit-card {
  background: var(--surface, #FFFFFF);
  border-radius: var(--r-lg, 24px);
  max-width: 480px;
  width: 92%;
  padding: 40px 36px 32px;
  position: relative;
  transform: scale(0.95);
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1);
  box-shadow: 0 24px 60px rgba(14, 17, 22, 0.25), 0 8px 20px rgba(14, 17, 22, 0.12);
}
.exit-overlay.active .exit-card { transform: scale(1); }
.exit-card-close {
  position: absolute;
  top: 14px;
  right: 14px;
  background: none;
  border: none;
  color: var(--ink-soft, #4A5260);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 4px 8px;
  line-height: 1;
  transition: color 0.2s;
}
.exit-card-close:hover { color: var(--ink, #0E1116); }
.exit-card h3 {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.65rem;
  font-weight: 300;
  font-style: italic;
  font-variation-settings: "opsz" 72, "SOFT" 60;
  letter-spacing: -0.02em;
  color: var(--ink, #0E1116);
  margin: 0 0 10px;
}
.exit-card p {
  font-family: 'Manrope', sans-serif;
  font-size: 0.95rem;
  color: var(--ink-soft, #4A5260);
  line-height: 1.6;
  margin: 0 0 22px;
}
.exit-form {
  display: flex;
  gap: 8px;
}
.exit-form input[type="email"] {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid var(--line, rgba(14,17,22,0.08));
  border-radius: var(--r-md, 16px);
  font-family: 'Manrope', sans-serif;
  font-size: 0.9rem;
  color: var(--ink, #0E1116);
  background: var(--bg, #FAFAF7);
  outline: none;
  transition: border-color 0.2s;
}
.exit-form input[type="email"]:focus {
  border-color: var(--accent, #C8664A);
}
.exit-form button {
  background: var(--accent, #C8664A);
  color: #fff;
  font-family: 'Manrope', sans-serif;
  font-size: 0.85rem;
  font-weight: 700;
  padding: 12px 20px;
  border: none;
  border-radius: var(--r-md, 16px);
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.2s;
}
.exit-form button:hover { background: var(--accent-deep, #9D4A32); }
.exit-trust {
  font-family: 'Manrope', sans-serif;
  font-size: 0.78rem;
  color: var(--ink-soft, #4A5260);
  margin-top: 14px;
  text-align: center;
  opacity: 0.7;
}
.exit-success {
  text-align: center;
  padding: 12px 0 4px;
}
.exit-success p {
  font-size: 1.05rem;
  color: var(--ink, #0E1116);
  font-weight: 600;
}
@media (max-width: 480px) {
  .exit-card { padding: 32px 24px 24px; }
  .exit-form { flex-direction: column; }
}
</style>

<!-- Sticky CTA Bar -->
<div class="sticky-cta-bar" id="stickyCta" aria-label="Get a free quote">
  <span class="sticky-cta-bar-text">Free quote in 60 seconds &mdash; From &pound;840 fixed fee</span>
  <a href="/quote.html" class="sticky-cta-bar-btn">Get my free quote &rarr;</a>
  <button class="sticky-cta-bar-close" id="stickyCtaClose" aria-label="Dismiss">&times;</button>
</div>

<!-- Exit-Intent Modal -->
<div class="exit-overlay" id="exitOverlay">
  <div class="exit-card">
    <button class="exit-card-close" id="exitClose" aria-label="Close">&times;</button>
    <div id="exitContent">
      <h3>Before you go&hellip;</h3>
      <p>Get a free, no-obligation quote for your project. Fixed fees from &pound;840. MCIAT chartered.</p>
      <form class="exit-form" id="exitForm">
        <input type="email" name="exit_email" placeholder="Your email address" required autocomplete="email" />
        <button type="submit">Send my quote &rarr;</button>
      </form>
      <div class="exit-trust">98% first-time approval rate &middot; All 33 London boroughs</div>
    </div>
    <div id="exitSuccess" class="exit-success" style="display:none;">
      <p>Thanks! We&rsquo;ll be in touch within 24 hours.</p>
    </div>
  </div>
</div>

<script>
(function() {
  /* ---- Sticky CTA Bar ---- */
  var bar = document.getElementById('stickyCta');
  var closeBtn = document.getElementById('stickyCtaClose');
  if (bar && closeBtn) {
    var dismissed = false;
    try { dismissed = sessionStorage.getItem('__ad_sticky_dismissed') === '1'; } catch(e) {}
    if (!dismissed) {
      var onScroll = function() {
        if (window.scrollY > 400) { bar.classList.add('visible'); }
        else { bar.classList.remove('visible'); }
      };
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }
    closeBtn.addEventListener('click', function() {
      bar.classList.remove('visible');
      try { sessionStorage.setItem('__ad_sticky_dismissed', '1'); } catch(e) {}
      window.removeEventListener('scroll', onScroll);
    });
  }

  /* ---- Exit-Intent Modal ---- */
  var overlay = document.getElementById('exitOverlay');
  var exitCloseBtn = document.getElementById('exitClose');
  var exitForm = document.getElementById('exitForm');
  var exitContent = document.getElementById('exitContent');
  var exitSuccess = document.getElementById('exitSuccess');

  if (overlay && exitCloseBtn) {
    var exitFired = false;
    try { exitFired = sessionStorage.getItem('__ad_exit_fired') === '1'; } catch(e) {}

    function closeModal() {
      overlay.classList.remove('active');
      try { sessionStorage.setItem('__ad_exit_fired', '1'); } catch(e) {}
    }

    if (!exitFired && window.innerWidth > 768) {
      document.addEventListener('mouseout', function(e) {
        if (e.clientY <= 0 && !exitFired) {
          exitFired = true;
          overlay.classList.add('active');
          try { sessionStorage.setItem('__ad_exit_fired', '1'); } catch(e2) {}
        }
      });
    }

    exitCloseBtn.addEventListener('click', closeModal);
    overlay.addEventListener('click', function(e) {
      if (e.target === overlay) closeModal();
    });

    if (exitForm) {
      exitForm.addEventListener('submit', function(e) {
        e.preventDefault();
        if (exitContent) exitContent.style.display = 'none';
        if (exitSuccess) exitSuccess.style.display = 'block';
        setTimeout(closeModal, 3000);
      });
    }
  }
})();
</script>
<!-- /STICKY-CTA -->
'''


def should_skip(path: Path) -> bool:
    """Return True if this file is inside an excluded directory."""
    parts = path.relative_to(PROJECT).parts
    return any(p in EXCLUDE_DIRS for p in parts)


def main():
    html_files = sorted(PROJECT.rglob("*.html"))
    updated = 0
    skipped_marker = 0
    skipped_dir = 0

    for f in html_files:
        if should_skip(f):
            skipped_dir += 1
            continue

        content = f.read_text(encoding="utf-8")

        if MARKER in content:
            skipped_marker += 1
            continue

        if "</body>" not in content:
            print(f"[SKIP] {f.relative_to(PROJECT)} — no </body> tag found")
            continue

        # Insert snippet just before the LAST </body>
        idx = content.rfind("</body>")
        new_content = content[:idx] + SNIPPET + "\n" + content[idx:]
        f.write_text(new_content, encoding="utf-8")
        updated += 1
        print(f"[OK] {f.relative_to(PROJECT)}")

    print(f"\n=== Summary ===")
    print(f"  Updated:            {updated}")
    print(f"  Skipped (already):  {skipped_marker}")
    print(f"  Skipped (excluded): {skipped_dir}")
    print(f"  Total HTML found:   {len(html_files)}")


if __name__ == "__main__":
    main()
