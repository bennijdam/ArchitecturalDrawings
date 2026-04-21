# CLAUDE.md — Working on Architectural Drawings London

This file is read automatically by Claude Code at the start of each session. It gives you the context you need to work on this codebase effectively. Read it first.

## Session-zero non-negotiables

Before you change anything in this repository, treat the following as hard requirements:

1. **Design cannot be changed.** The site must retain **100% visual parity** unless the operator gives written approval for a specific visual change.
2. **Any new UI or UX must inherit the existing `index.html` design scheme.** Use it as the reference for logo treatment, header/menu structure, footer structure, buttons, spacing rhythm, typography, palette, card treatment, and interaction tone.
3. **Do not introduce a parallel design language.** No new button family, no new footer variant, no new menu pattern, no new font, and no new accent colour.
4. **Additive work must feel native.** New sections, forms, states, or flows should look like they shipped with the original site.
5. **When unsure, preserve.** If there is any tradeoff between a quick change and exact visual preservation, preserve the current visual system.
6. **All design work MUST be mobile responsive.** Any new section, component, form, modal, or page you add must work correctly at 375px, 480px, 768px, and 1200px viewport widths. Specifically:
   - Grids collapse to single column on phones (use `grid-template-columns: 1fr` at ≤480px or ≤600px as appropriate)
   - No horizontal overflow — test with `overflow-x: hidden` on body but also ensure nothing actually overflows
   - Touch targets ≥ 44px tall (padding: 12px+ on buttons and links)
   - Input `font-size` ≥ 16px (1rem) to prevent iOS auto-zoom
   - Fixed-position elements (nav, modals) must not obstruct content on small screens
   - Images use `max-width: 100%` and the full `<picture>` + `srcset` pattern
   - After adding any new layout, add the corresponding `@media (max-width: ...)` rule in `assets/css/style.css` AND in the inlined `<style>` block of every affected HTML file

---

## 1. What this project is

**Architectural Drawings London** is a website + portal + payment platform for an MCIAT-chartered architectural technology practice in London. It sells planning permission drawings, building regulations drawings, loft conversions, house extensions, mansard roofs, and adjacent services at fixed fees 30% below typical London architect rates.

- **Public domain (intended):** `architecturaldrawings.uk`
- **Stack:** Static HTML/CSS/vanilla JS frontend + Node.js/Express/SQLite backend, Stripe for payments, JWT for auth, multer for file uploads.
- **Design language:** Warm editorial minimalism. Fraunces (display serif) + Manrope (body sans). Cream/ink/terracotta palette. 20–36px rounded cards. Staggered scroll-triggered reveals.
- **SEO focus:** Local London (33 boroughs), service × borough keyword permutations, rich schema (LocalBusiness, FAQPage, Service, BreadcrumbList), long-tail service detail pages.

**What the site is NOT:** a single-page React app. Every page is a standalone HTML file. Resist any urge to "modernise" by converting to Next.js or a SPA framework — the current architecture is deliberate, fast, and SEO-optimal.

---

## 2. File structure

```
architectural-drawings/
├── index.html                     Landing page (hero, services, process, pricing, FAQ, boroughs, CTA)
├── services.html                  Services overview (60+ services in 5 categories)
├── services/
│   ├── planning-drawings.html     Detailed service page — the "template" pattern
│   ├── building-regulations.html
│   ├── loft-conversions.html
│   ├── house-extensions.html
│   └── mansard-roof.html
├── quote.html                     5-step quote flow (property → service → details → contact → review → success)
├── pricing.html                   Fixed-fee matrix + tiered cards
├── about.html                     Team + credentials + story (E-E-A-T)
├── search.html                    Client-side search over services + boroughs
├── portal/
│   ├── login.html                 JWT auth — email/password + Google/Apple SSO buttons
│   ├── register.html              Account creation
│   └── dashboard.html             Portal — stats, projects, file upload, Stripe Checkout
├── assets/
│   ├── css/style.css              Design system (~1,000 lines). SOURCE OF TRUTH for styling.
│   ├── js/app.js                  Reveals, nav scroll, FAQ, mobile menu, smooth scroll
│   ├── js/quote.js                Quote flow state machine + price calc
│   └── img/                       Responsive AVIF + WebP + JPEG @ 640/1024/1600/2400px
├── api/
│   ├── server.js                  Express entrypoint
│   ├── package.json
│   ├── .env.example
│   ├── models/db.js               SQLite schema (users, quotes, projects, files, payments)
│   ├── middleware/auth.js         JWT verify + role gating
│   └── routes/
│       ├── auth.js                Register, login, /me
│       ├── quotes.js              Public POST + admin GET
│       ├── projects.js            CRUD, JWT-gated
│       ├── files.js               Multer upload + secure download
│       └── stripe.js              Checkout session + webhook handler
├── robots.txt
├── sitemap.xml
├── README.md                      Deployment guide
├── CLAUDE.md                      (this file)
└── SETUP.md                       Step-by-step for provisioning third-party services
```

