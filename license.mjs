#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync, mkdirSync, unlinkSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = __dirname;

const LICENSE_FILE = join(ROOT, 'config', 'license.json');
const VERIFY_ENDPOINT = 'https://cd-license.yashimosh.com/verify';

function readLicense() {
  if (!existsSync(LICENSE_FILE)) return null;
  try { return JSON.parse(readFileSync(LICENSE_FILE, 'utf-8')); }
  catch { return null; }
}

function writeLicense(data) {
  const dir = join(ROOT, 'config');
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  writeFileSync(LICENSE_FILE, JSON.stringify(data, null, 2));
}

async function activate(key) {
  if (!key) {
    console.error('Usage: node license.mjs activate <key>');
    process.exit(1);
  }

  console.log('Verifying license...');
  let data;
  try {
    const res = await fetch(VERIFY_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key }),
      signal: AbortSignal.timeout(12000),
    });
    data = await res.json();
  } catch (err) {
    console.error(`Verification failed: ${err.message}`);
    console.error('Check your connection and try again.');
    process.exit(1);
  }

  if (!data.valid) {
    console.error(`Invalid license key.`);
    console.error(`Get access at yashimosh.com/creative-department`);
    process.exit(1);
  }

  writeLicense({ ...data, key, activated_at: new Date().toISOString() });

  console.log(`\n✓ License activated`);
  console.log(`  Tier:    ${data.tier}`);
  if (data.seats) console.log(`  Seats:   ${data.seats}`);
  console.log(`  Expires: ${data.expires || 'never'}`);
  console.log(`\nRun /cd list to see premium skills now available.\n`);
}

function status() {
  const license = readLicense();
  if (!license) {
    console.log('\nNo license. Free tier active.');
    console.log('Pro + Studio at yashimosh.com/creative-department\n');
    return;
  }

  const expired = license.expires && new Date(license.expires) < new Date();
  console.log(`\nLicense`);
  console.log(`  Tier:       ${license.tier}`);
  console.log(`  Valid:      ${license.valid && !expired ? 'yes' : 'no' + (expired ? ' (expired)' : '')}`);
  if (license.seats) console.log(`  Seats:      ${license.seats}`);
  console.log(`  Expires:    ${license.expires || 'never'}`);
  console.log(`  Activated:  ${license.activated_at?.slice(0, 10)}`);
  console.log();
}

function deactivate() {
  if (!existsSync(LICENSE_FILE)) {
    console.log('No license to deactivate.');
    return;
  }
  unlinkSync(LICENSE_FILE);
  console.log('License deactivated. Free tier restored.');
}

const [,, cmd, key] = process.argv;
switch (cmd) {
  case 'activate':   await activate(key); break;
  case 'status':     status();            break;
  case 'deactivate': deactivate();        break;
  default:
    console.log('Usage: node license.mjs [activate <key>|status|deactivate]');
    process.exit(1);
}
