import express from 'express';
import crypto from 'node:crypto';
import bcrypt from 'bcryptjs';
import nodemailer from 'nodemailer';
import { body, validationResult } from 'express-validator';
import { dbGet, dbInsert, dbRun } from '../models/db.js';
import { requireAuth, signToken } from '../middleware/auth.js';

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

    await dbRun(
      'INSERT INTO password_resets (user_id, token, expires_at) VALUES (?, ?, ?)'
      , [user.id, token, expiresAt]);

    const resetUrl = `${process.env.ALLOWED_ORIGIN || 'http://localhost:8080'}/portal/reset.html?token=${token}`;

    const mailer = getMailer();
    if (mailer) {
      mailer.sendMail({
        from: process.env.EMAIL_FROM || 'hello@architecturaldrawings.uk',
        to: email,
        subject: 'Reset your password — Architectural Drawings',
        text: `Hi ${user.name},\n\nYou requested a password reset. Click the link below within 1 hour:\n\n${resetUrl}\n\nIf you didn't request this, ignore this email.\n\nArchitectural Drawings London`,
        html: `<p>Hi ${user.name},</p><p>You requested a password reset. Click the link below within 1 hour:</p><p><a href="${resetUrl}">${resetUrl}</a></p><p>If you didn't request this, ignore this email.</p><p>Architectural Drawings London</p>`,
      }).catch((err) => console.error('Reset email failed:', err));
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

    res.json({ ok: true });
  }
);

export default router;
