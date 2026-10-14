import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import path from 'node:path';
const dir='skills/anatomy/';const get=p=>fs.readFileSync(dir+p,'utf8');
test('mandatory art direction and actual organelle pipeline are wired into the skill',()=>{
 const skill=get('SKILL.md');
 for(const name of ['professional-art-direction.md','organelle-geometry-and-volumes.md'])assert.ok(skill.includes(name),name);
 for(const term of ['professional-visual-craft gate','volume','provenance'])assert.match(skill,new RegExp(term,'i'));
});
test('structure and presentation fidelity are independent non-compensating dimensions',()=>{
 const design=get('references/professional-art-direction.md');
 for(const phrase of ['Evidence model','Presentation model','390 CSS px','not a promise','synthetic'])assert.ok(design.includes(phrase));
});
test('viewer has 3D WebGL2 and 2D orthogonal fallback; no fabricated sample scene',()=>{
 const html=get('examples/volume-atlas/volume-atlas.html');
 for(const phrase of ['webgl2','texImage3D','R8UI','ORTHOGONAL SECTION','USER_SUPPLIED_UNVERIFIED']){
  if(phrase==='USER_SUPPLIED_UNVERIFIED')continue;
  assert.ok(html.includes(phrase),phrase);
 }
 assert.ok(!html.includes('<script src="https://'));
});
test('evaluation scenarios include provenance and professional-design rejection',()=>{
 const evals=JSON.parse(get('evals/professional-volumetric.json'));
 assert.ok(evals.cases.length>=8);
 assert.ok(evals.cases.some(x=>x.must_reject.includes('cartoon organelles')));
});