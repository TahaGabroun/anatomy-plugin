import json
from pathlib import Path
import tempfile
import unittest
import numpy as np

import organelle_volume as ov

class VolumeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/'synthetic.npy'
        z,y,x=np.ogrid[:32,:36,:40]
        mask=((x-20)**2/13**2+(y-18)**2/12**2+(z-16)**2/10**2)<1
        nested=((x-20)**2/7**2+(y-18)**2/6**2+(z-16)**2/5**2)<1
        v=np.zeros((32,36,40),dtype=np.uint8);v[mask]=1;v[nested]=2;np.save(self.path,v)
    def test_anisotropic_coordinates_and_hierarchy(self):
        full,disp,sp,dsp,ids,fmt,strides=ov.prepare(self.path,'labels',None,[4,5,9],None,None,24)
        self.assertEqual(ids,[1,2]);self.assertEqual(full.shape,(32,36,40));self.assertEqual(sp,(4,5,9))
        self.assertEqual(dsp,(4*strides[2],5*strides[1],9*strides[0]))
        self.assertLessEqual(max(disp.shape),24)
    def test_missing_scale_is_error(self):
        with self.assertRaisesRegex(ValueError,'Physical voxel size missing'):
            ov.prepare(self.path,'labels',None,None,None,None,64)
    def test_no_false_authentication(self):
        full,disp,sp,dsp,ids,fmt,strides=ov.prepare(self.path,'labels',None,[4,5,9],None,None,64)
        meta=ov.make_manifest(self.path,fmt,full.shape,sp,disp,dsp,ov.parse_map(None,ids),'unverified',None,None,'','labels',None,strides)
        self.assertEqual(meta['provenance']['status'],'USER_SUPPLIED_UNVERIFIED')
        self.assertFalse(meta['provenance']['independent_authentication'])
        with self.assertRaisesRegex(ValueError,'requires --source-url'):
            ov.make_manifest(self.path,fmt,full.shape,sp,disp,dsp,[],'source-documented',None,None,'','labels',None,strides)
    def test_threshold_explicit(self):
        with self.assertRaisesRegex(ValueError,'threshold required'):
            ov.prepare(self.path,'intensity',None,[4,5,9],None,None,64)
    def test_invalid_labels_rejected(self):
        np.save(self.path,np.full((4,4,4),500,dtype=np.uint16))
        with self.assertRaisesRegex(ValueError,'integers 0..255'):
            ov.prepare(self.path,'labels',None,[4,5,9],None,None,64)
    def test_mesh_export_glb_has_physical_extents(self):
        full,_,sp,_,ids,_,_=ov.prepare(self.path,'labels',None,[4,5,9],None,None,64)
        dest=Path(self.tmp.name)/'test.glb'
        out=ov.write_glb(full,sp,ov.parse_map(None,ids),dest)
        self.assertGreater(dest.stat().st_size,150)
        self.assertEqual(len(out),2)
        import trimesh
        scene=trimesh.load(dest,force='scene');bounds=scene.bounds
        self.assertGreater(bounds[1,2]-bounds[0,2],90)
    def test_ome_tiff_physical_size(self):
        import tifffile
        path=Path(self.tmp.name)/'em.ome.tif';a=np.zeros((5,8,9),dtype=np.uint8);a[1:4,2:6,2:6]=1
        tifffile.imwrite(path,a,ome=True,metadata={'axes':'ZYX','PhysicalSizeX':0.01,'PhysicalSizeY':0.02,'PhysicalSizeZ':0.03,'PhysicalSizeXUnit':'µm','PhysicalSizeYUnit':'µm','PhysicalSizeZUnit':'µm'})
        b,spacing,fmt=ov.read_volume(path)
        self.assertEqual(b.shape,a.shape)
        self.assertEqual(tuple(round(n,2) for n in spacing),(10.,20.,30.))
    def test_mrc_voxel_size_is_angstrom(self):
        import mrcfile
        path=Path(self.tmp.name)/'em.mrc';a=np.ones((7,8,9),dtype=np.uint8)
        with mrcfile.new(path,overwrite=True) as f:
            f.set_data(a);f.voxel_size=(14.,22.,35.)
        arr,sp,fmt=ov.read_volume(path)
        self.assertEqual(arr.shape,a.shape)
        self.assertTrue(np.allclose(sp,[1.4,2.2,3.5]))

if __name__=='__main__': unittest.main()