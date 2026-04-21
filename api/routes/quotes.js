import express from 'express';
import { body, validationResult } from 'express-validator';
import { Resend } from 'resend';
import { dbAll, dbInsert } from '../models/db.js';
import { requireAuth, requireRole } from '../middleware/auth.js';

const router = express.Router();

let resend;
function getResend() {
  if (!resend && process.env.RESEND_API_KEY) {
    resend = new Resend(process.env.RESEND_API_KEY);
  }
  return resend;
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

    const info = await dbInsert(`
      INSERT INTO quotes (property, service, tier, timeline, postcode, name, email, phone, notes)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `, [property, service, tier, timeline, postcode, name, email, phone || null, notes || null]);

    // Notify ops team (best-effort)
    const client = getResend();
    if (client && process.env.EMAIL_TO_OPS) {
      try {
        await client.emails.send({
          from: process.env.EMAIL_FROM || 'Architectural Drawings <noreply@send.architecturaldrawings.uk>',
          to: process.env.EMAIL_TO_OPS,
          subject: `[Quote] ${name} · ${service || '—'} · ${postcode}`,
          text: `New quote request:\n\n${JSON.stringify(req.body, null, 2)}`,
        });
      } catch (err) { console.error('Quote email failed:', err); }
    }

    res.status(201).json({ ok: true, id: info.id });
  }
);

/* GET /api/quotes — admin only */
router.get('/', requireAuth, requireRole('admin'), async (req, res) => {
  const rows = await dbAll('SELECT * FROM quotes ORDER BY created_at DESC LIMIT 100');
  res.json({ quotes: rows });
});

export default router;
