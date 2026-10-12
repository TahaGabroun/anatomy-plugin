import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';

const root = path.resolve(fileURLToPath(new URL('../', import.meta.url)));
const load = file => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
const manifest = load('plugin.json');
const legacy = load('.codex-plugin/plugin.json');
const marketplace = load('.agents/plugins/marketplace.json');
const metadata = load('package.json');
const snapshot = load('source-snapshot.json');

assert.equal(manifest.$schema, 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json');
assert.match(manifest.name, /^[a-z0-9]+(?:-[a-z0-9]+)*$/);
assert.match(manifest.version, /^\d+\.\d+\.\d+$/);
assert.ok(manifest.description.length > 0);
assert.equal(manifest.license, 'MIT');
for (const key of ['name', 'version', 'description', 'author', 'license', 'keywords']) {
  assert.deepEqual(legacy[key], manifest[key], `Compatibility manifest differs: ${key}`);
}
assert.equal(metadata.version, manifest.version);
assert.equal(metadata.private, true);
assert.equal(legacy.skills, './skills/');
const presentation = manifest.extensions['com.openai'].interface;
assert.deepEqual(legacy.interface, presentation);

function localPath(relative, base = root) {
  assert.ok(relative.startsWith('./'), `Path must start with ./: ${relative}`);
  const resolved = path.resolve(base, relative);
  assert.ok(resolved === base || resolved.startsWith(base + path.sep), `Path escapes package: ${relative}`);
  assert.ok(fs.existsSync(resolved), `Missing resource: ${relative}`);
  return resolved;
}
for (const key of ['composerIcon', 'logo']) localPath(presentation[key]);
assert.equal(marketplace.name, 'anatomy-plugins');
assert.equal(marketplace.plugins.length, 1);
const entry = marketplace.plugins[0];
assert.equal(entry.name, manifest.name);
assert.equal(entry.source.source, 'local');
assert.equal(localPath(entry.source.path), path.resolve(root));
assert.equal(entry.policy.installation, 'AVAILABLE');
assert.ok(['ON_INSTALL', 'ON_USE'].includes(entry.policy.authentication));
assert.equal(entry.category, presentation.category);

const skillRoot = path.join(root, 'skills', 'anatomy');
const skill = fs.readFileSync(path.join(skillRoot, 'SKILL.md'), 'utf8');
assert.match(skill, /^---\r?\nname: anatomy\r?\ndescription: \S[^\n]*\r?\n---/);
assert.match(skill, /references\/chatgpt-runtime\.md/);
assert.equal(fs.readFileSync(path.join(root, 'LICENSE'), 'utf8'), fs.readFileSync(path.join(skillRoot, 'LICENSE'), 'utf8'));
assert.match(fs.readFileSync(path.join(root, 'LICENSE'), 'utf8'), /Copyright \(c\) 2026 Ryan/);
assert.deepEqual(fs.readFileSync(path.join(root, 'assets/icon.svg')), fs.readFileSync(path.join(skillRoot, 'assets/icon.svg')));

function walk(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap(item => {
    const file = path.join(directory, item.name);
    assert.ok(!item.isSymbolicLink(), `Symlinks are not distributable: ${file}`);
    return item.isDirectory() ? walk(file) : [file];
  });
}
const exported = walk(skillRoot).map(file => path.relative(skillRoot, file).split(path.sep).join('/')).sort();
const currentHashes = snapshot.adaptation_sha256 || snapshot.sha256;
assert.deepEqual(exported, Object.keys(currentHashes).sort(), 'Skill file set differs from current adaptation snapshot');
for (const relative of exported) {
  const digest = createHash('sha256').update(fs.readFileSync(path.join(skillRoot, relative))).digest('hex');
  assert.equal(digest, currentHashes[relative], `Changed or damaged skill file: ${relative}`);
}
const adaptedBaselineFiles = new Set(['SKILL.md', 'references/chatgpt-runtime.md', 'references/upstream.md', 'evals/evals.json', 'agents/openai.yaml']);
for (const [relative, expected] of Object.entries(snapshot.sha256)) {
  if (adaptedBaselineFiles.has(relative)) continue;
  assert.equal(currentHashes[relative], expected, `Original resource changed: ${relative}`);
}
assert.equal(snapshot.upstream.repository, 'https://github.com/wheresryan22/anatomy');
assert.equal(snapshot.upstream.license, manifest.license);
assert.match(snapshot.upstream.revision, /^[a-f0-9]{40}$/);

const examples = fs.readdirSync(path.join(skillRoot, 'examples'), { withFileTypes: true }).filter(item => item.isDirectory());
assert.equal(examples.length, 9);
const programs = [...walk(skillRoot), ...walk(path.join(root, 'scripts'))].filter(file => /\.(mjs|js)$/.test(file));
for (const file of programs) {
  const checked = spawnSync(process.execPath, ['--check', file], { encoding: 'utf8' });
  assert.equal(checked.status, 0, `${path.relative(root, file)}: ${checked.stderr}`);
}
console.log(`Plugin validation passed: ${exported.length} adaptation files, preserved original resources, ${examples.length} examples, ${programs.length} JavaScript syntax checks.`);
