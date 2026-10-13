import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parent))
from structure_import import pdb_parse,build_scaffold,fetch_structure


def atom(serial,name,res,ch,resid,x,y,z,alt=' '):
    return f'ATOM  {serial:5d} {name:<4s}{alt}{res:>3s} {ch}{resid:4d}    {x:8.3f}{y:8.3f}{z:8.3f}{1.0:6.2f}{20.0:6.2f}           C\n'


class StructureImportTests(unittest.TestCase):
    def setUp(self):
        self.pdb=('HEADER    SYNTHETIC TEST COORDINATES\n'
                  'EXPDTA    X-RAY DIFFRACTION\n'
                  'REMARK   2 RESOLUTION.    2.10 ANGSTROMS.\n'
                  +atom(1,'CA','ALA','A',1,1,2,3)
                  +atom(2,'CA','GLY','A',2,4,5,6)
                  +atom(3,'CA','ALA','A',2,99,99,99,'B')
                  +atom(4,'CA','SER','B',1,0,1,2)
                  +atom(5,'CA','GLY','B',2,2,3,4))

    def test_exact_coordinates_and_provenance(self):
        chains,meta=pdb_parse(self.pdb.encode())
        self.assertEqual(list(chains),['A','B'])
        self.assertEqual(len(chains['A']),2)
        self.assertEqual(chains['A'][1]['xyz'],[4.,5.,6.])
        self.assertEqual(meta['method'],'X-RAY DIFFRACTION')
        obj=build_scaffold(chains,meta,'0'*64,'8H9S',assembly=1)
        self.assertEqual(obj['total_points'],4)
        self.assertEqual(obj['chains'][0]['points'][0]['x'],[1.,2.,3.])
        self.assertEqual(obj['source']['assembly'],'1')
        self.assertEqual(obj['source']['input_sha256'],'0'*64)
        self.assertEqual(obj['source']['resolution_angstrom'],2.1)

    def test_download_url_pinned_to_assembly_archive(self):
        import unittest.mock as mock
        class Resp:
            def __enter__(self): return self
            def __exit__(self,*args): return False
            def read(self,*args): return b'data-test'
        with mock.patch('structure_import.urlopen',return_value=Resp()) as patched:
            data,url=fetch_structure('8H9S',1)
        self.assertEqual(data,b'data-test')
        self.assertEqual(url,'https://data.pdbj.org/pub/pdb/data/assemblies/mmCIF/divided/h9/8h9s-assembly1.cif.gz')
        self.assertTrue(patched.called)
        with self.assertRaises(ValueError):fetch_structure('../../../etc/passwd',1)

    def test_cli_writes_real_input_not_invented_geometry(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td)
            inp=td/'sample.pdb'
            out=td/'scaffold.json'
            inp.write_text(self.pdb)
            script=Path(__file__).with_name('structure_import.py')
            p=subprocess.run([sys.executable,str(script),'--input',str(inp),'--output',str(out)],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            obj=json.loads(out.read_text())
            self.assertEqual(obj['total_points'],4)
            self.assertEqual(obj['source']['assembly'],'INPUT_FILE_UNVERIFIED')
            self.assertIn('biological assembly not verified',p.stderr)
            self.assertEqual(obj['coordinate_status'],'UNVERIFIED_COORDINATE_SOURCE')

    def test_incomplete_input_does_not_write_output(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td)
            inp=td/'bad.pdb';out=td/'scaffold.json'
            inp.write_text('HEADER    EMPTY\n')
            script=Path(__file__).with_name('structure_import.py')
            p=subprocess.run([sys.executable,str(script),'--input',str(inp),'--output',str(out)],capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0)
            self.assertFalse(out.exists())

    def test_cif_optional_when_gemmi_available(self):
        try:import gemmi
        except ImportError: self.skipTest('gemmi not installed; mmCIF requires optional dependency')
        # Minimal PDBx/mmCIF block: coordinates are synthetic, not a PDB deposit.
        cif='''data_test
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_alt_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_entity_id
_atom_site.label_seq_id
_atom_site.pdbx_PDB_ins_code
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
_atom_site.occupancy
_atom_site.B_iso_or_equiv
_atom_site.pdbx_formal_charge
_atom_site.auth_seq_id
_atom_site.auth_comp_id
_atom_site.auth_asym_id
_atom_site.auth_atom_id
_atom_site.pdbx_PDB_model_num
ATOM 1 C CA . ALA A 1 1 ? 1 2 3 1.00 15 ? 1 ALA A CA 1
ATOM 2 C CA . GLY A 1 2 ? 4 5 6 1.00 16 ? 2 GLY A CA 1
#
'''
        from structure_import import cif_parse
        chains,_=cif_parse(cif.encode())
        self.assertEqual(len(chains['A']),2)
        self.assertEqual(chains['A'][1]['xyz'],[4.,5.,6.])


if __name__=='__main__':unittest.main()
