# HANDOVER.md — Architectural Drawings London

**Last updated:** 2026-04-13
**Status:** Site scaffolded and structured. Ready for third-party service sign-ups and deployment.

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
├── areas/
│   ├── index.html                 Master borough index (48 KB)
│   ├── camden/
│   │   ├── index.html             Camden hub page (51 KB)
│   │   └── loft-conversions.html  Camden loft conversions (67 KB)
│   ├── hackney/
│   │   └── house-extensions.html  Hackney house extensions (66 KB)
│   └── westminster/
│       └── mansard-roof.html      Westminster mansard roof (67 KB)
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

---

## What Codex needs to do next — Third-party sign-ups

Follow SETUP.md sections in order. Each section captures credentials that later sections depend on.

### Priority 1 — Must have before launch
| # | Service | SETUP.md section | What to capture | Est. cost |
|---|---------|-----------------|-----------------|-----------|
| 1 | **GitHub** | §2 | Username, repo URL | Free |
| 2 | **Domain** (architecturaldrawings.co.uk) | §3 | Registrar login, expiry date | £8-12/yr |
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

1. **Images:** `assets/img/` is empty — hero images, service photos, team headshots needed
2. **pSEO pages:** Only 5 sample borough pages generated — run `python3 gen_pseo.py` to generate all 199 pages (33 boroughs × 5 services + 33 hubs + 1 index)
3. **Placeholder content:** Phone number (020 7946 0000), address, CIAT/ICO/Companies House numbers are placeholders — replace before launch
4. **Legal pages:** Privacy Policy and Terms of Service are linked but not created
5. **Testimonials:** Currently placeholder — replace with real client reviews
6. **Team bios:** Placeholder content in about.html
7. **Logo:** "A" monogram may not be final

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

---

## Launch checklist
See SETUP.md §16 for the full pre-launch checklist covering technical, SEO, content, legal, and business verification items.
