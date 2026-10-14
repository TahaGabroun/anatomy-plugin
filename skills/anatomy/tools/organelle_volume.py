#!/usr/bin/env python3
"""Anatomy: evidence-preserving organelle segmentation -> volumetric JSON + GLB.

The input is a REAL user-provided volume. No segmentation is inferred without
an explicit labelled mask or an explicitly specified intensity threshold.
Array axes are Z,Y,X; calibrated voxel sizes are provided as X,Y,Z in nm.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Any
import xml.etree.ElementTree as ET

import numpy as np

COLORS = ['#83b0b9','#d0a77e','#9483ad','#95a689','#b2a0a1','#bbb68b','#7b9ba3','#c2b1a0']
UNIT_NM = {'nm':1.,'µm':1000.,'um':1000.,'μm':1000.,'mm':1e6,'pm':0.001,'Å':0.1,'A':0.1}
MAX_VOXELS = 256**3


def source_sha(path:Path)->str:
    digest=hashlib.sha256()
    with path.open('rb') as fp:
        for b in iter(lambda:fp.read(1048576),b''):digest.update(b)
    return digest.hexdigest()


def ome_spacing_nm(tif):
    xml=tif.ome_metadata
    if not xml:return None
    root=ET.fromstring(xml)
    p=next((e for e in root.iter() if e.tag.rsplit('}',1)[-1]=='Pixels'),None)
    if p is None:return None
    vals=[]
    for ax in 'XYZ':
        size=p.get('PhysicalSize'+ax)
        if size is None:return None
        unit=p.get('PhysicalSize'+ax+'Unit','µm')
        if unit not in UNIT_NM:raise ValueError('Unsupported OME spatial unit '+unit)
        vals.append(float(size)*UNIT_NM[unit])
    return tuple(vals)


def read_volume(path:Path, key:str|None=None)->tuple[np.ndarray,tuple[float,float,float]|None,str]:
    p=path.name.lower()
    spacing=None
    if p.endswith('.npy'):
        data=np.load(path,allow_pickle=False)
        fmt='numpy-npy'
    elif p.endswith('.npz'):
        with np.load(path,allow_pickle=False) as archive:
            if not key:
                if len(archive.files)!=1:raise ValueError('NPZ contains multiple arrays; specify --array-key')
                key=archive.files[0]
            if key not in archive.files:raise ValueError(f'NPZ array {key!r} absent')
            data=archive[key]
        fmt='numpy-npz'
    elif p.endswith(('.tif','.tiff')):
        import tifffile
        with tifffile.TiffFile(path) as tif:
            if len(tif.series)!=1:raise ValueError('Multi-series TIFF requires preselection to a single series')
            series=tif.series[0];axes=series.axes;data=series.asarray()
            spacing=ome_spacing_nm(tif)
        # axes like ZYX or singleton T/C; reject non-singleton dimensions rather than silently discarding.
        for a in reversed(range(len(axes))):
            if axes[a] not in 'ZYX':
                if data.shape[a]!=1:raise ValueError(f'Unselected nonspatial dimension {axes[a]}={data.shape[a]}')
                data=np.take(data,0,axis=a);axes=axes[:a]+axes[a+1:]
        if set(axes)!=set('ZYX') or len(axes)!=3:raise ValueError('Expected a ZYX image stack, got '+axes)
        data=np.transpose(data,[axes.index(ax) for ax in 'ZYX'])
        fmt='ome-tiff' if spacing else 'tiff'
    elif p.endswith(('.mrc','.map','.mrc.gz')):
        import mrcfile
        with mrcfile.open(path,permissive=False) as mrc:
            data=np.array(mrc.data,copy=True)
            voxel=mrc.voxel_size
            if min(float(voxel.x),float(voxel.y),float(voxel.z))>0:
                spacing=tuple(float(v)*0.1 for v in (voxel.x,voxel.y,voxel.z)) # Å->nm
        fmt='mrc'
    elif p.endswith(('.zarr','.n5')) or path.is_dir():
        try:import zarr
        except ImportError as ex:raise ValueError('Zarr import requires optional package zarr') from ex
        obj=zarr.open(str(path),mode='r')
        if key:
            data=np.asarray(obj[key])
        elif hasattr(obj,'shape'):
            data=np.asarray(obj)
        else:raise ValueError('For grouped zarr, specify --array-key to an exact 3D array')
        fmt='zarr'
    else:raise ValueError('Supported formats: .npy/.npz/.ome.tif/.tif/.mrc/.zarr')
    if data.ndim!=3:raise ValueError('Input must be an unambiguous Z,Y,X volume; found '+str(data.shape))
    if not all(d>=2 for d in data.shape):raise ValueError('Volume dimensions must be >= 2')
    if data.size>MAX_VOXELS:raise ValueError('Volume exceeds safe importer size; crop/resample first')
    if not np.issubdtype(data.dtype,np.number) or not np.isfinite(data).all():
        raise ValueError('Volume must contain finite numeric values only')
    return data,spacing,fmt


def ensure_spacing(xyz):
    if xyz is None:raise ValueError('Physical voxel size missing. Supply --voxel-size-nm X Y Z (never assume isotropic pixels).')
    result=tuple(float(x) for x in xyz)
    if len(result)!=3 or not all(math.isfinite(x) and x>0 for x in result):raise ValueError('Voxel sizes must be three finite positive nm values')
    return result


def parse_map(s:str|None,labels:list[int])->list[dict[str,Any]]:
    supplied=json.loads(Path(s).read_text()) if s else {}
    if not isinstance(supplied,dict):raise ValueError('Label-map must be an object keyed by label ID')
    entries=[]
    for ix,k in enumerate(labels):
        item=supplied.get(str(k),{})
        if isinstance(item,str):item={'name':item}
        if not isinstance(item,dict):raise ValueError('Invalid label map entry '+str(k))
        color=item.get('color',COLORS[ix%len(COLORS)])
        if not isinstance(color,str) or not __import__('re').fullmatch(r'#[0-9a-fA-F]{6}',color):raise ValueError('Invalid six-digit hex color')
        entries.append({'id':int(k),'name':str(item.get('name','Region '+str(k)))[:100],'color':color,'segmentation_method':str(item.get('method','not specified'))[:120]})
    return entries


def prepare(path,kind,threshold,voxel_size,array_key,label_map,downsample_limit):
    data,meta_spacing,fmt=read_volume(path,array_key)
    spacing=ensure_spacing(voxel_size if voxel_size is not None else meta_spacing)
    if kind=='labels':
        if not np.issubdtype(data.dtype,np.integer) or (data<0).any() or (data>255).any():
            raise ValueError('For labels use integers 0..255 (0 background); convert larger label IDs explicitly')
        full=data.astype(np.uint8,copy=False)
        ids=[int(x) for x in np.unique(full) if x!=0]
    else:
        if threshold is None:raise ValueError('--threshold required when --kind intensity (no automatic biology inference)')
        full=(data>=float(threshold)).astype(np.uint8)
        ids=[1] if full.any() else []
    if not ids:raise ValueError('No segmented non-background voxels')
    if len(ids)>32:raise ValueError('Maximum of 32 label classes for interactive viewer; merge or select classes')
    if downsample_limit<16 or downsample_limit>256:raise ValueError('--max-axis must be 16..256')
    strides=tuple(max(1,int(math.ceil(d/downsample_limit))) for d in full.shape)
    display=np.ascontiguousarray(full[::strides[0],::strides[1],::strides[2]])
    display_spacing=tuple(spacing[i]*strides[2-i] for i in range(3))
    return full,display,spacing,display_spacing,ids,fmt,strides


def make_manifest(path,fmt,shape,spacing,display,display_spacing,labels,provenance,source_url,dataset_id,notes,kind,threshold,strides):
    if provenance=='source-documented' and (not source_url or not dataset_id):
        raise ValueError('source-documented requires --source-url and --dataset-id; this still is not independent verification')
    return {
      'schema':'anatomy.volume.v1',
      'provenance':{
       'status':'USER_SUPPLIED_SOURCE_DOCUMENTED' if provenance=='source-documented' else 'USER_SUPPLIED_UNVERIFIED',
       'input_file':path.name,'sha256':source_sha(path),'source_url':source_url,'dataset_id':dataset_id,
       'notes':notes,'independent_authentication':False,
      },
      'volume':{'axis_order':'ZYX','shape_zyx':list(shape),'voxel_size_nm_xyz':list(spacing),
                'display_shape_zyx':list(display.shape),'display_voxel_size_nm_xyz':list(display_spacing),
                'display_stride_zyx':list(strides),'source_format':fmt,
                'kind':kind,'intensity_threshold':threshold if kind=='intensity' else None},
      'labels':labels,
    }


def write_glb(full,spacing,labels,path,step_size=1):
    try:from skimage.measure import marching_cubes
    except ImportError as ex:raise RuntimeError('Surface export requires scikit-image') from ex
    try:import trimesh
    except ImportError as ex:raise RuntimeError('Surface export requires trimesh') from ex
    components=[]
    for ent in labels:
        mask=(full==ent['id'])
        if not mask.any():continue
        # pad input to ensure enclosed boundary intersections behave correctly
        pad=np.pad(mask,1,constant_values=False)
        try:vertices,faces,_,_=marching_cubes(pad.astype(np.float32),level=0.5,spacing=(spacing[2],spacing[1],spacing[0]),step_size=step_size)
        except ValueError:continue
        vertices=vertices[:,[2,1,0]]-np.array([spacing[0],spacing[1],spacing[2]])
        # Reverse triangle winding to preserve normals when changing axes ZYX->XYZ
        faces=faces[:,[0,2,1]]
        if len(faces)>1500000:raise ValueError(f'Mesh for {ent["name"]} exceeds face cap; use --mesh-step')
        rgba=tuple(bytes.fromhex(ent['color'][1:]))+(255,)
        mesh=trimesh.Trimesh(vertices=vertices,faces=faces,process=False)
        mesh.visual.vertex_colors=rgba
        mesh.metadata['label_id']=ent['id'];mesh.metadata['source']='segmentation marching cubes'
        components.append((ent['name'],mesh))
    if not components:raise ValueError('No extractable surfaces')
    scene=trimesh.Scene()
    for idx,(name,mesh) in enumerate(components):scene.add_geometry(mesh,node_name=f'{idx:02d}-{name}')
    scene.export(str(path),file_type='glb')
    return [{'name':name,'faces':len(mesh.faces),'vertices':len(mesh.vertices)} for name,mesh in components]


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('--input',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path,help='Portable browser-viewer JSON with downsampled voxel labels')
    p.add_argument('--mesh-output',type=Path,help='Optional spatially calibrated GLB surface reconstruction')
    p.add_argument('--mesh-step',type=int,default=1)
    p.add_argument('--kind',choices=['labels','intensity'],default='labels')
    p.add_argument('--threshold',type=float)
    p.add_argument('--voxel-size-nm',type=float,nargs=3,metavar=('X','Y','Z'))
    p.add_argument('--array-key',help='Exact NPZ/Zarr array name')
    p.add_argument('--label-map',help='JSON mapping of numeric IDs to name, color, method')
    p.add_argument('--max-axis',type=int,default=128)
    p.add_argument('--provenance',choices=['unverified','source-documented'],default='unverified')
    p.add_argument('--source-url');p.add_argument('--dataset-id');p.add_argument('--notes',default='')
    args=p.parse_args(argv)
    if not args.input.exists():p.error('Input file/directory missing')
    full,display,spacing,ds,ids,fmt,strides=prepare(args.input,args.kind,args.threshold,args.voxel_size_nm,args.array_key,args.label_map,args.max_axis)
    labels=parse_map(args.label_map,ids)
    manifest=make_manifest(args.input,fmt,full.shape,spacing,display,ds,labels,args.provenance,args.source_url,args.dataset_id,args.notes,args.kind,args.threshold,strides)
    manifest['payload']={'encoding':'base64-uint8-zyx','data':base64.b64encode(display.tobytes(order='C')).decode('ascii')}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(manifest,separators=(',',':')),encoding='utf8')
    if args.mesh_output:
        if args.mesh_step<1 or args.mesh_step>12:p.error('--mesh-step must be 1..12')
        args.mesh_output.parent.mkdir(parents=True,exist_ok=True)
        meshes=write_glb(full,spacing,labels,args.mesh_output,args.mesh_step)
        manifest.pop('payload')
        manifest['meshes']=meshes
        args.mesh_output.with_suffix('.provenance.json').write_text(json.dumps(manifest,indent=2))
    print(f'Anatomy volume: {fmt}, {full.shape} ZYX, {spacing} nm XYZ, labels={ids}, view={display.shape}, sha256={manifest["provenance"]["sha256"]}')
    return 0

if __name__=='__main__':sys.exit(main())