import express from 'express';
import { body, validationResult } from 'express-validator';
import { Resend } from 'resend';
import { dbAll, dbInsert } from '../models/db.js';
import { requireAuth, requireRole } from '../middleware/auth.js';
import { logEmailSent } from './emailAudit.js';
import { quoteConfirmationEmail, quoteOpsEmail } from './emailTemplates.js';

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

    const quoteId = info.id;
    const client = getResend();
    const from = process.env.EMAIL_FROM || 'Architectural Drawings <noreply@send.architecturaldrawings.uk>';

    if (client) {
      // Customer confirmation
      const customerTpl = quoteConfirmationEmail({ name, service, tier, postcode, quoteId });
      client.emails.send({ from, to: email, subject: customerTpl.subject, html: customerTpl.html, text: customerTpl.text })
        .then((result) => {
          const emailMessageId = logEmailSent('quote_customer_email_sent', {
            quoteId,
            email,
          }, result);
          if (emailMessageId) {
            return dbRun('UPDATE quotes SET customer_email_message_id = ? WHERE id = ?', [emailMessageId, quoteId]);
          }
          return null;
        })
        .catch(err => console.error('Quote customer email failed:', err));

      // Ops notification
      if (process.env.EMAIL_TO_OPS) {
        const opsTpl = quoteOpsEmail({ name, email, phone, service, tier, property, postcode, timeline, notes, quoteId });
        client.emails.send({ from, to: process.env.EMAIL_TO_OPS, subject: opsTpl.subject, html: opsTpl.html, text: opsTpl.text })
          .then((result) => {
            const emailMessageId = logEmailSent('quote_ops_email_sent', {
              quoteId,
              email: process.env.EMAIL_TO_OPS,
            }, result);
            if (emailMessageId) {
              return dbRun('UPDATE quotes SET ops_email_message_id = ? WHERE id = ?', [emailMessageId, quoteId]);
            }
            return null;
          })
          .catch(err => console.error('Quote ops email failed:', err));
      }
    }

    res.status(201).json({ ok: true, id: quoteId });
  }
);

/* GET /api/quotes — admin only */
router.get('/', requireAuth, requireRole('admin'), async (req, res) => {
  const rows = await dbAll('SELECT * FROM quotes ORDER BY created_at DESC LIMIT 100');
  res.json({ quotes: rows });
});

export default router;
