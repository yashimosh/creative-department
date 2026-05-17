#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = __dirname;

const REGISTRY_URL = 'https://raw.githubusercontent.com/yashimosh/creative-department/main/registry.json';
const INSTALL_DIR = join(ROOT, '.claude', 'skills', 'creative-department');
const INSTALLED_FILE = join(ROOT, 'config', 'installed.json');
const LICENSE_FILE = join(ROOT, 'config', 'license.json');

function ensureDir(dir) {
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

function readInstalled() {
  if (!existsSync(INSTALLED_FILE)) return { skills: {} };
  try { return JSON.parse(readFileSync(INSTALLED_FILE, 'utf-8')); }
  catch { return { skills: {} }; }
}

function writeInstalled(data) {
  ensureDir(join(ROOT, 'config'));
  writeFileSync(INSTALLED_FILE, JSON.stringify(data, null, 2));
}

function readLicense() {
  if (!existsSync(LICENSE_FILE)) return null;
  try { return JSON.parse(readFileSync(LICENSE_FILE, 'utf-8')); }
  catch { return null; }
}

async function fetchRegistry() {
  try {
    const res = await fetch(REGISTRY_URL, {
      signal: AbortSignal.timeout(8000),
      headers: { 'User-Agent': 'creative-department-registry' },
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    const local = join(ROOT, 'registry.json');
    if (existsSync(local)) return JSON.parse(readFileSync(local, 'utf-8'));
    throw new Error(`Cannot reach registry: ${err.message}`);
  }
}

async function list(args) {
  const catIdx = args.indexOf('--category');
  const tierIdx = args.indexOf('--tier');
  const category = catIdx >= 0 ? args[catIdx + 1] : null;
  const tier = tierIdx >= 0 ? args[tierIdx + 1] : 'all';

  const registry = await fetchRegistry();
  let skills = registry.skills;
  if (category) skills = skills.filter(s => s.category === category);
  if (tier !== 'all') skills = skills.filter(s => s.tier === tier);

  const installed = readInstalled();
  console.log(`\ncreative-department registry  v${registry.version}  (${skills.length} skills)\n`);

  for (const s of skills) {
    const check = installed.skills[s.id] ? '✓' : ' ';
    const badge = s.tier === 'premium' ? '[PRO]  ' : s.tier === 'community' ? '[comm] ' : '[free] ';
    console.log(`  ${check} ${s.id.padEnd(26)}${badge}  ${s.description}`);
  }

  console.log(`\nCategories: ${registry.categories.join(', ')}`);
  console.log(`Installed: node registry.mjs installed`);
  console.log(`Install:   node registry.mjs install <skill-id>`);
  console.log(`Pro skills: yashimosh.com/creative-department\n`);
}

async function install(skillId) {
  if (!skillId) {
    console.error('Usage: node registry.mjs install <skill-id>');
    process.exit(1);
  }

  const registry = await fetchRegistry();
  const skill = registry.skills.find(s => s.id === skillId);
  if (!skill) {
    console.error(`Skill not found: ${skillId}`);
    console.error(`Run node registry.mjs list to see available skills.`);
    process.exit(1);
  }

  if (skill.tier === 'premium') {
    const license = readLicense();
    const hasAccess = license?.valid && ['pro', 'studio'].includes(license?.tier);
    if (!hasAccess) {
      console.log(`\nThis skill requires creative-department Pro.`);
      console.log(`Get access at yashimosh.com/creative-department\n`);
      process.exit(1);
    }
    // Premium install_url comes from the license server to allow rotation
    if (license.premium_base_url) {
      skill.install_url = `${license.premium_base_url}/${skillId}/`;
    }
  }

  const destDir = join(INSTALL_DIR, skillId);
  ensureDir(destDir);

  console.log(`Installing ${skill.name} v${skill.version}...`);
  const downloaded = [];

  for (const file of skill.files) {
    const url = `${skill.install_url}${file}`;
    try {
      const res = await fetch(url, {
        signal: AbortSignal.timeout(15000),
        headers: { 'User-Agent': 'creative-department-registry' },
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      writeFileSync(join(destDir, file), await res.text());
      downloaded.push(file);
    } catch (err) {
      console.error(`  Failed to download ${file}: ${err.message}`);
    }
  }

  if (downloaded.length === 0) {
    console.error(`Install failed — no files downloaded.`);
    process.exit(1);
  }

  const data = readInstalled();
  data.skills[skillId] = {
    version: skill.version,
    installed_at: new Date().toISOString(),
    tier: skill.tier,
  };
  writeInstalled(data);

  console.log(`✓ ${skill.name} installed → .claude/skills/creative-department/${skillId}/`);
  if (skill.requires?.length) console.log(`  Requires: ${skill.requires.join(', ')}`);
}

function installed() {
  const data = readInstalled();
  const skills = Object.entries(data.skills);
  if (!skills.length) {
    console.log('\nNo skills installed. Run: node registry.mjs list\n');
    return;
  }
  console.log(`\nInstalled skills (${skills.length})\n`);
  for (const [id, info] of skills) {
    const tag = info.bundled ? '[bundled]' : `v${info.version}`;
    const date = info.installed_at?.slice(0, 10) || 'unknown';
    console.log(`  ${id.padEnd(26)} ${tag.padEnd(12)}  ${date}`);
  }
  console.log();
}

async function upgrade() {
  const data = readInstalled();
  const ids = Object.keys(data.skills).filter(id => !data.skills[id].bundled);
  if (!ids.length) {
    console.log('No registry-installed skills to upgrade. (Bundled skills update with the system.)');
    return;
  }

  const registry = await fetchRegistry();
  let upgraded = 0;

  for (const id of ids) {
    const skill = registry.skills.find(s => s.id === id);
    if (!skill) { console.log(`  ${id}: not found in registry — skipping`); continue; }
    const current = data.skills[id].version;
    if (current === skill.version) { console.log(`  ${id}: already at v${current}`); continue; }
    console.log(`  ${id}: v${current} → v${skill.version}`);
    await install(id);
    upgraded++;
  }

  console.log(`\n${upgraded} skill(s) upgraded.`);
}

async function submit(skillPath) {
  if (!skillPath) {
    console.error('Usage: node registry.mjs submit <path-to-skill-folder>');
    process.exit(1);
  }

  const skillMd = join(skillPath, 'SKILL.md');
  if (!existsSync(skillMd)) {
    console.error('No SKILL.md found. Skill folder must contain a SKILL.md with frontmatter.');
    process.exit(1);
  }

  const content = readFileSync(skillMd, 'utf-8');
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  const id = fmMatch ? (fmMatch[1].match(/skill:\s*(.+)/) || [])[1]?.trim() : null;
  if (!id) {
    console.error('SKILL.md must have a `skill:` frontmatter field.');
    process.exit(1);
  }

  console.log(`\nSubmission package for: ${id}`);
  console.log('─'.repeat(40));
  console.log(JSON.stringify({
    id,
    submitted_at: new Date().toISOString(),
    files: ['SKILL.md'],
    note: 'Include full skill folder in your PR.',
  }, null, 2));
  console.log('\nOpen a PR at: https://github.com/yashimosh/creative-department/pulls');
  console.log('See CONTRIBUTING.md for submission guidelines.\n');
}

const [,, cmd, ...rest] = process.argv;
switch (cmd) {
  case 'list':      await list(rest);       break;
  case 'install':   await install(rest[0]); break;
  case 'installed': installed();            break;
  case 'upgrade':   await upgrade();        break;
  case 'submit':    await submit(rest[0]);  break;
  default:
    console.log('Usage: node registry.mjs [list|install <id>|installed|upgrade|submit <path>]');
    process.exit(1);
}
