# HANDOVER.md — Architectural Drawings London

> **Handover protocol (mandatory):** every agent, at the end of every task, appends a new entry at the TOP of the "Agent handover log" section below. UTC timestamp, self-identify as `Author:`, use the template in `.codex/GUARDRAILS.md` §6. No entry = the work didn't happen. Full rules in [.codex/GUARDRAILS.md](.codex/GUARDRAILS.md#6-handovermd--mandatory-post-task-update).

---

## Agent handover log

## 2026-04-21 — Stripe return handling verified and patched

**Author:** Codex
**Task:** Verify live Stripe Checkout return URLs and close the missing dashboard return-state handling.
**Scope touched:** portal/dashboard.html, HANDOVER.md.
**Result:** partially shipped locally. Live Stripe Checkout exposes the correct return targets: `dashboard.html?payment=success` and `dashboard.html?payment=cancelled`. Browser verification confirmed the cancel path lands on the dashboard route, but the dashboard had no logic to read the `payment` query param. Added a native-status banner in the payments section so successful or cancelled returns now surface clear feedback and then clean the URL. During the same verification pass, a fresh live checkout-session creation attempt intermittently returned HTTP 500 `Could not create checkout session`, so the redirect targets are now understood but the session-creation instability still needs Render-side investigation.
**Next action for the next agent:** Commit and push the dashboard return-state fix, then inspect Render logs/env for the intermittent Stripe checkout 500.
**Links:** portal/dashboard.html, api/routes/stripe.js

## 2026-04-21 — Auth hardening deployed and reverified

**Author:** GitHub Copilot
**Task:** Deploy the auth hardening and Neon/Postgres support changes, then re-test the live production reset and Stripe flows.
**Scope touched:** HANDOVER.md (this entry only).
**Result:** shipped. Commit 415e1ae was pushed to origin/main and matched the remote head. Production now serves `portal/reset`, invalid reset tokens return the expected API-backed error state, and the authenticated Stripe checkout endpoint now returns a live session URL instead of 404. Direct `/uploads` access was already returning 404 from the deployed API.
**Next action for the next agent:** Run a full browser-level Stripe redirect success/cancel pass and then decide whether to commit the remaining untracked documentation files separately.
**Links:** portal/reset.html, api/routes/stripe.js, api/server.js, portal/login.html, portal/register.html

## 2026-04-21 — Full production readiness audit

**Author:** Codex
**Task:** Perform a full production-readiness audit across frontend, backend, database, API wiring, authentication, and E2E flows; add missing agent/runtime guidance docs.
**Scope touched:** CLAUDE.md (strengthened visual-parity guardrails), AGENTS.md (session-start instructions), ARCHITECTURE.md (new), OPENAI.md (new), TODO.md (new), HANDOVER.md (this entry).
**Result:** shipped. Existing agent docs already existed; they were tightened to make visual parity non-negotiable and to force new UI/UX to inherit the `index.html` design language. Added architecture and OpenAI-specific instructions plus a repo todo list based on concrete audit findings.
**Next action for the next agent:** Execute `TODO.md` in priority order, starting with auth reset completion, removing production demo fallbacks, and closing upload/static file exposure. Validate each fix against live flows before expanding scope.
**Links:** CLAUDE.md, AGENTS.md, ARCHITECTURE.md, OPENAI.md, TODO.md

## 2026-04-17 — Codex setup author

**Author:** Codex Setup (initial scaffolding, performed by Claude Opus 4.7)
**Task:** Scaffold the Codex/Paperclip agent framework for Architectural Drawings London as a new company, isolated from Tradematch.
**Scope touched:** AGENTS.md (new), .codex/GUARDRAILS.md (new), .codex/PAPERCLIP_SETUP.md (new), .codex/SKILLS.md (new), .codex/agents/README.md (new), .codex/agents/seo-strategist.md (new), .codex/agents/backlink-hunter.md (new), .codex/agents/content-writer.md (new), .codex/agents/outreach-specialist.md (new), .codex/agents/social-media-manager.md (new), .codex/agents/local-seo-auditor.md (new), .codex/agents/pseo-optimiser.md (new), HANDOVER.md (appended protocol header + this entry).
**Result:** shipped. Seven agent specs in place, skills catalogue written, Paperclip workspace runbook drafted, guardrails locked (100% visual parity, no stack changes, full Tradematch isolation). No design, framework, or copy changes to existing site — additive only.
**Next action for the next agent:** Operator to execute `.codex/PAPERCLIP_SETUP.md` §1–§7 (workspace creation, repo link, secrets, domain/GA4/GSC/GBP setup, social handle claiming, agent provisioning, isolation smoke test). Once live, SEO Strategist runs the v1 topical map as described in PAPERCLIP_SETUP.md §8 kickoff.
**Links:** AGENTS.md, .codex/PAPERCLIP_SETUP.md, .codex/agents/README.md

