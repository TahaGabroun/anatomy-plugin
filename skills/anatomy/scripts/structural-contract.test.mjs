import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const root=new URL('../',import.meta.url);
const get=p=>fs.readFileSync(new URL(p,root),'utf8');
test('skill routes molecular tasks to actual structural import and disclosure',()=>{
 const skill=get('SKILL.md');
 for(const part of ['references/experimental-structures.md','references/provenance-and-disclosure.md','references/benchmark-nonregression.md','tools/structure_import.py','examples/structure-viewer/structure-viewer.html'])assert.ok(skill.includes(part),part);
 assert.match(skill,/8H9S/);
});
test('structural evals enforce evidence-based representation',()=>{
 const cases=JSON.parse(get('evals/structural-grounding.json')).cases;
 assert.ok(cases.length>=8);
 for(const c of cases)for(const k of ['id','prompt','required','disallow'])assert.ok(c[k],c.id+':'+k);
});
test('viewer distinguishes structure from schematic surface and motion',()=>{
 const html=get('examples/structure-viewer/structure-viewer.html');
 assert.match(html,/coordinate-scaffold/);
 assert.match(html,/not a solvent-accessible surface/i);
 assert.match(html,/SOURCE UNVERIFIED/);
 assert.match(html,/id="file"/);
 assert.match(html,/id="scene"/);
});
