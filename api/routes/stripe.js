import express from 'express';
import { Resend } from 'resend';
import Stripe from 'stripe';
import { dbAll, dbGet, dbRun } from '../models/db.js';
import { requireAuth, requireRole } from '../middleware/auth.js';
import { logEmailSent } from './emailAudit.js';
import { paymentConfirmationEmail } from './emailTemplates.js';

const router = express.Router();

let resend;
function getResend() {
  if (!resend && process.env.RESEND_API_KEY) {
    resend = new Resend(process.env.RESEND_API_KEY);
  }
  return resend;
}

// Lazy init — allows server to boot without Stripe keys in dev
function getStripe() {
  if (!process.env.STRIPE_SECRET_KEY) return null;
  return new Stripe(process.env.STRIPE_SECRET_KEY, { apiVersion: '2024-12-18.acacia' });
}

function normaliseLimit(rawLimit, fallback = 20, max = 100) {
  const parsed = Number.parseInt(rawLimit, 10);
  if (!Number.isInteger(parsed) || parsed <= 0) return fallback;
  return Math.min(parsed, max);
}

function mapPaymentRow(row) {
  if (!row) return null;
  return {
    id: row.id,
    projectId: row.project_id,
    userId: row.user_id,
    amountPence: row.amount_pence,
    currency: row.currency,
    description: row.description,
    stripeSessionId: row.stripe_session_id,
    stripePaymentIntent: row.stripe_payment_intent,
    emailMessageId: row.email_message_id,
    status: row.status,
    createdAt: row.created_at,
    userEmail: row.user_email,
    userName: row.user_name,
    projectTitle: row.project_title,
  };
}

/* GET /api/stripe/payments/mine — current user's recent payments */
router.get('/payments/mine', requireAuth, async (req, res) => {
  const limit = normaliseLimit(req.query.limit, 10, 50);
  const rows = await dbAll(`
    SELECT
      p.id,
      p.project_id,
      p.user_id,
      p.amount_pence,
      p.currency,
      p.description,
      p.stripe_session_id,
      p.stripe_payment_intent,
      p.email_message_id,
      p.status,
      p.created_at,
      projects.title AS project_title
    FROM payments p
    LEFT JOIN projects ON projects.id = p.project_id
    WHERE p.user_id = ?
    ORDER BY p.created_at DESC
    LIMIT ?
  `, [req.user.id, limit]);

  res.json({
    payments: rows.map(mapPaymentRow),
  });
});

/* GET /api/stripe/payments — admin-only payment audit view */
router.get('/payments', requireAuth, requireRole('admin'), async (req, res) => {
  const limit = normaliseLimit(req.query.limit, 20, 100);
  const sessionId = typeof req.query.session_id === 'string' ? req.query.session_id.trim() : '';
  const status = typeof req.query.status === 'string' ? req.query.status.trim() : '';

  let sql = `
    SELECT
      p.id,
      p.project_id,
      p.user_id,
      p.amount_pence,
      p.currency,
      p.description,
      p.stripe_session_id,
      p.stripe_payment_intent,
      p.email_message_id,
      p.status,
      p.created_at,
      users.email AS user_email,
      users.name AS user_name,
      projects.title AS project_title
    FROM payments p
    LEFT JOIN users ON users.id = p.user_id
    LEFT JOIN projects ON projects.id = p.project_id
  `;
  const params = [];
  const filters = [];

  if (sessionId) {
    filters.push('p.stripe_session_id = ?');
    params.push(sessionId);
  }
  if (status) {
    filters.push('p.status = ?');
    params.push(status);
  }
  if (filters.length) {
    sql += ` WHERE ${filters.join(' AND ')}`;
  }
  sql += ' ORDER BY p.created_at DESC LIMIT ?';
  params.push(limit);

  const rows = await dbAll(sql, params);
  res.json({
    payments: rows.map(mapPaymentRow),
  });
});

/* GET /api/stripe/payments/:sessionId — admin-only payment lookup */
router.get('/payments/:sessionId', requireAuth, requireRole('admin'), async (req, res) => {
  const sessionId = req.params.sessionId?.trim();
  if (!sessionId) {
    return res.status(400).json({ error: 'Session id is required' });
  }

  const row = await dbGet(`
    SELECT
      p.id,
      p.project_id,
      p.user_id,
      p.amount_pence,
      p.currency,
      p.description,
      p.stripe_session_id,
      p.stripe_payment_intent,
      p.email_message_id,
      p.status,
      p.created_at,
      users.email AS user_email,
      users.name AS user_name,
      projects.title AS project_title
    FROM payments p
    LEFT JOIN users ON users.id = p.user_id
    LEFT JOIN projects ON projects.id = p.project_id
    WHERE p.stripe_session_id = ?
  `, [sessionId]);

  if (!row) {
    return res.status(404).json({ error: 'Payment not found' });
  }

  res.json({ payment: mapPaymentRow(row) });
});