---

## 3. Critical architectural decisions

### 3.1 HTML files are BOTH standalone and assembly-based

Each `.html` file has its CSS **inlined in a `<style>` block** AND references `/assets/css/style.css`. Same for JavaScript.

**Why:** the site can be previewed as individual files (preview viewers can't resolve relative paths) AND deploys cleanly as a proper multi-file site on any static host.

**Consequence:** when you change CSS, you must update BOTH `assets/css/style.css` AND the inlined `<style>` block in every HTML file. Use the rebuild script (§7) rather than hand-editing 14 files.

### 3.2 CSS reveal safety net

Every page has this keyframe in the inlined CSS:

```css
@keyframes __ad_safety_in { to { opacity: 1; transform: none; } }
.reveal { animation: __ad_safety_in 0.01s linear 1.5s forwards; }
.reveal.in { animation: none; opacity: 1; transform: none; }
```

**Why:** the `.reveal` class starts at `opacity: 0`. The normal JS path adds `.in` via `IntersectionObserver` to fade content in. If JS fails for any reason, the keyframe forces everything visible after 1.5 seconds. Blank sections can't happen.

**Do not remove this.** If you ever need to modify reveal timing, keep the safety net intact.

### 3.3 No localStorage or sessionStorage in code run as artifacts

The portal uses `sessionStorage` for JWT tokens. This works in deployed production browsers but FAILS in Claude artifact sandboxes. If asked to render the portal as an artifact, replace sessionStorage with in-memory React state.

### 3.4 Images use the full `<picture>` + `srcset` pattern

```html
<picture>
  <source type="image/avif" srcset="assets/img/name-640.avif 640w, assets/img/name-1024.avif 1024w, ..." sizes="..." />
  <source type="image/webp" srcset="assets/img/name-640.webp 640w, ..." />
  <img src="assets/img/name-1600.jpg" alt="..." width="1600" height="945" />
</picture>
```

Always include explicit `width` and `height` attributes to prevent CLS. Critical hero images additionally have their 640px AVIF embedded as a base64 data URI in HTML (embedded at build time), so the preview viewer always shows the hero.

### 3.5 Service pages use a shared structural pattern

`services/planning-drawings.html` is the canonical long template. The other four service detail pages (`building-regulations`, `loft-conversions`, `house-extensions`, `mansard-roof`) are lighter variants generated by `/home/claude/gen_services.py`. If you need to regenerate them or add a new service, extend that script rather than hand-writing from scratch.

### 3.6 100% visual parity — do not break existing layouts

When adding features, sections, or modals to any existing page, the existing layout MUST remain pixel-identical. Specifically:

- **Treat `index.html` as the canonical visual reference.** Any new UI must reuse the same logo language, footer pattern, navigation treatment, button hierarchy, typography, and warm editorial styling already established there.
- **Do NOT wrap existing HTML in new container `<div>`s.** Adding a wrapper changes the DOM tree and can break CSS grid/flex layouts. Instead, add `class` or `data-*` attributes to existing elements and toggle visibility with CSS.
- **Do NOT override `.portal-main`, `.portal`, or other structural CSS.** If you need to suppress styles on child elements (e.g. `section { padding }` inherited from the global design system), use scoped selectors like `.portal-main section { padding: 0; }` rather than changing the parent.
- **Do NOT change media query breakpoints** unless you've verified the element lives in a context where the viewport width equals the content width. Inside the portal, the main area is `viewport minus 260px sidebar` — a 900px breakpoint on the viewport fires at 640px of actual content width.
- **Always test against the original** before committing. If in doubt, compare with `portal/dashboard-original.html` (the unmodified original kept for reference).
- **New sections go alongside existing content, not around it.** Use `display: none` / `display: block` toggling on sibling elements rather than `portal-section` wrapper divs.

---

## 4. Design system — the non-negotiables

### Palette (CSS variables in `assets/css/style.css`)

```
--bg:         #F5F8FF    (cool white, barely blue-tinted)
--bg-2:       #EBF0FB    (light blue-grey paper)
--surface:    #FFFFFF
--ink:        #0B1222    (deep navy-black)
--ink-soft:   #3B4F72
--line:       rgba(11, 18, 34, 0.08)
--accent:     #2563EB    (blueprint blue — the brand colour)
--accent-deep:#1D4ED8
--accent-soft:#EBF0FF
--success:    #47845A
```

### Typography

- **Display:** Fraunces (variable, `opsz` 60–144, `SOFT` 40–80) — USE italic for accent words in headers
- **Body:** Manrope (300–800 weights)

**Do not introduce:** Inter, Roboto, Arial, system-ui fonts. They're banned by the frontend-design guidelines. Do not introduce Space Grotesk either (it's become the new generic).

