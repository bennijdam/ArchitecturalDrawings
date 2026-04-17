# agents/ — how the fleet is structured

> Seven agents. Each owns a narrow domain. They do not bleed into each other's work. They communicate via [HANDOVER.md](../../HANDOVER.md).

---

## The fleet

| # | Agent | Owns | Does not own |
|---|---|---|---|
| 1 | [SEO Strategist](./seo-strategist.md) | Keyword research, SERP analysis, topical map, reporting | Writing content, building links, posting social |
| 2 | [Backlink Hunter](./backlink-hunter.md) | Prospecting + qualification | Sending outreach, writing guest posts |
| 3 | [Content Writer](./content-writer.md) | Long-form guides, glossary, case studies, FAQ | Technical SEO, schema audits, social posts |
| 4 | [Outreach Specialist](./outreach-specialist.md) | Email sequences, HARO/Qwoted, unlinked mentions, broken links | Finding new prospects, writing the linked-to content |
| 5 | [Social Media Manager](./social-media-manager.md) | All 7–8 platforms, daily posts, DMs, engagement | Technical site work |
| 6 | [Local SEO Auditor](./local-seo-auditor.md) | GBP, citations, NAP, reviews, local schema | National SEO, content authoring |
| 7 | [pSEO Optimiser](./pseo-optimiser.md) | The 209 programmatic pages, their data, their template | Hand-authored pages, social content |

---

## Coordination rules

1. **Handover is the only source of truth.** No verbal state, no "Claude-to-Claude" side channels. Every task ends with a `HANDOVER.md` entry.
2. **Narrow scope = no bleed.** The Content Writer does not edit the pSEO template. The pSEO Optimiser does not write a blog post. If a task straddles two agents, the operator decides who owns it.
3. **One agent per Paperclip session.** Don't multiplex — it corrupts the audit trail.
4. **Escalate on guardrail conflicts.** Any task that appears to require breaking a guardrail goes to the operator, not to another agent.
5. **No secret sharing between agents.** The Social Media Manager holds the X API key and never passes it to the Outreach Specialist even if "it would be convenient".

---

## Default cadence

| Agent | Cadence |
|---|---|
| SEO Strategist | Weekly GSC report + monthly topical map review |
| Backlink Hunter | Continuous prospect refresh; weekly qualified-prospect hand-off to Outreach |
| Content Writer | 2 long-form + 4 short-form pieces per week |
| Outreach Specialist | Daily sends (capped 30/day) + daily HARO triage |
| Social Media Manager | Daily posts (per platform calendar) + twice-daily engagement window |
| Local SEO Auditor | Weekly GBP post + monthly citation audit + continuous review response |
| pSEO Optimiser | On-demand (new borough / new service) + monthly sanity regeneration |

---

## Operator interventions

The operator reviews:
- All outbound email before the sequence goes live.
- All social accounts' first post on each platform.
- Any guest-post manuscript before submission.
- Any schema block the first time a new type is introduced.
- Any change that might touch branding, colours, fonts, framework, or stack (answer is usually no).

---

**End of agents/README.md.**
