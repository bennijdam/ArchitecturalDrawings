import express from 'express';
import multer from 'multer';
import path from 'node:path';
import fs from 'node:fs';
import { v4 as uuidv4 } from 'uuid';
import { getDb } from '../models/db.js';
import { requireAuth } from '../middleware/auth.js';

const router = express.Router();

function resolveUploadDir() {
  const preferred = process.env.UPLOAD_DIR || './uploads';
  try {
    if (!fs.existsSync(preferred)) fs.mkdirSync(preferred, { recursive: true });
    return preferred;
  } catch {
    const fallback = path.join(process.cwd(), 'uploads');
    if (!fs.existsSync(fallback)) fs.mkdirSync(fallback, { recursive: true });
    console.warn(`Upload dir "${preferred}" is not writable, falling back to "${fallback}"`);
    return fallback;
  }
}

const UPLOAD_DIR = resolveUploadDir();

const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, UPLOAD_DIR),
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname).slice(0, 10);
    cb(null, `${uuidv4()}${ext}`);
  }
});

const ALLOWED = /\.(pdf|dwg|dxf|jpe?g|png|webp|avif|heic|doc|docx|xls|xlsx)$/i;

const upload = multer({
  storage,
  limits: { fileSize: (parseInt(process.env.MAX_FILE_SIZE_MB || '100', 10)) * 1024 * 1024 },
  fileFilter: (req, file, cb) => {
    if (!ALLOWED.test(file.originalname)) return cb(new Error('File type not allowed'));
    cb(null, true);
  }
});

/* POST /api/files/upload */
router.post('/upload', requireAuth, upload.array('file', 10), (req, res) => {
  if (!req.files?.length) return res.status(400).json({ error: 'No files uploaded' });

  const db = getDb();
  const stmt = db.prepare(
    'INSERT INTO files (project_id, user_id, filename, original_name, mimetype, size_bytes, direction) VALUES (?, ?, ?, ?, ?, ?, ?)'
  );

  const projectId = req.body.project_id ? parseInt(req.body.project_id, 10) : null;
  const records = req.files.map((f) => {
    const info = stmt.run(projectId, req.user.id, f.filename, f.originalname, f.mimetype, f.size, 'upload');
    return { id: info.lastInsertRowid, name: f.originalname, size: f.size };
  });

  res.status(201).json({ ok: true, files: records });
});

/* GET /api/files/:id — secure download (auth-checked) */
router.get('/:id', requireAuth, (req, res) => {
  const db = getDb();
  const row = db.prepare('SELECT * FROM files WHERE id = ?').get(req.params.id);
  if (!row) return res.status(404).json({ error: 'File not found' });

  // Client can only access their own files, unless admin
  if (row.user_id !== req.user.id && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden' });
  }

  const filepath = path.join(UPLOAD_DIR, row.filename);
  if (!fs.existsSync(filepath)) return res.status(410).json({ error: 'File gone' });

  res.download(filepath, row.original_name);
});

/* GET /api/files — list for current user or a specific project */
router.get('/', requireAuth, (req, res) => {
  const db = getDb();
  const { project_id } = req.query;
  const rows = project_id
    ? db.prepare('SELECT id, original_name, size_bytes, direction, created_at FROM files WHERE user_id = ? AND project_id = ? ORDER BY created_at DESC').all(req.user.id, project_id)
    : db.prepare('SELECT id, original_name, size_bytes, direction, created_at FROM files WHERE user_id = ? ORDER BY created_at DESC LIMIT 50').all(req.user.id);
  res.json({ files: rows });
});

export default router;