---

**Last updated:** 2026-04-16
**Status:** Site fully built with 710 URLs across 2 sub-sitemaps, SEO/AEO/GEO optimised. UK-wide coverage: 33 London boroughs + 120 London neighbourhoods + 30 M25 commuter belt towns (Guildford, Watford, St Albans, Oxford, etc.) + 12 major UK cities (Manchester, Birmingham, Leeds, Liverpool, Bristol, Edinburgh, Glasgow, Brighton, Cambridge, Oxford, Bath, York). 135 blog posts, 10 case studies, 3 cornerstone guide hubs, 5 property-type hubs, team hub, FAQ hub, glossary, resources hub, why-us, stats, 364 pSEO pages. 5 interactive tools. Real Unsplash stock images on 155+ content pages. GEO: llms.txt for AI agents. PWA: service worker + manifest + offline + 404. Conversion: sticky CTA + exit-intent + WhatsApp FABs + chat widget + callback forms + counters + testimonials. 100% schema coverage, zero invalid JSON-LD.

---

## What has been done

### Phase 1: File extraction and directory structure
- Extracted all 75 files from `files (75).zip` (41 unique files including pSEO borough pages)
- Created the full directory structure per CLAUDE.md specification:

```
architectural-drawings/
├── index.html                     Landing page (147 KB — hero, services, process, pricing, FAQ, boroughs, CTA)
├── services.html                  Services overview (62 KB — 60+ services in 5 categories)
├── quote.html                     5-step quote flow (64 KB)
├── pricing.html                   Fixed-fee matrix + tiered cards (59 KB)
├── about.html                     Team + credentials + story (54 KB)
├── search.html                    Client-side search (49 KB)
├── services/
│   ├── planning-drawings.html     Canonical service template (59 KB)
│   ├── building-regulations.html  (54 KB)
│   ├── loft-conversions.html      (54 KB)
│   ├── house-extensions.html      (54 KB)
│   └── mansard-roof.html          (54 KB)
├── portal/
│   ├── login.html                 JWT auth (44 KB)
│   ├── register.html              Account creation (43 KB)
│   └── dashboard.html             Portal — stats, projects, uploads, Stripe (49 KB)
├── assets/
│   ├── css/style.css              Design system (38 KB, ~1,000 lines)
│   ├── js/app.js                  Reveals, nav, FAQ, mobile menu (3 KB)
│   ├── js/quote.js                Quote flow state machine + price calc (8 KB)
│   └── img/                       (empty — images to be added)
├── api/
│   ├── server.js                  Express entrypoint (3 KB)
│   ├── package.json               14 dependencies, ES modules
│   ├── .env.example               Template with all required env vars
│   ├── .env                       Local copy (gitignored)
│   ├── models/db.js               SQLite schema (3 KB)
│   ├── middleware/auth.js          JWT verify + role gating (1 KB)
│   ├── routes/
│   │   ├── auth.js                Register, login, /me (2 KB)
│   │   ├── quotes.js              Public POST + admin GET (3 KB)
│   │   ├── projects.js            CRUD, JWT-gated (2 KB)
│   │   ├── files.js               Multer upload + secure download (3 KB)
│   │   └── stripe.js              Checkout session + webhook handler (4 KB)
│   └── node_modules/              156 packages installed
├── areas/                         199 pSEO pages (generated by gen_pseo.py)
│   ├── index.html                 Master borough index — all 33 boroughs
│   ├── camden/                    (hub + 5 service pages per borough)
│   ├── islington/
│   ├── hackney/
│   ├── westminster/
│   ├── ... (33 borough dirs total, each with index.html + 5 service pages)
│   └── city-of-london/
├── gen_pseo.py                    pSEO page generator (43 KB)
├── gen_sitemap.py                 Sitemap regenerator (2 KB)
├── pseo_boroughs.py               33 borough data (33 KB)
├── pseo_services.py               5 service templates (16 KB)
├── robots.txt                     Disallows /portal/ and /api/
├── sitemap.xml                    All public URLs (38 KB)
├── vercel.json                    Frontend deploy config (clean URLs, caching headers)
├── .vercelignore                  Excludes api/, *.md, *.py from frontend deploy
├── .gitignore                     Excludes node_modules, .env, data, uploads
├── README.md                      Deployment guide (9 KB)
├── CLAUDE.md                      Agent working instructions (19 KB)
├── SETUP.md                       Third-party provisioning runbook (27 KB)
└── HANDOVER.md                    (this file)
```

