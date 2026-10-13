import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const meta=JSON.parse(fs.readFileSync(path.join(here,'manifest.json'),'utf8'));
const bin=fs.readFileSync(path.join(here,meta.source_file));
const src=bin.toString('utf8');
const hash=crypto.createHash('sha256').update(bin).digest('hex');
test('approved v0.6 HTML remains byte-for-byte locked',()=>{
  assert.equal(meta.version,'0.6.0');
  assert.equal(meta.status,'APPROVED_VISUAL_AND_INTERACTION_BASELINE');
  assert.equal(meta.source_bytes,bin.length);
  assert.equal(meta.source_sha256,hash);
  assert.equal(hash,'364ddb139d4a8eb4923c315714a7755b76884133f41022bf442b4f25fb44bbbd');
});
test('baseline interactive exploration controls remain present',()=>{
  for(const id of ['atpCanvas','atpPartTitle','atpPlay','atpStep45','atpStep120','atpTimeline','atpReset','atpYaw','atpGradient','atpWipeRange','atpCut','atpExplode','atpProtons','atpResetCam','atpSites','atpH','atpATP']){
   assert.ok(src.includes(`id="${id}"`),`lost ${id}`);
  }
  for(const mode of ['bio','split','mech'])assert.ok(src.includes(`data-mode="${mode}"`),`lost ${mode}`);
  for(const part of ['head','shaft','ring','channel','stator'])assert.ok(src.includes(`data-part="${part}"`),`lost ${part}`);
  assert.match(src,/8 H⁺ \/ 3 ATP/i);
});
test('benchmark is standalone and retains explicit scientific disclaimer',()=>{
 assert.doesNotMatch(src,/<script[^>]+src=/i);
 assert.match(src,/Surfaces are procedurally generated—not atomic coordinates/);
 assert.match(src,/Conformational motion and proton trajectories are illustrative/);
});
