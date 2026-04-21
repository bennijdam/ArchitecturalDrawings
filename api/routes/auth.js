import express from 'express';
import crypto from 'node:crypto';
import bcrypt from 'bcryptjs';
import { body, validationResult } from 'express-validator';
import { Resend } from 'resend';
import { dbGet, dbInsert, dbRun } from '../models/db.js';
import { requireAuth, signToken } from '../middleware/auth.js';
import { logEmailSent } from './emailAudit.js';
import { passwordResetEmail, passwordChangedEmail, welcomeEmail } from './emailTemplates.js';

let resend;
function getResend() {
  if (!resend && process.env.RESEND_API_KEY) {
    resend = new Resend(process.env.RESEND_API_KEY);
  }
  return resend;
}

const router = express.Router();

/* POST /api/auth/register */
router.post('/register',
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 8 }),
  body('name').isLength({ min: 1, max: 120 }).trim().escape(),
  body('phone').optional().trim(),
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ error: 'Validation failed', details: errors.array() });

    const { email, password, name, phone } = req.body;
    const existing = await dbGet('SELECT id FROM users WHERE email = ?', [email]);
    if (existing) return res.status(409).json({ error: 'An account with this email already exists.' });

    const hash = bcrypt.hashSync(password, 10);
    const info = await dbInsert(
      'INSERT INTO users (email, password_hash, name, phone) VALUES (?, ?, ?, ?)'
      , [email, hash, name, phone || null]);

    const user = { id: info.id, email, name, phone: phone || null, role: 'client' };
    const token = signToken(user);

    // Send welcome email (best-effort)
    const welcomeClient = getResend();
    if (welcomeClient) {
      const tpl = welcomeEmail({ name, email });
      welcomeClient.emails.send({
        from: process.env.EMAIL_FROM || 'Architectural Drawings <noreply@send.architecturaldrawings.uk>',
        to: email,
        subject: tpl.subject,
        html: tpl.html,
        text: tpl.text,
      }).then((result) => {
        logEmailSent('welcome_email_sent', {
          userId: info.id,
          email,
        }, result);
      }).catch(err => console.error('Welcome email failed:', err));
    }

    res.status(201).json({ token, user });
  }
);

/* POST /api/auth/login */
router.post('/login',
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 1 }),
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ error: 'Validation failed' });

    const { email, password } = req.body;
    const user = await dbGet('SELECT * FROM users WHERE email = ?', [email]);
    if (!user) return res.status(401).json({ error: 'Invalid email or password.' });

    if (!bcrypt.compareSync(password, user.password_hash)) {
      return res.status(401).json({ error: 'Invalid email or password.' });
    }

    const safeUser = { id: user.id, email: user.email, name: user.name, phone: user.phone, role: user.role };
    const token = signToken(safeUser);
    res.json({ token, user: safeUser });
  }
);

/* GET /api/auth/me */
router.get('/me', requireAuth, (req, res) => {
  res.json({ user: req.user });
});

/* PATCH /api/auth/me */
router.patch('/me',
  requireAuth,
  body('name').optional().isLength({ min: 1, max: 120 }).trim().escape(),
  body('email').optional().isEmail().normalizeEmail(),
  body('phone').optional({ nullable: true }).isLength({ max: 40 }).trim(),
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ error: 'Validation failed', details: errors.array() });

    const currentUser = await dbGet('SELECT id, email, name, phone, role FROM users WHERE id = ?', [req.user.id]);
    if (!currentUser) return res.status(404).json({ error: 'User not found.' });

    const nextName = req.body.name ?? currentUser.name;
    const nextEmail = req.body.email ?? currentUser.email;
    const nextPhone = Object.prototype.hasOwnProperty.call(req.body, 'phone')
      ? (req.body.phone || null)
      : currentUser.phone;

    if (nextEmail !== currentUser.email) {
      const existing = await dbGet('SELECT id FROM users WHERE email = ?', [nextEmail]);
      if (existing && Number(existing.id) !== Number(req.user.id)) {
        return res.status(409).json({ error: 'An account with this email already exists.' });
      }
    }

    await dbRun(
      'UPDATE users SET name = ?, email = ?, phone = ? WHERE id = ?'
      , [nextName, nextEmail, nextPhone, req.user.id]
    );

    const user = {
      id: currentUser.id,
      email: nextEmail,
      name: nextName,
      phone: nextPhone,
      role: currentUser.role || 'client',
    };

    res.json({ token: signToken(user), user });
  }
);

