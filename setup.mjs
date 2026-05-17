#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { createInterface } from 'readline';
import { randomUUID } from 'crypto';
import { execSync } from 'child_process';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = __dirname;

function ensureDir(dir) {
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

function ask(rl, question) {
  return new Promise(resolve => rl.question(question, resolve));
}

function checkNodeVersion() {
  const major = parseInt(process.versions.node.split('.')[0], 10);
  if (major < 18) {
    console.error(`\nNode.js 18+ required. You have v${process.versions.node}.`);
    console.error('Download the latest LTS at https://nodejs.org\n');
    process.exit(1);
  }
}

async function main() {
  checkNodeVersion();

  console.log('\n╔══════════════════════════════════════╗');
  console.log('║     creative-department  setup       ║');
  console.log('╚══════════════════════════════════════╝\n');

  const configDir = join(ROOT, 'config');
  ensureDir(configDir);

  if (existsSync(join(configDir, 'profile.yml'))) {
    console.log('Already configured. To reconfigure, delete config/profile.yml and re-run.');
    console.log('  /cd list            — browse skills');
    console.log('  /cd license status  — check license tier\n');
    return;
  }

  const rl = createInterface({ input: process.stdin, output: process.stdout });

  try {
    const name = (await ask(rl, 'Your name: ')).trim() || 'Anonymous';

    const useRaw = (await ask(rl, 'Primary use [personal / team / agency]: ')).trim().toLowerCase();
    const use = ['personal', 'team', 'agency'].includes(useRaw) ? useRaw : 'personal';

    console.log('\n─────────────────────────────────────────');
    console.log('Send anonymous usage data to help improve creative-department?');
    console.log('No personal data, no content — just which skills run and how often.');
    const telemetryRaw = (await ask(rl, '(y/n): ')).trim().toLowerCase();
    const telemetry = telemetryRaw === 'y' || telemetryRaw === 'yes';
    console.log('─────────────────────────────────────────\n');

    // Write profile.yml
    const examplePath = join(ROOT, 'config', 'profile.example.yml');
    let profileContent = existsSync(examplePath)
      ? readFileSync(examplePath, 'utf-8')
      : `name: ""\nuse: personal\ntimezone: ""\n\nbrand:\n  name: ""\n  url: ""\n  tone: ""\n`;
    profileContent = profileContent
      .replace(/^name:.*$/m, `name: "${name}"`)
      .replace(/^use:.*$/m, `use: ${use}`);
    writeFileSync(join(configDir, 'profile.yml'), profileContent);

    // Write telemetry.json
    const installId = randomUUID();
    writeFileSync(
      join(configDir, 'telemetry.json'),
      JSON.stringify({ telemetry, install_id: installId }, null, 2)
    );

    if (telemetry) {
      try {
        execSync('node telemetry.mjs install system', { cwd: ROOT, timeout: 6000, stdio: 'ignore' });
      } catch { /* fail silently */ }
    }

    // Initialize installed.json with bundled skills
    writeFileSync(
      join(configDir, 'installed.json'),
      JSON.stringify({
        skills: {
          'audio-enhance':  { version: '1.0.0', installed_at: new Date().toISOString(), bundled: true },
          'whisper':        { version: '1.0.0', installed_at: new Date().toISOString(), bundled: true },
          'remotion-studio':{ version: '1.0.0', installed_at: new Date().toISOString(), bundled: true },
        }
      }, null, 2)
    );

    console.log('✓ config/profile.yml');
    console.log(`✓ config/telemetry.json  (telemetry: ${telemetry})`);
    console.log('✓ config/installed.json  (audio-enhance, whisper, remotion-studio)');
    console.log('\nYou\'re set.\n');
    console.log('  /cd list              — browse available skills');
    console.log('  /cd install <skill>   — add a skill from the registry');
    console.log('  node registry.mjs list — same from terminal\n');
    console.log('Pro skills at yashimosh.com/creative-department\n');

  } finally {
    rl.close();
  }
}

await main();
