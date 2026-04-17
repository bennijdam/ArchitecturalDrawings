# SKILLS.md — capabilities catalogue for Architectural Drawings agents

> A skill is a repeatable capability an agent is expected to be fluent in. Before starting a task, check whether a skill already covers it. If one does, use it verbatim rather than reinventing.
>
> Each skill has: purpose, when to use it, the method, and the output shape. Where a skill needs external data, the data source is named.
>
> **Before every task starts:** re-read `.codex/GUARDRAILS.md`.
> **After every task ends:** append an entry to `HANDOVER.md` with yourself as `Author:`.

---

## Skill index

### SEO
- [S-01 Keyword clustering](#s-01-keyword-clustering)
- [S-02 SERP gap analysis](#s-02-serp-gap-analysis)
- [S-03 Topical map authoring](#s-03-topical-map-authoring)
- [S-04 On-page optimisation audit](#s-04-on-page-optimisation-audit)
- [S-05 Schema authoring (JSON-LD)](#s-05-schema-authoring-json-ld)
- [S-06 Internal-link planning](#s-06-internal-link-planning)
- [S-07 pSEO expansion (borough / service)](#s-07-pseo-expansion)
- [S-08 Featured-snippet targeting](#s-08-featured-snippet-targeting)
- [S-09 Search Console reporting](#s-09-search-console-reporting)
- [S-10 Crawl + index audit](#s-10-crawl--index-audit)

### Local SEO
- [L-01 Google Business Profile ops](#l-01-google-business-profile-ops)
- [L-02 Citation building (NAP)](#l-02-citation-building-nap)
- [L-03 Review generation + response](#l-03-review-generation--response)
- [L-04 Local-intent content patterning](#l-04-local-intent-content-patterning)

### Backlinks
- [B-01 Prospect list building](#b-01-prospect-list-building)
- [B-02 Prospect qualification](#b-02-prospect-qualification)
- [B-03 Cold outreach sequences](#b-03-cold-outreach-sequences)
- [B-04 Digital PR / HARO / Qwoted](#b-04-digital-pr--haro--qwoted)
- [B-05 Unlinked-mention conversion](#b-05-unlinked-mention-conversion)
- [B-06 Broken-link recovery](#b-06-broken-link-recovery)
- [B-07 Guest-post placement](#b-07-guest-post-placement)
- [B-08 Resource-page inclusion](#b-08-resource-page-inclusion)

### Content
- [C-01 Long-form guide authoring](#c-01-long-form-guide-authoring)
- [C-02 Glossary + definition pages](#c-02-glossary--definition-pages)
- [C-03 FAQ expansion](#c-03-faq-expansion)
- [C-04 Case study authoring](#c-04-case-study-authoring)
- [C-05 London planning-policy explainers](#c-05-london-planning-policy-explainers)

### Social
- [X-01 Content-calendar planning](#x-01-content-calendar-planning)
- [X-02 Platform-native post authoring](#x-02-platform-native-post-authoring)
- [X-03 Engagement + community management](#x-03-engagement--community-management)
- [X-04 OG / social-card generation](#x-04-og--social-card-generation)
- [X-05 Short-form video scripting](#x-05-short-form-video-scripting)

### Engineering hygiene
- [E-01 Inliner + CSS token propagation](#e-01-inliner--css-token-propagation)
- [E-02 Sitemap regeneration](#e-02-sitemap-regeneration)
- [E-03 Backend route scaffolding](#e-03-backend-route-scaffolding)
- [E-04 HANDOVER.md entry](#e-04-handovermd-entry)

---

## SEO skills

### S-01 Keyword clustering
**Purpose:** group raw keyword lists into pages so one page targets one intent cluster.
**When:** before content planning, pSEO expansion, or topical-map work.
**Method:** pull keywords (Ahrefs/Semrush API, or GSC queries for existing traffic). Cluster by SERP overlap (≥3 shared URLs in top-10 = same cluster). Assign each cluster to a single URL.
**Output:** CSV or markdown table with columns: `cluster_name | primary_keyword | secondary_keywords | target_url | search_volume | kd`.

### S-02 SERP gap analysis
**Purpose:** find keywords competitors rank for that we don't.
**When:** quarterly, and before planning new content sprints.
**Method:** compare our domain against 5 named competitors (Resi, Urbanist Architecture, Extension Architecture, Simply Extend, any borough-specific rival). Use Ahrefs "Content Gap" or equivalent. Filter to KD ≤ 30, intent = informational or commercial, UK results.
**Output:** ranked list of top 50 gap keywords with recommended target URL (existing or new).

### S-03 Topical map authoring
**Purpose:** define the universe of pages we intend to own for a topic.
**When:** launching a new service line or borough cluster.
**Method:** pillar → cluster → supporting. Each pillar = core service (e.g. "loft conversions"). Each cluster = intent group (e.g. "cost", "permitted development", "borough rules"). Each supporting page = long-tail query or FAQ.
**Output:** nested markdown outline in `docs/topical-maps/{topic}.md`.

### S-04 On-page optimisation audit
**Purpose:** make sure a target page is maxed out for its keyword.
**When:** before requesting indexing, or when a page has impressions but weak rank.
**Method:** verify: H1 matches intent, title 50–60 chars with primary keyword, meta 150–160 chars with CTA, first 100 words contain the primary keyword, entities present (MCIAT, borough name, LPA, Article 4, Class MA, etc.), internal links to 3+ related pages, schema present, image alts descriptive, canonical correct.
**Output:** checklist filled in, plus edits applied directly.

### S-05 Schema authoring (JSON-LD)
**Purpose:** ship rich-result-eligible schema without breaking validators.
**When:** every new page. Required types: `LocalBusiness`, `Service`, `FAQPage`, `BreadcrumbList`, `Article`, `HowTo`, `Review`, `AggregateRating`, `Place`.
**Method:** copy the matching block from existing pages, substitute data, run through Google's Rich Results Test and Schema.org validator. Keep `@id` URLs consistent.
**Output:** `<script type="application/ld+json">` block, test result screenshot linked in handover.

### S-06 Internal-link planning
**Purpose:** distribute PageRank and keep crawl depth ≤ 3.
**When:** every new page, and during quarterly audits.
**Method:** each new page needs ≥3 inbound contextual links from existing pages, and ≥3 outbound to related clusters. Borough hub ↔ borough×service ↔ parent service ↔ relevant blog/guide ↔ glossary. Anchor text varied, never stuffed.
**Output:** diff showing added anchors + target URLs.

### S-07 pSEO expansion
**Purpose:** add new rows (borough / service / combination) to the 364-page programmatic set (33 boroughs × 10 services + 33 hubs + 1 index).
**When:** expanding into a new borough, town, or service.
**Method:** follow `CLAUDE.md` §6.6. Edit `scripts/pseo_boroughs.py` or `scripts/pseo_services.py`, run `gen_pseo.py`, run `gen_sitemap.py`. Never hand-edit the generated pages.
**Output:** new pages under `/areas/`, refreshed `sitemap.xml`, handover entry.

### S-08 Featured-snippet targeting
**Purpose:** claim position-zero boxes.
**When:** when a page has stable top-5 rank but no snippet.
**Method:** identify the SERP snippet format (paragraph / list / table). Add an exact-format answer block at the top of the page's content body, under a question-phrased H2. 40–55 words for paragraph, 6–8 items for list, include units/numbers where SERP does.
**Output:** edited section + SERP screenshot pre/post.

### S-09 Search Console reporting
**Purpose:** turn GSC data into decisions.
**When:** weekly. Also ad-hoc before any content sprint.
**Method:** pull impressions / clicks / CTR / avg position at query × page granularity for last 28 days. Flag: queries with position 8–20 and CTR < 1% (opportunity), pages with impressions down > 25% WoW (investigate), new queries we started ranking for.
**Output:** markdown report with three sections: `Wins`, `Opportunities`, `Regressions`.

### S-10 Crawl + index audit
**Purpose:** make sure everything we ship gets indexed.
**When:** after every launch or sitemap update.
**Method:** run Screaming Frog (or similar), compare to `sitemap.xml`, compare to GSC indexed count. Chase 404s, 3xx chains, canonical mismatches, orphan pages.
**Output:** report + fixes applied.

---

## Local SEO skills

### L-01 Google Business Profile ops
**Purpose:** make the GBP a conversion surface.
**When:** setup + weekly updates.
**Method:** fill 100% of profile fields. Post updates weekly (service spotlights, planning-policy commentary, case studies). Upload new photos monthly. Respond to every review within 24 hours. Add service-area boroughs individually (not a radius).
**Output:** post published + handover entry.

### L-02 Citation building (NAP)
**Purpose:** consistent Name/Address/Phone across the web for local trust signals.
**When:** setup, then monthly top-up.
**Method:** build citations on: Yell, Thomson Local, Bing Places, Apple Maps, Brownbook, Cylex, Hotfrog, FreeIndex, Scoot, CIAT directory, RIBA-adjacent directories, London-specific trade directories. Keep NAP character-for-character identical.
**Output:** tracker spreadsheet of citations with URL + date + verification status.

### L-03 Review generation + response
**Purpose:** move the GBP review count and the aggregate rating.
**When:** continuous.
**Method:** post-project email (templated, reviewed by operator first) with a one-click GBP review link. Respond to every review: thank positives, address negatives with the operator-approved playbook. Never fake reviews.
**Output:** review-velocity chart (weekly new reviews), response-rate percentage.

### L-04 Local-intent content patterning
**Purpose:** make every local page answer "why this borough specifically".
**When:** every pSEO page.
**Method:** include verifiable local facts — council name, LPA portal URL, Article 4 status, conservation-area count, common housing stock, average application timeline, recent planning committee decisions of note. All facts source-linked in page comments (not visible) for later re-verification.
**Output:** page passes the "would a local homeowner believe we work here" smell test.

---

## Backlinks skills

### B-01 Prospect list building
**Purpose:** fill the outreach pipeline.
**When:** continuously; refresh weekly.
**Method:** sources — Ahrefs "Link Intersect" (what links to 3 competitors but not us), London property blogs, home-renovation publications, CIAT member directory reciprocals, borough-level community sites, Help-a-B2B-Writer, HARO, Qwoted, Terkel, SourceBottle, Featured, Connectively. Dedupe by root domain.
**Output:** Airtable / sheet with: `domain | page_url | DR | topical_relevance | contact_name | contact_email | angle | status`.

### B-02 Prospect qualification
**Purpose:** avoid wasted outreach and toxic links.
**When:** every prospect before it enters outreach.
**Method:** qualify on: DR ≥ 20, organic traffic ≥ 500/mo, topical relevance (home/property/London/architecture/planning), not a link farm (spam score, outbound/inbound ratio), not a PBN (whois, hosting overlap), not already linking to us.
**Output:** the `status` column moves from `raw` to `qualified` or `rejected`.

### B-03 Cold outreach sequences
**Purpose:** get replies and placements.
**When:** every qualified prospect.
**Method:** 3-touch sequence over 10 days. Personalised first line (must reference something specific to the prospect's site). Clear, small ask. No link in touch 1. Plain-text, no images, no signature bloat. Send via a domain that is **not** Tradematch's.
**Output:** reply rate, placement rate, cost per placement — logged weekly.

### B-04 Digital PR / HARO / Qwoted
**Purpose:** earn high-DR editorial links via journalist quotes.
**When:** daily review of queries from HARO + Qwoted + Featured + Terkel.
**Method:** respond only to queries where the MCIAT credential + London planning expertise is a genuine fit. Answer in ≤150 words with a quotable sentence early. Include byline: name, MCIAT, Architectural Drawings London, link.
**Output:** pitch sent + placement tracker.

### B-05 Unlinked-mention conversion
**Purpose:** turn brand mentions without a link into linked ones.
**When:** weekly (Google Alerts + Ahrefs Mentions feed).
**Method:** find mentions of "Architectural Drawings London" or operator/founder name without a link. Email the author politely requesting the link. Include the exact anchor suggestion.
**Output:** request sent + tracker.

### B-06 Broken-link recovery
**Purpose:** reclaim links pointing to dead URLs on our domain.
**When:** monthly.
**Method:** Ahrefs "Best by Backlinks" with 404 filter → either restore the page at the old URL or 301 it to the best modern equivalent. Email linkers if the old content is genuinely gone.
**Output:** 301 map updated + inbound link count recovered.

### B-07 Guest-post placement
**Purpose:** authoritative contextual links on topically relevant sites.
**When:** opportunistic; target 2 placements per month.
**Method:** pitch ideas tailored to each target's existing gaps (from S-02). Deliver manuscripts that are genuinely the best content the host has on that topic. One relevant link in the body, one in bio, both with varied anchors.
**Output:** published URL + DR + indexed status.

### B-08 Resource-page inclusion
**Purpose:** land on curated "best of" resource pages.
**When:** continuous.
**Method:** search for `intitle:"resources" loft conversion London`, `"useful links" planning permission`, `"recommended" architect London`, etc. Pitch inclusion with a one-sentence value prop.
**Output:** placements logged.

---

## Content skills

### C-01 Long-form guide authoring
**Purpose:** comprehensive pages that earn links on their own merit.
**When:** per content sprint (see SEO Strategist cadence).
**Method:** 2,500–4,500 words. Intent-first structure (answer the query in the first paragraph, then expand). Include a costed example, a decision tree, a downloadable checklist, original diagrams (commissioned from the operator, not AI-generated unless approved). Fully schema'd (Article + HowTo where fits). Internal links to 5+ related pages. Images with descriptive alt.
**Output:** page shipped under `/guides/` or `/blog/`.

### C-02 Glossary + definition pages
**Purpose:** rank for `what is X` queries and feed the topical map.
**When:** whenever a new term is introduced in any page.
**Method:** 300–800 words per term. Definition in first sentence (snippet-eligible). Worked example. Related terms sidebar. Link to the service pages where the term applies.
**Output:** page under `/glossary/`.

### C-03 FAQ expansion
**Purpose:** capture long-tail question queries and feed FAQ schema.
**When:** continuously.
**Method:** pull questions from GSC, People-Also-Ask, AnswerThePublic, and Reddit (London planning threads). Answer each in 40–80 words. Add to the page's inline FAQ + `FAQPage` schema block.
**Output:** edited page + schema diff.

### C-04 Case study authoring
**Purpose:** E-E-A-T + conversion asset.
**When:** per completed project (with client permission).
**Method:** before / brief / challenge / drawings (images) / outcome (approval, timeline, cost). 600–1,200 words. Borough-tagged. Linked from the matching borough hub and service page.
**Output:** page under `/projects/{slug}.html`.

### C-05 London planning-policy explainers
**Purpose:** topical authority + cited by journalists (= backlinks).
**When:** when a borough updates its Local Plan, an Article 4 direction changes, or a national permitted-development change is tabled.
**Method:** explain the change plainly, cite the source document (LPA PDF), explain who's affected and how, suggest next steps. Publish within 72 hours of the change being public.
**Output:** timely guide + PR outreach to property journalists.

---

## Social skills

### X-01 Content-calendar planning
**Purpose:** predictable cadence so nothing is ad-hoc.
**When:** weekly planning for the following week.
**Method:** 5–7 posts per week per platform on LinkedIn + Instagram; 3 per week on Pinterest; 2 per week on TikTok/YouTube Shorts; 1–2 per week on X/Threads/Facebook. Mix: educational (40%), case study (20%), planning-policy commentary (20%), cultural/brand (10%), CTA (10%).
**Output:** calendar committed to a shared sheet with slot × platform × brief × asset link.

### X-02 Platform-native post authoring
**Purpose:** each platform gets the format it rewards — no lazy cross-posting.
**When:** every post.
**Method:** LinkedIn — hook line + structured body + CTA, 1,200–1,600 chars, no link in post (put in comment). Instagram — carousel 6–10 slides, hook on slide 1, single focal CTA. Pinterest — vertical 2:3 with bold title overlay. TikTok/Shorts — 30–60s, caption hook first line, voiceover tight. X/Threads — thread if > 280 chars, hook + 3–7 follow-ups.
**Output:** post published on schedule.

### X-03 Engagement + community management
**Purpose:** reach comes from interaction, not broadcast.
**When:** twice daily weekdays.
**Method:** comment on 10 relevant posts per day (architects, property journalists, London borough accounts, renovation creators). Respond to DMs and comments within 4 business hours. Never use generic replies.
**Output:** engagement log + conversions tracked via UTM'd profile links.

### X-04 OG / social-card generation
**Purpose:** every shared URL has an on-brand preview card.
**When:** every new published page.
**Method:** generate 1200×630 OG image using Fraunces + Manrope + terracotta accent on cream. Use the existing card template — do not design a new one. Save to `assets/img/og/{slug}.jpg`.
**Output:** OG image + updated `<meta property="og:image">`.

### X-05 Short-form video scripting
**Purpose:** scalable explainers for TikTok / Shorts / Reels.
**When:** 2 per week minimum.
**Method:** 30–60 seconds. First 2 seconds = hook. One idea per video. Subtitle-burned. End on a CTA to the matching guide or borough hub. Voiceover recorded by the operator or an approved contractor.
**Output:** script + storyboard + final video file.

---

## Engineering hygiene skills

### E-01 Inliner + CSS token propagation
**Purpose:** keep the 14 HTML files in sync with `assets/css/style.css`.
**When:** after any CSS token change.
**Method:** edit `assets/css/style.css`. Run the inliner script. Grep old values to confirm none remain. Follow `CLAUDE.md` §6.5.
**Output:** diff of updated HTML files.

### E-02 Sitemap regeneration
**Purpose:** keep `sitemap.xml` in sync with the page set.
**When:** after adding/removing any public page.
**Method:** `python3 scripts/gen_sitemap.py`.
**Output:** updated `sitemap.xml` + resubmit in GSC + Bing.

### E-03 Backend route scaffolding
**Purpose:** add new API endpoints without drifting from conventions.
**When:** new feature needs server logic.
**Method:** follow `CLAUDE.md` §5. Validator + prepared statements + auth where required. Never refactor middleware order.
**Output:** new route file + mount in `server.js` + handover entry.

### E-04 HANDOVER.md entry
**Purpose:** the handoff is the product of every session. No entry = the work didn't happen.
**When:** at the end of every task, without exception.
**Method:** follow the template in `.codex/GUARDRAILS.md` §6. UTC timestamp. Your role as `Author:`. Newest entry at the top.
**Output:** one new entry in `HANDOVER.md`.

---

**End of SKILLS.md.** Skills are living — propose additions via PR with the operator's review.
