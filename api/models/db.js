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

function sqliteColumnExists(tableName, columnName) {
  const rows = getSqliteDb().prepare(`PRAGMA table_info(${tableName})`).all();
  return rows.some((row) => row.name === columnName);
}

function ensureSqliteColumn(tableName, columnName, definition) {
  if (sqliteColumnExists(tableName, columnName)) return;
  getSqliteDb().exec(`ALTER TABLE ${tableName} ADD COLUMN ${columnName} ${definition}`);
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
      email_message_id TEXT,
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
      customer_email_message_id TEXT,
      ops_email_message_id TEXT,
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
      drawing_ready_email_message_id TEXT,
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
      email_message_id TEXT,
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
      source_ip TEXT,
      user_agent TEXT,
      referrer TEXT,
      request_path TEXT,
      honeypot TEXT,
      email_message_id TEXT,
      created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    )`,
    `CREATE TABLE IF NOT EXISTS project_admin_audits (
      id BIGSERIAL PRIMARY KEY,
      action TEXT NOT NULL,
      admin_user_id BIGINT,
      admin_email TEXT,
      project_id BIGINT,
      project_title TEXT,
      client_email TEXT,
      created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    )`,
  ];

  for (const statement of statements) {
    await pool.query(statement);
  }

  await pool.query('ALTER TABLE callbacks ADD COLUMN IF NOT EXISTS source_ip TEXT');
  await pool.query('ALTER TABLE callbacks ADD COLUMN IF NOT EXISTS user_agent TEXT');
  await pool.query('ALTER TABLE callbacks ADD COLUMN IF NOT EXISTS referrer TEXT');
  await pool.query('ALTER TABLE callbacks ADD COLUMN IF NOT EXISTS request_path TEXT');
  await pool.query('ALTER TABLE callbacks ADD COLUMN IF NOT EXISTS honeypot TEXT');
  await pool.query('ALTER TABLE callbacks ADD COLUMN IF NOT EXISTS email_message_id TEXT');
  await pool.query('ALTER TABLE password_resets ADD COLUMN IF NOT EXISTS email_message_id TEXT');
  await pool.query('ALTER TABLE quotes ADD COLUMN IF NOT EXISTS customer_email_message_id TEXT');
  await pool.query('ALTER TABLE quotes ADD COLUMN IF NOT EXISTS ops_email_message_id TEXT');
  await pool.query('ALTER TABLE payments ADD COLUMN IF NOT EXISTS email_message_id TEXT');
  await pool.query('ALTER TABLE projects ADD COLUMN IF NOT EXISTS drawing_ready_email_message_id TEXT');
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
      email_message_id TEXT,
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
      customer_email_message_id TEXT,
      ops_email_message_id TEXT,
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
      drawing_ready_email_message_id TEXT,
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
      email_message_id TEXT,
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
      source_ip TEXT,
      user_agent TEXT,
      referrer TEXT,
      request_path TEXT,
      honeypot TEXT,
      email_message_id TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS project_admin_audits (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      action TEXT NOT NULL,
      admin_user_id INTEGER,
      admin_email TEXT,
      project_id INTEGER,
      project_title TEXT,
      client_email TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
  `);

  ensureSqliteColumn('callbacks', 'source_ip', 'TEXT');
  ensureSqliteColumn('callbacks', 'user_agent', 'TEXT');
  ensureSqliteColumn('callbacks', 'referrer', 'TEXT');
  ensureSqliteColumn('callbacks', 'request_path', 'TEXT');
  ensureSqliteColumn('callbacks', 'honeypot', 'TEXT');
  ensureSqliteColumn('callbacks', 'email_message_id', 'TEXT');
  ensureSqliteColumn('password_resets', 'email_message_id', 'TEXT');
  ensureSqliteColumn('quotes', 'customer_email_message_id', 'TEXT');
  ensureSqliteColumn('quotes', 'ops_email_message_id', 'TEXT');
  ensureSqliteColumn('payments', 'email_message_id', 'TEXT');
  ensureSqliteColumn('projects', 'drawing_ready_email_message_id', 'TEXT');
}

export async function initDb() {
  if (isPostgres) {
    await initPostgres();
  } else {
    initSqlite();
  }
  console.log(`✓ Database initialised (${isPostgres ? 'postgres' : 'sqlite'})`);
}
