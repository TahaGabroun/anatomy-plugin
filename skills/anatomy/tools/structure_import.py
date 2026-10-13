#!/usr/bin/env python3
"""Anatomy: export provenance-traceable 3D backbone coordinates from experimental files.

PDB support uses Python stdlib; PDBx/mmCIF requires gemmi (`pip install gemmi`).
No structure/model is invented if fetching or parsing fails. Not a molecular
surface generator or molecular dynamics simulator.
"""
import argparse
import gzip
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from urllib.request import Request, urlopen

VERSION = 'anatomy-coordinate-scaffold/1.0'
PDB_ID = re.compile(r'^[0-9][A-Za-z0-9]{3}$')


def load_bytes(path):
    raw = Path(path).read_bytes()
    return (gzip.decompress(raw) if raw.startswith(b'\x1f\x8b') else raw), raw


def fetch_structure(pdb_id, assembly, timeout=30):
    if not PDB_ID.fullmatch(pdb_id):
        raise ValueError('PDB ID must be exactly four alphanumeric characters, starting with a digit')
    code = pdb_id.lower()
    if assembly:
        url = (f'https://data.pdbj.org/pub/pdb/data/assemblies/mmCIF/divided/'
               f'{code[1:3]}/{code}-assembly{assembly}.cif.gz')
    else:
        url = f'https://files.rcsb.org/download/{pdb_id.upper()}.cif.gz'
    req = Request(url, headers={'User-Agent': 'Anatomy-structure-import/1.0 (educational; https://github.com/TahaGabroun/anatomy-plugin)'})
    with urlopen(req, timeout=timeout) as res:
        content = res.read(90_000_001)
    if len(content) > 90_000_000:
        raise ValueError('Input exceeds 90MB safety limit')
    return content, url


def pdb_parse(content):
    """Return C-alpha protein or phosphate nucleic backbone coordinates."""
    chains, metadata, seen = {}, {'method': None, 'resolution_angstrom': None}, set()
    for line in content.decode('utf8', errors='replace').splitlines():
        if line.startswith('EXPDTA'):
            metadata['method'] = line[6:].strip()
        if line.startswith('REMARK   2 RESOLUTION.'):
            m = re.search(r'([0-9]+(?:\.[0-9]+)?)\s+ANGSTROMS', line)
            if m: metadata['resolution_angstrom'] = float(m.group(1))
        if not line.startswith(('ATOM  ', 'HETATM')) or len(line) < 54:
            continue
        name = line[12:16].strip()
        if name not in ('CA','P'): continue
        alt = line[16:17]
        if alt not in (' ', 'A', '1'): continue
        ch = line[21:22].strip() or '_'
        resid = line[22:27].strip()
        key = (ch,resid,name)
        if key in seen: continue
        try:
            xyz = [float(line[i:i+8]) for i in (30,38,46)]
        except ValueError:
            continue
        if not all(math.isfinite(x) for x in xyz): continue
        seen.add(key)
        chains.setdefault(ch, []).append({'xyz':xyz, 'residue':resid, 'atom':name, 'resname':line[17:20].strip()})
    return chains, metadata


def cif_parse(content):
    try:
        import gemmi
    except ImportError as exc:
        raise RuntimeError('PDBx/mmCIF requires gemmi: run `python -m pip install gemmi`') from exc
    text=content.decode('utf8')
    doc=gemmi.cif.read_string(text)
    block=doc.sole_block()
    structure=gemmi.make_structure_from_block(block)
    # The input must ALREADY be the intended biological assembly mmCIF.
    # Do not silently replace its coordinates with an asymmetric unit.
    metadata={'method':None,'resolution_angstrom':None}
    for k in ('_exptl.method',):
        v=block.find_value(k)
        if v and v not in ('.','?'): metadata['method']=v.strip('"\'')
    for k in ('_em_3d_reconstruction.resolution','_refine.ls_d_res_high'):
        v=block.find_value(k)
        try:
            if v and v not in ('?','.'):
                val=float(v)
                if val>0 and math.isfinite(val): metadata['resolution_angstrom']=val;break
        except (TypeError,ValueError): pass
    chains={}
    if not len(structure): return chains, metadata
    model=structure[0]
    for chain in model:
        key=chain.name or '_'
        for res in chain:
            for atom in res:
                if atom.name not in ('CA','P') or str(atom.altloc) not in ('\x00','A','1',' '): continue
                xyz=[float(atom.pos.x),float(atom.pos.y),float(atom.pos.z)]
                if not all(math.isfinite(x) for x in xyz): continue
                # Strictly prefer CA for proteins and P for nucleic acids, no duplicates.
                chains.setdefault(key,[]).append({'xyz':xyz,'residue':str(res.seqid),'atom':atom.name,'resname':res.name})
    return chains,metadata