### Radius, shadow, motion tokens

```
--r-sm: 10px      --shadow-sm: 0 1px 2px rgba(...), 0 2px 6px rgba(...)
--r-md: 16px      --shadow-md: 0 4px 12px, 0 12px 32px
--r-lg: 24px      --shadow-lg: 0 24px 60px, 0 8px 20px
--r-xl: 36px      --shadow-glow: 0 20px 60px rgba(200, 102, 74, 0.18)

--ease: cubic-bezier(0.22, 1, 0.36, 1)
--ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1)
```

### Component patterns

- **Service card:** `.service-card` — rounded 24px, hover lift + accent glow corner radial
- **Pricing card:** `.pricing-card.popular` gets dark ink background, terracotta features ticks
- **Process step:** numbered circle + icon, dashed connector line
- **Testimonial:** large italic pull quote with oversized opening bracket

Copy the structural HTML from existing sections when adding new ones. Do not invent new components unless the task requires it.

### Footer SEO link grid

Every page must include a `.footer-seo` 4-column grid above the main footer content. This grid contains keyword-rich links to service pages and borough-specific service pages, matching the pattern used by top-ranking competitors (Extension Architecture, LCCL, Crown Architecture).

```
.footer-seo (4-column grid, collapses to 2 then 1 on mobile)
├── Services in London (10 keyword links to /services/*.html)
├── Loft conversions by borough (10 links to /areas/{borough}/loft-conversions.html)
├── Extension plans by borough (12 links to /areas/{borough}/house-extensions.html)
└── Planning drawings by borough (11 links to /areas/{borough}/planning-drawings.html)
```

- **CSS:** `.footer-seo` is defined in `assets/css/style.css` AND must be inlined in every HTML page's `<style>` block.
- **pSEO pages:** use a condensed 5-link version per column (defined in `gen_pseo.py`).
- **Path prefixes:** root pages use no prefix, `/services/` and `/blog/` pages use `../`, pSEO pages use absolute `/` paths.
- When adding new pages, always include the footer-seo block. Use `scripts/add_seo_footer.py` to batch-add it.

---

## 5. Backend conventions

- **ES modules** (`"type": "module"` in `api/package.json`). Use `import`/`export`, not `require`.
- **SQLite via `better-sqlite3`** — synchronous prepared statements. Swap for Postgres (`pg`) when moving beyond a single node.
- **JWT auth** via `middleware/auth.js`. Routes that need auth: `router.get('/', requireAuth, handler)`.
- **express-validator** on every public POST. Never trust untyped `req.body`.
- **Stripe webhook** MUST be mounted BEFORE `express.json()` in `server.js` so signature verification works on raw body. Do not refactor this order.
- **Rate limiting** at `/api/` level: 100 req / 15 min per IP. Raise only with clear need.
- **File uploads** via `multer` — max 100 MB, allowlist of extensions in `routes/files.js`. Do not allow arbitrary MIME types.
- **Errors:** throw with `.status = 400/401/404/etc.` and let the global error handler serialize. Don't `res.status().json()` in nested promise chains.

Example route skeleton:

```javascript
router.post('/',
  requireAuth,
  body('title').isLength({ min: 1, max: 200 }).trim().escape(),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ error: 'Validation failed' });
    const db = getDb();
    // ... prepared statement ...
    res.status(201).json({ id: ... });
  }
);
```

---

## 6. Common tasks

### 6.1 Add a new service detail page