### Phase 2: Tech stack setup
- **Git:** Initialized repo with 44 tracked files, `.gitignore` configured
- **Node.js API:** `npm install` completed — 156 packages, all 8 JS files pass `node --check`
- **Vercel config:** `vercel.json` with clean URLs, cache headers, redirect rules
- **Vercel ignore:** `.vercelignore` excludes API and build scripts from frontend deploy
- **Local dev:** `.env` created from `.env.example` (placeholder values — needs real secrets)

### Phase 3: Backend verification
- All backend files syntax-checked and passing:
  - `api/server.js` — Express entrypoint with Stripe raw-body before express.json()
  - `api/middleware/auth.js` — JWT verify, role gating, token signing
  - `api/models/db.js` — SQLite schema (users, quotes, projects, files, payments)
  - `api/routes/auth.js` — Register, login, /me endpoints
  - `api/routes/quotes.js` — Public quote submission + admin listing
  - `api/routes/projects.js` — CRUD with JWT gating
  - `api/routes/files.js` — Multer upload with extension allowlist
  - `api/routes/stripe.js` — Checkout session creation + webhook handler

### Phase F: Monitoring account provisioning (completed 2026-04-15)

**Verified live in browser:**
- **Plausible** account login succeeded and the dashboard shows the site `architecturaldrawings.uk`
- **Sentry** account login succeeded and the project feed is visible under the `architecturaldrawings` organization

### SEO/AEO/GEO Audit + Priority 1 & 2 fixes (completed 2026-04-14)

**Full 4-stream audit run:** on-page SEO, AEO/GEO readiness, local London SEO, technical SEO + content gaps.

**Priority 1 fixes (applied):**
- Mansard H1: added "in London" for keyword match
- Building-regs hero: added "MCIAT chartered" to opening lede
- Homepage: replaced 33 `search.html?q=` borough links with direct `/areas/{borough}/` links
- LocalBusiness schema: added all 33 boroughs as individual `AdministrativeArea` objects in `areaServed`
- OG tags: added to 8 core pages missing them (services, pricing, about, 5 service detail pages)
- `dateModified`: added to schema blocks on index.html and all 5 service pages
- `app.set('trust proxy', 1)` added to server.js for CDN/proxy deployments
- Password reset: full `/api/auth/reset-password` + `/confirm` routes with token table, email, 1-hour expiry
- Title tags tightened: all primary pages now 50-57 chars

**Priority 2 fixes (applied):**
- TL;DR quick-fact boxes added to all 5 service detail pages (price, turnaround, includes, coverage, approval rate, team)
- Borough links: 12 top-borough links + "All 33 boroughs" CTA added to all 5 service pages
- Cross-service internal links: each service page now links to the other 4 services
- PI insurance: "£2m PI insured" badge added to hero-trust on all 5 service pages
- Homepage hero: "From £840 fixed fee" trust badge added
- Image alt text: improved across all 5 service pages + index.html with keyword-rich descriptions

### SEO Footer link grid (completed 2026-04-14)
- Added `.footer-seo` 4-column keyword link grid to ALL pages (matching Crown Architecture / competitor pattern)
- 4 columns: "Services in London" (10 links), "Loft conversions by borough" (10 links), "Extension plans by borough" (12 links), "Planning drawings by borough" (11 links)
- CSS added to `assets/css/style.css` and inlined in all HTML pages
- Applied to: 8 root pages, 5 service pages, 5 blog pages, 2 project pages, 199 pSEO pages (via gen_pseo.py)
- Created `scripts/add_seo_footer.py` for batch-applying to new pages
- Updated CLAUDE.md §4 with footer-seo documentation

**Priority 3 content (completed 2026-04-14):**
- `/blog/` hub page with 4 article cards → updated to 8 cards (2026-04-16)
- `/blog/planning-permission-london.html` — 7,900+ word pillar guide, 13 sections, 8 FAQs, all 33 boroughs linked, pricing tables, Article schema
- `/blog/building-regulations-explained.html` — 6,700+ word guide, Approved Documents A-R table, Part L/B detail, 6 FAQs
- `/blog/architect-vs-architectural-technologist.html` — 5,300+ word comparison, 3 cost tables, 5 FAQs
- `/blog/planning-vs-permitted-development.html` — 8,500+ word disambiguation, PD Class A-E limits, LDC costs, comparison table, 6 FAQs
- `/projects/` hub page with 5 project cards
- `/projects/side-return-camden.html` — full case study (brief, challenge, approach, result, planning ref PA/2025/03421)
- All articles have: FAQPage schema, Article schema, BreadcrumbList, OG tags, author byline, TL;DR boxes, placeholder images, internal links, "Last updated: April 2026"
- Sitemap updated to 243 URLs

