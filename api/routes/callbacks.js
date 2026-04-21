import express from 'express';
import { body, validationResult } from 'express-validator';
import { Resend } from 'resend';
import { requireAuth, requireRole } from '../middleware/auth.js';
import { dbAll, dbGet, dbInsert, dbRun } from '../models/db.js';

const router = express.Router();

let resend;
function getResend() {
  if (!resend && process.env.RESEND_API_KEY) {
    resend = new Resend(process.env.RESEND_API_KEY);
  }
  return resend;
}

function getRequestIp(req) {
  const forwarded = req.headers['x-forwarded-for'];
  if (typeof forwarded === 'string' && forwarded.trim()) {
    return forwarded.split(',')[0].trim();
  }
  return req.ip || req.socket?.remoteAddress || null;
}

function clip(value, max = 500) {
  if (value == null) return null;
  const text = String(value);
  return text.length > max ? text.slice(0, max) : text;
}

/* GET /api/callbacks — admin only */
router.get('/', requireAuth, requireRole('admin'), async (req, res) => {
  const rows = await dbAll(`
    SELECT id, name, phone, call_when, topic, source_ip, user_agent, referrer, request_path, email_message_id, created_at
    FROM callbacks
    WHERE COALESCE(honeypot, '') = ''
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
  body('website').optional().isLength({ max: 200 }).trim(),
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ error: 'Validation failed', details: errors.array() });

    const { name, phone, when: callWhen, topic, website } = req.body;
    const sourceIp = clip(getRequestIp(req), 120);
    const userAgent = clip(req.get('user-agent'), 500);
    const referrer = clip(req.get('referer') || req.get('referrer'), 500);
    const requestPath = clip(req.originalUrl || req.path, 200);
    const honeypot = clip(website, 200);

    console.info('[callback_request]', JSON.stringify({
      name,
      phone,
      when: callWhen || null,
      topic: topic || null,
      sourceIp,
      userAgent,
      referrer,
      requestPath,
      honeypotTriggered: Boolean(honeypot),
    }));

    const insertResult = await dbInsert(`
      INSERT INTO callbacks (name, phone, call_when, topic, source_ip, user_agent, referrer, request_path, honeypot)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `, [name, phone, callWhen || null, topic || null, sourceIp, userAgent, referrer, requestPath, honeypot]);

    const callbackId = insertResult?.id || null;

    if (honeypot) {
      return res.status(202).json({ ok: true });
    }

    const client = getResend();
    if (client) {
      try {
        const resendResult = await client.emails.send({
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
              <tr><td style="padding:8px 0;color:#666">Source IP</td><td style="padding:8px 0">${sourceIp || 'Unknown'}</td></tr>
              <tr><td style="padding:8px 0;color:#666">Referrer</td><td style="padding:8px 0">${referrer || 'Direct / unavailable'}</td></tr>
              <tr><td style="padding:8px 0;color:#666">Path</td><td style="padding:8px 0">${requestPath || 'Unknown'}</td></tr>
              <tr><td style="padding:8px 0;color:#666">User agent</td><td style="padding:8px 0">${userAgent || 'Unknown'}</td></tr>
            </table>
          `,
        });

        const emailMessageId = resendResult?.data?.id || resendResult?.id || null;
        console.info('[callback_email_sent]', JSON.stringify({
          callbackId,
          emailMessageId,
          name,
          sourceIp,
          requestPath,
        }));

        if (callbackId && emailMessageId) {
          await dbRun('UPDATE callbacks SET email_message_id = ? WHERE id = ?', [emailMessageId, callbackId]);
        }
      } catch (err) {
        console.error('Resend error:', err.message);
      }
    }

    res.status(201).json({ ok: true });
  }
);

export default router;