1. Add an entry to the `SERVICES` dict in `/home/claude/gen_services.py` following the existing shape (title, h1, lede, price, whats_included list of tuples, faqs list of tuples).
2. Run `python3 /home/claude/gen_services.py`.
3. Add the new page to `sitemap.xml` and to the services overview in `services.html`.
4. Re-run the inline-CSS build (§7) so the new page gets the current stylesheet.

### 6.2 Add a new backend route

1. Create `api/routes/foo.js` following the auth/quotes pattern.
2. Mount in `api/server.js`: `app.use('/api/foo', fooRouter);`.
3. If the route needs a new DB table, add the CREATE TABLE to `api/models/db.js`.
4. Test: `cd api && npm start`, then curl.

### 6.3 Add or update an image

1. Put the source JPEG in `/mnt/user-data/uploads/` (or any path).
2. Run `/home/claude/optimize_images.sh` after updating the `IMAGES` map. Produces AVIF + WebP + JPEG at 640/1024/1600/2400 widths.
3. Reference with the full `<picture>` pattern (§3.4). Always include `width`, `height`, and descriptive `alt`.
4. AVIF target at 1600px should be under 80 KB. If larger, raise `-crf` toward 36 in `optimize_images.sh`.

### 6.4 Update branding (logo / name / colour)

Never hand-edit 14 HTML files. Use `/home/claude/rebrand.py` as a template — it does ordered string replacements across all HTML/JS/MD files. Add new tuples to its `REPLACEMENTS` list.

### 6.5 Change a CSS token (e.g. accent colour)

1. Edit `assets/css/style.css` — change the `:root` custom property.
2. Re-run the CSS inliner (`/home/claude/inline_assets.py` pattern) so every HTML file picks up the change.
3. Verify with grep that no page has a stale inlined copy.

### 6.6 Regenerate all pSEO pages

The site has **199 programmatic SEO pages** under `/areas/` (33 boroughs × 5 services + 33 hubs + 1 master index). These are generated from data + templates, not hand-written.

Generator files (in `scripts/`):
- `pseo_boroughs.py` — data for all 33 London boroughs (Article 4 status, conservation areas, housing stock, adjacent boroughs, basement policy, etc.)
- `pseo_services.py` — 5 core services with location-placeholder copy and FAQ templates
- `gen_pseo.py` — the template + renderer
- `gen_sitemap.py` — rebuilds `sitemap.xml` with all 209 URLs

To regenerate after any data/template change:

```bash
cd architectural-drawings
python3 scripts/gen_pseo.py          # writes /areas/*/*.html
python3 scripts/gen_sitemap.py       # refreshes sitemap.xml
```

**To add a new service** (e.g. "basement conversions"):
1. Add service dict entry to `scripts/pseo_services.py` following the existing shape (name, summary with `{location}` placeholders, 5 `local_faqs` with placeholders, etc.)
2. Run `python3 scripts/gen_pseo.py` — adds 33 new pages (one per borough)
3. Run `python3 scripts/gen_sitemap.py`
4. Add a link from the borough hub template (already auto-links any service in `SERVICE_SLUGS`)

**To add a new location** (e.g. a town outside London):
1. Add borough dict entry to `scripts/pseo_boroughs.py` with the planning-specific local facts (council, Article 4, conservation areas, housing stock, adjacent boroughs)
2. Run both generators
3. Update `/areas/` master index automatically picks it up

**pSEO page structure** — each page has these SEO/AEO/GEO elements (do not remove):
- **H1** with exact-match keyword ("Loft Conversions in Camden")
- **TL;DR box** with 6 quick facts (for AEO/featured snippets)
- **Local context paragraphs** with verifiable facts (GEO-friendly for AI citations)
- **What's included** cards with location placeholders filled
- **Pricing** tier cards with location-specific council name
- **Location-specific FAQ** (5 questions, all answering local-intent queries)
- **Nearby boroughs** cards (internal linking for SEO)
- **Other services in this location** cards (internal linking)
- **Schema:** Service, FAQPage, BreadcrumbList (all generated from data)

Do not hand-edit individual pSEO pages — changes won't survive the next regeneration. Always edit the data or template and regenerate.


---

## 7. Development commands

