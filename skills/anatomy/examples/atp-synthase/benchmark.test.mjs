import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import test from 'node:test';
const here=path.dirname(fileURLToPath(import.meta.url));
const source=fs.readFileSync(path.join(here,'atp-synthase.html'),'utf8');
test('preferred ATP visual benchmark retains license and a real SVG mechanism',()=>{
  assert.match(source,/Copyright \(c\) 2026 Ryan/);
  assert.match(source,/<svg[\s\S]*viewBox=/);
  assert.match(source,/data-camera/);
  for(const part of ['rotor','shaft','stator']) assert.match(source,new RegExp('data-piece="'+part+'"'));
});
test('ATP benchmark retains distinct exploration/inspection controls',()=>{
  for(const view of ['whole','rotor','beta']) assert.ok(source.includes('data-view="'+view+'"'),view);
  for(const phrase of ['Cutaway on','Separate parts','Advance 120°','Reset cycle','Proton half-channels','Three catalytic β sites','Cycle position']) assert.ok(source.includes(phrase),phrase);
  assert.match(source,/data-site=/);
  assert.match(source,/type="range"/);
});
test('ATP benchmark is distributable offline',()=>{
  assert.doesNotMatch(source,/<script[^>]+src=/i);
  assert.doesNotMatch(source,/<link[^>]+href="https?:/i);
});
