import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
const tests=[['node',['--test','skills/anatomy/examples/atp-synthase/benchmark.test.mjs']],['node',['--test','skills/anatomy/examples/animal-cell/model.test.mjs']],['node',['skills/anatomy/examples/animal-cell/build.mjs','--check']],['node',['skills/anatomy/examples/animal-cell/validate.mjs','--check']]];
for(const [exe,args] of tests){const ret=spawnSync(exe,args,{stdio:'inherit',encoding:'utf8'});if(ret.status!==0)process.exit(ret.status||1)}
for(const file of ['skills/anatomy/examples/animal-cell/live.js','skills/anatomy/examples/animal-cell/build.mjs']){const ret=spawnSync('node',['--check',file],{stdio:'inherit'});if(ret.status!==0)process.exit(1)}
console.log('Local smoke checks passed (ATP benchmark contract + animal-cell model; browser visual tests not included).');
