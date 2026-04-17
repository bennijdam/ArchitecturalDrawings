# PAPERCLIP_SETUP.md — spinning up Architectural Drawings London as a new company

> This document is the one-and-only runbook for creating the Architectural Drawings workspace on Paperclip. Follow it top to bottom. Do not improvise. **Nothing in this setup touches the existing Tradematch workspace.**

---

## 0. Principle of isolation

Architectural Drawings London and Tradematch are two separate companies that happen to share an operator. They must **not** share:

- Paperclip workspaces
- Repos / branches
- API keys or secrets
- Domains, subdomains, or DNS records
- Analytics properties (GA4, Search Console)
- Stripe accounts or Stripe Connect profiles
- Mail providers / sending domains
- Social handles
- Ad accounts
- Review/citation profiles

If an agent ever finds itself needing a Tradematch credential to finish an Architectural Drawings task, the answer is "stop and ask". They do not share credentials.

---

## 1. Create the Paperclip workspace

1. Log into Paperclip with the operator account.
2. **Create a new workspace** — name it exactly: `Architectural Drawings London`.
3. Set workspace slug: `architectural-drawings-london`.
4. Set timezone: `Europe/London`.
5. Set default model for agents: whatever the operator has standardised on. Do not pick a weaker model to save cost — SEO and content work degrades noticeably below Sonnet / GPT-4-class.
6. **Do not** clone any settings from the Tradematch workspace. Start clean.

---

## 2. Link the repo

1. Create (or identify) the git repo for this project. Suggested name: `architectural-drawings-london`.
2. In the new Paperclip workspace, connect the repo.
3. Set the **primary working directory** inside the repo: `architectural-drawings/` (the actual site lives in this subfolder — matches the `CLAUDE.md` at the root of that folder).
4. Add these files to the workspace's default context (so every agent session loads them):
   - [AGENTS.md](../AGENTS.md)
   - [CLAUDE.md](../CLAUDE.md)
   - [.codex/GUARDRAILS.md](./GUARDRAILS.md)
   - [.codex/SKILLS.md](./SKILLS.md)
   - [HANDOVER.md](../HANDOVER.md)

---

## 3. Secrets and env

Create a **new** secret store for this workspace. Do not re-use Tradematch secrets.

### Required secrets
| Key | Purpose | Where it's used |
|---|---|---|
| `STRIPE_SECRET_KEY` | Stripe payments (live or test) | `api/routes/stripe.js` |
| `STRIPE_WEBHOOK_SECRET` | Webhook signature verification | `api/routes/stripe.js` |
| `JWT_SECRET` | Portal auth | `api/middleware/auth.js` |
| `DATABASE_URL` | SQLite path (or Postgres URL when we migrate) | `api/models/db.js` |
| `SMTP_HOST` / `SMTP_USER` / `SMTP_PASS` / `SMTP_FROM` | Transactional mail (quotes, receipts) | future `api/routes/mail.js` |
| `GSC_SERVICE_ACCOUNT_JSON` | Search Console API for reporting | SEO Strategist agent |
| `AHREFS_API_KEY` *or* `SEMRUSH_API_KEY` | Keyword + backlink data | SEO Strategist, Backlink Hunter |
| `GOOGLE_API_KEY` | PageSpeed Insights, Places API | Local SEO Auditor |
| `GBP_OAUTH_TOKEN` | Google Business Profile posts + review replies | Local SEO Auditor |

### Social media credentials (per-agent scope — see §5)
| Key | Platform |
|---|---|
| `INSTAGRAM_ACCESS_TOKEN` / `INSTAGRAM_BUSINESS_ID` | Instagram |
| `LINKEDIN_ACCESS_TOKEN` / `LINKEDIN_ORG_URN` | LinkedIn Company Page |
| `X_API_KEY` / `X_API_SECRET` / `X_ACCESS_TOKEN` / `X_ACCESS_SECRET` | X / Twitter |
| `TIKTOK_ACCESS_TOKEN` | TikTok Business |
| `PINTEREST_ACCESS_TOKEN` | Pinterest Business |
| `FACEBOOK_PAGE_TOKEN` / `FACEBOOK_PAGE_ID` | Facebook Page |
| `YOUTUBE_OAUTH_TOKEN` / `YOUTUBE_CHANNEL_ID` | YouTube |
| `THREADS_ACCESS_TOKEN` | Threads |

> Tag every secret with `workspace:architectural-drawings-london`. Paperclip's secret scoping must prevent agents in the Tradematch workspace from ever seeing them.

---

## 4. Domain + analytics + search consoles

