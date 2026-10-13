import subprocess,zipfile,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
version=__import__('json').loads((root/'package.json').read_text())['version']
name=f'anatomy-plugin-{version}.zip'
out=root.parent/name
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(root.rglob('*')):
  if p.is_file() and '.git' not in p.parts and 'node_modules' not in p.parts:
   z.write(p,arcname=p.relative_to(root))
print(out)