### Content expansion + SEO hardening (completed 2026-04-16)

**4 new blog posts added:**
- `/blog/planning-drawings-cost-london.html` — 2,500+ word cost guide with breakdown by project type, DIY vs professional, FAQ
- `/blog/extension-cost-guide-london.html` — 2,500+ word extension cost guide with per-sqm pricing, hidden costs, borough variations
- `/blog/loft-vs-mansard.html` — 2,000+ word comparison, build costs, planning requirements, ROI, borough preferences
- `/blog/drawing-service-vs-architect.html` — 2,000+ word three-way comparison (drawing service vs architect vs technologist), cost tables
- All 4 posts have: Article + FAQPage + BreadcrumbList schema, OG tags, WhatsApp FABs, dark footer-seo grid, dateModified

**Team/author hub page:**
- `/team/index.html` — 3 team member profiles with Person schema (name, jobTitle, worksFor, knowsAbout, alumniOf, memberOf)
- "Why chartered matters" section explaining MCIAT credentials
- Responsive 3-column grid with credential badges

**Blog hub updated:**
- Fixed broken links (Cards 2-4 pointed to non-existent pages)
- Added 4 new article cards (planning drawings cost, extension cost, loft vs mansard, drawing service vs architect)
- Now 8 article cards total

**WhatsApp + Phone FABs on pSEO pages:**
- Added inline-styled FAB (phone + WhatsApp) to all 3 gen_pseo.py templates (service-location, borough hub, master index)
- Regenerated all 199 pSEO pages with location-specific WhatsApp messages
- Total: every public page on the site now has contact FABs

**Sitemap:**
- `gen_sitemap.py` updated with 4 new blog posts + team page
- `lastmod` updated to 2026-04-16
- Regenerated: 243 URLs total

### Service expansion + conversion optimisation (completed 2026-04-16)

**5 new services added to pSEO:**
- `garage-conversions` — from £995, garage-to-habitable drawings + building regs
- `basement-conversions` — from £1,950, underpinning + waterproofing + Party Wall
- `structural-calculations` — from £350, standalone structural engineering (beams, foundations, lintels)
- `party-wall` — from £450, Party Wall Act notices + schedule of condition + award support
- `rear-dormer` — from £1,225, full-width rear dormer loft conversions (PD or planning route)

Each service × 33 boroughs = **165 new service-location pages**.
Total pSEO pages: **364** (10 services × 33 boroughs + 33 hubs + 1 master index).
Sitemap: **408 URLs** (up from 243).

**Sticky CTA bar added to all pages:**
- Fixed bottom bar appears after 400px scroll: "Free quote in 60 seconds — From £840 fixed fee"
- Dismissable per session (sessionStorage), z-index 80 (below WhatsApp FABs)
- Accent-colored CTA button linking to /quote.html

**Exit-intent modal added to all pages:**
- Triggers on mouse-leave (desktop only, >768px viewport)
- One-time per session (sessionStorage)
- Email capture form with "Send my quote →" CTA
- Trust signals: "98% first-time approval rate · All 33 London boroughs"
- Success state on submit

### Technical SEO quick wins + content pages (completed 2026-04-16)

**Schema enhancements:**
- Organization schema added to `about.html` (ProfessionalService type, CIAT membership, knowsAbout, social profiles)
- BreadcrumbList schema added to `about.html`
- Review schema added to `index.html` (3 testimonials as individual Review objects with ratings)
- Person schema already present on `team/index.html` (3 team members)

**E-E-A-T signals:**
- Cross-link: about.html now links to `/team/` ("Meet the full team →")
- `rel="author"` added to all 9 blog HTML files pointing to `/team/`
- `hreflang="en-GB"` added to all 409 pages + gen_pseo.py templates

**New content pages:**
- `/faq/index.html` — 40+ FAQs consolidated from across the site, 6 sections, FAQPage schema, AEO-optimized for featured snippets
- `/glossary/index.html` — 50+ planning and building terms, alphabetical with A-Z jump nav, DefinedTermSet schema, definition-intent SEO

**Sitemap:** 410 URLs (up from 408)

### Interactive cost calculator (completed 2026-04-16)

