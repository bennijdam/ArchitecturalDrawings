# SETUP.md — Tech Stack Provisioning Runbook

Step-by-step guide for an agent (or a human) to sign up for every third-party service needed to run **Architectural Drawings London** in production.

Follow sections in order — later steps depend on values captured in earlier ones. Every step lists: **URL**, **what to do**, **what to capture**, **rough cost**.

Total recurring cost at launch scale: **~£15–45/month**. Optional bolt-ons (Google Workspace, paid analytics) push it to ~£60–80/month.

---

## Table of contents

1. [Prerequisites — tools on your machine](#1-prerequisites)
2. [GitHub — version control](#2-github)
3. [Domain registration — architecturaldrawings.uk](#3-domain-registration)
4. [Cloudflare — DNS, CDN, email routing](#4-cloudflare)
5. [Vercel — frontend hosting](#5-vercel)
6. [Railway — backend API + SQLite](#6-railway)
7. [Stripe — payments](#7-stripe)
8. [Postmark — transactional email](#8-postmark)
9. [Google Workspace — professional email (optional)](#9-google-workspace-optional)
10. [Google Search Console — SEO indexing](#10-google-search-console)
11. [Google Business Profile — local SEO](#11-google-business-profile)
12. [Plausible / Fathom — privacy analytics](#12-plausible-or-fathom)
13. [Sentry — error monitoring](#13-sentry)
14. [Trade directory listings — CIAT, Houzz, Trustpilot](#14-trade-directories)
15. [Environment variables — consolidation](#15-environment-variables)
16. [Launch checklist](#16-launch-checklist)

---

## 1. Prerequisites

Install these locally before anything else:

| Tool | Install |
|---|---|
| **Node.js 20+** | https://nodejs.org/en/download — choose the LTS installer |
| **Git** | https://git-scm.com/downloads |
| **GitHub CLI (`gh`)** | https://cli.github.com/ — `brew install gh` on macOS, `winget install GitHub.cli` on Windows |
| **Vercel CLI** | `npm i -g vercel` |
| **Railway CLI** | `npm i -g @railway/cli` |
| **Stripe CLI** | https://docs.stripe.com/stripe-cli — needed for local webhook testing |

Verify everything:

```bash
node --version     # should be v20+
git --version
gh --version
vercel --version
railway --version
stripe --version
```

---

## 2. GitHub

**URL:** https://github.com/signup

### 2.1 Create account
If signing up fresh: use the business email (e.g. `ops@architecturaldrawings.uk` — set this up later in §9, or use a personal email for now and transfer later).

Enable two-factor authentication immediately: https://github.com/settings/security

### 2.2 Create the repository

```bash
# In the project folder
cd architectural-drawings

# Auth
gh auth login            # follow browser prompt

# Create private repo and push
git init
git add .
git commit -m "Initial commit — Architectural Drawings London"
gh repo create architectural-drawings-london --private --source=. --push
```

**Capture:**
- GitHub username: `________`
- Repo URL: `https://github.com/<username>/architectural-drawings-london`

### 2.3 Add `.gitignore`

Before pushing, make sure `api/.env`, `api/data/`, `api/uploads/`, and `node_modules/` are gitignored. Create or verify:

```
# .gitignore (at repo root)
node_modules/
api/.env
api/data/
api/uploads/
.DS_Store
*.log
.vercel
```

**Cost:** Free for private repos (unlimited, for personal accounts).

---

## 3. Domain registration

### 3.1 Check availability

**URL:** https://www.nominet.uk/lookup/ (authoritative .uk WHOIS — free)

Enter: `architecturaldrawings.uk`

If it shows as available, buy it through a registrar in §3.2. If it's taken, fall back options:
- `architecturaldrawings.london` (check at https://www.nic.london/)
- `architecturaldrawings.uk`
- `architectural-drawings.co.uk`

### 3.2 Register the domain

**Registrar options (pick one):**

| Registrar | URL | .co.uk price / year | Notes |
|---|---|---|---|
| **Cloudflare Registrar** | https://www.cloudflare.com/products/registrar/ | At cost (~£8) | Cheapest; requires DNS on Cloudflare (we want this anyway) |
| **Namecheap** | https://www.namecheap.com/domains/uk-domain/ | ~£8–10 | Good UI, easy transfer |
| **123-reg** | https://www.123-reg.co.uk/ | ~£12 first year | UK-based, mainstream |
| **Gandi** | https://www.gandi.net/en-GB/domain/price | ~£10 | Ethical registrar, strong privacy |

**Recommendation:** Register at Cloudflare Registrar for at-cost pricing and zero DNS friction — but you must first sign up for Cloudflare (§4), add the zone there, then transfer in. For launch speed, use Namecheap or 123-reg today and transfer to Cloudflare later.

**Capture:**
- Registrar: `________`
- Domain: `architecturaldrawings.uk`
- Expiry date: `________` (set a calendar reminder 60 days before)
- Registrar login: `________`

**Cost:** £8–12 first year, £8–15/year to renew.

---

## 4. Cloudflare

**URL:** https://dash.cloudflare.com/sign-up

Cloudflare handles DNS, provides a free CDN, free SSL, and free email routing (forwards `hello@architecturaldrawings.uk` to any existing Gmail/Outlook).

### 4.1 Sign up and add the site

1. Sign up at https://dash.cloudflare.com/sign-up
2. Click **Add a site** → enter `architecturaldrawings.uk` → pick **Free plan** → next.
3. Cloudflare scans existing DNS records. If registered today with no DNS yet, there'll be nothing to import.
4. Cloudflare shows two nameservers like `xxx.ns.cloudflare.com` and `yyy.ns.cloudflare.com`.
5. **Go back to your registrar** (§3.2). In the domain management → DNS/nameservers section, replace the default nameservers with the two Cloudflare ones. Save.
6. Propagation takes 5 min–24 h. Cloudflare will email when active.

### 4.2 Configure DNS records (do this after Cloudflare is active)

In Cloudflare → DNS → Records, you'll add records in §5 (Vercel) and §6 (Railway) below. For now, leave the zone empty.

### 4.3 Set up email routing (free)

1. In Cloudflare dashboard → **Email** → **Email Routing** → Enable.
2. Under **Destination addresses**, add your personal Gmail/Outlook. Verify.
3. Under **Routes**, create:
   - `hello@architecturaldrawings.uk` → forwards to your personal inbox
   - `ops@architecturaldrawings.uk` → same (or another inbox)
   - `*@architecturaldrawings.uk` (catch-all) → same
4. Cloudflare auto-adds the required MX records.

For **outbound** email from those addresses, you'll use Postmark (§8) for transactional and Google Workspace (§9) if you want human email with full send/reply at `hello@…`.

**Capture:**
- Cloudflare account email: `________`
- Nameservers (confirm on registrar): `________`

**Cost:** Free (Pro plan £20/mo optional, not needed at launch).

---

## 5. Vercel

**URL:** https://vercel.com/signup

Vercel hosts the static HTML/CSS/JS frontend. Free tier easily covers this use case (100 GB bandwidth/mo).

### 5.1 Sign up

Sign up with the GitHub account from §2. Vercel auto-links — grant repository access when prompted.

### 5.2 Import the project

1. In Vercel dashboard → **Add New…** → **Project**.
2. Pick `architectural-drawings-london` from the GitHub list.
3. Vercel auto-detects — it's a static site with no framework.
4. **Framework Preset:** Other
5. **Build command:** leave empty (no build step)
6. **Output directory:** `.` (repo root) — but exclude `api/` from deploys (see §5.3)
7. Click **Deploy**.

### 5.3 Exclude the API from Vercel

Create `vercel.json` at repo root:

```json
{
  "cleanUrls": true,
  "trailingSlash": false,
  "buildCommand": null,
  "outputDirectory": ".",
  "ignoreCommand": "exit 0",
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    },
    {
      "source": "/(.*).html",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=0, must-revalidate" }
      ]
    }
  ],
  "redirects": [
    { "source": "/home", "destination": "/", "permanent": true }
  ]
}
```

Also create `.vercelignore`:

```
api/
*.md
gen_services.py
inline_assets.py
rebrand.py
```

Commit and push — Vercel auto-redeploys.

### 5.4 Connect the custom domain

1. Vercel dashboard → Project → **Settings** → **Domains**.
2. Add `architecturaldrawings.uk` and `www.architecturaldrawings.uk`.
3. Vercel displays two DNS records to add. Go to Cloudflare → DNS → Records:
   - Add `CNAME www → cname.vercel-dns.com` (proxy OFF / DNS only)
   - Add `A @ → 76.76.21.21` (Vercel's anycast IP; proxy OFF / DNS only)
4. Wait 1–2 minutes. Vercel auto-issues SSL.

**Capture:**
- Vercel project URL: `https://architectural-drawings-london.vercel.app`
- Production URL: `https://www.architecturaldrawings.uk`

**Cost:** Free (Hobby plan). Upgrade to Pro at $20/mo only if bandwidth exceeds 100 GB/month.

---

## 6. Railway

**URL:** https://railway.com (or railway.app — both resolve)

Railway hosts the Node/Express API + the SQLite file on a persistent volume.

### 6.1 Sign up

Sign up with GitHub (same account as §2). https://railway.com/login

Grant Railway access to the `architectural-drawings-london` repo.

### 6.2 Create the service

1. Dashboard → **New Project** → **Deploy from GitHub repo** → select `architectural-drawings-london`.
2. Railway auto-detects Node, but will fail the first build because `package.json` is inside `api/`, not the root.
3. Fix: **Settings** → **Root Directory** → set to `/api`.
4. **Settings** → **Build** → Build Command: `npm ci`.
5. **Settings** → **Deploy** → Start Command: `npm start`.
6. **Settings** → **Networking** → click **Generate Domain** to get a public `.up.railway.app` URL.

### 6.3 Add a persistent volume for SQLite

1. Service → **Volumes** → **New Volume**.
2. Name: `data`. Mount path: `/app/data`. Size: 1 GB.
3. Update `api/.env` (§6.5): `DATABASE_URL=/app/data/ad.sqlite` and `UPLOAD_DIR=/app/data/uploads`.

### 6.4 Add environment variables (temporary values — fill in later sections)

Railway → Service → **Variables** → add:

```
NODE_ENV=production
PORT=3001
ALLOWED_ORIGIN=https://www.architecturaldrawings.uk

DATABASE_URL=/app/data/ad.sqlite
UPLOAD_DIR=/app/data/uploads

JWT_SECRET=<generate with `openssl rand -hex 32`>
JWT_EXPIRES_IN=7d

# These come from later sections — add now as placeholders, update after
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_SUCCESS_URL=https://www.architecturaldrawings.uk/portal/dashboard.html?payment=success
STRIPE_CANCEL_URL=https://www.architecturaldrawings.uk/portal/dashboard.html?payment=cancelled

SMTP_HOST=smtp.postmarkapp.com
SMTP_PORT=587
SMTP_USER=xxx
SMTP_PASS=xxx
EMAIL_FROM="Architectural Drawings London <hello@architecturaldrawings.uk>"
EMAIL_TO_OPS=ops@architecturaldrawings.uk

RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX=100
MAX_FILE_SIZE_MB=100
```

### 6.5 Custom domain for the API

1. Railway → Service → **Networking** → **Custom Domain** → add `api.architecturaldrawings.uk`.
2. Railway gives you a CNAME target. Go to Cloudflare → DNS → add:
   - `CNAME api → <railway-target>.up.railway.app` (proxy OFF / DNS only — Railway handles SSL)

### 6.6 Update frontend to call production API

In `portal/login.html`, `portal/register.html`, `portal/dashboard.html`, `assets/js/quote.js` — the `fetch('/api/...')` calls use relative paths. Since Vercel serves the frontend and Railway the API, update to absolute URLs:

```javascript
const API = location.hostname === 'localhost'
  ? 'http://localhost:3001'
  : 'https://api.architecturaldrawings.uk';

fetch(`${API}/api/auth/login`, ...)
```

Commit, push, Vercel redeploys.

**Capture:**
- Railway project URL: `________`
- API domain: `https://api.architecturaldrawings.uk`

**Cost:** $5 Trial credit. Hobby plan from $5/mo, typical usage ~£5–10/month.

---

## 7. Stripe

**URL:** https://dashboard.stripe.com/register

### 7.1 Create account

1. Sign up at https://dashboard.stripe.com/register — use the business email.
2. Business type: **Company** → Limited company.
3. Provide Companies House number, trading address, director details, bank account.
4. Verification takes 1–3 business days. During that time you can use test mode.

### 7.2 Get API keys

**Dashboard → Developers → API keys**

- **Test keys** (use while Stripe is verifying the business):
  - Publishable: `pk_test_xxx`
  - Secret: `sk_test_xxx`
- **Live keys** (after verification):
  - Publishable: `pk_live_xxx`
  - Secret: `sk_live_xxx`

Add to Railway env vars (§6.4):
```
STRIPE_SECRET_KEY=sk_test_xxx       (or sk_live_xxx after verification)
```

### 7.3 Configure the webhook

1. **Dashboard → Developers → Webhooks → Add endpoint**.
2. Endpoint URL: `https://api.architecturaldrawings.uk/api/stripe/webhook`
3. Events to send (select these three):
   - `checkout.session.completed`
   - `checkout.session.expired`
   - `checkout.session.async_payment_failed`
4. Save. Stripe shows a **Signing secret** — `whsec_xxx`. Copy it.

Add to Railway env vars:
```
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

### 7.4 Test a payment

With test keys active:

```bash
# Use Stripe CLI for local webhook testing
stripe listen --forward-to localhost:3001/api/stripe/webhook

# Trigger a test checkout from the portal dashboard
# Use test card: 4242 4242 4242 4242, any future expiry, any CVC
```

Verify the `payments` table in SQLite shows `status = 'paid'` after successful Checkout.

### 7.5 Activate GBP and UK-specific features

- **Dashboard → Settings → Business settings → Payment methods** — enable:
  - Card
  - Apple Pay
  - Google Pay
  - Link
  - Optionally: Klarna / Clearpay (BNPL — common for 5-figure architecture invoices)

**Capture:**
- Stripe live publishable: `________`
- Stripe live secret: `________` (stored as env var, never commit)
- Webhook signing secret: `________`

**Cost:** 1.5% + 20p per UK card transaction (domestic). 2.5% + 20p for European. No monthly fee.

---

## 8. Postmark

**URL:** https://postmarkapp.com/sign_up

Postmark handles transactional email — the quote-confirmation emails to `ops@`, account emails, password resets. Free tier covers 100 emails/month; $15/mo for 10k.

### 8.1 Sign up and create server

1. Sign up at https://postmarkapp.com/sign_up.
2. Dashboard → **Servers** → **Create server** → name `ad-london-production`.
3. Pick **Transactional Stream**.

### 8.2 Verify the sender domain

1. Server → **Sender Signatures** → **Add Domain** → enter `architecturaldrawings.uk`.
2. Postmark shows DKIM and Return-Path DNS records. Go to Cloudflare → DNS → add all of them as `TXT` and `CNAME` records.
3. Wait 5–30 min, click **Verify** in Postmark.

### 8.3 Get SMTP credentials

**Server → API Tokens / SMTP** → capture:

```
SMTP_HOST=smtp.postmarkapp.com
SMTP_PORT=587
SMTP_USER=<Postmark server API token>
SMTP_PASS=<same as user — Postmark uses token for both>
```

Add to Railway env vars (§6.4).

### 8.4 Alternatives

If Postmark doesn't fit:
- **SendGrid** — https://sendgrid.com/ (Twilio owned, 100 free/day)
- **Resend** — https://resend.com/ (developer-friendly, 3k free/mo, good docs)
- **AWS SES** — https://aws.amazon.com/ses/ (cheapest at scale, more setup)

**Cost:** Free at launch. $15/mo if hitting 10k/month.

---

## 9. Google Workspace (optional)

**URL:** https://workspace.google.com/

For a proper `hello@architecturaldrawings.uk` mailbox you can send AND receive from (unlike Cloudflare Email Routing which is forward-only).

### 9.1 Sign up

1. https://workspace.google.com/ → **Start free trial**.
2. Business name: Architectural Drawings Ltd. Employees: 1–5.
3. Use existing domain → `architecturaldrawings.uk`.
4. Create admin account `hello@architecturaldrawings.uk` + password.

### 9.2 Verify domain ownership

Google provides a TXT record. Add to Cloudflare DNS. Verify.

### 9.3 Update MX records

**WARNING:** Google Workspace MX records will REPLACE Cloudflare Email Routing MX records. Pick one or the other — cannot run both.

- If switching to Google Workspace: delete the Cloudflare Email Routing MX records and add Google's (`SMTP.GOOGLE.COM` etc. — Google provides them).
- If keeping Cloudflare Routing: don't set up Google Workspace yet.

**Cost:** £5.20/user/month for Business Starter (enough for a solo founder).

### 9.4 Alternative: Fastmail

- https://www.fastmail.com/ — £3/mo/user, excellent product, no tracking. If you're privacy-minded this is the better pick.

**Recommendation:** Start with Cloudflare Email Routing (free, §4.3). Upgrade to Fastmail or Google Workspace once you're sending 20+ client emails a week from `hello@`.

---

## 10. Google Search Console

**URL:** https://search.google.com/search-console

### 10.1 Add property

1. Visit https://search.google.com/search-console → **Add property**.
2. Pick **Domain** (not URL-prefix) → enter `architecturaldrawings.uk`.
3. Google provides a TXT record. Add to Cloudflare DNS. Verify.

### 10.2 Submit the sitemap

Sidebar → **Sitemaps** → submit `https://www.architecturaldrawings.uk/sitemap.xml` → submit.

Google will crawl the 10 URLs. First pages typically indexed within 24–72 hours for a clean new site.

### 10.3 Bing Webmaster Tools (while you're there)

Same pattern: https://www.bing.com/webmasters → add site → verify → submit sitemap. Bing also powers DuckDuckGo and ChatGPT's search.

**Capture:**
- Search Console account: `________`
- Verification date: `________`

**Cost:** Free.

---

## 11. Google Business Profile

**URL:** https://business.google.com/create

Critical for local London SEO — drives map-pack appearances for queries like "architectural technologist London" and "planning drawings Shoreditch".

### 11.1 Create profile

1. https://business.google.com/create → **Add your business**.
2. Name: `Architectural Drawings London`.
3. Category: `Architect` or `Architectural designer` (Google picks — choose the closest).
4. Address: 86–90 Paul Street, London EC2A 4NE (use the real trading address — it's printed on Companies House and verifiable).
5. Service area: Greater London (select all 33 boroughs).
6. Phone: 020 7946 0000 (or real number).
7. Website: `https://www.architecturaldrawings.uk`.

### 11.2 Verification

Google sends a **postcard to the trading address** with a 5-digit code. Arrives in 5–14 days. Enter code on the dashboard.

Once verified:
- Upload 10+ photos (hero image, team, sample drawings if non-confidential).
- Complete "Services" section — add every service from the site.
- Complete "Products" with the three pricing tiers.
- Enable messaging.
- Set business hours matching the site's LocalBusiness schema.

### 11.3 Request first reviews

After verification, send the review-request link to the first 5 satisfied clients (link: `g.page/r/<CID>/review`). Target 10 reviews in the first month — local SEO compounds from there.

**Cost:** Free.

---

## 12. Plausible or Fathom

Privacy-first, GDPR-compliant analytics. No cookie banner needed. Preferred over Google Analytics for a UK business.

| Tool | URL | Cost | Notes |
|---|---|---|---|
| **Plausible** | https://plausible.io/ | €9/mo (10k pageviews) | Open source, EU-based |
| **Fathom** | https://usefathom.com/ | $15/mo (100k pageviews) | Canadian, great UI |
| **Google Analytics 4** | https://analytics.google.com/ | Free | Requires cookie banner in UK/EU |

### Recommended: Plausible

1. Sign up at https://plausible.io/register.
2. **Add a site** → `architecturaldrawings.uk`.
3. Copy the snippet:

```html
<script defer data-domain="architecturaldrawings.uk" src="https://plausible.io/js/script.js"></script>
```

4. Paste into the `<head>` of every HTML file (use the rebrand script pattern to insert across all pages).
5. Verify in Plausible dashboard after first pageview.

### Goal events to configure

- Quote form submission: `Quote Completed`
- Callback form submission: `Callback Requested`
- Account registration: `Portal Registered`
- Payment completed: `Payment Completed`

Trigger these via `plausible('Quote Completed')` JS calls on form success.

**Cost:** €9–15/mo. Free tier on Fathom for under 1k views/mo is possible via trial.

---

## 13. Sentry

**URL:** https://sentry.io/signup/

Error monitoring for the frontend JS and the Express backend. Catches quote-flow JS exceptions, Stripe failures, DB errors.

### 13.1 Sign up

1. https://sentry.io/signup/ — free tier = 5,000 errors/month (plenty for a launching site).
2. Create organisation: `architectural-drawings-london`.

### 13.2 Create two projects

**Project 1: Frontend (browser JS)**
- Platform: **Browser JavaScript**
- DSN: `https://xxx@xxx.ingest.sentry.io/xxx` — copy.
- Add to every HTML file's `<head>`:

```html
<script src="https://browser.sentry-cdn.com/7.100.0/bundle.tracing.min.js" crossorigin="anonymous"></script>
<script>
  Sentry.init({
    dsn: 'https://xxx@xxx.ingest.sentry.io/xxx',
    tracesSampleRate: 0.1
  });
</script>
```

**Project 2: Backend (Node.js)**
- Platform: **Node.js → Express**
- Install: `cd api && npm install @sentry/node`
- Init at top of `server.js`:

```javascript
import * as Sentry from '@sentry/node';
Sentry.init({ dsn: process.env.SENTRY_DSN, tracesSampleRate: 0.1 });
```

Add to Railway env: `SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/yyy`

**Cost:** Free at launch.

---

## 14. Trade directories

These are the **highest-ROI backlinks for local architectural SEO**. Sign up and complete profiles for each.

| Directory | URL | Cost | Backlink value |
|---|---|---|---|
| **CIAT member directory** | https://www.ciat.org.uk/directory (via member portal) | Free w/ CIAT membership | Very high — gov-adjacent authority |
| **Google Business Profile** | §11 above | Free | Critical |
| **Trustpilot Business** | https://business.trustpilot.com/signup | Free / paid tiers | High — reviews + backlink |
| **Houzz** | https://pro.houzz.co.uk/ | Free basic / paid Pro | High — design-specific |
| **Architect Your Home** | https://architect-yourhome.com/ | Paid listing | Medium |
| **CheckATrade** | https://www.checkatrade.com/join-checkatrade | ~£90/mo | High — UK trade authority |
| **MyBuilder** | https://www.mybuilder.com/register-trade | Commission-based leads | Medium |
| **Bark.com** | https://www.bark.com/en/gb/ | Lead credits | Low-medium |
| **Yell** | https://business.yell.com/ | Free listing + paid SEO | Medium (legacy authority) |
| **Thomson Local** | https://www.thomsonlocal.com/ | Free / paid | Medium |

### Priority order (if short on time)
1. Google Business Profile (§11)
2. CIAT directory
3. Trustpilot
4. Houzz Pro
5. CheckATrade (if budget permits)

Each listing should link back to `architecturaldrawings.uk` with branded anchor text ("Architectural Drawings London") — 6–8 authoritative directory backlinks is enough to kickstart ranking for local keywords.

---

## 15. Environment variables — consolidation

By the end of this runbook you should have these values. Store them in a password manager (1Password, Bitwarden) as well as Railway:

```env
# ===== Server =====
NODE_ENV=production
PORT=3001
ALLOWED_ORIGIN=https://www.architecturaldrawings.uk

# ===== Database + storage =====
DATABASE_URL=/app/data/ad.sqlite
UPLOAD_DIR=/app/data/uploads
MAX_FILE_SIZE_MB=100

# ===== Auth =====
JWT_SECRET=<64-hex from `openssl rand -hex 32`>
JWT_EXPIRES_IN=7d

# ===== Stripe =====
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_SUCCESS_URL=https://www.architecturaldrawings.uk/portal/dashboard.html?payment=success
STRIPE_CANCEL_URL=https://www.architecturaldrawings.uk/portal/dashboard.html?payment=cancelled

# ===== Email (Postmark) =====
SMTP_HOST=smtp.postmarkapp.com
SMTP_PORT=587
SMTP_USER=<Postmark API token>
SMTP_PASS=<same as user>
EMAIL_FROM="Architectural Drawings London <hello@architecturaldrawings.uk>"
EMAIL_TO_OPS=ops@architecturaldrawings.uk

# ===== Rate limiting =====
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX=100

# ===== Error monitoring =====
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/yyy
```

Do NOT commit `.env` to git. Only commit `.env.example` with placeholder values.

---

## 16. Launch checklist

Run through this before announcing the site:

### Technical
- [ ] `architecturaldrawings.uk` resolves and shows Vercel-hosted site with valid SSL
- [ ] `www.architecturaldrawings.uk` 301-redirects to the apex
- [ ] `api.architecturaldrawings.uk/api/health` returns `{"ok": true}`
- [ ] Quote form submits and appears in Railway logs (`quotes` table)
- [ ] Account register/login round-trip works (check sessionStorage has `ad_token`)
- [ ] Portal dashboard loads with user data
- [ ] File upload works (check `/app/data/uploads/`)
- [ ] Stripe Checkout completes a test payment
- [ ] Stripe webhook updates `payments.status = 'paid'`
- [ ] Sending `hello@architecturaldrawings.uk` from external account arrives in inbox
- [ ] Ops email fires on quote submission

### SEO
- [ ] Google Search Console property verified
- [ ] Sitemap submitted
- [ ] `robots.txt` accessible at `/robots.txt`
- [ ] All 33 borough links work from landing page
- [ ] Lighthouse Performance ≥ 90, Accessibility ≥ 95, SEO = 100
- [ ] Schema validator passes: https://validator.schema.org/ → paste URL → no errors
- [ ] Open Graph preview renders: https://www.opengraph.xyz/ → paste URL

### Content
- [ ] Replace placeholder Companies House number, CIAT ID, ICO ID in `about.html` with real values
- [ ] Replace placeholder phone number (020 7946 0000) with real number site-wide (grep for `442079460000` in WhatsApp link too)
- [ ] Replace placeholder team bios if you're a solo founder — reduce `about.html` team section
- [ ] Replace placeholder testimonials with real ones (or mark clearly as "examples")
- [ ] Upload real logo if "A" monogram isn't final

### Legal
- [ ] Privacy Policy page added (link in footer — currently placeholder `#`)
- [ ] Terms of Service page added (link in register form — currently placeholder `#`)
- [ ] Cookie notice if using Google Analytics (not needed for Plausible)
- [ ] ICO registration confirmed and number added to footer (currently placeholder ZA847291)
- [ ] PI Insurance certificate available on request (noted in about.html)

### Business
- [ ] Google Business Profile verified (postcard arrived, code entered)
- [ ] CIAT directory listing submitted
- [ ] Trustpilot account created
- [ ] First review-request links sent to known contacts
- [ ] Bank account connected to Stripe and first payout received in test

---

## Ongoing maintenance

- **Weekly:** Check Sentry for unresolved errors, Search Console for crawl errors.
- **Monthly:** Review Stripe disputes, renew any expiring DNS records in Cloudflare.
- **Quarterly:** Content refresh — update pricing if changed, add new borough-specific content, refresh testimonials.
- **Annually:** Renew domain (Cloudflare auto-renews), review all subscriptions for cost creep.

---

**Done.** At the end of this runbook, `architecturaldrawings.uk` is live, accepts quotes, processes payments, sends emails, and is indexed by Google. Total setup time for an experienced agent: ~4–6 hours. Total monthly cost: ~£15–45 at launch scale.
