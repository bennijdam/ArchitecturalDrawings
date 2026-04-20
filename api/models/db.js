/**
 * SQLite database — initialisation + schema
 * Swap better-sqlite3 for pg (Postgres) in production at scale.
 */
import Database from 'better-sqlite3';
import fs from 'node:fs';
import path from 'node:path';

function resolveDbPath() {
  const preferred = process.env.DATABASE_URL || './data/ad.sqlite';
  try {
    fs.mkdirSync(path.dirname(preferred), { recursive: true });
    return preferred;
  } catch {
    const fallback = path.join(process.cwd(), 'data', 'ad.sqlite');
    fs.mkdirSync(path.dirname(fallback), { recursive: true });
    console.warn(`Database path "${preferred}" is not writable, falling back to "${fallback}"`);
    return fallback;
  }
}

const DB_PATH = resolveDbPath();

let db;

export function getDb() {
  if (!db) {
    db = new Database(DB_PATH);
    db.pragma('journal_mode = WAL');
    db.pragma('foreign_keys = ON');
  }
  return db;
}

export function initDb() {
  const d = getDb();
  d.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      name TEXT NOT NULL,
      phone TEXT,
      role TEXT NOT NULL DEFAULT 'client',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

    CREATE TABLE IF NOT EXISTS password_resets (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      token TEXT UNIQUE NOT NULL,
      expires_at DATETIME NOT NULL,
      used INTEGER NOT NULL DEFAULT 0,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    CREATE INDEX IF NOT EXISTS idx_resets_token ON password_resets(token);

    CREATE TABLE IF NOT EXISTS quotes (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      property TEXT,
      service TEXT,
      tier TEXT,
      timeline TEXT,
      postcode TEXT,
      name TEXT,
      email TEXT,
      phone TEXT,
      notes TEXT,
      estimated_fee INTEGER,
      status TEXT NOT NULL DEFAULT 'new',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id)
    );
    CREATE INDEX IF NOT EXISTS idx_quotes_email ON quotes(email);

    CREATE TABLE IF NOT EXISTS projects (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      title TEXT NOT NULL,
      service TEXT,
      postcode TEXT,
      status TEXT NOT NULL DEFAULT 'pending',
      value_pence INTEGER NOT NULL DEFAULT 0,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS files (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      project_id INTEGER,
      user_id INTEGER NOT NULL,
      filename TEXT NOT NULL,
      original_name TEXT NOT NULL,
      mimetype TEXT,
      size_bytes INTEGER,
      direction TEXT NOT NULL DEFAULT 'upload',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS payments (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      project_id INTEGER,
      user_id INTEGER NOT NULL,
      amount_pence INTEGER NOT NULL,
      currency TEXT NOT NULL DEFAULT 'gbp',
      description TEXT,
      stripe_session_id TEXT,
      stripe_payment_intent TEXT,
      status TEXT NOT NULL DEFAULT 'pending',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (project_id) REFERENCES projects(id),
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    CREATE INDEX IF NOT EXISTS idx_payments_session ON payments(stripe_session_id);

    CREATE TABLE IF NOT EXISTS callbacks (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      phone TEXT NOT NULL,
      call_when TEXT,
      topic TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
  `);
  console.log('✓ Database initialised');
}
