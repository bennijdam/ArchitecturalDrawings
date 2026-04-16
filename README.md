# Architectural Drawings London

A full-stack platform for a chartered architectural technology practice in London. Landing site + multi-step quote flow + user portal + Stripe-powered payments + secure file uploads.

## Project overview

```
architectural-drawings/
├── index.html                  Landing page (hero, services, pricing, FAQ, boroughs, CTA)
├── services.html               Services overview (60+ services in 5 categories)
├── services/
│   ├── planning-drawings.html  Detailed service page (SEO template pattern)
│   ├── building-regulations.html
│   ├── loft-conversions.html
│   ├── house-extensions.html
│   └── mansard-roof.html
├── quote.html                  5-step quote flow (property → service → details → contact → review)
├── pricing.html                Fixed-fee price matrix vs. London architect benchmarks
├── about.html                  Team + E-E-A-T credentials
├── search.html                 Client-side search over services + boroughs
├── portal/
│   ├── login.html              JWT-auth login (email/password, Google, Apple)
│   ├── register.html           Account creation
│   └── dashboard.html          Stats + projects + file upload + Stripe Checkout
├── assets/
│   ├── css/style.css           Design system (Fraunces + Manrope, 1,000+ lines)
│   ├── js/app.js               Reveals, nav, FAQ, mobile menu
│   ├── js/quote.js             Quote flow state machine + price calc + API POST
│   └── img/                    Responsive AVIF + WebP + JPG at 640/1024/1600/2400
├── api/
│   ├── server.js               Express entrypoint
│   ├── package.json
│   ├── .env.example
│   ├── models/db.js            SQLite schema (users, quotes, projects, files, payments)
│   ├── middleware/auth.js      JWT verify + role gating
│   └── routes/
│       ├── auth.js             Register, login, /me
│       ├── quotes.js           Public POST + admin GET
│       ├── projects.js         CRUD, JWT-gated
│       ├── files.js            Multer upload + secure download
│       └── stripe.js           Checkout session + webhook handler
├── robots.txt
└── sitemap.xml
```

## Design commitments