- `/calculator/index.html` — 4-step interactive tool (2,159 lines):
  - Step 1: 12 project types with visual cards and SVG icons
  - Step 2: Property details (type, area, borough dropdown, conservation/listed status)
  - Step 3: Package tier selector (Essentials/Complete/Bespoke) with live price recalculation
  - Step 4: Full cost breakdown (drawing fee, council fee, structural, build cost estimate, total range)
- Shareable URL via query params (`?type=loft&property=terraced&area=50-100&borough=camden&tier=complete`)
- Print button, share button (copies URL), "Get your exact quote" CTA
- WebApplication schema, BreadcrumbList, OG tags
- Linked from homepage hero ("Cost calculator" button) and pricing page CTA
- Sitemap: 411 URLs

### Content expansion phase (completed 2026-04-16)

**34 new neighbourhood pages** (total: 50):
- Generated via `scripts/gen_neighbourhoods.py` from data dict
- New areas: Shoreditch, Dalston, Camden Town, Kentish Town, Belsize Park, Finsbury Park, Holloway, Tooting, Balham, Bermondsey, Streatham, Herne Hill, Blackheath, Deptford, Woolwich, Bow, Bethnal Green, Acton, Twickenham, Teddington, Wembley, Kilburn, Tottenham, Wood Green, Walthamstow, Sydenham, Forest Hill, East Dulwich, Earlsfield, Putney, Barnes, Maida Vale, Hackney Wick, Queens Park
- Each page: Service + FAQPage + BreadcrumbList schema, 5 location-specific FAQs, nearby neighbourhoods grid, borough service links

**8 new blog posts** (total: 16):
- Kitchen extension cost London (side return vs rear, build costs, kitchen fitting)
- Permitted development rules 2026 (Class A-E limits, Prior Approval, Article 4)
- Planning permission refused — what next (resubmission, appeal, redesign)
- Side return extension London guide (costs, structural, Party Wall, design tips)
- Loft conversion without planning (PD rules, LDC process, when PD removed)
- Choosing an architect in London (RIBA vs CIAT, fee structures, red flags)
- Part L building regulations guide (U-values, SAP, MVHR, Future Homes Standard)
- Conservation area planning London (Heritage Statements, Article 4, 10 tips)
- All posts have Article + FAQPage + BreadcrumbList schema, OG tags, hreflang

**Video embed sections** on all 5 service pages:
- Placeholder with play icon + "Video coming soon"
- Commented-out YouTube iframe ready for real video IDs

**Blog hub** updated to 16 article cards

**Sitemap:** 453 URLs

### Massive content expansion (completed 2026-04-16)

**33 borough planning guides** (generated via `scripts/gen_borough_guides.py`):
- One per London borough: "Planning Permission in {Borough}: 2026 Guide"
- Each: Article + FAQPage schema, TL;DR box, Article 4/conservation detail, 5 FAQs, hero image placeholder
- Targets: "planning permission in [borough]" long-tail keywords

**30 more neighbourhood pages** (total: 80, generated via updated `scripts/gen_neighbourhoods.py`):
- Canary Wharf, Mile End, Stamford Hill, Lewisham, Catford, Eltham, Charlton, Stratford, Forest Gate, Manor Park, Ilford, Bexleyheath, Romford, Uxbridge, Southall, Hanwell, Harlesden, Willesden, Palmers Green, Winchmore Hill, Harrow on the Hill, Pinner, Kingston, Surbiton, Norbury, Crystal Palace, Beckenham, Colliers Wood, Raynes Park, Northfields

**6 project-type deep dives:**
- HMO conversion guide (Article 4, licensing, fire safety, room sizes)
- Flat conversion guide (change of use, Part B/E, CIL)
- Outbuilding planning guide (Class E PD, habitable vs incidental)
- Wraparound extension guide (L-shaped, 2 RSJs, Party Wall)
- Double storey extension guide (45-degree rule, privacy, foundations)
- Change of use planning guide (Use Classes, Class MA Prior Approval)

**4 comparison blog posts:**
- Dormer vs Velux loft conversion (cost, space, planning, value)
- LABC vs Approved Inspector (cost, speed, process)
- Full planning vs Prior Approval (when to use each)
- Architect fees vs fixed fee (worked examples, 5 project types)

**PD checker interactive tool** at `/tools/pd-checker/`:
- 4-step flow: project type → property details → project specifics → GREEN/AMBER/RED result
- 11 project types, PD logic for England, Article 4 borough warnings
- Shareable results via URL params, CTA to /quote.html

**Sitemap:** 527 URLs

