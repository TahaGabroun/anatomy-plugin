"""Create a reproducible plugin ZIP without checkout metadata or local output."""

from pathlib import Path
import json
import stat
import zipfile

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "plugin.json").read_text())
output = root.parent / f"anatomy-plugin-{manifest['version']}.zip"
excluded = {".git", "node_modules", "__pycache__", ".qa", "shots", "dist"}

with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for file in sorted(root.rglob("*")):
        relative = file.relative_to(root)
        if any(part in excluded for part in relative.parts):
            continue
        if file.is_symlink():
            raise ValueError(f"Refusing to package a symlink: {relative}")
        if not file.is_file():
            continue
        if file.name == ".DS_Store" or file.name.startswith(".env") or file.suffix in {".pyc", ".zip"}:
            continue
        info = zipfile.ZipInfo(f"anatomy-plugin/{relative.as_posix()}", date_time=(1980, 1, 1, 0, 0, 0))
        info.create_system = 3
        info.external_attr = (stat.S_IFREG | 0o644) << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, file.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

with zipfile.ZipFile(output) as archive:
    if archive.testzip() is not None:
        raise ValueError("ZIP integrity check failed")
    count = len(archive.infolist())

print(json.dumps({"archive": str(output), "files": count, "bytes": output.stat().st_size}))
