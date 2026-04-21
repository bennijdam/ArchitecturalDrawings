import Database from 'better-sqlite3';
import fs from 'node:fs';
import path from 'node:path';
import pg from 'pg';

const { Pool } = pg;

const rawDatabaseUrl = process.env.DATABASE_URL || './data/ad.sqlite';
const isPostgres = /^(postgres|postgresql):\/\//i.test(rawDatabaseUrl);

let sqliteDb;
let pgPool;

function resolveDbPath() {
  const preferred = rawDatabaseUrl;
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

function getSqliteDb() {
  if (!sqliteDb) {
    sqliteDb = new Database(resolveDbPath());
    sqliteDb.pragma('journal_mode = WAL');
    sqliteDb.pragma('foreign_keys = ON');
  }
  return sqliteDb;
}

function getPgPool() {
  if (!pgPool) {
    pgPool = new Pool({
      connectionString: rawDatabaseUrl,
      ssl: process.env.PGSSLMODE === 'disable' ? false : { rejectUnauthorized: false },
    });
  }
  return pgPool;
}

function toPgSql(sql) {
  let index = 0;
  return sql.replace(/\?/g, () => `$${++index}`);
}

export function usingPostgres() {
  return isPostgres;
}

export function getDb() {
  return isPostgres ? getPgPool() : getSqliteDb();
}

export async function dbGet(sql, params = []) {
  if (!isPostgres) return getSqliteDb().prepare(sql).get(...params);
  const result = await getPgPool().query(toPgSql(sql), params);
  return result.rows[0];
}

export async function dbAll(sql, params = []) {
  if (!isPostgres) return getSqliteDb().prepare(sql).all(...params);
  const result = await getPgPool().query(toPgSql(sql), params);
  return result.rows;
}

export async function dbRun(sql, params = []) {
  if (!isPostgres) return getSqliteDb().prepare(sql).run(...params);
  const result = await getPgPool().query(toPgSql(sql), params);
  return {
    changes: result.rowCount,
    rows: result.rows,
  };
}

export async function dbInsert(sql, params = []) {
  if (!isPostgres) {
    const info = getSqliteDb().prepare(sql).run(...params);
    return { id: Number(info.lastInsertRowid) };
  }

  const text = /returning\s+/i.test(sql) ? sql : `${sql} RETURNING id`;
  const result = await getPgPool().query(toPgSql(text), params);
  return result.rows[0] || { id: null };
}

async function initPostgres() {
  const pool = getPgPool();
  const statements = [
    `CREATE TABLE IF NOT EXISTS users (
      id BIGSERIAL PRIMARY KEY,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      name TEXT NOT NULL,
      phone TEXT,
      role TEXT NOT NULL DEFAULT 'client',
      created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    )`,
    'CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)',
    `CREATE TABLE IF NOT EXISTS password_resets (
      id BIGSERIAL PRIMARY KEY,
      user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      token TEXT UNIQUE NOT NULL,
      expires_at TIMESTAMPTZ NOT NULL,
      used BOOLEAN NOT NULL DEFAULT FALSE,
      created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    )`,
    'CREATE INDEX IF NOT EXISTS idx_resets_token ON password_resets(token)',
    `CREATE TABLE IF NOT EXISTS quotes (
      id BIGSERIAL PRIMARY KEY,
      user_id BIGINT REFERENCES users(id),
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
      created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    )`,
    'CREATE INDEX IF NOT EXISTS idx_quotes_email ON quotes(email)',
    `CREATE TABLE IF NOT EXISTS projects (
      id BIGSERIAL PRIMARY KEY,
      user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      title TEXT NOT NULL,
      service TEXT,
      postcode TEXT,
      status TEXT NOT NULL DEFAULT 'pending',
      value_pence INTEGER NOT NULL DEFAULT 0,
      created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    )`,
    `CREATE TABLE IF NOT EXISTS files (
      id BIGSERIAL PRIMARY KEY,
      project_id BIGINT REFERENCES projects(id) ON DELETE CASCADE,
      user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      filename TEXT NOT NULL,
      original_name TEXT NOT NULL,
      mimetype TEXT,
      size_bytes INTEGER,
      direction TEXT NOT NULL DEFAULT 'upload',
      created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    )`,
    `CREATE TABLE IF NOT EXISTS payments (
      id BIGSERIAL PRIMARY KEY,
      project_id BIGINT REFERENCES projects(id),
      user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      amount_pence INTEGER NOT NULL,
      currency TEXT NOT NULL DEFAULT 'gbp',
      description TEXT,
      stripe_session_id TEXT,
      stripe_payment_intent TEXT,
      status TEXT NOT NULL DEFAULT 'pending',
      created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    )`,
    'CREATE INDEX IF NOT EXISTS idx_payments_session ON payments(stripe_session_id)',
    `CREATE TABLE IF NOT EXISTS callbacks (
      id BIGSERIAL PRIMARY KEY,
      name TEXT NOT NULL,
      phone TEXT NOT NULL,
      call_when TEXT,
      topic TEXT,
      created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    )`,
  ];

  for (const statement of statements) {
    await pool.query(statement);
  }
}

function initSqlite() {
  const d = getSqliteDb();
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
}

export async function initDb() {
  if (isPostgres) {
    await initPostgres();
  } else {
    initSqlite();
  }
  console.log(`✓ Database initialised (${isPostgres ? 'postgres' : 'sqlite'})`);
}
