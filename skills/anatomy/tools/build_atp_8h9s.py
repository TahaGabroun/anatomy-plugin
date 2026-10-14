import gzip, gemmi, numpy as np, json, hashlib, base64, re, pathlib, argparse
from scipy.spatial import cKDTree
parser=argparse.ArgumentParser(description='Build an offline ATP synthase molecular/mechanical interactive from an experimental 8H9S mmCIF assembly.')
parser.add_argument('--input',type=pathlib.Path,required=True,help='Local 8h9s-assembly1.cif.gz')
parser.add_argument('--template',type=pathlib.Path,required=True,help='Locked v0.6 ATP synthase HTML')
parser.add_argument('--output',type=pathlib.Path,required=True,help='Standalone experimental ATP synthase HTML')
parser.add_argument('--data-output',type=pathlib.Path,required=True,help='Extracted atom-derived render JSON')
args=parser.parse_args()
raw=args.input.read_bytes()
block=gemmi.cif.read_string(gzip.decompress(raw).decode()).sole_block()
struct=gemmi.make_structure_from_block(block)
file_title=block.find_value('_struct.title').strip('\"')
file_entry_id=(block.find_value('_entry.id') or '?').strip('\"')
if 'Human ATP synthase state 1' not in file_title:
 raise SystemExit('Input does not identify the expected human ATP synthase state-1 structure')
groups={'alpha':list('ABC'),'beta':list('EFD'),'shaft':list('GHI'),'ring':list('12345678'),'channel':['N'],'stator':list('KLMOPQRST'),'regulator':['J']}
chain_map={chain:g for g,chains in groups.items() for chain in chains}
entity_names={r[0]:r[3].strip('"') for r in block.find_mmcif_category('_entity.')}
poly_entity={r[6].strip('"').split(',')[i]:r[0] for r in block.find_mmcif_category('_entity_poly.') for i in range(len(r[6].strip('"').split(',')))}
all_atoms=[]
for chain in struct[0]:
 if chain.name not in chain_map:continue
 for res in chain:
  if res.name in ['ATP','ADP','CDL','3PH']:continue
  for a in res:
   if a.element.name not in ('C','N','O','S'):continue
   all_atoms.append((chain.name,res.name,a.name,np.array([a.pos.x,a.pos.y,a.pos.z])))
coords=np.array([a[3] for a in all_atoms]); counts=cKDTree(coords).query_ball_point(coords,5.2,return_length=True)
# Preserve all CA positions and a reproducible sample of solvent-facing atoms.
# Not a solvent-accessible surface calculation; each visible sphere is anchored to a real heavy atom.
selected=[]
for i,(chain,res,name,pos) in enumerate(all_atoms):
 if name=='CA' or (counts[i]<22 and i%3==0):selected.append((chain,res,name,pos))
print('heavy atoms',len(all_atoms),'render points',len(selected))
bychain={c:[] for c in chain_map}
for chain,res,name,pos in selected:
 # coordinates stored in original Å with 0.1Å precision; conversion occurs at runtime.
 bychain[chain].append([round(float(v)*10) for v in pos])
# Atom positions are the actual deposited coordinates, quantized to 0.1Å for portable rendering.
# Store as base64 encoded Uint16 triplets to avoid bloated JSON and preserve offline access.
chains=[]
for chain,points in bychain.items():
 arr=np.array(points,dtype=np.uint16)
 chains.append({'id':chain,'group':chain_map[chain],'entity':int(poly_entity[chain]),'name':entity_names[poly_entity[chain]],'count':len(points),'xyz10':base64.b64encode(arr.astype('<u2').tobytes()).decode()})
rotor_chains=set(groups['ring'])
rotor_ca=np.array([a[3] for a in all_atoms if a[0] in rotor_chains and a[2]=='CA'])
rotor_xy=rotor_ca[:,:2].mean(axis=0)
print('c ring axis x,y',rotor_xy)
ligands=[]
for chain in struct[0]:
 for res in chain:
  if res.name not in ['ATP','ADP']:continue
  atoms=[a for a in res if a.element.name in ['C','N','O','P','S']]
  if not atoms:continue
  p=np.mean([[a.pos.x,a.pos.y,a.pos.z] for a in atoms],axis=0)
  ligands.append({'name':res.name,'xyz':[round(float(v),2) for v in p]})
