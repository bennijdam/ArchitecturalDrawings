import express from 'express';
import { body, validationResult } from 'express-validator';
import { dbAll, dbGet, dbInsert, dbRun } from '../models/db.js';
import { requireAuth } from '../middleware/auth.js';

const router = express.Router();

/* GET /api/projects — list current user's projects */
router.get('/', requireAuth, async (req, res) => {
  const rows = await dbAll(
    'SELECT id, title, service, postcode, status, value_pence, created_at FROM projects WHERE user_id = ? ORDER BY created_at DESC'
  , [req.user.id]);
  res.json({ projects: rows });
});

/* GET /api/projects/:id */
router.get('/:id', requireAuth, async (req, res) => {
  const row = await dbGet('SELECT * FROM projects WHERE id = ? AND user_id = ?', [req.params.id, req.user.id]);
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
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ error: 'Validation failed' });

    const { title, service, postcode, value_pence } = req.body;
    const info = await dbInsert(
      'INSERT INTO projects (user_id, title, service, postcode, value_pence) VALUES (?, ?, ?, ?, ?)'
    , [req.user.id, title, service || null, postcode || null, value_pence || 0]);

    res.status(201).json({ id: info.id });
  }
);

/* PATCH /api/projects/:id */
router.patch('/:id', requireAuth, async (req, res) => {
  const existing = await dbGet('SELECT id FROM projects WHERE id = ? AND user_id = ?', [req.params.id, req.user.id]);
  if (!existing) return res.status(404).json({ error: 'Project not found' });

  const allowed = ['title', 'service', 'postcode', 'status', 'value_pence'];
  const sets = [];
  const vals = [];
  for (const k of allowed) {
    if (k in req.body) { sets.push(`${k} = ?`); vals.push(req.body[k]); }
  }
  if (!sets.length) return res.status(400).json({ error: 'No fields to update' });
  vals.push(req.params.id, req.user.id);

  await dbRun(`UPDATE projects SET ${sets.join(', ')} WHERE id = ? AND user_id = ?`, vals);
  res.json({ ok: true });
});

export default router;
