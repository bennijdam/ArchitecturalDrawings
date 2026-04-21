# OPENAI.md

This file is for OpenAI-family agents working in this repository. Read it at the start of every session.

## Core rule

You are working inside a live commercial codebase. Your default posture is production safety, visual preservation, and minimal surface-area change.

## Non-negotiables

1. **Design cannot be changed.** Maintain **100% visual parity** with the existing site unless the operator explicitly approves a visual change.
2. **Use `index.html` as the canonical UI reference.** Any new UI or UX must match its design language, including logo treatment, footer layout, navigation/menu behavior, button styles, typography, color palette, spacing rhythm, and interaction tone.
3. **Do not create a new design system.** No alternate component family, no new visual motif, and no new branding interpretation.
4. **Preserve structure where possible.** Make the smallest viable change that solves the problem.
5. **Audit like a staff engineer.** Prefer specific, reproducible, file-backed findings over summaries or opinions.

## What to read first

1. `AGENTS.md`
2. `CLAUDE.md`
3. `ARCHITECTURE.md`
4. `HANDOVER.md`
5. `TODO.md`

## Expected working style

1. Verify assumptions from code before changing anything.
2. Prioritize launch blockers: auth, payments, uploads, callbacks, quote submission, broken links, missing files, security exposure, and deployment mismatch.
3. If a flow has a demo fallback, treat it as a production risk until proven otherwise.
4. If a page or endpoint is referenced but missing, treat it as a real defect.
5. If a route is public by accident, or data/files can leak outside intended auth gates, treat it as a high-severity issue.

## Output standard

When asked for an audit:

1. Lead with findings, ordered by severity.
2. Reference specific files and lines.
3. State why each issue is real and how it can fail in production.
4. Then provide a prioritized remediation list.

## Change standard

When implementing fixes:

1. Preserve exact visuals.
2. Keep the stack unchanged.
3. Avoid unrelated cleanup.
4. Update `HANDOVER.md` after substantial work.