```bash
# Frontend — serve locally
cd architectural-drawings
npx serve .                              # or: python3 -m http.server 8080

# Backend — run with hot reload
cd architectural-drawings/api
cp .env.example .env                     # fill in secrets
npm install
npm run dev                              # uses node --watch

# Tests — there are currently no automated tests. If adding:
# - Use Vitest for backend (lightweight, ESM-native).
# - Use Playwright for e2e if needed.

# Regenerate service detail pages
python3 /home/claude/gen_services.py

# Re-optimize images
bash /home/claude/optimize_images.sh

# Re-inline CSS + JS into every HTML after source changes
python3 /home/claude/inline_assets.py    # or the equivalent updated script

# Syntax-check backend
for f in api/server.js api/routes/*.js api/middleware/*.js; do node --check "$f"; done
```

---

## 8. SEO invariants (don't break these)

1. **Every page has a unique `<title>` and `<meta name="description">`.** Title 50–60 chars, description 150–160 chars.
2. **Every page has a `<link rel="canonical">`.** Absolute URL, no trailing slash after `.html`.
3. **Landing page has LocalBusiness + FAQPage + BreadcrumbList schema.** Service detail pages have Service + FAQPage schema.
4. **All 33 London boroughs link from the landing page** — this is local-SEO weight.
5. **Service pages link to their pricing tier in the quote flow** via query params: `quote.html?service=loft&tier=complete`.
6. **`robots.txt` disallows `/portal/` and `/api/`** but allows everything else.
7. **`sitemap.xml` lists every public page** with `lastmod` and `priority`. Update when adding pages.

---

## 9. Brand copy guidelines

- **MCIAT chartered** is the core authority claim. Mention it in hero lede, service pages, about page, credentials block.
- **"30% below London architects"** is the price hook. Repeat in hero, pricing page, service pages.
- **"98% first-time approval rate"** is the outcome claim.
- **All 33 London boroughs** — phrase exactly this way, never "all London boroughs" (less specific).
- **Fees:** Essentials from £840, Complete from £1,750, Loft from £1,225, Mansard from £1,575. Never round these without updating schema, pricing table, service cards, quote.js price map, and the README.
- **Contact:** 86–90 Paul Street, London EC2A 4NE · 020 7946 0000 · hello@architecturaldrawings.uk. The phone number and address are placeholders — confirm with the user before shipping production.
- **CIAT / ICO / Companies House numbers in `about.html` are placeholders.** Swap for real values before going live.

---

## 10. Gotchas and things you'll waste time on

### The preview viewer problem
Preview viewers in chat interfaces can't resolve `assets/css/style.css` or `<picture>` `srcset`. That's why the site inlines CSS and base64-encodes hero images. If someone says "the site is broken / blank," ask if they're viewing a file in a preview tool or a deployed URL.

### The CSS/HTML duplication
Changing a CSS variable requires updating it in 14 HTML files AND the external stylesheet. Always use the inliner script. Grep after to make sure no page has a stale copy:

```bash
grep -r "old-value" architectural-drawings/*.html architectural-drawings/services/ architectural-drawings/portal/
```

### Stripe raw-body gotcha
`server.js` mounts the webhook with `express.raw()` BEFORE `express.json()`. If you refactor middleware order, signature verification silently fails and webhook events are rejected.

### Quote flow price calc
`assets/js/quote.js` has a `servicePrices` map and `tierMultiplier` map. These are the source of truth for the quote-flow price. They must stay in sync with `pricing.html` and the service cards on `services.html`. If you change one, change all three.

### Font loading
Fraunces is loaded from Google Fonts with specific axis ranges (`opsz,wght,SOFT`). Do not swap to a generic Fraunces load — you'll lose the soft-vs-hard serif variation that gives the hero headings their character.

### The `<details>` FAQ elements
FAQs use native `<details>` + `<summary>` for accessibility. The `.open` class is toggled by a JS listener. Don't replace with custom JS accordions — you'll lose keyboard operability.

### Localstorage vs sessionStorage
The portal uses sessionStorage so the user is logged out when they close the tab. This is intentional for a B2C architectural practice (low-frequency visits, public computers possible). If the user asks for "remember me," implement it as a server-side longer-lived JWT, not as localStorage.

---

## 11. When uncertain, ask

This codebase was built with specific choices for specific reasons. If a task seems like it should be simpler (e.g., "why isn't this just Next.js?"), ask the user before refactoring. The reasons are usually: SEO performance, preview-viewer compatibility, or deliberate simplicity over feature count.

---

**End of CLAUDE.md.** Now go build.
