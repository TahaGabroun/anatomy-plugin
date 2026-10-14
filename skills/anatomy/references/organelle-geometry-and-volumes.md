# Experimental organelle geometry and volumetric microscopy

**Required for cells, organelles, tissue ultrastructure and electron-microscopy-derived anatomy.** Read along with `biological-figures.md`, `professional-art-direction.md` and `provenance-and-disclosure.md`. A scientific source is not a substitute for a professionally finished figure; neither is attractive styling proof of scientific fidelity.

## Source hierarchy and specimen specificity

1. **Same-specimen paired imagery and segmentation** (e.g., FIB-SEM image stack with matched per-voxel ground-truth labels). Preserve acquisition modality, experimental specimen, anatomical context, scale, axes and segmentation provenance. Build the rendered geometry from those labels, *not* from a lookalike hand-drawn primitive.
2. **Registered experimental organelle segmentations** from a published collection: label them as being from *that specimen*. Do not paste those organelles into a synthetic generalised “animal cell” and label the assembled whole as one experimentally observed cell. If illustrative recomposition is useful, document per-organelle source, rescaling, placement and which transitions/contacts are inferred.
3. **Literature/micrograph-informed reconstruction** when no usable segmentation exists. Use characteristic topologies, compartment continuity, measured approximate ranges when published and clear structural boundaries; label as an evidence-informed reconstruction, not segmentation-derived.
4. **Schematic** only when data or resolution does not support something more. Present explicitly as simplified anatomy, not “high-fidelity ultrastructure.”

### Trusted example data portals (not bundled)

- [OpenOrganelle](https://openorganelle.janelia.org/): Janelia FIB-SEM volumes with available organelle segmentations (coverage differs by dataset).
- [CellMap segmentation challenge](https://github.com/janelia-cellmap/cellmap-segmentation-challenge): actual labelled EM crops distributed via the project's dataset tooling; [FAQ](https://github.com/janelia-cellmap/cellmap-segmentation-challenge/blob/main/FAQ.md) lists example per-organelle Zarr crop paths. Do not download terabyte-scale archives just to illustrate a single structure; select an approved bounded crop. Inspect dataset rights and attribution.
- [OME-TIFF specification](https://github.com/ome/ome-model-documentation/blob/main/ome-tiff/specification.rst): OME-XML stores axis and voxel-physical-size metadata. Do not treat unitless pixels as nanometres. For EM density maps, read the accompanying pixel scale and acknowledge reconstruction artifacts.

## Reproducible import (implemented)

Run from the repository root with Python `numpy`; TIFF/MRC/meshes additionally require `tifffile`, `mrcfile`, `scikit-image`, `trimesh` (see `tools/requirements-volume.txt`). Supported direct input: **ZYX `.npy`, `.npz`, TIFF/OME-TIFF, MRC, or 3D Zarr arrays.** Read-only importer. More complex OME channel/time series and multiscale Zarr group selection must be explicitly resolved upstream; do not guess their level or axes.

```sh
python3 -m pip install -r skills/anatomy/tools/requirements-volume.txt
python3 skills/anatomy/tools/organelle_volume.py \
  --input my_mitochondria_labels.ome.tif \
  --kind labels \
  --label-map my_labels.json \
  --source-url 'https://original.dataset/identifier' \
  --dataset-id 'dataset/crop/original' --provenance source-documented \
  --output mitochondria.volume.json \
  --mesh-output mitochondria.glb
```

OME or MRC calibration is read when present. For NPY or other uncalibrated arrays **`--voxel-size-nm X Y Z` is mandatory**. Axes are **array ZYX**, pixel scale is **physical XYZ in nm**. The program writes a compact downsampled unsigned-byte label volume for the interactive 3D raycaster and an optional physically scaled GLB mesh via marching cubes; original input is never replaced. Mesh surfaces are **segmentation isosurfaces**, not automatically biological membranes, bilayers, or confirmed inner cristae. Set `--max-axis` to bound WebGL memory (default 128) without affecting the optional full-resolution GLB (use `--mesh-step` for deliberate mesh subsampling). Record the distinct voxel sizes for both derivatives. Array labels must be unsigned 0–255, at most 32 nonzero classes, with 0 background. Larger instance IDs need a deliberate documented remap, never silent clipping.

Thresholds for unsegmented intensity stacks **must be explicit** (`--kind intensity --threshold VALUE`). Simple thresholding is not validated organelle segmentation and must not acquire a named organelle label without independent validation. The importer will not invent a morphology mask from a grayscale micrograph.

### Visual output

Open [`examples/volume-atlas/volume-atlas.html`](../examples/volume-atlas/volume-atlas.html) and load the exported `.volume.json`. The standalone viewer uses a WebGL2 integer 3D texture for volume rendering, 3D orbit, opacity, cutaway, zoom and labelled compartments. When WebGL2 is absent, it offers calibrated orthogonal slice inspection, not a fake 3D scene. The renderer uses discrete labelled masks, an illustrative transfer function and colour, **not experimental transmitted-light intensity or electron-density rendering**. A GLB file can be loaded into a 3D authoring workflow for higher-quality lighting and material work; this viewer does not currently import/display GLB or pair raw EM image channels with masks. GPU functionality depends on the host's WebGL2 availability.

`examples/volume-atlas/SYNTHETIC_DEMO.json` and the paired `.npy` are **synthetic test-only shapes**, intentionally not claimed as microscopy, organelles or reference morphology. Never use the synthetic fixture as a default animal-cell illustration.

## True volumetric scientific-art direction

- Preserve 3D compartment topology and relative scale when sharing a source coordinate space; trace whether the nuclear envelope and RER are *actually segmented as continuous*, otherwise annotate the conceptual connection rather than fabricating a join.
- Mitochondria: do not transform a low-resolution outer-body mask into asserted cristae geometry. Distinguish outer membrane segmentation and inner-membrane folds only if both resolved; use documented schematic cutaway otherwise.
- Golgi: actual stacks and cisternal lumina when segmented; never replace with rigid flat plates without identifying a simplification.
- Plasma membrane: render actual boundaries if visible or intentionally add a separate labelled reconstruction. An enclosing generic sphere is not evidence.
- Choose an expressive, non-generic view that reveals topology and provides a high-resolution organelle focus, not a cloud of coloured bubbles inside a translucent shell. Consistent reference space, crop, lighting, hierarchy, camera and organelle identity across views.
- For large volumes use tiled/multiscale workflows; **do not** load arbitrarily large files into a mobile browser. Crop and disclose the field of view. Simulated depth of field and roughness are artistic choices, never substitutes for physically registered geometry.

## Submission evidence

Log: dataset and exact crop, access date, original file SHA-256, channel/label definitions and segmentation provenance, image modality, calibrated voxel size and axis order, downsample factors, reconstructed surface algorithm, renderer, visual inspection screenshots and observed quality regressions. Report experimental/source-documented/unverified versus reconstructed layers **per layer**. Without those records, say 'schematic' or 'unverified local mask', not 'experimentally verified animal cell'.