def build_scaffold(chains, metadata, source_hash, pdb_id=None, source_url=None, assembly=None, max_points=1000):
    if not chains: raise ValueError('No usable CA/P backbone coordinates found; no model generated')
    out=[]
    for ch,points in sorted(chains.items()):
        if not points: continue
        # Uniformly sample while preserving original residue order and coordinates.
        if len(points)>max_points:
            ix=[round(i*(len(points)-1)/(max_points-1)) for i in range(max_points)]
            points=[points[j] for j in ix]
        out.append({'chain':ch,'backbone_atoms':len(points),'points':[{'r':p['residue'],'n':p['resname'],'a':p['atom'],'x':[round(x,3) for x in p['xyz']]} for p in points]})
    if not out: raise ValueError('No protein/nucleotide chains remain')
    return {
        'schema':VERSION,
        'kind':'coordinate-scaffold',
        'coordinate_status':'EXPERIMENTALLY_DERIVED' if source_url else 'UNVERIFIED_COORDINATE_SOURCE',
        'rendering_disclosure':'Backbone coordinates retained from source file. Origin is independently verifiable only when fetched from a wwPDB archive; stylized point/tube visualization, NOT a solvent-accessible molecular surface. Animation must not be represented as an experimental trajectory.',
        'source':{'pdb_id':pdb_id.upper() if pdb_id else None,'assembly':str(assembly) if assembly else 'INPUT_FILE_UNVERIFIED','url':source_url,'input_sha256':source_hash,'verified_wwpdb_retrieval':bool(source_url),'method':metadata.get('method'),'resolution_angstrom':metadata.get('resolution_angstrom')},
        'chains':out,
        'total_points':sum(len(c['points']) for c in out),
    }


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    group=ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--input', help='Local PDB/mmCIF file, optionally .gz')
    group.add_argument('--fetch-id', help='Download a PDB ID from a verified wwPDB distribution host')
    ap.add_argument('--assembly',type=int,default=None,help='Author biological assembly number (with --fetch-id; strongly recommended)')
    ap.add_argument('--pdb-id',help='Verified ID of local deposited structure, if known')
    ap.add_argument('--output',required=True, help='JSON file containing experimental backbone coordinates')
    ap.add_argument('--max-points-per-chain',type=int,default=1000)
    args=ap.parse_args(argv)
    if not 2<=args.max_points_per_chain<=10000: ap.error('max-points-per-chain must be 2..10000')
    if args.assembly is not None and not (1<=args.assembly<=20):ap.error('assembly must be 1..20')
    if args.assembly and args.input: ap.error('--assembly is only valid with --fetch-id; for local inputs supply an already assembled mmCIF file')
    if args.fetch_id:
        raw,url=fetch_structure(args.fetch_id,args.assembly)
        pdb_id=args.fetch_id
    else:
        if Path(args.input).stat().st_size>90_000_000: raise ValueError('Input exceeds 90MB safety limit')
        raw=Path(args.input).read_bytes();url=None;pdb_id=args.pdb_id
    data=gzip.decompress(raw) if raw.startswith(b'\x1f\x8b') else raw
    if data.lstrip()[:5].lower().startswith(b'data_'):
        chains,metadata=cif_parse(data)
    elif b'ATOM  ' in data[:100_000] or b'HEADER' in data[:1000]:
        chains,metadata=pdb_parse(data)
    else:raise ValueError('Unknown file format: expected PDB or PDBx/mmCIF')
    scaffold=build_scaffold(chains,metadata,hashlib.sha256(raw).hexdigest(),pdb_id,url,args.assembly,args.max_points_per_chain)
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(scaffold,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    print(f'Wrote {scaffold["total_points"]} observed backbone positions across {len(scaffold["chains"])} chains to {out}')
    if not args.assembly: print('WARNING: biological assembly not verified; input may be only the asymmetric unit.',file=sys.stderr)
    return 0

if __name__=='__main__':
    try: sys.exit(main())
    except (ValueError,RuntimeError,OSError) as e:
        print(f'Structure import failed: {e}',file=sys.stderr)
        sys.exit(1)
