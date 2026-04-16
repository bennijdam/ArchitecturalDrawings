/**
 * Architectural Drawings London — API Server
 * Node.js + Express + SQLite + Stripe + JWT
 */
import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import morgan from 'morgan';
import rateLimit from 'express-rate-limit';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';
import { Sentry, sentryEnabled } from './instrument.js';

import { initDb } from './models/db.js';
import authRouter from './routes/auth.js';
import quotesRouter from './routes/quotes.js';
import projectsRouter from './routes/projects.js';
import filesRouter from './routes/files.js';
import stripeRouter, { stripeWebhookHandler } from './routes/stripe.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3001;

// Trust first proxy (Cloudflare, Railway, Vercel) so rate limiting and req.ip work correctly
app.set('trust proxy', 1);

/* ---------- Initialise filesystem + DB ---------- */
['data', process.env.UPLOAD_DIR || './uploads'].forEach((dir) => {
  try {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  } catch {
    console.warn(`Skipping unwritable directory during startup: ${dir}`);
  }
});
initDb();

/* ---------- Middleware ---------- */
app.use(helmet({
  crossOriginResourcePolicy: { policy: 'cross-origin' },
  contentSecurityPolicy: false,
}));
app.use(compression());
app.use(morgan(process.env.NODE_ENV === 'production' ? 'combined' : 'dev'));

app.use(cors({
  origin: process.env.ALLOWED_ORIGIN || 'http://localhost:8080',
  credentials: true,
}));

// Stripe webhook needs raw body — mount BEFORE express.json
app.post('/api/stripe/webhook', express.raw({ type: 'application/json' }), stripeWebhookHandler);

// Normal JSON body parsing for all other routes
app.use(express.json({ limit: '5mb' }));
app.use(express.urlencoded({ extended: true, limit: '5mb' }));

// Rate limiting
const limiter = rateLimit({
  windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS || '900000', 10),
  max: parseInt(process.env.RATE_LIMIT_MAX || '100', 10),
  standardHeaders: true,
  legacyHeaders: false,
});
app.use('/api/', limiter);

/* ---------- Routes ---------- */
app.get('/api/health', (req, res) => res.json({ ok: true, ts: Date.now() }));

app.use('/api/auth', authRouter);
app.use('/api/quotes', quotesRouter);
app.use('/api/projects', projectsRouter);
app.use('/api/files', filesRouter);
app.use('/api/stripe', stripeRouter);

// Static uploaded files (auth-gated — see files.js for secure route)
app.use('/uploads', express.static(process.env.UPLOAD_DIR || './uploads'));

/* ---------- Static frontend (optional — for single-server deploy) ---------- */
// Comment this block if frontend is served separately (CDN, Nginx, etc.)
const FRONTEND_DIR = path.join(__dirname, '..');
app.use(express.static(FRONTEND_DIR, { extensions: ['html'] }));

if (sentryEnabled) {
  Sentry.setupExpressErrorHandler(app);
}

/* ---------- Error handling ---------- */
app.use((err, req, res, next) => {
  console.error('API error:', err);
  if (res.headersSent) return next(err);
  res.status(err.status || 500).json({
    error: err.message || 'Internal server error',
    ...(process.env.NODE_ENV !== 'production' && { stack: err.stack }),
  });
});

/* ---------- Start ---------- */
app.listen(PORT, () => {
  console.log(`🏛  Architectural Drawings API listening on :${PORT}`);
  console.log(`   ENV: ${process.env.NODE_ENV || 'development'}`);
});