- **Typography**: [Fraunces](https://fonts.google.com/specimen/Fraunces) (display serif, variable) paired with [Manrope](https://fonts.google.com/specimen/Manrope) (body sans) — distinctive, avoids generic Inter/Roboto feel.
- **Palette**: Warm cream (#FAFAF7) backgrounds, ink (#0E1116) text, terracotta (#C8664A) accent — warm editorial minimalism rather than tech-bro purple.
- **Layout**: 20–36px rounded cards, soft shadows, generous whitespace, staggered scroll-triggered reveals.
- **Performance**: AVIF images (as small as 9 KB at 640px wide). WebP fallback. JPEG last-resort. Responsive `<picture>` + `srcset` everywhere. Hero image preloaded. Fonts preconnected.
- **Accessibility**: Focus rings, `prefers-reduced-motion` honoured, native `<details>` for FAQ (keyboard-operable), semantic HTML throughout.

## SEO / GEO / AEO

- **LocalBusiness schema** on landing page with address, opening hours, geo coordinates, aggregate rating, offer catalog.
- **FAQPage schema** on landing + every service detail page.
- **BreadcrumbList schema** on deep pages.
- **Service schema** on each service detail page.
- All 33 London boroughs linked directly from the landing page and service pages.
- Canonical URLs, Open Graph, Twitter Card metadata on every page.
- Semantic H1/H2/H3 hierarchy with keyword-rich but natural prose.
- Long-tail keyword coverage across service × borough permutations via search page and internal linking.

## Pricing strategy — 30% below London architects

Every fee benchmarked against 50 London competitors (Fast Plans, Draw Plans, 4D Planning, Extension Architecture, LCCL, RIBA practices). See `/pricing.html` for the full matrix.

Headline numbers:
- Essentials (single submission): from **£840** vs. London architect £1,200–£1,800
- Complete (planning + regs + structural): from **£1,750** vs. London architect £2,500–£4,500
- Loft conversion: from **£1,225** vs. £1,750–£3,500
- Mansard: from **£1,575** vs. £2,250–£6,000

## Running locally

### 1. Frontend (static)

Any static server works:

```bash
cd architectural-drawings
npx serve .     # or python3 -m http.server 8080
```

Open `http://localhost:3000` (or 8080).

### 2. Backend API

Prerequisites: Node.js 20+.

```bash
cd architectural-drawings/api
cp .env.example .env
# Edit .env — set JWT_SECRET, STRIPE_SECRET_KEY, SMTP_*, etc.
npm install
npm start
```

The API auto-creates SQLite DB and `uploads/` folder on first boot, then listens on `:3001`.

### Key env vars

| Variable | Purpose |
|---|---|
| `JWT_SECRET` | HMAC secret for auth tokens (64+ random chars) |
| `STRIPE_SECRET_KEY` | `sk_live_...` or `sk_test_...` |
| `STRIPE_WEBHOOK_SECRET` | `whsec_...` from Stripe dashboard |
| `SMTP_HOST` / `SMTP_USER` / `SMTP_PASS` | Outbound email (SendGrid, Postmark, SES) |
| `EMAIL_TO_OPS` | Where new-quote notifications land |
| `ALLOWED_ORIGIN` | CORS allowlist (your frontend origin) |

## Deployment

### Option A — single-server (fastest)

Deploy to Railway, Fly.io, Render, or any Node host:

1. Push the repo.
2. Set environment variables from `.env.example`.
3. Build command: `cd api && npm ci`.
4. Start command: `cd api && npm start`.
5. Point your domain's A/AAAA records to the host.
6. The Express server serves both the static frontend and the API — `server.js` includes a static middleware pointing at the repo root.

### Option B — split frontend + backend (recommended at scale)

**Frontend:** Upload the entire `architectural-drawings/` repo (minus `api/`) to any static host — Netlify, Vercel, Cloudflare Pages, S3+CloudFront. Set the SPA fallback so unknown routes return the homepage if needed.

**Backend:** Deploy `architectural-drawings/api/` as a Node service. Set `ALLOWED_ORIGIN` to your frontend origin (e.g. `https://www.architecturaldrawings.uk`).

**Update frontend fetch URLs** if different origin — replace `/api/...` with full URL like `https://api.architecturaldrawings.uk/api/...` in `assets/js/quote.js`, `portal/login.html`, `portal/register.html`, `portal/dashboard.html`.

### Stripe setup

1. Create a Stripe account → dashboard → Developers → API keys.
2. Copy the **Secret key** into `STRIPE_SECRET_KEY`.
3. Developers → Webhooks → Add endpoint → `https://your-domain.com/api/stripe/webhook`.
4. Subscribe to `checkout.session.completed` + `checkout.session.expired` + `checkout.session.async_payment_failed`.
5. Copy the signing secret into `STRIPE_WEBHOOK_SECRET`.

### Domain + DNS

- Point apex domain (architecturaldrawings.uk) to the host.
- Also configure `www.architecturaldrawings.uk` with a 301 redirect to apex (or vice versa — pick one canonical).
- Enable HTTPS (Railway, Fly, Netlify, Cloudflare all do this automatically with Let's Encrypt).

## SEO post-deploy checklist

- [ ] Submit `sitemap.xml` to Google Search Console + Bing Webmaster Tools.
- [ ] Claim Google Business Profile for "Architectural Drawings London" at the EC2A 4NE address.
- [ ] Add business to Yell, Thomson Local, TrustATrader, CheckATrade, Houzz.
- [ ] Create CIAT practice directory listing (members.ciat.org.uk).
- [ ] File CompaniesHouse → Trustpilot business profile.
- [ ] Start a content series on borough-specific planning quirks (Article 4, basement policies, mansard guides).
- [ ] Backlink outreach: architect publications (Dezeen, Building Design), local London blogs.
- [ ] Schema validator pass: `https://validator.schema.org/`.
- [ ] Lighthouse audit target: 95+ on Performance, Accessibility, Best Practices, SEO.

## Content generation for service imagery

The four uploaded stock photos are used throughout. For more bespoke service imagery (loft conversions, mansards, building regs in action), the recommended workflow:

```bash
# Use the ffmpeg script at ../optimize_images.sh as a reference
# Source: generate via Claude (claude.ai), ChatGPT (DALL·E 3), or Midjourney
# Target: 2400px wide JPEG

# Then re-run image optimization to produce responsive AVIF + WebP:
ffmpeg -i source.jpg -vf "scale=1600:-2" \
  -c:v libaom-av1 -crf 32 -b:v 0 -still-picture 1 \
  output-1600.avif
```

Ship AVIF as primary (5–10× smaller than JPEG), WebP as fallback, JPEG as last resort. All three wrapped in a `<picture>` element — browsers pick the first they support.

## Security notes

- Passwords hashed with bcrypt (cost 10).
- JWT tokens 7-day expiry; no refresh token rotation yet (consider adding).
- File upload validated by extension + multer's size limit; mime sniffing would be an upgrade.
- Helmet default headers (CSP, HSTS, X-Frame-Options, etc.).
- Rate limit: 100 req / 15 min per IP.
- CORS restricted to `ALLOWED_ORIGIN`.
- Stripe webhook signature verified on raw body.
- SQLite WAL mode + foreign keys enabled. **Swap to PostgreSQL before multi-node deployment.**

## License

Proprietary — © 2026 Architectural Drawings Ltd. Registered in England No. 14872049.
