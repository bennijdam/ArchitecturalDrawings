import express from 'express';
import { body, validationResult } from 'express-validator';
import { Resend } from 'resend';
import { requireAuth, requireRole } from '../middleware/auth.js';
import { dbAll, dbGet, dbRun } from '../models/db.js';

const router = express.Router();

let resend;
function getResend() {
  if (!resend && process.env.RESEND_API_KEY) {
    resend = new Resend(process.env.RESEND_API_KEY);
  }
  return resend;
}

/* GET /api/callbacks — admin only */
router.get('/', requireAuth, requireRole('admin'), async (req, res) => {
  const rows = await dbAll(`
    SELECT id, name, phone, call_when, topic, created_at
    FROM callbacks
    ORDER BY created_at DESC
    LIMIT 100
  `);

  res.json({ callbacks: rows });
});

/* DELETE /api/callbacks/:id — admin only */
router.delete('/:id', requireAuth, requireRole('admin'), async (req, res) => {
  const callbackId = Number.parseInt(req.params.id, 10);
  if (!Number.isInteger(callbackId) || callbackId <= 0) {
    return res.status(400).json({ error: 'Invalid callback id' });
  }

  const existing = await dbGet('SELECT id FROM callbacks WHERE id = ?', [callbackId]);
  if (!existing) {
    return res.status(404).json({ error: 'Callback not found' });
  }

  await dbRun('DELETE FROM callbacks WHERE id = ?', [callbackId]);

  res.json({ ok: true });
});

/* POST /api/callbacks — public (from landing page callback widget) */
router.post('/',
  body('name').isLength({ min: 1, max: 120 }).trim().escape(),
  body('phone').isLength({ min: 6, max: 30 }).trim(),
  body('when').optional().isString().trim(),
  body('topic').optional().isLength({ max: 300 }).trim().escape(),
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ error: 'Validation failed', details: errors.array() });

    const { name, phone, when: callWhen, topic, createdAt } = req.body;
    await dbRun(`
      INSERT INTO callbacks (name, phone, call_when, topic)
      VALUES (?, ?, ?, ?)
    `, [name, phone, callWhen || null, topic || null]);

    const client = getResend();
    if (client) {
      try {
        await client.emails.send({
          from: process.env.EMAIL_FROM || 'Architectural Drawings <noreply@send.architecturaldrawings.uk>',
          to: 'hello@architecturaldrawings.uk',
          subject: `[Callback request] ${name} — ${callWhen || 'ASAP'}`,
          html: `
            <h2 style="font-family:sans-serif;margin:0 0 16px">New callback request</h2>
            <table style="font-family:sans-serif;border-collapse:collapse;width:100%;max-width:480px">
              <tr><td style="padding:8px 0;color:#666;width:120px">Name</td><td style="padding:8px 0;font-weight:600">${name}</td></tr>
              <tr><td style="padding:8px 0;color:#666">Phone</td><td style="padding:8px 0;font-weight:600">${phone}</td></tr>
              <tr><td style="padding:8px 0;color:#666">When</td><td style="padding:8px 0">${callWhen || 'As soon as possible'}</td></tr>
              <tr><td style="padding:8px 0;color:#666">Topic</td><td style="padding:8px 0">${topic || '—'}</td></tr>
              <tr><td style="padding:8px 0;color:#666">Received</td><td style="padding:8px 0">${new Date().toLocaleString('en-GB', { timeZone: 'Europe/London' })}</td></tr>
            </table>
          `,
        });
      } catch (err) {
        console.error('Resend error:', err.message);
      }
    }

    res.status(201).json({ ok: true });
  }
);

export default router;
