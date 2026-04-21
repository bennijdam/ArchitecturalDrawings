import express from 'express';
import { body, validationResult } from 'express-validator';
import { Resend } from 'resend';
import { dbAll, dbGet, dbInsert, dbRun } from '../models/db.js';
import { requireAuth, requireRole } from '../middleware/auth.js';
import { logEmailSent } from './emailAudit.js';
import { drawingReadyEmail } from './emailTemplates.js';

const router = express.Router();

let resend;
function getResend() {
  if (!resend && process.env.RESEND_API_KEY) {
    resend = new Resend(process.env.RESEND_API_KEY);
  }
  return resend;
}

function normaliseLimit(rawLimit, fallback = 20, max = 100) {
  const parsed = Number.parseInt(rawLimit, 10);
  if (!Number.isInteger(parsed) || parsed <= 0) return fallback;
  return Math.min(parsed, max);
}

function mapProjectRow(row) {
  if (!row) return null;
  return {
    id: row.id,
    userId: row.user_id,
    userEmail: row.user_email,
    userName: row.user_name,
    title: row.title,
    service: row.service,
    postcode: row.postcode,
    status: row.status,
    valuePence: row.value_pence,
    drawingReadyEmailMessageId: row.drawing_ready_email_message_id,
    createdAt: row.created_at,
  };
}

function mapProjectAuditRow(row) {
  if (!row) return null;
  return {
    id: row.id,
    action: row.action,
    adminUserId: row.admin_user_id,
    adminEmail: row.admin_email,
    projectId: row.project_id,
    projectTitle: row.project_title,
    clientEmail: row.client_email,
    createdAt: row.created_at,
  };
}

async function getAdminProjectRow(projectId) {
  const row = await dbGet(`
    SELECT
      p.id,
      p.user_id,
      u.email AS user_email,
      u.name AS user_name,
      p.title,
      p.service,
      p.postcode,
      p.status,
      p.value_pence,
      p.drawing_ready_email_message_id,
      p.created_at
    FROM projects p
    JOIN users u ON u.id = p.user_id
    WHERE p.id = ?
  `, [projectId]);
  return mapProjectRow(row);
}

/* GET /api/projects/admin — admin-only project operations view */
router.get('/admin', requireAuth, requireRole('admin'), async (req, res) => {
  const limit = normaliseLimit(req.query.limit, 20, 100);
  const status = typeof req.query.status === 'string' ? req.query.status.trim().toLowerCase() : '';

  let sql = `
    SELECT
      p.id,
      p.user_id,
      u.email AS user_email,
      u.name AS user_name,
      p.title,
      p.service,
      p.postcode,
      p.status,
      p.value_pence,
      p.drawing_ready_email_message_id,
      p.created_at
    FROM projects p
    JOIN users u ON u.id = p.user_id
  `;
  const params = [];

  if (status) {
    sql += ' WHERE LOWER(p.status) = ?';
    params.push(status);
  }

  sql += ' ORDER BY p.created_at DESC LIMIT ?';
  params.push(limit);

  const rows = await dbAll(sql, params);
  res.json({ projects: rows.map(mapProjectRow) });
});

/* GET /api/projects/admin/audit — admin-only project deletion audit trail */
router.get('/admin/audit', requireAuth, requireRole('admin'), async (req, res) => {
  const limit = normaliseLimit(req.query.limit, 20, 100);
  const rows = await dbAll(`
    SELECT id, action, admin_user_id, admin_email, project_id, project_title, client_email, created_at
    FROM project_admin_audits
    ORDER BY created_at DESC
    LIMIT ?
  `, [limit]);
  res.json({ audits: rows.map(mapProjectAuditRow) });
});

/* POST /api/projects/admin — admin-only project creation */
router.post('/admin',
  requireAuth,
  requireRole('admin'),
  body('user_email').isEmail().normalizeEmail(),
  body('title').isLength({ min: 1, max: 200 }).trim().escape(),
  body('service').optional({ nullable: true }).isString().trim(),
  body('postcode').optional({ nullable: true }).isLength({ max: 12 }).trim(),
  body('status').optional({ nullable: true }).isIn(['active', 'review', 'approved', 'completed', 'pending', 'new']),
  body('value_pence').optional({ nullable: true }).isInt({ min: 0 }),
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ error: 'Validation failed', details: errors.array() });

    const { user_email, title, service, postcode, status, value_pence } = req.body;
    const owner = await dbGet('SELECT id, email, name FROM users WHERE email = ?', [user_email]);
    if (!owner) {
      return res.status(404).json({ error: 'Client account not found for that email address' });
    }

    const info = await dbInsert(
      'INSERT INTO projects (user_id, title, service, postcode, status, value_pence) VALUES (?, ?, ?, ?, ?, ?)'
    , [owner.id, title, service || null, postcode || null, status || 'pending', value_pence || 0]);

    const project = await getAdminProjectRow(info.id);
    res.status(201).json({ project });
  }
);