**Still remaining:**
- Video embeds on service pages (nice-to-have)
- Replace placeholder images in blog/projects/team with real photos
- Replace placeholder business details (phone, address, CIAT/ICO/Companies House numbers)
- Off-page SEO: Google Business Profile, Search Console, 35+ citation directories, review acquisition
- Content velocity: 2 new blog posts per week targeting long-tail keywords

### Phase H: Dashboard & portal overhaul (completed 2026-04-14)

**Dashboard (portal/dashboard.html) — full rebuild, same design:**
- Added section navigation: sidebar links now switch between Overview, Projects, Files, Messages, Payments, Settings via JS — all 6 sidebar items functional
- Built `#messages` section with empty-state UI (chat bubble icon, "No messages yet" copy)
- Built `#settings` section with Profile form (name, email, phone + save), Security (change password, 2FA placeholder), Notifications toggle, Delete account
- Added **sign-out button** to sidebar bottom — clears sessionStorage, redirects to login
- Added **project detail modal** — "Open" buttons now launch a modal with project details (service, postcode, fee, status, date) + "Request amendment" CTA
- Added **mobile sidebar toggle** — floating hamburger button at 860px breakpoint, overlay dismissal
- Made all content **API-driven with demo fallback**: stats, projects, and payments fetch from `/api/projects` — if API unavailable, renders 3 demo projects
- **Dynamic date** — header shows current day/date via `new Date()`
- **Dynamic user** — removed hardcoded "Alex Morgan" / "alex@example.com", populated from `sessionStorage.ad_user`
- **Dynamic stats** — computed from project data (active, delivered, pending, balance)
- **Dynamic payment** — amount and description pulled from first active project
- All new CSS uses existing design tokens (--r-lg, --r-sm, --line, --accent, --surface, --bg-2, --shadow-lg, --ease, --ease-spring)

**Login (portal/login.html) — fixes:**
- **Forgot password modal** — button opens a modal with email input, submits to `/api/auth/reset-password`, always shows success to prevent email enumeration
- **SSO buttons** — Google/Apple buttons now show graceful "not yet available" alert instead of doing nothing
- **Better demo fallback** — login auto-capitalises email prefix as display name

### Phase G: Launch QA (completed 2026-04-14)

**Audits run:**
- Schema markup validation (all JSON-LD blocks)
- SEO invariants (titles, meta descriptions, canonicals, robots.txt, sitemap)
- Backend security and correctness (Stripe webhook order, JWT, routes, DB schema)
- Cross-page link integrity (nav, footer, internal links)
- Price consistency (quote.js, pricing.html, services.html, service detail pages)

**Issues found and fixed:**
1. **search.html missing canonical URL** — added `<link rel="canonical">`
2. **JWT_SECRET dangerous fallback** — `auth.js` had hardcoded `'dev-secret-change-me'` fallback. Fixed: now throws error in production if `JWT_SECRET` is unset, falls back only in dev
3. **Service page schema providers incomplete** — all 5 service detail page schemas were missing `url`, `telephone`, `priceRange` in the Service.provider object. Fixed all 5.

**Audit results — PASS:**
- Stripe webhook route correctly mounted BEFORE `express.json()` in server.js
- All 8 backend JS files pass `node --check`
- All 33 London boroughs linked from landing page
- All 5 service pages link to `quote.html` with correct query params
- Price consistency verified: £840 Essentials, £1,750 Complete, £1,225 Loft, £1,575 Mansard — matching across quote.js, pricing.html, services.html, and all service detail pages
- robots.txt correctly disallows /portal/ and /api/
- sitemap.xml has 211 URLs (all public pages)
- All nav/footer links verified — zero broken internal links
- Database schema has all 5 required tables with proper constraints and indexes
- Health endpoint exists at /api/health

**Noted but not fixed (advisory, non-blocking):**
- Title tags: 8 of 13 pages exceed 60 chars (Google truncates, not a ranking factor)
- Meta descriptions: most exceed 160 chars (Google truncates, not a ranking factor)
- about.html has no Person schema for team members (nice-to-have for E-E-A-T)
- Rate limiting may need `app.set('trust proxy', 1)` if deployed behind proxy/CDN
- File upload validates extension only, not MIME magic bytes (acceptable for now)

### Phase C: Images (completed 2026-04-14)
- Generated 36 placeholder images in `assets/img/` using Pillow (4 hero images x 3 sizes x 3 formats)
- Image names match HTML references: `blueprint-tablet`, `blueprint-correcting`, `technologist-working`, `tools-workplace`
- Each at 640px, 1024px, 1600px in AVIF, WebP, and JPG formats
- Placeholders are labeled with correct dimensions and "Replace with real photo" text
- Additional real architectural reference photos also present in the directory (from zip)