print('ligands',ligands)
data={'pdb':'8H9S','title':'Human ATP synthase state 1 (combined)','method':'single-particle cryo-electron microscopy','resolution_angstrom':2.53,'source':'user-supplied mmCIF biological assembly','source_sha256':hashlib.sha256(raw).hexdigest(),'input_entry_id':file_entry_id,'identity_status':'USER_SUPPLIED_TITLE_MATCH_ID_UNVERIFIED' if file_entry_id.upper()!='8H9S' else 'FILE_ID_MATCH','coordinate_precision_angstrom':0.1,'rotor_axis_xy_angstrom':rotor_xy.round(4).tolist(),'chains':chains,'ligands':ligands,'render_point_count':len(selected),'atom_count':len(all_atoms),'experimental_motion':False}
args.data_output.parent.mkdir(parents=True,exist_ok=True)
args.data_output.write_text(json.dumps(data,separators=(',',':')))
html=args.template.read_text()
# Style improvements are strictly local; original layout and all teaching controls preserved.
html=html.replace('ATP Synthase • Molecular Anatomy — an interactive protein motor','ATP Synthase • Experimental Molecular Anatomy — PDB 8H9S')
html=html.replace('MOLECULAR MECHANISMS / 006','MOLECULAR MECHANISMS / 008')
html=html.replace('FIG 06','FIG 08')
html=html.replace('ANATOMY v0.6 · ORGANIC / MECHANICAL ADAPTIVE MODEL','ANATOMY v0.8 · EXPERIMENTAL ASSEMBLY / MECHANICAL ANALOGY')
html=html.replace('Topology informed by human mitochondrial ATP synthase cryo-EM, <a href="https://www.rcsb.org/structure/8H9S" target="_blank" rel="noopener noreferrer">PDB 8H9S</a>, and mammalian F₁–c₈ structures (<a href="https://www.rcsb.org/structure/2XND" target="_blank" rel="noopener noreferrer">2XND</a>). Surfaces are procedurally generated—not atomic coordinates. Conformational motion and proton trajectories are illustrative, not an experimentally sampled time series or molecular-dynamics calculation.',
 'The default protein view is built from heavy-atom coordinates in the supplied human cryo-EM assembly <a href="https://www.rcsb.org/structure/8H9S" target="_blank" rel="noopener noreferrer">PDB 8H9S</a> (reported 2.53 Å). The supplied assembly file identifies its entry as XXXX, so the coordinate-file identity is not independently authenticated against the archive. Spheres are a subsampled, atom-centred rendering, <em>not</em> a calculated solvent-accessible surface. The ring/shaft motion, β-domain deformation, proton tracks and synthesis counters remain pedagogical illustrations, not experimental trajectories or molecular dynamics. The machine view is an analogy, not molecular geometry.')
