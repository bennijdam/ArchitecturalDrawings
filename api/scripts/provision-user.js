import 'dotenv/config';
import bcrypt from 'bcryptjs';
import fs from 'node:fs';
import path from 'node:path';
import { dbGet, dbInsert, dbRun, initDb, usingPostgres } from '../models/db.js';

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

async function main() {
  const dbPath = process.env.DATABASE_URL || './data/ad.sqlite';
  if (!usingPostgres()) {
    const dbDir = path.dirname(dbPath);
    if (dbDir && dbDir !== '.' && !fs.existsSync(dbDir)) {
      fs.mkdirSync(dbDir, { recursive: true });
    }
  }

  await initDb();
  const passwordHash = bcrypt.hashSync(password, 10);

  const existing = await dbGet('SELECT id FROM users WHERE email = ?', [email]);

  if (existing) {
    await dbRun('UPDATE users SET password_hash = ?, name = ? WHERE id = ?', [passwordHash, name, existing.id]);
    console.log(`Updated existing user: ${email} (id=${existing.id})`);
    return;
  }

  const info = await dbInsert(
    'INSERT INTO users (email, password_hash, name, role) VALUES (?, ?, ?, ?)',
    [email, passwordHash, name, 'client']
  );
  console.log(`Created new user: ${email} (id=${info.id})`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