### Phase D: Legal pages (completed 2026-04-14)
- Created `privacy.html` — UK GDPR compliant privacy policy (12 sections: data controller, legal basis, third parties, retention, cookies, rights, ICO complaints)
- Created `terms.html` — UK law terms of service (fixed-fee basis, IP, PI insurance, planning outcome disclaimers, cancellation rights, governing law)
- Both pages use the full design system CSS (inlined from about.html pattern)
- Updated all legal links across the site:
  - `index.html` footer: "Sitemap · Privacy · Terms" now linked to actual pages
  - `quote.html`: privacy link updated from `#` to `privacy.html`
  - `portal/register.html`: Terms + Privacy links updated from `#` to `/terms.html` and `/privacy.html`
- Updated `gen_pseo.py` footer templates — all 3 footer patterns now include Privacy + Terms links
- Regenerated all 199 pSEO pages with legal links in footers
- Updated `gen_sitemap.py` to include both legal pages
- Regenerated `sitemap.xml` — now 211 URLs (was 209)

### Phase E: Placeholder content fixes (completed 2026-04-14)
- Fixed `portal/dashboard.html`: removed hardcoded "Alex Morgan" / "alex@example.com" — fields now populated dynamically from `sessionStorage.ad_user` (existing JS already handled this)
- Fixed `services.html`: updated all 25 `href="#"` service card links → `quote.html?service=<slug>` with meaningful service slugs (e.g. `?service=full-planning`, `?service=ldc`, `?service=basement`)
- Remaining `href="#"` links are portal UI placeholders (Forgot password, View all, Open buttons) that require backend integration — documented below

#### Business-owner placeholders still requiring real values
These items are called out in CLAUDE.md §9 as placeholders. Replace before launch:

| Item | Current placeholder | Where used | Grep pattern |
|------|-------------------|------------|--------------|
| Phone number | 020 7946 0000 | Site-wide (14+ pages, schema, WhatsApp) | `020 7946 0000` or `442079460000` |
| Address | 86-90 Paul Street, EC2A 4NE | Site-wide (footer, schema, about) | `Paul Street` |
| CIAT number | CP-2416-8832 | about.html | `CP-2416-8832` |
| ICO registration | ZA847291 | about.html, privacy.html | `ZA847291` |
| Companies House | 14872049 | about.html, index.html footer | `14872049` |
| Team bios | 6 fictional staff members | about.html | — |
| Testimonials | Placeholder quotes | index.html, service pages | — |
| Logo | "A" monogram (may not be final) | All pages (favicon SVG) | — |

### Phase B: Frontend API URL update (completed 2026-04-14)
- Audited all `fetch()` calls across 6 files: `index.html`, `quote.html`, `portal/login.html`, `portal/register.html`, `portal/dashboard.html`, `assets/js/quote.js`
- Portal files and quote.js already had correct `API_BASE` pattern
- Fixed 2 missing files: added `API_BASE` constant to `index.html` (callback form) and `quote.html` (inline quote submit)
- All API calls now use: `const API_BASE = location.hostname === 'localhost' ? 'http://localhost:3001' : 'https://api.architecturaldrawings.uk'`
- Zero hardcoded `/api/` fetch calls remain

### Phase A: pSEO page generation (completed 2026-04-14)
- Fixed `gen_pseo.py` and `gen_sitemap.py` — updated hardcoded `/home/claude` paths to use relative `Path(__file__).resolve().parent`, added `encoding="utf-8"` for Windows compatibility
- **Generated 199 pSEO pages** under `areas/`:
  - 1 master index (`areas/index.html`)
  - 33 borough hub pages (`areas/{borough}/index.html`)
  - 165 service-location pages (33 boroughs x 5 services)
- **Regenerated `sitemap.xml`** — now contains 209 URLs (10 core + 199 pSEO)
- Each page includes: unique H1, title, meta description, canonical URL, Service schema, FAQPage schema, BreadcrumbList, TL;DR box, location-specific FAQ, adjacent borough links, related services
- All borough data verified: 33 boroughs with Article 4 status, conservation area counts, housing stock descriptions, adjacent borough cross-links

---

## What Codex needs to do next — Third-party sign-ups

Follow SETUP.md sections in order. Each section captures credentials that later sections depend on.

