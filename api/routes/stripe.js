import express from 'express';
import Stripe from 'stripe';
import { getDb } from '../models/db.js';
import { requireAuth } from '../middleware/auth.js';

const router = express.Router();

// Lazy init — allows server to boot without Stripe keys in dev
function getStripe() {
  if (!process.env.STRIPE_SECRET_KEY) return null;
  return new Stripe(process.env.STRIPE_SECRET_KEY, { apiVersion: '2024-12-18.acacia' });
}

/* POST /api/stripe/checkout — create a Checkout Session */
router.post('/checkout', requireAuth, async (req, res) => {
  const stripe = getStripe();
  if (!stripe) return res.status(503).json({ error: 'Payments not configured' });

  const { amount, currency = 'gbp', description = 'Architectural Drawings services', project_id } = req.body;
  if (!Number.isInteger(amount) || amount < 50) {
    return res.status(400).json({ error: 'Amount must be an integer in minor units, at least 50.' });
  }

  try {
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
      success_url: process.env.STRIPE_SUCCESS_URL || 'https://architecturaldrawings.co.uk/portal/dashboard.html?payment=success',
      cancel_url: process.env.STRIPE_CANCEL_URL || 'https://architecturaldrawings.co.uk/portal/dashboard.html?payment=cancelled',
      customer_email: req.user.email,
      metadata: {
        user_id: String(req.user.id),
        project_id: project_id ? String(project_id) : '',
        description,
      },
    });

    const db = getDb();
    db.prepare(
      'INSERT INTO payments (project_id, user_id, amount_pence, currency, description, stripe_session_id) VALUES (?, ?, ?, ?, ?, ?)'
    ).run(project_id || null, req.user.id, amount, currency, description, session.id);

    res.json({ sessionUrl: session.url, sessionId: session.id });
  } catch (err) {
    console.error('Stripe checkout error:', err.message);
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

  const db = getDb();

  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object;
      db.prepare(
        'UPDATE payments SET status = ?, stripe_payment_intent = ? WHERE stripe_session_id = ?'
      ).run('paid', session.payment_intent, session.id);
      console.log('✓ Payment succeeded:', session.id);
      break;
    }
    case 'checkout.session.expired':
    case 'checkout.session.async_payment_failed': {
      const session = event.data.object;
      db.prepare('UPDATE payments SET status = ? WHERE stripe_session_id = ?').run('failed', session.id);
      break;
    }
    default:
      // Log but don't fail — unknown event types shouldn't break the pipe
      console.log(`Stripe event (unhandled): ${event.type}`);
  }

  res.json({ received: true });
}

export default router;