/* PATCH /api/projects/admin/:id — admin-only project updates */
router.patch('/admin/:id',
  requireAuth,
  requireRole('admin'),
  body('title').optional().isLength({ min: 1, max: 200 }).trim().escape(),
  body('service').optional({ nullable: true }).isString().trim(),
  body('postcode').optional({ nullable: true }).isLength({ max: 12 }).trim(),
  body('status').optional({ nullable: true }).isIn(['active', 'review', 'approved', 'completed', 'pending', 'new']),
  body('value_pence').optional({ nullable: true }).isInt({ min: 0 }),
  async (req, res) => {
    const projectId = Number.parseInt(req.params.id, 10);
    if (!Number.isInteger(projectId) || projectId <= 0) {
      return res.status(400).json({ error: 'Invalid project id' });
    }

    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ error: 'Validation failed', details: errors.array() });

    const existing = await dbGet('SELECT id FROM projects WHERE id = ?', [projectId]);
    if (!existing) {
      return res.status(404).json({ error: 'Project not found' });
    }

    const allowed = ['title', 'service', 'postcode', 'status', 'value_pence'];
    const sets = [];
    const vals = [];
    for (const key of allowed) {
      if (Object.prototype.hasOwnProperty.call(req.body, key)) {
        sets.push(`${key} = ?`);
        vals.push(req.body[key] || (key === 'value_pence' ? 0 : null));
      }
    }

    if (!sets.length) return res.status(400).json({ error: 'No fields to update' });

    vals.push(projectId);
    await dbRun(`UPDATE projects SET ${sets.join(', ')} WHERE id = ?`, vals);
    const project = await getAdminProjectRow(projectId);
    res.json({ project });
  }
);

/* DELETE /api/projects/admin/:id — admin-only project deletion for unbilled projects */
router.delete('/admin/:id', requireAuth, requireRole('admin'), async (req, res) => {
  const projectId = Number.parseInt(req.params.id, 10);
  if (!Number.isInteger(projectId) || projectId <= 0) {
    return res.status(400).json({ error: 'Invalid project id' });
  }

  const existing = await dbGet(`
    SELECT p.id, p.title, u.email AS user_email
    FROM projects p
    JOIN users u ON u.id = p.user_id
    WHERE p.id = ?
  `, [projectId]);
  if (!existing) {
    return res.status(404).json({ error: 'Project not found' });
  }

  const paymentUsage = await dbGet('SELECT COUNT(*) AS count FROM payments WHERE project_id = ?', [projectId]);
  const paymentCount = Number(paymentUsage?.count || 0);
  const fileUsage = await dbGet('SELECT COUNT(*) AS count FROM files WHERE project_id = ?', [projectId]);
  const fileCount = Number(fileUsage?.count || 0);

  if (paymentCount > 0) {
    return res.status(409).json({ error: 'Projects with payment records cannot be deleted.' });
  }

  if (fileCount > 0) {
    return res.status(409).json({ error: 'Projects with uploaded files cannot be deleted.' });
  }

  const audit = await dbInsert(
    'INSERT INTO project_admin_audits (action, admin_user_id, admin_email, project_id, project_title, client_email) VALUES (?, ?, ?, ?, ?, ?)',
    ['project_deleted', req.user.id, req.user.email || null, projectId, existing.title || null, existing.user_email || null]
  );

  await dbRun('DELETE FROM projects WHERE id = ?', [projectId]);
  res.json({ ok: true, deletedProjectId: projectId, title: existing.title || null, auditId: audit.id || null });
});

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

/* POST /api/projects/:id/drawings-ready — admin-only project transition + email */
router.post('/:id/drawings-ready', requireAuth, requireRole('admin'), async (req, res) => {
  const projectId = Number.parseInt(req.params.id, 10);
  if (!Number.isInteger(projectId) || projectId <= 0) {
    return res.status(400).json({ error: 'Invalid project id' });
  }

  const project = await dbGet(`
    SELECT
      p.id,
      p.title,
      p.status,
      p.drawing_ready_email_message_id,
      u.id AS user_id,
      u.email AS user_email,
      u.name AS user_name
    FROM projects p
    JOIN users u ON u.id = p.user_id
    WHERE p.id = ?
  `, [projectId]);

  if (!project) {
    return res.status(404).json({ error: 'Project not found' });
  }

  if (project.drawing_ready_email_message_id) {
    return res.status(409).json({
      error: 'Drawing-ready email already sent for this project',
      emailMessageId: project.drawing_ready_email_message_id,
    });
  }

  if (!project.user_email) {
    return res.status(400).json({ error: 'Project owner has no email address' });
  }

  const client = getResend();
  if (!client) {
    return res.status(503).json({ error: 'Email not configured' });
  }

  const portalUrl = `${process.env.ALLOWED_ORIGIN || 'https://www.architecturaldrawings.uk'}/portal/dashboard.html`;

  try {
    const tpl = drawingReadyEmail({
      name: project.user_name,
      projectTitle: project.title,
      portalUrl,
    });

    const sendResult = await client.emails.send({
      from: process.env.EMAIL_FROM || 'Architectural Drawings <noreply@send.architecturaldrawings.uk>',
      to: project.user_email,
      subject: tpl.subject,
      html: tpl.html,
      text: tpl.text,
    });

    const emailMessageId = logEmailSent('drawing_ready_email_sent', {
      projectId: project.id,
      userId: project.user_id,
      email: project.user_email,
    }, sendResult);

    await dbRun(
      'UPDATE projects SET status = ?, drawing_ready_email_message_id = ? WHERE id = ?'
      , ['review', emailMessageId, project.id]
    );

    res.json({
      ok: true,
      projectId: project.id,
      status: 'review',
      emailMessageId,
    });
  } catch (err) {
    console.error('[projects] drawing ready email failed', {
      projectId: project.id,
      userId: project.user_id,
      error: err.message,
    });
    res.status(502).json({ error: 'Could not send drawing-ready email' });
  }
});

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