1. **Register** `architecturaldrawings.uk` on a **new** registrar account or a separate account, not Tradematch's.
2. DNS: Cloudflare or registrar-native. Separate account from Tradematch.
3. **Google Search Console**: verify via DNS TXT. Add both `https://architecturaldrawings.uk` and `https://www.architecturaldrawings.uk`.
4. **Bing Webmaster Tools**: verify and submit sitemap.
5. **Google Analytics 4**: new property, new data stream. Do **not** add it to the Tradematch GA4 account.
6. **Google Business Profile**: new listing at `86–90 Paul Street, London EC2A 4NE` (confirm address with operator — see §9 of `CLAUDE.md`).
7. **Plausible / Fathom** (if used): new site.

---

## 5. Agent provisioning

Provision the agents defined in [.codex/agents/](./agents/). Spin up one Paperclip agent per spec sheet, with:

- **Scope:** limit each agent's file-system access and secret access to what it needs. The Social Media Manager never needs the database; the SEO Strategist never needs Stripe keys.
- **Model:** whatever the operator standardised on (don't downgrade).
- **Context files:** `AGENTS.md` + `GUARDRAILS.md` + `SKILLS.md` + the agent's own spec.
- **Handover discipline:** every agent run must update [HANDOVER.md](../HANDOVER.md) (see `GUARDRAILS.md` §6).

Agents to provision:

1. **SEO Strategist** — owns keyword research, SERP analysis, topical map, pSEO expansion planning.
2. **Backlink Hunter** — owns prospecting (Ahrefs/Majestic), qualification, outreach pipeline.
3. **Content Writer** — owns long-form blog, guide, glossary, and FAQ expansion.
4. **Outreach Specialist** — owns email sequences, replies, unlinked mentions, digital PR pitches.
5. **Social Media Manager** — owns the 7–8 social accounts and daily content cadence.
6. **Local SEO Auditor** — owns GBP, citations, NAP consistency, review velocity.
7. **pSEO Optimiser** — owns the 209 programmatic pages, their data, and their template.

See [.codex/agents/README.md](./agents/README.md) for coordination rules between them.

---

## 6. Social media account setup

The Social Media Manager agent needs live accounts before it can post. Create (or claim) them in this order and hand credentials over via secrets (§3), not plain text.

| Priority | Platform | Handle (suggested) | Why |
|---|---|---|---|
| 1 | **LinkedIn Company Page** | `architectural-drawings-london` | Trust signal for B2B + homeowner researchers; strong for MCIAT credential story |
| 1 | **Instagram Business** | `@architecturaldrawings.london` | Visual — before/after, drawings, site photos |
| 2 | **Pinterest Business** | `architecturaldrawings` | High intent for home-renovation searches; long-tail referral traffic |
| 2 | **YouTube Channel** | `Architectural Drawings London` | How-to and explainer videos. Enormous long-tail SEO value. |
| 3 | **TikTok Business** | `@architecturaldrawings.london` | Short explainers — "what triggers planning in Camden" type content |
| 3 | **Facebook Page** | `architecturaldrawings.london` | Local London groups, reviews surface |
| 4 | **X / Twitter** | `@ADrawingsLondon` | Industry visibility, RIBA / CIAT / planning-policy conversations |
| 4 | **Threads** | `@architecturaldrawings.london` | Mirror Instagram with minimal extra effort |

After creation:
- Fill out every bio, link-in-bio, pinned post, and cover image following the brand system (Fraunces + terracotta — export OG-style covers from the existing design tokens).
- Cross-verify the business on Instagram and Facebook (Meta Business Suite).
- Connect all accounts to the agent via the tokens in §3.

---

## 7. Verify the boundary

Before handing off to the agents, run this smoke test:

- [ ] From an Architectural Drawings agent session, try to list files in the Tradematch workspace → should be denied.
- [ ] From an Architectural Drawings agent session, try to read a Tradematch secret → should be denied.
- [ ] `grep -r "tradematch" architectural-drawings/` → zero matches.
- [ ] `grep -r "architecturaldrawings" tradematch/` → zero matches.
- [ ] GA4 properties: two distinct measurement IDs.
- [ ] Stripe dashboards: two distinct accounts.
- [ ] Git remotes: two distinct repos.

If any of these fail, fix the isolation before continuing.

---

## 8. Kickoff task

Once the workspace is live, the first real task is **not** to write code. It is:

1. SEO Strategist builds the v1 topical map and keyword list (2 days).
2. pSEO Optimiser verifies the 209 pages render clean and submits the sitemap to GSC + Bing (1 day).
3. Local SEO Auditor claims GBP + starts citation build (ongoing).
4. Content Writer queues 12 long-form guides against the topical map (2 weeks of capacity).
5. Backlink Hunter builds the prospect list (Ahrefs + manual SERP scraping) — target 200 qualified prospects in week 1.
6. Outreach Specialist launches email sequence v1 (week 2).
7. Social Media Manager publishes launch-week content calendar on all platforms (week 1).

Each of these lands an entry in `HANDOVER.md` the moment it ships. No silent work.

---

**End of PAPERCLIP_SETUP.md.**
