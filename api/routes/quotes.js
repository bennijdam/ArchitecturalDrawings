import express from 'express';
import { body, validationResult } from 'express-validator';
import nodemailer from 'nodemailer';
import { getDb } from '../models/db.js';
import { requireAuth, requireRole } from '../middleware/auth.js';

const router = express.Router();

// Lazily built transporter
let transporter;
function getMailer() {
  if (!transporter && process.env.SMTP_HOST) {
    transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port: parseInt(process.env.SMTP_PORT || '587', 10),
      secure: process.env.SMTP_PORT === '465',
      auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
    });
  }
  return transporter;
}

/* POST /api/quotes — public (from the quote flow) */
router.post('/',
  body('email').isEmail().normalizeEmail(),
  body('name').isLength({ min: 1, max: 120 }).trim().escape(),
  body('postcode').isLength({ min: 2, max: 12 }).trim(),
  body('property').optional().isString(),
  body('service').optional().isString(),
  body('tier').optional().isIn(['essentials', 'complete', 'bespoke']),
  body('phone').optional().trim(),
  body('notes').optional().isLength({ max: 2000 }).trim(),
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ error: 'Validation failed', details: errors.array() });

    const { property, service, tier, timeline, postcode, name, email, phone, notes } = req.body;
    const db = getDb();

    const info = db.prepare(`
      INSERT INTO quotes (property, service, tier, timeline, postcode, name, email, phone, notes)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).run(property, service, tier, timeline, postcode, name, email, phone || null, notes || null);

    // Notify ops team (best-effort)
    const mailer = getMailer();
    if (mailer && process.env.EMAIL_TO_OPS) {
      try {
        await mailer.sendMail({
          from: process.env.EMAIL_FROM,
          to: process.env.EMAIL_TO_OPS,
          subject: `[Quote] ${name} · ${service || '—'} · ${postcode}`,
          text: `New quote request:\n\n${JSON.stringify(req.body, null, 2)}`,
        });
      } catch (err) { console.error('Mail error:', err.message); }
    }

    res.status(201).json({ ok: true, id: info.lastInsertRowid });
  }
);

/* GET /api/quotes — admin only */
router.get('/', requireAuth, requireRole('admin'), (req, res) => {
  const db = getDb();
  const rows = db.prepare('SELECT * FROM quotes ORDER BY created_at DESC LIMIT 100').all();
  res.json({ quotes: rows });
});

export default router;
