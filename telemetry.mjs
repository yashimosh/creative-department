#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = __dirname;

const CONFIG_FILE = join(ROOT, 'config', 'telemetry.json');
const ENDPOINT = 'https://cd-telemetry.yashimosh.com/event';

function readConfig() {
  if (!existsSync(CONFIG_FILE)) return null;
  try { return JSON.parse(readFileSync(CONFIG_FILE, 'utf-8')); }
  catch { return null; }
}

function writeConfig(data) {
  const dir = join(ROOT, 'config');
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  writeFileSync(CONFIG_FILE, JSON.stringify(data, null, 2));
}

function readVersion() {
  const p = join(ROOT, 'VERSION');
  return existsSync(p) ? readFileSync(p, 'utf-8').trim() : '0.0.0';
}

function getOs() {
  const p = process.platform;
  if (p === 'win32') return 'win';
  if (p === 'darwin') return 'mac';
  return 'linux';
}

async function fire(event, skillId) {
  const cfg = readConfig();
  if (!cfg?.telemetry) return; // opt-out or not configured — silent no-op

  const payload = {
    install_id: cfg.install_id,
    skill_id: skillId || null,
    event,
    version: readVersion(),
    os: getOs(),
    ts: new Date().toISOString(),
  };

  // Fails silently — telemetry must never block the user's work
  try {
    await fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(4000),
    });
  } catch { /* intentionally swallowed */ }
}

async function optOut() {
  await fire('opted-out', null); // one final event before disabling
  const cfg = readConfig() || {};
  cfg.telemetry = false;
  writeConfig(cfg);
  console.log('Telemetry disabled. config/telemetry.json updated.');
  console.log('Run `node telemetry.mjs opt-in` to re-enable.');
}

async function optIn() {
  const { randomUUID } = await import('crypto');
  const cfg = readConfig() || {};
  cfg.telemetry = true;
  if (!cfg.install_id) cfg.install_id = randomUUID();
  writeConfig(cfg);
  await fire('opted-in', null);
  console.log('Telemetry enabled. No personal data, no content — just which skills run.');
  console.log('Run `node telemetry.mjs opt-out` anytime to disable.');
}

const [,, cmd, skillId] = process.argv;
switch (cmd) {
  case 'run':     await fire('run',     skillId); break;
  case 'error':   await fire('error',   skillId); break;
  case 'install': await fire('install', skillId); break;
  case 'opt-out': await optOut();                 break;
  case 'opt-in':  await optIn();                  break;
  default:
    // Called as: node telemetry.mjs <skill-id>  (shorthand for `run`)
    if (cmd) await fire('run', cmd);
    else console.log('Usage: node telemetry.mjs [run|error|install|opt-out|opt-in] [skill-id]');
}
