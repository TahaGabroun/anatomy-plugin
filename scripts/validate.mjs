import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const req=p=>{const f=path.join(root,p);if(!fs.existsSync(f))throw Error(`missing ${p}`);return f};
const manifest=JSON.parse(fs.readFileSync(req('source-snapshot.json'),'utf8'));
const plugin=JSON.parse(fs.readFileSync(req('plugin.json'),'utf8'));
const compat=JSON.parse(fs.readFileSync(req('.codex-plugin/plugin.json'),'utf8'));
const pkg=JSON.parse(fs.readFileSync(req('package.json'),'utf8'));
if(new Set([plugin.version,compat.version,pkg.version,manifest.version]).size!==1)throw Error('version mismatch');
const md=fs.readFileSync(req('skills/anatomy/SKILL.md'),'utf8');
for(const m of md.matchAll(/\]\((references\/[^)#?]+|evals\/[^)#?]+)\)/g)) req('skills/anatomy/'+m[1]);
for(const [name,sha] of Object.entries(manifest.files)) {
 const hash=crypto.createHash('sha256').update(fs.readFileSync(req(name))).digest('hex');
 if(hash!==sha)throw Error(`SHA256 mismatch: ${name}`);
}
for(const p of ['LICENSE','assets/icon.svg','skills/anatomy/agents/openai.yaml'])req(p);
console.log(`Validated Anatomy v${plugin.version}: ${Object.keys(manifest.files).length} content hashes; local references present.`);
