import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const html=fs.readFileSync(path.join(dir,'ATP_Synthase_Anatomy_Experimental_8H9S.html'),'utf8');
const data=JSON.parse(fs.readFileSync(path.join(dir,'8h9s-render-data.json'),'utf8'));
const manifest=JSON.parse(fs.readFileSync(path.join(dir,'manifest.json'),'utf8'));
test('experimental ATP artifact and source hashes are pinned',()=>{
 assert.equal(sha(path.join(dir,'ATP_Synthase_Anatomy_Experimental_8H9S.html')),manifest.html_sha256);
 assert.equal(sha(path.join(dir,'8h9s-render-data.json')),manifest.data_sha256);
 assert.equal(data.source_sha256,manifest.input_mmcif_gz_sha256);
 assert.equal(sha(path.join(dir,'../v06/ATP_Synthase_Anatomy_v06.html')),manifest.locked_v06_sha256);
});
test('source-based geometry replaces rather than overlays procedural protein',()=>{
 assert.match(html,/function proteins\(\)\{if\(expGeometry\.real\)\{experimentalProteins\(\);return\}/);
 assert.match(html,/const rotating=c\.group==='ring'\|\|c\.group==='shaft'/);
 assert.match(html,/function experimentalProteins\(/);
 assert.match(html,/function mech\(/);
 assert.match(html,/id="atpWipeRange"/);
 assert.match(html,/id="expChain"/);
 assert.match(html,/id="expOld"/);
 assert.match(html,/id="expReal"/);
 assert.match(html,/illustrative/i);
});
test('embedded atom data matches exported data byte for byte',()=>{
 const m=html.match(/<script id="experimentalStructureData" type="application\/json">([^<]+)<\/script>/);
 assert.ok(m,'embedded coordinate data');
 assert.deepEqual(JSON.parse(m[1]),data);
});
test('deposited protein chain groups and point counts are internally consistent',()=>{
 assert.equal(data.pdb,'8H9S');
 assert.equal(data.chains.length,28);
 assert.equal(data.chains.filter(c=>c.group==='ring').length,8);
 assert.equal(data.chains.filter(c=>c.group==='alpha').length,3);
 assert.equal(data.chains.filter(c=>c.group==='beta').length,3);
 assert.equal(data.chains.filter(c=>c.group==='shaft').length,3);
 assert.equal(data.chains.filter(c=>c.group==='channel').length,1);
 assert.equal(data.chains.reduce((n,c)=>n+c.count,0),data.render_point_count);
 assert.equal(data.input_entry_id,'XXXX');
 assert.match(data.identity_status,/UNVERIFIED/);
 for(const c of data.chains){
  const bytes=Buffer.from(c.xyz10,'base64');
  assert.equal(bytes.length,c.count*6,`chain ${c.id}`);
  for(let i=0;i<bytes.length;i+=2)assert.ok(bytes.readUInt16LE(i)>0);
 }
 assert.equal(data.ligands.filter(x=>x.name==='ATP').length,3);
 assert.equal(data.ligands.filter(x=>x.name==='ADP').length,2);
});