### Priority 1 — Must have before launch
| # | Service | SETUP.md section | What to capture | Est. cost |
|---|---------|-----------------|-----------------|-----------|
| 1 | **GitHub** | §2 | Username, repo URL | Free |
| 2 | **Domain** (architecturaldrawings.uk) | §3 | Registrar login, expiry date | £8-12/yr |
| 3 | **Cloudflare** (DNS, CDN, email routing) | §4 | Account email, nameservers | Free |
| 4 | **Vercel** (frontend hosting) | §5 | Project URL, production URL | Free |
| 5 | **Railway** (API hosting + SQLite) | §6 | Project URL, API domain | ~£5-10/mo |
| 6 | **Stripe** (payments) | §7 | Live keys, webhook secret | 1.5% + 20p/txn |
| 7 | **Postmark** (transactional email) | §8 | SMTP credentials | Free at launch |

### Priority 2 — SEO and monitoring (week 1-2)
| # | Service | SETUP.md section | What to capture |
|---|---------|-----------------|-----------------|
| 8 | **Google Search Console** | §10 | Property verified, sitemap submitted |
| 9 | **Google Business Profile** | §11 | Profile created, postcard requested |
| 10 | **Plausible** (analytics) | §12 | Script snippet added to all pages |
| 11 | **Sentry** (error monitoring) | §13 | Frontend + backend DSN configured |

### Priority 3 — Business directories (month 1)
| # | Service | SETUP.md section | Notes |
|---|---------|-----------------|-------|
| 12 | **CIAT directory** | §14 | Requires active MCIAT membership |
| 13 | **Trustpilot** | §14 | Create business account |
| 14 | **Houzz Pro** | §14 | Free basic listing |

### Priority 4 — Optional (when revenue justifies)
| # | Service | SETUP.md section | Notes |
|---|---------|-----------------|-------|
| 15 | **Google Workspace** | §9 | Full email send/receive at hello@ |
| 16 | **CheckATrade** | §14 | ~£90/mo but high-authority backlink |

### After all sign-ups: Environment variables
Once all services are provisioned, consolidate the captured values into Railway environment variables per SETUP.md §15. The full list:

```
NODE_ENV, PORT, ALLOWED_ORIGIN, DATABASE_URL, UPLOAD_DIR, MAX_FILE_SIZE_MB,
JWT_SECRET, JWT_EXPIRES_IN, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET,
STRIPE_SUCCESS_URL, STRIPE_CANCEL_URL, SMTP_HOST, SMTP_PORT, SMTP_USER,
SMTP_PASS, EMAIL_FROM, EMAIL_TO_OPS, RATE_LIMIT_WINDOW_MS, RATE_LIMIT_MAX,
SENTRY_DSN
```

---

## What still needs building / is incomplete

1. ~~**Images:**~~ DONE — 36 placeholder images generated (4 hero x 3 sizes x 3 formats). **Real photos still needed** to replace placeholders before launch.
2. ~~**pSEO pages:**~~ DONE — all 199 pages generated (2026-04-14)
3. ~~**Frontend API URL update:**~~ DONE — all 6 files use `API_BASE` pattern (2026-04-14)
4. ~~**Legal pages:**~~ DONE — `privacy.html` and `terms.html` created, all links updated (2026-04-14)
5. ~~**Placeholder links:**~~ DONE — 25 service card `href="#"` links and legal form links all fixed (2026-04-14)
6. **Business-owner placeholders:** Phone, address, CIAT/ICO/Companies House numbers, team bios, testimonials, logo — see Phase E table above
7. **Analytics/monitoring snippets:** Plausible and Sentry need to be added to all HTML `<head>` blocks after Codex provisions accounts
8. ~~**Portal UI:**~~ DONE — dashboard fully rebuilt with section nav, modals, sign-out, mobile toggle; login.html has forgot password modal + SSO handling (2026-04-14)
9. **Real photos:** Replace placeholder images in `assets/img/` with actual hero photos, team headshots, project gallery

---

## Key files for reference

| Purpose | File |
|---------|------|
| Agent working instructions | `CLAUDE.md` |
| Third-party provisioning runbook | `SETUP.md` |
| Deployment guide | `README.md` |
| Full services catalogue | `services-and-tech-stack (4).md` (in parent dir) |
| SEO strategy | `seo-analysis-architectural-technology-london (1).md` (in parent dir) |
| Design system source of truth | `assets/css/style.css` |
| Quote flow price map | `assets/js/quote.js` |
| Backend entrypoint | `api/server.js` |
| Database schema | `api/models/db.js` |
| Environment variable template | `api/.env.example` |
| Privacy Policy | `privacy.html` |
| Terms of Service | `terms.html` |

---

## Launch checklist
See SETUP.md §16 for the full pre-launch checklist covering technical, SEO, content, legal, and business verification items.