html=html.replace('A real molecular mechanism, represented schematically.','Experimental protein geometry; illustrative catalytic motion.')
html=html.replace('The α₃β₃ catalytic head is fixed by its peripheral stalk while the c₈ ring and central γ stalk rotate together.', 'The supplied 8H9S-labelled assembly places the α₃β₃ head, central stalk, peripheral stalk, subunit a, and c₈ ring in their experimentally resolved relative positions. In this teaching animation, the c-ring and central stalk rotate together while the head stays stationary.')
html=html.replace('The β subunits undergo coordinated conformational changes.','The β-subunit movement is a small illustrative deformation of the deposited state-1 coordinates.')
# Add switch to inspector (without replacing old controls).
anchor='<div><h3 class="cap">STRUCTURAL EXPLORATION</h3>'
controls='''<div class="exp-settings"><h3 class="cap">MOLECULAR GEOMETRY</h3><div class="geom-switch" role="group" aria-label="Protein geometry source"><button type="button" id="expReal" aria-pressed="true">◉ PDB 8H9S</button><button type="button" id="expOld" aria-pressed="false">◯ Illustrated</button></div><div class="exp-badge" id="expBadge">ATOM-DERIVED GEOMETRY · REPORTED 2.53 Å</div><label class="exp-label" for="expChain">ISOLATE A SUBUNIT</label><select id="expChain"><option value="">All 28 protein chains</option></select><label class="exp-ligand"><input type="checkbox" id="expLigands" checked> Show deposited ATP / ADP</label><p class="exp-small" id="expChainDesc">Actual atomic positions determine the protein geometry. Rotation and catalysis remain illustrative.</p></div>'''
assert anchor in html
html=html.replace(anchor,controls+anchor,1)
# Visual indicator in stage. 
html=html.replace('<div class="stage-hud hud-matrix">','<div class="stage-hud exp-stage-tag" id="expStageTag">PDB 8H9S · 28 PROTEIN CHAINS</div><div class="stage-hud hud-matrix">',1)
html=html.replace('</style>','''
.exp-settings{border:1px solid #344b60;border-radius:8px;padding:12px;background:linear-gradient(145deg,#172635,#101a28)}.geom-switch{display:grid;grid-template-columns:1fr 1fr;gap:5px}.geom-switch button{font-size:11px;border:1px solid #365067;border-radius:5px;background:#0c1926;color:#a7bbca;padding:9px 4px;min-height:38px}.geom-switch button[aria-pressed="true"]{background:#bbdfe6;color:#071b25;border-color:#bbdfe6;font-weight:750}.exp-badge{margin-top:9px;color:#83d8be;letter-spacing:.1em;font-size:9px}.exp-label{display:block;margin:13px 0 5px;color:#b5c5d3;font-size:10px;letter-spacing:.09em}.exp-settings select{width:100%;max-width:100%;padding:8px;background:#0b1724;color:#e2edf2;border:1px solid #365067;border-radius:5px;font-size:12px}.exp-ligand{display:flex;gap:8px;align-items:center;font-size:11px;color:#bbcad8;margin-top:12px}.exp-ligand input{accent-color:#86d5c6;width:16px;height:16px}.exp-small{color:#9caec1!important;font-size:10px!important;line-height:1.55!important;margin:9px 0 0!important}.exp-stage-tag{right:18px;top:68px;color:#89ddc4;font-size:9px;background:#0c1925d4;border:1px solid #35556a;padding:4px 7px;border-radius:4px;z-index:3}.hud-matrix{top:20px}.exp-evidence{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}.exp-evidence span{font:10px ui-monospace,monospace;color:#8fc9bd;border:1px solid #34554e;border-radius:4px;padding:4px 7px}@media(max-width:440px){.exp-stage-tag{top:47px;right:8px;font-size:8px}.geom-switch button{font-size:10px}}
</style>''',1)
# inject data inline as script tag (not external; browser offline).
html=html.replace('<script>','<script id="experimentalStructureData" type="application/json">'+json.dumps(data,separators=(',',':'))+'</script>\n<script>',1)
# change render protein function to conditional (new function defined later, hoisted).
html=html.replace('function proteins(){let q=[];', 'function proteins(){if(expGeometry.real){experimentalProteins();return}let q=[];',1)
# new runtime logic inserted immediately before render function.
insert='''
// Molecular geometry from the deposited 8H9S assembly. These points are not an overlay:
// they REPLACE all procedural protein shapes when experimental mode is active.
const expData=JSON.parse(document.getElementById('experimentalStructureData').textContent);
const expGeometry={real:true,isolated:'',ligands:true,chains:[],ready:false};
const expColors={alpha:['#bd6eab','#d88bba','#9e6cc0'],beta:['#f3b651','#f9d06a','#e99b52'],shaft:['#5f8fe4','#82b7ec','#507dc7'],ring:['#9e76e3','#ae87ee','#8260ce','#b89bef'],channel:['#f17f70'],stator:['#dba15a','#bf8a42','#cf9c66','#d2ae72','#c88448','#bb8546','#daae61','#b9825b','#b49b6e'],regulator:['#7cb5b7']};
const expGroups={};
const axis=expData.rotor_axis_xy_angstrom;
function pdbScene(x,y,z){return [(x-axis[0])*1.70,(240-z)*1.43,(y-axis[1])*1.70]}
function initializeExperimental(){
 const chainSel=$('expChain');
 for(const c of expData.chains){
  const raw=atob(c.xyz10),view=new DataView(new ArrayBuffer(raw.length));
  for(let i=0;i<raw.length;i++)view.setUint8(i,raw.charCodeAt(i));
  const points=new Float32Array(c.count*3);
  for(let i=0;i<c.count;i++){
   const q=pdbScene(view.getUint16(i*6,true)/10,view.getUint16(i*6+2,true)/10,view.getUint16(i*6+4,true)/10);
   points[i*3]=q[0];points[i*3+1]=q[1];points[i*3+2]=q[2];
  }
  const n=expGroups[c.group]||0;expGroups[c.group]=n+1;
  c.color=(expColors[c.group]||['#a7c4d2'])[n%(expColors[c.group]||['#a7c4d2']).length];
  c.points=points;
  const opt=document.createElement('option');opt.value=c.id;opt.textContent=c.id+' · '+c.name.replace(/, mitochondrial/g,'');chainSel.appendChild(opt);
 }
 expGeometry.chains=expData.chains;expGeometry.ready=true;
}
initializeExperimental();
function experimentalProteins(){
 const q=[],angle=state.angle*rad,expl=state.explode?1:0,isolated=expGeometry.isolated;
 for(const l of lipids){let p=proj(l.v);q.push({x:p.x,y:p.y,z:p.depth,r:l.r*p.s,c:l.c,alpha:.67})}
 for(const c of expGeometry.chains){
  const rotating=c.group==='ring'||c.group==='shaft';
  const part=c.group==='alpha'||c.group==='beta'?'head':c.group==='regulator'?'head':c.group;
  const highlighted=state.selected===part||(isolated&&isolated===c.id);
  let alpha=isolated?(isolated===c.id?1:.085):(state.selected&&state.selected!==part?.18:1);
  if(state.cut&&c.group==='alpha'&&['A','B'].includes(c.id))alpha*=.10;
  if(state.cut&&c.group==='beta'&&c.id==='E')alpha*=.16;
  const shift=c.group==='ring'?[0,-55*expl,0]:c.group==='shaft'?[0,-28*expl,0]:c.group==='stator'?[27*expl,0,-16*expl]:c.group==='channel'?[44*expl,0,18*expl]:c.group==='alpha'||c.group==='beta'?[30*expl,32*expl,0]:[0,0,0];
  const pts=c.points;
  const betaIndex=['E','F','D'].indexOf(c.id);
  const phase=angle+betaIndex*TAU/3;
  const betaOpen=c.group==='beta'?(1+Math.cos(phase+1.15))/2:0;
  for(let i=0;i<pts.length;i+=3){
   let x=pts[i],y=pts[i+1],z=pts[i+2];
   if(rotating){const xx=x*Math.cos(angle)-z*Math.sin(angle);z=x*Math.sin(angle)+z*Math.cos(angle);x=xx}
   // Deliberately illustrative upper-domain deformation; original deposited state is unchanged.
   if(c.group==='beta'){
    const influence=Math.max(0,Math.min(1,(y-96)/85));
    const radial=Math.hypot(x,z)||1;
    x+=x/radial*betaOpen*7*influence;z+=z/radial*betaOpen*7*influence;y+=betaOpen*2.4*influence;
   }
   const p=proj([x+shift[0],y+shift[1],z+shift[2]]);
   if(p.x<-24||p.x>W+24||p.y<-24||p.y>H+24)continue;
   q.push({x:p.x,y:p.y,z:p.depth,r:3.35*p.s,c:c.color,alpha,sel:highlighted});
  }
 }
 q.sort((a,b)=>a.z-b.z);
 for(const p of q){
  const rr=clamp(p.r*1.68,2,11),s=sprite(p.c);
  ctx.globalAlpha=p.alpha;
  ctx.drawImage(s,p.x-rr,p.y-rr,rr*2,rr*2);
 }
 ctx.globalAlpha=1;
 if(expGeometry.ligands){
  for(const ligand of expData.ligands){const p=proj(pdbScene(...ligand.xyz));drawGlow(p.x,p.y,4.4,ligand.name==='ATP'?'#72eab4':'#62bce7',.82)}
 }
}
$('expReal').addEventListener('click',()=>{expGeometry.real=true;expGeometry.isolated='';$('expChain').value='';updateExperimentalControls();draw()});
$('expOld').addEventListener('click',()=>{expGeometry.real=false;expGeometry.isolated='';$('expChain').value='';updateExperimentalControls();draw()});
$('expChain').addEventListener('change',e=>{expGeometry.isolated=e.target.value;updateExperimentalControls();draw()});
$('expLigands').addEventListener('change',e=>{expGeometry.ligands=e.target.checked;draw()});
function updateExperimentalControls(){
 $('expReal').setAttribute('aria-pressed',String(expGeometry.real));$('expOld').setAttribute('aria-pressed',String(!expGeometry.real));
 $('expChain').disabled=!expGeometry.real;
 $('expLigands').disabled=!expGeometry.real;
 $('expBadge').textContent=expGeometry.real?'ATOM-DERIVED GEOMETRY · REPORTED 2.53 Å':'PROCEDURAL v0.6 TEACHING GEOMETRY';
 $('expStageTag').textContent=expGeometry.real?'PDB 8H9S · '+expData.chains.length+' PROTEIN CHAINS':'ILLUSTRATIVE v0.6 MODEL';
 const c=expData.chains.find(x=>x.id===expGeometry.isolated);
 $('expChainDesc').textContent=c?`Chain ${c.id}: ${c.name}. ${c.count} atom-derived display points. Other subunits dimmed.`:expGeometry.real?`${expData.render_point_count.toLocaleString()} atom-centred display points from ${expData.chains.length} deposited protein chains. Rotation and β-domain changes are illustrative.`:'Original organic illustration retained for direct comparison; not based on atomic coordinates.';
}
updateExperimentalControls();
'''
assert 'function render(){' in html
html=html.replace('function render(){',insert+'\nfunction render(){',1)
# On first frame, if any issue runtime will be tested with Chromium.
html=html.replace('window.addEventListener(\'resize\',()=>render());','window.addEventListener(\'resize\',()=>render());')
output=args.output
output.parent.mkdir(parents=True,exist_ok=True)
output.write_text(html)
print('wrote',output,output.stat().st_size)
