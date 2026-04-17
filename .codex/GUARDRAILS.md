# GUARDRAILS.md — the hard "do not touch" list

> These rules override any inferred best practice, personal taste, or "I think it would be better if...". Break one of them and the work gets reverted.

---

## 1. Visual parity — **100%, non-negotiable**

The site has a warm editorial minimalist design language that is already shipped and approved. You are not a designer on this project. See `CLAUDE.md` §3.6 for the structural-parity rules (no wrapping existing HTML in new container divs, no overriding `.portal-main`, no changing media query breakpoints, new sections live alongside existing content not around it).

### Forbidden
- New colour values. The palette is fixed:
  - `--bg: #FAFAF7` · `--bg-2: #F2EFE8` · `--surface: #FFFFFF`
  - `--ink: #0E1116` · `--ink-soft: #4A5260`
  - `--accent: #C8664A` · `--accent-deep: #9D4A32` · `--accent-soft: #F5E6DD`
  - `--success: #47845A` · `--line: rgba(14, 17, 22, 0.08)`
- New fonts. **Fraunces (display) and Manrope (body) only.** No Inter, Roboto, Space Grotesk, system-ui, Arial, DM Sans, Satoshi, Geist, or anything else.
- New radii, shadows, spacings, easings. Use the existing tokens in `assets/css/style.css`.
- New component shapes. Reuse `.service-card`, `.pricing-card`, `.process-step`, `.testimonial`, etc.
- Changing the logo, wordmark, or favicon.
- Changing the gloss/glow effect on the accent radial (`--shadow-glow: 0 20px 60px rgba(200, 102, 74, 0.18)`).
- Dark mode. Not in scope.
- Any animation longer than 600ms or any easing outside `--ease` / `--ease-spring`.

### Allowed
- **Adding** new pages that reuse existing patterns.
- **Adding** new sections inside existing pages that reuse existing patterns.
- **Adding** new pSEO rows or services via the generators in [scripts/](../scripts/).
- **Adding** new schema blocks, meta tags, or OG images (following the existing style).

If a task seems to require a new visual pattern — **stop and ask the operator**. Ninety percent of the time the answer is "reuse what's there."

---

## 2. Stack parity — no framework changes

### Forbidden
- Porting to Next.js, Remix, Astro, SvelteKit, Nuxt, Gatsby, or any other framework.
- Introducing React, Vue, Svelte, Solid, Preact, Alpine, htmx, Lit, or any other frontend library.
- Replacing vanilla JS with TypeScript (source-level — you can add JSDoc types).
- Replacing SQLite with Postgres / MySQL / Mongo **unless the operator asks** (the `better-sqlite3` swap path is documented but dormant).
- Replacing Express with Fastify / Hono / Elysia / Nest.
- Adding a bundler (Vite, Webpack, esbuild) to the frontend. It's deliberately bundler-free.
- Adding Tailwind, CSS-in-JS, or a CSS preprocessor. The stylesheet is hand-authored.

### Allowed
- Adding new Express routes under `api/routes/`.
- Adding new SQLite tables via `api/models/db.js`.
- Adding new static HTML pages that follow the inlined-CSS pattern (§3.1 of `CLAUDE.md`).
- Adding npm packages to `api/package.json` when strictly necessary (justify in the PR).

---

## 3. Tradematch isolation

**Architectural Drawings London and Tradematch are separate companies on Paperclip.** The fact that both use Claude/Codex and are owned by the same operator does not mean they share anything.

### Forbidden
- Reading files from the Tradematch workspace, repo, or Paperclip project.
- Copying code, assets, schema, copy, images, or config from Tradematch into Architectural Drawings (or vice versa).
- Sharing secrets, API keys, Stripe accounts, mail providers, analytics properties, or social handles across the two.
- Cross-linking the two properties in navigation, footers, schema, or backlinks.
- Mentioning Tradematch in Architectural Drawings copy, meta, or schema.

### Allowed
- Nothing. Treat the other project as if it belongs to a different company you have no access to.

---

## 4. Codebase hygiene

### Forbidden
- Hand-editing CSS inside `<style>` blocks across 14 HTML files. Always edit `assets/css/style.css`, then run the inliner.
- Reordering middleware in `api/server.js` — the Stripe webhook's `express.raw()` must sit **before** `express.json()` or signature verification silently fails.
- Removing the `.reveal` safety-net keyframe from any page.
- Swapping `sessionStorage` to `localStorage` in the portal. It's intentional.
- Breaking the `<picture>` + `srcset` pattern on images.
- Deleting the explicit `width` / `height` attributes on `<img>` (CLS regression).
- Removing existing schema blocks from any page.

---

## 5. SEO invariants (repeating these because they are life or death)

1. Every page has a unique `<title>` (50–60 chars) and `<meta name="description">` (150–160 chars).
2. Every page has a `<link rel="canonical">` — absolute URL, no trailing slash quirks.
3. Service detail pages have `Service` + `FAQPage` schema. Borough hubs have `Place` + `BreadcrumbList`. Landing has `LocalBusiness` + `FAQPage` + `BreadcrumbList`.
4. `robots.txt` disallows `/portal/` and `/api/`. Everything else is crawlable.
5. `sitemap.xml` lists every public page. Regenerate via `scripts/gen_sitemap.py` after adding pages.
6. Internal linking: every new page must link into and out of the existing topical cluster (borough hub ↔ service × borough ↔ parent service ↔ blog/guide).
7. **Footer SEO link grid (`.footer-seo` 4-column)** must appear on every page — inlined in the `<style>` block and in `assets/css/style.css`. New pages must include the block; use `scripts/add_seo_footer.py` to batch-add. See `CLAUDE.md` §4 "Footer SEO link grid".
8. **BreadcrumbList schema** must be present on every page. All 616 existing pages have it — do not regress.

---

## 6. HANDOVER.md — mandatory post-task update

**Every agent, after completing any task, must append an entry to [HANDOVER.md](../HANDOVER.md) before closing the session.**

Template:

```markdown
## {YYYY-MM-DD HH:MM UTC} — {Agent role/name}

**Author:** {agent identifier — e.g. "SEO Strategist", "Backlink Hunter", "Codex:content-writer", "Claude:pseo-optimiser"}
**Task:** {one-line task summary}
**Scope touched:** {files / routes / pages / external services}
**Result:** {shipped / partial / blocked — one sentence}
**Next action for the next agent:** {what's queued, what's waiting, what to verify}
**Links:** {PR, dashboard URL, ticket, Google Doc — whatever is relevant}
```

Rules:
- One entry per task completion. Not per file edit.
- Newest entries go at the **top** (reverse chronological) under the header.
- Use UTC timestamps so handoffs across agents and timezones line up.
- The `Author:` line is non-negotiable. Name yourself. A blank author is treated as a broken handoff.
- If you are blocked, still write the entry. A blocker is a handoff signal.
- If you changed branding, colours, fonts, framework, or stack — call it out explicitly in `Scope touched` with a 🛑 marker so a reviewer catches it. (It should be zero, per §1–§2, but flag it if it happened.)

The handover log is how the next agent (or the operator) gets caught up without re-reading the diff. Skipping it wastes everyone's time.

---

## 7. Escalation

If a task appears to require breaking any rule in §1–§6:

1. Do not do it.
2. Write the proposed change and its justification into the handover entry under `Next action for the next agent`.
3. Ask the operator in-channel.
4. Wait.

---

**End of GUARDRAILS.md.**
