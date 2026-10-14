import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import crypto from 'node:crypto';import path from 'node:path';import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const m=JSON.parse(fs.readFileSync(path.join(dir,'manifest.json')));const b=fs.readFileSync(path.join(dir,m.file));
test('archived cell reference is unmodified and not falsely called experimental',()=>{
 assert.equal(crypto.createHash('sha256').update(b).digest('hex'),m.sha256);
 assert.match(m.status,/SCHEMATIC_NOT_APPROVED/);
 assert.ok(m.exclusions.includes('experimental microscopy-derived organelle geometry'));
 assert.match(m.visual_acceptance,/manual/);
});