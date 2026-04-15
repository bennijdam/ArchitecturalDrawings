import 'dotenv/config';
import bcrypt from 'bcryptjs';
import fs from 'node:fs';
import path from 'node:path';
import { getDb, initDb } from '../models/db.js';

const [emailArg, passwordArg, nameArg] = process.argv.slice(2);

if (!emailArg || !passwordArg) {
  console.error('Usage: node scripts/provision-user.js <email> <password> [name]');
  process.exit(1);
}

const email = emailArg.trim().toLowerCase();
const password = passwordArg;
const name = (nameArg || 'Portal Account').trim();

if (password.length < 8) {
  console.error('Password must be at least 8 characters.');
  process.exit(1);
}

const dbPath = process.env.DATABASE_URL || './data/ad.sqlite';
const dbDir = path.dirname(dbPath);
if (dbDir && dbDir !== '.' && !fs.existsSync(dbDir)) {
  fs.mkdirSync(dbDir, { recursive: true });
}

initDb();
const db = getDb();
const passwordHash = bcrypt.hashSync(password, 10);

const existing = db.prepare('SELECT id FROM users WHERE email = ?').get(email);

if (existing) {
  db.prepare('UPDATE users SET password_hash = ?, name = ? WHERE id = ?').run(passwordHash, name, existing.id);
  console.log(`Updated existing user: ${email} (id=${existing.id})`);
} else {
  const info = db
    .prepare('INSERT INTO users (email, password_hash, name, role) VALUES (?, ?, ?, ?)')
    .run(email, passwordHash, name, 'client');
  console.log(`Created new user: ${email} (id=${info.lastInsertRowid})`);
}
