import express from 'express';
import { body, validationResult } from 'express-validator';
import { getDb } from '../models/db.js';
import { requireAuth } from '../middleware/auth.js';

const router = express.Router();

/* GET /api/projects — list current user's projects */
router.get('/', requireAuth, (req, res) => {
  const db = getDb();
  const rows = db.prepare(
    'SELECT id, title, service, postcode, status, value_pence, created_at FROM projects WHERE user_id = ? ORDER BY created_at DESC'
  ).all(req.user.id);
  res.json({ projects: rows });
});

/* GET /api/projects/:id */
router.get('/:id', requireAuth, (req, res) => {
  const db = getDb();
  const row = db.prepare('SELECT * FROM projects WHERE id = ? AND user_id = ?').get(req.params.id, req.user.id);
  if (!row) return res.status(404).json({ error: 'Project not found' });
  res.json({ project: row });
});

/* POST /api/projects */
router.post('/',
  requireAuth,
  body('title').isLength({ min: 1, max: 200 }).trim().escape(),
  body('service').optional().isString(),
  body('postcode').optional().isLength({ max: 12 }).trim(),
  body('value_pence').optional().isInt({ min: 0 }),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ error: 'Validation failed' });

    const { title, service, postcode, value_pence } = req.body;
    const db = getDb();
    const info = db.prepare(
      'INSERT INTO projects (user_id, title, service, postcode, value_pence) VALUES (?, ?, ?, ?, ?)'
    ).run(req.user.id, title, service || null, postcode || null, value_pence || 0);

    res.status(201).json({ id: info.lastInsertRowid });
  }
);

/* PATCH /api/projects/:id */
router.patch('/:id', requireAuth, (req, res) => {
  const db = getDb();
  const existing = db.prepare('SELECT id FROM projects WHERE id = ? AND user_id = ?').get(req.params.id, req.user.id);
  if (!existing) return res.status(404).json({ error: 'Project not found' });

  const allowed = ['title', 'service', 'postcode', 'status', 'value_pence'];
  const sets = [];
  const vals = [];
  for (const k of allowed) {
    if (k in req.body) { sets.push(`${k} = ?`); vals.push(req.body[k]); }
  }
  if (!sets.length) return res.status(400).json({ error: 'No fields to update' });
  vals.push(req.params.id, req.user.id);

  db.prepare(`UPDATE projects SET ${sets.join(', ')} WHERE id = ? AND user_id = ?`).run(...vals);
  res.json({ ok: true });
});

export default router;
