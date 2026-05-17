#!/usr/bin/env node
import { execFileSync, execSync } from 'child_process';
import { readFileSync, writeFileSync, existsSync, unlinkSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = __dirname;

const CANONICAL_REPO = 'https://github.com/yashimosh/creative-department.git';
const RAW_VERSION_URL = 'https://raw.githubusercontent.com/yashimosh/creative-department/main/VERSION';
const RAW_CHANGELOG_URL = 'https://raw.githubusercontent.com/yashimosh/creative-department/main/CHANGELOG.md';

// System layer — only these paths are updated by `apply`
const SYSTEM_PATHS = [
  'ANTI-AI-VOICE.md', 'ARCHITECTURE.md', 'BRIEF-TEMPLATE.md', 'CODE_OF_CONDUCT.md',
  'CONTRIBUTING.md', 'DECISIONS.md', 'DESIGN-RATIONALE.md', 'DESIGN-TOKENS.json',
  'HANDOFF.md', 'INTEGRATION.md', 'PIPELINE.md', 'PLATFORM-SPECS.md', 'README.md',
  'REGISTRY.md', 'REGISTRY-TEMPLATE.md', 'TOOLS.md', 'DATA_CONTRACT.md',
  'CLAUDE.md', 'VERSION', 'CHANGELOG.md', 'registry.json',
  'update-system.mjs', 'registry.mjs', 'telemetry.mjs', 'license.mjs', 'setup.mjs',
  'scripts/', 'audio-enhance/', 'whisper/', 'remotion-studio/', 'templates/',
  'config/profile.example.yml', 'package.json', 'LICENSE',
];

// User layer — NEVER touched by updates
const USER_PATHS = [
  'config/profile.yml', 'config/license.json', 'config/telemetry.json',
  'config/installed.json', 'clients/', 'registries/', 'dispatches/',
  'data/', 'output/', 'CONTEXT.md', 'CLIENT.md', 'BRAND-VOICE.md', 'CREATIVE-PLAYBOOK.md',
];

function localVersion() {
  const p = join(ROOT, 'VERSION');
  return existsSync(p) ? readFileSync(p, 'utf-8').trim() : '0.0.0';
}

function compareVersions(a, b) {
  const pa = a.split('.').map(Number);
  const pb = b.split('.').map(Number);
  for (let i = 0; i < 3; i++) {
    if ((pa[i] || 0) < (pb[i] || 0)) return -1;
    if ((pa[i] || 0) > (pb[i] || 0)) return 1;
  }
  return 0;
}

function git(...args) {
  return execFileSync('git', args, { cwd: ROOT, encoding: 'utf-8', timeout: 30000 }).trim();
}

function gitStatusEntries() {
  const status = git('status', '--porcelain');
  if (!status) return [];
  return status.split('\n').filter(Boolean).map(line => ({ code: line.slice(0, 2), path: line.slice(3) }));
}

function addPaths(paths) {
  if (paths.length > 0) git('add', '--', ...paths);
}

async function check() {
  if (existsSync(join(ROOT, '.update-dismissed'))) {
    console.log(JSON.stringify({ status: 'dismissed' }));
    return;
  }

  const local = localVersion();
  let remote = '';

  const controller = new AbortController();
  const tid = setTimeout(() => controller.abort(), 8000);
  try {
    const res = await fetch(RAW_VERSION_URL, {
      signal: controller.signal,
      headers: { 'User-Agent': 'creative-department-update-checker' },
    });
    if (res.ok) {
      const raw = (await res.text()).trim();
      const m = raw.match(/^v?(\d+\.\d+\.\d+)$/i);
      if (m) remote = m[1];
    }
  } catch {
    // network error
  } finally {
    clearTimeout(tid);
  }

  if (!remote) {
    console.log(JSON.stringify({ status: 'offline', local }));
    return;
  }

  if (compareVersions(local, remote) >= 0) {
    console.log(JSON.stringify({ status: 'up-to-date', local, remote }));
    return;
  }

  let changelog = '';
  try {
    const res = await fetch(RAW_CHANGELOG_URL, { signal: AbortSignal.timeout(5000) });
    if (res.ok) {
      const lines = (await res.text()).split('\n');
      const idx = lines.findIndex(l => l.includes(remote));
      if (idx >= 0 && idx + 1 < lines.length) changelog = lines[idx + 1].replace(/^[-*]\s*/, '').trim();
    }
  } catch { /* ignore */ }

  console.log(JSON.stringify({ status: 'update-available', local, remote, changelog }));
}

async function apply() {
  const local = localVersion();
  const lockFile = join(ROOT, '.update-lock');

  if (existsSync(lockFile)) {
    console.error('Update already in progress (.update-lock exists). If stuck, delete it manually.');
    process.exit(1);
  }
  writeFileSync(lockFile, new Date().toISOString());

  const initialPaths = new Set(gitStatusEntries().map(e => e.path));

  try {
    const backupBranch = `backup-pre-update-${local}`;
    try {
      git('branch', backupBranch);
      console.log(`Backup branch: ${backupBranch}`);
    } catch {
      console.log(`Backup branch already exists (${backupBranch}), continuing.`);
    }

    console.log('Fetching upstream...');
    git('fetch', CANONICAL_REPO, 'main');

    console.log('Updating system files...');
    const updated = [];
    for (const p of SYSTEM_PATHS) {
      try { git('checkout', 'FETCH_HEAD', '--', p); updated.push(p); }
      catch { /* path may not exist in remote yet */ }
    }

    // Safety: abort if any user file was modified
    for (const entry of gitStatusEntries()) {
      if (initialPaths.has(entry.path)) continue;
      for (const u of USER_PATHS) {
        if (entry.path.startsWith(u)) {
          console.error(`SAFETY VIOLATION: user file touched: ${entry.path}. Rolling back.`);
          try { git('checkout', '--', entry.path); } catch { /* best effort */ }
          process.exit(1);
        }
      }
    }

    try { execSync('npm install --silent', { cwd: ROOT, timeout: 60000 }); }
    catch { /* optional */ }

    const newVersion = localVersion();
    const dismissFile = join(ROOT, '.update-dismissed');
    if (existsSync(dismissFile)) { unlinkSync(dismissFile); updated.push('.update-dismissed'); }

    try {
      addPaths(updated);
      git('commit', '-m', `chore: update system files to v${newVersion}`);
    } catch { /* nothing to commit */ }

    console.log(`\nDone: v${local} → v${newVersion}  (${updated.length} paths)`);
    console.log(`Rollback available: node update-system.mjs rollback`);
  } finally {
    if (existsSync(lockFile)) unlinkSync(lockFile);
  }
}

function rollback() {
  try {
    const branches = git(
      'for-each-ref', '--sort=-committerdate',
      '--format=%(refname:short)', 'refs/heads/backup-pre-update-*'
    );
    const list = branches.split('\n').map(b => b.trim()).filter(Boolean);
    if (!list.length) { console.error('No backup branches found.'); process.exit(1); }

    const latest = list[0];
    console.log(`Rolling back to: ${latest}`);
    for (const p of SYSTEM_PATHS) {
      try { git('checkout', latest, '--', p); } catch { /* skip */ }
    }
    addPaths(SYSTEM_PATHS);
    git('commit', '-m', `chore: rollback system files from ${latest}`);
    console.log(`Rollback complete. User data was not affected.`);
  } catch (err) {
    console.error('Rollback failed:', err.message);
    process.exit(1);
  }
}

function dismiss() {
  writeFileSync(join(ROOT, '.update-dismissed'), new Date().toISOString());
  console.log('Update check dismissed. Delete .update-dismissed or run check to re-enable.');
}

const cmd = process.argv[2] || 'check';
switch (cmd) {
  case 'check':    await check();    break;
  case 'apply':    await apply();    break;
  case 'rollback': rollback();       break;
  case 'dismiss':  dismiss();        break;
  default:
    console.log('Usage: node update-system.mjs [check|apply|rollback|dismiss]');
    process.exit(1);
}
