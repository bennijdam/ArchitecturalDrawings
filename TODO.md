# FULL PRODUCTION READINESS AUDIT TODO

You are performing a FULL PRODUCTION READINESS AUDIT of this codebase.

This is NOT a summary task.
This is NOT a high-level review.

Your job is to find REAL, SPECIFIC, VERIFIABLE problems across the entire system:
- frontend
- backend
- database
- API wiring
- authentication
- E2E flows

You MUST operate like a senior staff engineer doing a pre-launch audit.

## Priority 0

- [ ] Create the missing password reset completion page at `portal/reset.html` and wire it to `POST /api/auth/reset-password/confirm`.
- [ ] Remove production demo-auth fallbacks from `portal/login.html` and `portal/register.html` so API outages do not create fake logged-in sessions.
- [ ] Remove or strictly gate direct static serving of uploaded files from `api/server.js`; access should only flow through authenticated file routes.
- [ ] Validate that upload records cannot be attached to arbitrary `project_id` values without ownership checks.

## Priority 1

- [ ] Replace placeholder project imagery and placeholder content on project pages and the projects index.
- [ ] Audit all public callback, quote, and exit-intent forms for real submission handling versus cosmetic success states.
- [ ] Validate Stripe success/cancel return URLs against the actual deployed routing model.
- [ ] Confirm CORS settings support every real production origin that needs API access.
- [ ] Confirm JWT secret and environment defaults cannot fall back to development values in a live deployment.

## Priority 2

- [ ] Audit portal flows end to end: login, register, session restore, profile update, file upload, callbacks admin view, payment redirect, and sign-out.
- [ ] Audit data-layer durability assumptions for SQLite and local file uploads in the chosen hosting model.
- [ ] Review rate limits and abuse controls on public form endpoints.
- [ ] Review email delivery guarantees and failure handling for auth reset, quotes, and callback notifications.

## Evidence-backed findings to address first

1. Missing reset page: backend emails users a reset link to `portal/reset.html`, but that file does not exist.
2. Demo login fallback: failed login requests in the portal still create `sessionStorage` auth state and redirect into the dashboard.
3. Demo register fallback: failed registration requests also create fake authenticated portal state.
4. Upload exposure risk: uploads are auth-gated in `api/routes/files.js` but also statically exposed in `api/server.js`.
5. Public-facing placeholders remain in production content, especially in project pages and the projects index.

## Audit execution rule

Do not mark an item done until it has been verified against the actual user flow, not just by code inspection.