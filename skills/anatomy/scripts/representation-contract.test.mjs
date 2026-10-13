import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const base=new URL('../',import.meta.url);
const get=p=>readFileSync(new URL(p,base),'utf8');
const modes=new Set(['BIOLOGICAL','MECHANISTIC','HYBRID']);
const examples=JSON.parse(get('evals/representation-routing.json'));
const ids=new Set();
test('adaptive representation fixtures specify a defensible expected mode',()=>{
 assert.ok(examples.cases.length>=14);
 for(const c of examples.cases){
  assert.ok(c.id&&c.prompt&&c.why,'every fixture needs an id, prompt and rationale');
  assert.ok(modes.has(c.expected_mode),c.id+' invalid mode');
  assert.ok(!ids.has(c.id),'duplicate '+c.id);ids.add(c.id);
 }
 for(const mode of modes)assert.ok(examples.cases.filter(c=>c.expected_mode===mode).length>=2,mode+' underrepresented');
});
test('skill entrypoint actually routes to the distinct build guidance',()=>{
 const skill=get('SKILL.md');
 for(const ref of ['references/representation-routing.md','references/molecular-rendering.md','references/biological-figures.md','references/engineering.md'])assert.ok(skill.includes(ref),'missing link: '+ref);
 const routing=get('references/representation-routing.md');
 const rendering=get('references/molecular-rendering.md');
 assert.match(routing,/ATP synthase/i);assert.match(routing,/HYBRID/);assert.match(routing,/BIOLOGICAL/);assert.match(routing,/MECHANISTIC/);
 assert.match(rendering,/PDBx\/mmCIF/);assert.match(rendering,/illustrative interpolation/);assert.match(rendering,/colour/i);
});
test('ATP benchmark is not installed as biological ground truth',()=>{
 assert.match(get('references/atp-benchmark.md'),/not the final organic rendering target/);
 assert.match(get('references/molecular-rendering.md'),/not bundled or redistributed/);
});
// This verifies specification and evaluation coverage only. It does not evaluate
// a language model's choice or any browser-rendered visualization.