/* POST /api/stripe/checkout — create a Checkout Session */
router.post('/checkout', requireAuth, async (req, res) => {
  const stripe = getStripe();
  if (!stripe) return res.status(503).json({ error: 'Payments not configured' });

  const { amount, currency = 'gbp', description = 'Architectural Drawings services', project_id } = req.body;
  if (!Number.isInteger(amount) || amount < 50) {
    return res.status(400).json({ error: 'Amount must be an integer in minor units, at least 50.' });
  }

  try {
    console.log('[stripe] creating checkout session', {
      userId: req.user.id,
      projectId: project_id || null,
      amount,
      currency,
      description,
    });

    const session = await stripe.checkout.sessions.create({
      mode: 'payment',
      payment_method_types: ['card'],
      line_items: [{
        price_data: {
          currency,
          product_data: { name: description },
          unit_amount: amount,
        },
        quantity: 1,
      }],
      success_url: process.env.STRIPE_SUCCESS_URL || 'https://www.architecturaldrawings.uk/portal/dashboard.html?payment=success',
      cancel_url: process.env.STRIPE_CANCEL_URL || 'https://www.architecturaldrawings.uk/portal/dashboard.html?payment=cancelled',
      customer_email: req.user.email,
      metadata: {
        user_id: String(req.user.id),
        project_id: project_id ? String(project_id) : '',
        description,
      },
    });

    await dbRun(
      'INSERT INTO payments (project_id, user_id, amount_pence, currency, description, stripe_session_id) VALUES (?, ?, ?, ?, ?, ?)'
    , [project_id || null, req.user.id, amount, currency, description, session.id]);

    console.log('[stripe] checkout session created', {
      sessionId: session.id,
      userId: req.user.id,
      projectId: project_id || null,
      amount,
      currency,
    });

    res.json({ sessionUrl: session.url, sessionId: session.id });
  } catch (err) {
    console.error('[stripe] checkout error', {
      userId: req.user?.id || null,
      projectId: project_id || null,
      amount,
      currency,
      error: err.message,
    });
    res.status(500).json({ error: 'Could not create checkout session' });
  }
});

/**
 * Webhook handler — exported separately and mounted in server.js
 * BEFORE express.json() so Stripe can verify the raw-body signature.
 */
export async function stripeWebhookHandler(req, res) {
  const stripe = getStripe();
  if (!stripe) return res.status(503).send('Payments not configured');

  const sig = req.headers['stripe-signature'];
  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    console.error('Webhook signature verification failed:', err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  console.log('[stripe] webhook received', {
    eventId: event.id,
    eventType: event.type,
  });

  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object;
      const result = await dbRun(
        'UPDATE payments SET status = ?, stripe_payment_intent = ? WHERE stripe_session_id = ?'
      , ['paid', session.payment_intent, session.id]);
      if (!result.changes) {
        console.warn('[stripe] completed webhook did not match a payment row', {
          sessionId: session.id,
          paymentIntent: session.payment_intent,
        });
      }
      console.log('[stripe] payment marked paid', {
        sessionId: session.id,
        paymentIntent: session.payment_intent,
        rowsUpdated: result.changes || 0,
      });

      const payment = await dbGet(`
        SELECT
          p.id,
          p.amount_pence,
          p.currency,
          p.description,
          p.email_message_id,
          u.email AS user_email,
          u.name AS user_name,
          projects.title AS project_title
        FROM payments p
        LEFT JOIN users u ON u.id = p.user_id
        LEFT JOIN projects ON projects.id = p.project_id
        WHERE p.stripe_session_id = ?
      `, [session.id]);

      if (!payment) {
        console.warn('[stripe] payment email skipped: payment row missing after update', {
          sessionId: session.id,
        });
        break;
      }

      if (payment.email_message_id) {
        console.info('[payment_confirmation_email_skipped]', JSON.stringify({
          paymentId: payment.id,
          email: payment.user_email,
          reason: 'already_sent',
          emailMessageId: payment.email_message_id,
        }));
        break;
      }

      if (!payment.user_email) {
        console.warn('[stripe] payment email skipped: user email missing', {
          paymentId: payment.id,
          sessionId: session.id,
        });
        break;
      }

      const emailClient = getResend();
      if (!emailClient) {
        console.warn('[stripe] payment email skipped: resend not configured', {
          paymentId: payment.id,
          sessionId: session.id,
        });
        break;
      }

      try {
        const tpl = paymentConfirmationEmail({
          name: payment.user_name,
          amountGbp: Number(payment.amount_pence || 0) / 100,
          projectTitle: payment.project_title || payment.description,
          paymentId: payment.id,
          receiptUrl: null,
        });
        const sendResult = await emailClient.emails.send({
          from: process.env.EMAIL_FROM || 'Architectural Drawings <noreply@send.architecturaldrawings.uk>',
          to: payment.user_email,
          subject: tpl.subject,
          html: tpl.html,
          text: tpl.text,
        });
        const emailMessageId = logEmailSent('payment_confirmation_email_sent', {
          paymentId: payment.id,
          sessionId: session.id,
          email: payment.user_email,
        }, sendResult);
        if (emailMessageId) {
          await dbRun('UPDATE payments SET email_message_id = ? WHERE id = ?', [emailMessageId, payment.id]);
        }
      } catch (err) {
        console.error('[stripe] payment confirmation email failed', {
          paymentId: payment.id,
          sessionId: session.id,
          error: err.message,
        });
      }
      break;
    }
    case 'checkout.session.expired':
    case 'checkout.session.async_payment_failed': {
      const session = event.data.object;
      const result = await dbRun('UPDATE payments SET status = ? WHERE stripe_session_id = ?', ['failed', session.id]);
      console.log('[stripe] payment marked failed', {
        sessionId: session.id,
        eventType: event.type,
        rowsUpdated: result.changes || 0,
      });
      break;
    }
    default:
      // Log but don't fail — unknown event types shouldn't break the pipe
      console.log(`Stripe event (unhandled): ${event.type}`);
  }

  res.json({ received: true });
}

export default router;
