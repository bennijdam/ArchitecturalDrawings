import jwt from 'jsonwebtoken';
import { dbGet } from '../models/db.js';

function getJwtSecret() {
  const secret = process.env.JWT_SECRET;
  if (!secret && process.env.NODE_ENV === 'production') {
    throw new Error('JWT_SECRET must be set in production');
  }
  return secret || 'dev-secret-change-me';
}

export async function requireAuth(req, res, next) {
  const header = req.headers.authorization || '';
  const [scheme, token] = header.split(' ');
  if (scheme !== 'Bearer' || !token) {
    return res.status(401).json({ error: 'Missing or invalid Authorization header' });
  }
  try {
    const payload = jwt.verify(token, getJwtSecret());

    // Reject tokens for users that no longer exist in the current database.
    const user = await dbGet(
      'SELECT id, email, name, phone, role FROM users WHERE id = ?'
      , [payload.id]
    );

    if (!user) {
      return res.status(401).json({ error: 'Session is no longer valid. Please sign in again.' });
    }

    req.user = {
      id: user.id,
      email: user.email,
      name: user.name,
      phone: user.phone,
      role: user.role || 'client',
    };
    next();
  } catch (err) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
}

export function requireRole(role) {
  return (req, res, next) => {
    if (!req.user) return res.status(401).json({ error: 'Unauthorized' });
    if (req.user.role !== role && req.user.role !== 'admin') {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}

export function signToken(user) {
  return jwt.sign(
    { id: user.id, email: user.email, name: user.name, role: user.role || 'client' },
    getJwtSecret(),
    { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
  );
}
