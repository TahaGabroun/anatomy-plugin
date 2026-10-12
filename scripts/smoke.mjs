import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const root = fileURLToPath(new URL('../', import.meta.url));
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'anatomy-plugin-smoke-'));
try {
  const skill = path.join(temporary, 'anatomy');
  fs.cpSync(path.join(root, 'skills', 'anatomy'), skill, { recursive: true });
  for (const example of ['dial-indicator', 'desk-computer']) {
    for (const light of [false, true]) {
      const command = [`examples/${example}/build.mjs`, ...(light ? ['--light'] : [])];
      const result = spawnSync(process.execPath, command, { cwd: skill, encoding: 'utf8', timeout: 120000 });
      assert.equal(result.status, 0, `${command.join(' ')}: ${result.stderr || result.error || result.stdout}`);
      const output = path.join(skill, 'examples', example, `${example}${light ? '-light' : ''}.html`);
      const html = fs.readFileSync(output, 'utf8');
      assert.match(html, /<svg\b/);
      assert.match(html, /<script\b/);
      assert.match(html, /anatomy/);
      console.log(`Built ${example} (${light ? 'light' : 'dark'}).`);
    }
  }
  console.log('Standalone smoke builds passed. Browser interaction was not tested by this command.');
} finally {
  fs.rmSync(temporary, { recursive: true, force: true });
}