/* POST /api/auth/reset-password — request a reset link */
router.post('/reset-password',
  body('email').isEmail().normalizeEmail(),
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ error: 'Valid email required.' });

    const { email } = req.body;

    // Always return 200 to prevent email enumeration
    const user = await dbGet('SELECT id, name FROM users WHERE email = ?', [email]);
    if (!user) return res.json({ ok: true });

    const token = crypto.randomBytes(32).toString('hex');
    const expiresAt = new Date(Date.now() + 60 * 60 * 1000).toISOString(); // 1 hour

    const resetInfo = await dbInsert(
      'INSERT INTO password_resets (user_id, token, expires_at) VALUES (?, ?, ?)'
      , [user.id, token, expiresAt]);

    const resetUrl = `${process.env.ALLOWED_ORIGIN || 'http://localhost:8080'}/portal/reset.html?token=${token}`;

    const client = getResend();
    if (client) {
      try {
        const tpl = passwordResetEmail({ name: user.name, resetUrl });
        const result = await client.emails.send({
          from: process.env.EMAIL_FROM || 'Architectural Drawings <noreply@send.architecturaldrawings.uk>',
          to: email,
          subject: tpl.subject,
          html: tpl.html,
          text: tpl.text,
        });
        logEmailSent('reset_email_sent', {
          userId: user.id,
          resetId: resetInfo.id,
          email,
        }, result);
      } catch (err) {
        console.error('Reset email failed:', err);
      }
    } else {
      console.log(`[DEV] Password reset link for ${email}: ${resetUrl}`);
    }

    res.json({ ok: true });
  }
);

/* POST /api/auth/reset-password/confirm — set new password with token */
router.post('/reset-password/confirm',
  body('token').isLength({ min: 64, max: 64 }).isHexadecimal(),
  body('password').isLength({ min: 8 }),
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ error: 'Invalid token or password too short.' });

    const { token, password } = req.body;
    const reset = await dbGet(
      'SELECT * FROM password_resets WHERE token = ? AND used = ? AND expires_at > CURRENT_TIMESTAMP',
      [token, false]
    );

    if (!reset) return res.status(400).json({ error: 'Reset link is invalid or has expired.' });

    const hash = bcrypt.hashSync(password, 10);
    await dbRun('UPDATE users SET password_hash = ? WHERE id = ?', [hash, reset.user_id]);
    await dbRun('UPDATE password_resets SET used = ? WHERE id = ?', [true, reset.id]);

    // Send password-changed confirmation (best-effort)
    const changedUser = await dbGet('SELECT email, name FROM users WHERE id = ?', [reset.user_id]);
    const changedClient = getResend();
    if (changedClient && changedUser) {
      const tpl = passwordChangedEmail({ name: changedUser.name });
      changedClient.emails.send({
        from: process.env.EMAIL_FROM || 'Architectural Drawings <noreply@send.architecturaldrawings.uk>',
        to: changedUser.email,
        subject: tpl.subject,
        html: tpl.html,
        text: tpl.text,
      }).then((result) => {
        logEmailSent('password_changed_email_sent', {
          userId: reset.user_id,
          email: changedUser.email,
        }, result);
      }).catch(err => console.error('Password changed email failed:', err));
    }

    res.json({ ok: true });
  }
);

export default router;
