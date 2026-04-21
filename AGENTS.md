# AGENTS.md — Codex entry point for Architectural Drawings London

> Codex reads this file automatically at session start. It is the authoritative brief for any agent (Codex, Cursor, Claude, or a human operator) working on **Architectural Drawings London** inside Paperclip.
>
> **If you are an agent working on Tradematch: STOP. You are in the wrong repo.** This project is a new company being set up alongside Tradematch on Paperclip. Do not touch, reference, copy from, or import anything from Tradematch. Treat the two companies as hermetically sealed.

---

## 0. Prime directive

You are not here to redesign, refactor, or "modernise" anything. The site, stack, branding, fonts, colours, gloss/glow effects, logo, component patterns, and file layout are **frozen**. You are here to:

1. Build **on top of** the existing codebase (new pages, new pSEO, new content, new schema, new integrations).
2. Win **organic UK search** — page 1 on Google for every service × borough combination, every long-tail intent, every featured snippet we can claim.
3. Acquire **high-quality backlinks** to grow domain authority.
4. Run the **social media presence** across platforms where architects, homeowners, and London property circles live.
5. Report what moved and what did not.

Anything outside this scope needs the operator's written approval before you touch it.

Every agent must also follow these session-start rules:

1. Read `CLAUDE.md` for project constraints and implementation conventions.
2. Read `OPENAI.md` if you are an OpenAI-family agent or using GPT/Codex tooling.
3. Preserve **100% visual parity** with the shipped site.
4. Use `index.html` as the canonical design reference for any additive UI or UX work, including logo, footer, menu, and button styling.
5. If a proposed change would alter the established look and feel, stop and ask the operator.

---

## 1. Hard constraints — read `.codex/GUARDRAILS.md` before every session

The short version, so you cannot miss it:

| Area | Rule |
|---|---|
| Design | **100% visual parity.** No new colours, fonts, spacings, radii, shadows, or component styles. |
| Stack | Static HTML + vanilla JS frontend, Node/Express/SQLite backend. **Do not port to Next.js, React, Astro, etc.** |
| Branding | Fraunces + Manrope only. `#C8664A` terracotta accent only. Warm cream palette only. Do not introduce Inter, Space Grotesk, system-ui, or any other font. |
| Tradematch | **Do not read, reference, or import anything from the Tradematch project on Paperclip.** They are separate companies. |
| File layout | Follow §2 of `CLAUDE.md`. Do not restructure directories. |
| Tokens | Edit CSS tokens in `assets/css/style.css`, then re-run the inliner. Do not hand-edit 14 HTML files. |

Full detail lives in [.codex/GUARDRAILS.md](.codex/GUARDRAILS.md).

---

## 2. Project context (quick version)

- **Company:** Architectural Drawings London — MCIAT-chartered architectural technology practice.
- **Domain (intended):** `architecturaldrawings.uk`
- **What it sells:** Planning drawings, building regs, loft conversions, house extensions, mansard roofs — fixed-fee, 30% below typical London architect rates.
- **Content surface area:** 616 URLs across 2 sub-sitemaps — 364 pSEO pages (33 boroughs × 10 services + 33 hubs), 135 blog posts, 80 neighbourhood pages, 10 case studies, 3 cornerstone guide hubs, team/FAQ/glossary/resources/why-us hubs, cost calculator, PD checker.
- **Authority claims:** MCIAT chartered · 98% first-time approval · all 33 London boroughs.

The full product brief lives in [CLAUDE.md](CLAUDE.md). Read it before writing code.

---

## 3. Paperclip setup

Setting up this company as a new Paperclip workspace (separate from Tradematch): follow [.codex/PAPERCLIP_SETUP.md](.codex/PAPERCLIP_SETUP.md) step by step. It covers workspace creation, repo linking, secrets, env vars, and the hard boundary that keeps this company isolated from the Tradematch workspace.

---

## 4. Agents

This repo uses a small fleet of focused agents. Each has a spec sheet under [.codex/agents/](.codex/agents/). Spawn only the agent that matches the task; do not let agents bleed into each other's scope.

| Agent | File | Purpose | Spawn when... |
|---|---|---|---|
| **SEO Strategist** | [.codex/agents/seo-strategist.md](.codex/agents/seo-strategist.md) | Keyword research, SERP gap analysis, topical maps, pSEO expansion | You're planning content or targeting new keywords |
| **Backlink Hunter** | [.codex/agents/backlink-hunter.md](.codex/agents/backlink-hunter.md) | Prospect + qualify link targets, outreach, HARO, digital PR | You're building DR/DA |
| **Content Writer** | [.codex/agents/content-writer.md](.codex/agents/content-writer.md) | Long-form guides, blog posts, glossary entries, FAQ expansion | You need new on-page content |
| **Outreach Specialist** | [.codex/agents/outreach-specialist.md](.codex/agents/outreach-specialist.md) | Cold email, link reclamation, unlinked-mention conversion, guest posts | You have a backlink prospect list and need replies |
| **Social Media Manager** | [.codex/agents/social-media-manager.md](.codex/agents/social-media-manager.md) | Posts + engagement on Instagram, LinkedIn, X, TikTok, Pinterest, Facebook | You need distribution + brand awareness |
| **Local SEO Auditor** | [.codex/agents/local-seo-auditor.md](.codex/agents/local-seo-auditor.md) | GBP, citations, NAP consistency, review velocity, local schema | You're chasing map-pack + "near me" queries |
| **pSEO Optimiser** | [.codex/agents/pseo-optimiser.md](.codex/agents/pseo-optimiser.md) | Maintain + extend the 209 programmatic pages, add new boroughs/services | You're editing the pSEO data or template |

How they work together is described in [.codex/agents/README.md](.codex/agents/README.md).

---

## 5. Skills

The repertoire of things agents should know how to do (keyword clustering, schema authoring, outreach email templates, OG image generation, etc.) is catalogued in [.codex/SKILLS.md](.codex/SKILLS.md). Before starting a task, skim that file to see whether a skill already exists for it.

---

## 6. Success metric

The only north-star metric is **organic clicks from UK searchers to commercial-intent pages**, measured in Google Search Console, with conversion to quote-form submissions as the validating signal. Every task should be traceable to that number.

Secondary metrics:
- Referring domains (Ahrefs/Majestic) — target +20 DR30+ domains per quarter
- Indexed pages (GSC coverage) — target 100% of 209 URLs indexed within 60 days of launch
- Map-pack impressions for `{service} {borough}` — target top-3 in 20 boroughs by month 6
- Social: follower growth is vanity; referral traffic to quote flow is the real number

---

## 7. When in doubt

Ask the operator. Do not guess. Do not ship. Do not "clean up". The codebase is the way it is on purpose — re-read §10 of `CLAUDE.md` ("Gotchas") before assuming anything is broken.

---

**End of AGENTS.md.** Proceed to [.codex/GUARDRAILS.md](.codex/GUARDRAILS.md) next.
