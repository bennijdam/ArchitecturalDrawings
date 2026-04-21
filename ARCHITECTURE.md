# ARCHITECTURE.md

## Purpose

This document describes the runtime architecture of the repository so agents can reason about production risk without redesigning the system.

## System shape

The codebase is a hybrid of:

1. A static multi-page marketing site served from root-level `.html` files and nested content folders.
2. A Node/Express API under `api/` for auth, quotes, callbacks, projects, file upload, and Stripe checkout.
3. A static portal UI under `portal/` that talks to the API with browser `fetch` calls and bearer tokens stored in `sessionStorage`.
4. SQLite persistence in `api/models/db.js`.

## Frontend architecture

- Public pages are standalone HTML documents.
- Shared styling lives in `assets/css/style.css`, but pages also carry inlined CSS snapshots.
- Shared behavior lives mainly in `assets/js/app.js` and `assets/js/quote.js`.
- The public site relies on direct HTML links, not client-side routing.
- The homepage `index.html` is the canonical design reference.

## Portal architecture

- `portal/login.html` handles email/password login.
- `portal/register.html` handles account creation.
- `portal/dashboard.html` renders the authenticated portal shell and admin callback feed.
- Portal auth state is stored client-side in `sessionStorage` keys such as `ad_token` and `ad_user`.
- Portal pages call the API directly at `https://api.architecturaldrawings.uk` in production and `http://localhost:3001` on localhost.

## API architecture

- Entrypoint: `api/server.js`
- Middleware: Helmet, compression, morgan, CORS, JSON parsing, rate limiting
- Routers:
  - `api/routes/auth.js`
  - `api/routes/quotes.js`
  - `api/routes/projects.js`
  - `api/routes/files.js`
  - `api/routes/stripe.js`
  - `api/routes/callbacks.js`
- Authentication uses JWT bearer tokens from `api/middleware/auth.js`.
- Stripe webhook is mounted before JSON parsing to preserve raw-body verification.

## Database architecture

- Engine: `better-sqlite3`
- Initialisation: `api/models/db.js`
- Tables:
  - `users`
  - `password_resets`
  - `quotes`
  - `projects`
  - `files`
  - `payments`
  - `callbacks`

## Deployment architecture

- Frontend appears intended for Vercel/static hosting.
- API appears intended for Render or another Node host.
- Public frontend domain and API domain are split.
- Production flows therefore depend on correct cross-origin configuration between static frontend and API backend.

## Architectural constraints

1. Do not redesign the frontend stack.
2. Do not convert pages to a framework.
3. Do not change the visual system.
4. Treat `index.html` as the canonical design reference for all additive UI.
5. Preserve exact header, footer, logo, button, typography, and spacing language when extending pages.

## Known pressure points for production

1. Static HTML and API are deployed separately, so hardcoded origin assumptions can break flows.
2. SQLite and local uploads are simple but fragile for horizontally scaled or ephemeral environments.
3. Auth and portal behavior rely on browser storage and exact page-path assumptions.
4. The site mixes production behavior with demo fallback behavior in some portal flows.

## Audit rule

When auditing or modifying this repository, optimize for correctness, deployment realism, and preservation of the existing shipped experience. Do not use architecture work as a reason to restyle or restructure the system.