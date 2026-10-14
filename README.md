# Anatomy for ChatGPT and Codex — v0.9.0

## v0.9.0: professional scientific art direction + real volumetric cell data

**Release goal:** Every task, biological or mechanical, must meet independently reviewed professional scientific/technical illustration standards; no cartoon-looking organelle stand-ins, misleading PDB/EM geometry claims or dashboard-first substitutes. This is an enforceable design-review workflow, not an automatic guarantee of artistic quality.

- **New real-volume ingestion:** [`organelle_volume.py`](skills/anatomy/tools/organelle_volume.py) loads spatially calibrated labelled ZYX `.npy`, `.npz`, OME-TIFF/TIFF, MRC and Zarr (optional), exports 3D marching-cubes **GLB meshes** and portable sampled volume **JSON**. Labels, scale, axes, data SHA-256 and verification limitations are preserved. No real microscopy dataset is bundled.
- **New volumetric viewer:** [`Volume Atlas`](skills/anatomy/examples/volume-atlas/volume-atlas.html) renders labelled voxels via WebGL2 3D texture ray marching, orbit/cutaway/opacity controls; **calibrated orthogonal-slice fallback** works without WebGL. Its included demo dataset is **SYNTHETIC TEST-ONLY**, not an animal-cell reference. See [volume guidelines](skills/anatomy/references/organelle-geometry-and-volumes.md).
- **Hard art-direction gate:** Read [professional-art-direction.md](skills/anatomy/references/professional-art-direction.md) for specimen-first composition, refined lighting/materials/typography, required render reviews, mobile checks and design non-regression; failure in anatomy/construction/professional visual craft cannot be offset by passing code tests.
- **Benchmarks:** Retain approved ATP v0.6, experimental hybrid v0.8; archive a previous animal-cell illustration as **transitional schematic** (not accepted experimental/visual gold). Include new evaluation specifications, regression tests, and optional test dependencies.

**Quick start:**

```bash
python3 -m pip install -r skills/anatomy/tools/requirements-volume.txt
python3 skills/anatomy/tools/organelle_volume.py --input segmented.ome.tif --kind labels --output segment.volume.json --mesh-output segment.glb
```

Open the standalone Volume Atlas HTML and choose the generated JSON. For uncalibrated arrays, explicitly supply `--voxel-size-nm X Y Z`; never invent scale.

---

# Anatomy for ChatGPT and Codex — v0.8.0

An unofficial ChatGPT/Codex adaptation of [Ryan’s Anatomy](https://github.com/wheresryan22/anatomy), with the original MIT attribution preserved. Creates detailed interactive isometric illustrations of real mechanisms, including scientific cutaways and mechanism-led animations. It is **not** a diagnostic imaging system or clinical anatomy atlas.

## What changed in v0.8.0

**Real experimental coordinates now drive the biological view of ATP synthase.** The standalone [ATP synthase experimental hybrid](skills/anatomy/benchmarks/atp-synthase/v08/ATP_Synthase_Anatomy_Experimental_8H9S.html) is a self-contained HTML model, derived from a user-supplied human ATP synthase state-1 mmCIF assembly associated with PDB 8H9S. The file supplies 28 protein chains, 7,546 sampled heavy-atom-centred display points, and bound ATP/ADP positions. The molecular geometry **replaces** the earlier procedural protein model by default; an Illustrated switch allows direct comparison. Protein / Compare / Machine views, synchronized rotation, interactive separator, cutaway, exploded view, component inspection and mobile controls remain intact.

- **Reproducible builder:** `skills/anatomy/tools/build_atp_8h9s.py` extracts deposited heavy-atom coordinates and writes the portable HTML plus compact embedded coordinate JSON. Python dependencies: `gemmi numpy scipy`. The raw input is not checked into the repository.
- **Provenance caution:** The user-supplied mmCIF file has the expected title and chain composition but its internal entry ID is `XXXX`. Its identity was **not independently authenticated** against an official archive hash; the input SHA-256 is recorded. The reported 2.53 Å resolution is from the RCSB record.
- **Motion is illustrative:** c₈ ring and central stalk rotate as rigid units around the measured c-ring axis; small β-domain deformation, proton trajectories and ATP release timing are teaching animations, not observed trajectories or molecular dynamics. The displayed spheres are **atom-centred**, not a computed solvent-accessible surface.
- **Benchmarks preserved:** v0.6 remains byte-for-byte locked. v0.8 adds its own coordinate/provenance/interaction contracts. See [v0.8 integration guide](skills/anatomy/references/atp-8h9s-integration.md) and [v0.8 manifest](skills/anatomy/benchmarks/atp-synthase/v08/manifest.json).

## What changed in v0.7.0

- **Experimental-coordinate workflow implemented:** new `skills/anatomy/tools/structure_import.py` imports PDB files with Python's standard library and PDBx/mmCIF with optional `gemmi`, including direct wwPDB/PDBj assembly download on a network-connected computer. It exports real Cα/P backbone coordinates, chain identity, retrieval/source-file SHA-256, method and reported resolution when present. It does **not** fabricate coordinates on download failure.
- **Offline experimental backbone viewer:** `skills/anatomy/examples/structure-viewer/structure-viewer.html` renders an interactive 3D projection of imported coordinates, supports orbit, zoom and chain inspection, and explicitly distinguishes source-verified vs local/unverified files. A backbone viewer is *not* a solvent-accessible surface or a time-resolved molecular dynamics simulation.
- **Locked approved v0.6 ATP synthase benchmark:** `skills/anatomy/benchmarks/atp-synthase/v06/ATP_Synthase_Anatomy_v06.html` is byte-for-byte preserved with a pinned SHA-256; smoke checks confirm its unchanged source and core controls. The v0.6 model remains procedurally drawn and its animation remains illustrative, not retrospectively called atomistically grounded.
- **Evidence-aware instructions and regression cases:** new guides for experimental assemblies, structural provenance, motion claims and independent visual non-regression review. Automated checks verify contracts; human/browser review remains necessary for visual equivalence.

### Using human ATP synthase structure 8H9S

On a **network-connected machine**, install optional `gemmi`, download the author-defined biological assembly, and export backbone positions:

```sh
python3 -m pip install gemmi
python3 skills/anatomy/tools/structure_import.py --fetch-id 8H9S --assembly 1 --output atp-8h9s-backbone.json
```

Open `skills/anatomy/examples/structure-viewer/structure-viewer.html` in a browser and select that JSON. In v0.7 the 8H9S coordinates were **not bundled**; v0.8 now embeds derived display coordinates from a user-supplied assembly in the ATP example, while the original raw input remains separate. See [experimental structures](skills/anatomy/references/experimental-structures.md) and [source provenance](skills/anatomy/references/provenance-and-disclosure.md). Source record: [RCSB 8H9S](https://www.rcsb.org/structure/8H9S) and [PDBj assembly download](https://pdbj.org/mine/resources/8h9s).

## What changed in v0.6.0

- **Adaptive visual-model selection:** biological, engineered/mechanistic or synchronized hybrid according to the real subject and the requested explanation.
- **Organic molecular presentation:** support chain/domain surfaces, subunit-specific colours, biologically coupled conformation changes and source provenance instead of forcing all proteins into isometric metal-like solids.
- **Renderer-appropriate workflow:** use the original Anatomy kit for engineering and suitable molecular/3D rendering when biological surfaces require it. No upstream kit replacement.
- **New tests:** 16 semantic routing evaluation cases, five extended generation prompts, and executable checks that verify the routing spec is wired to the skill. These are *not* claimed to prove the model follows instructions.
- **Claude reference:** observations from the user-supplied ATP synthase video inform the biological/hybrid design language; the video is not redistributed, and its structure or motion is not assumed experimentally validated.

## What changed in v0.5.0 (retained)

- **Restored mechanism-first quality:** detailed, true-isometric assembly geometry, material treatment, shaded depth and meaningful contact interfaces are independent acceptance requirements, not optional decoration. Scientific clarity does not require shrinking the illustration into a dashboard.
- **Stored a user-preferred ATP synthase predecessor** in `skills/anatomy/examples/atp-synthase/atp-synthase.html` as a visual and exploration benchmark. Its source MIT notice remains intact. It is a *design* reference, not a validated atomistic or kinetic model.
- **Non-regression protocol:** compare the revised subject against an earlier working artifact at equivalent rendered scale/theme/pose, checking cutaways, exploded/subsystem views and visual quality separately from copy, numbers and interface polish. A worse physical model cannot be offset by more cards or explanatory text.
- **Expanded regression checks:** benchmark structure and expected interaction affordances are checked by `npm run smoke`. Browser interaction and scientific correctness still require their own verification.

## Earlier v0.4.0 improvements retained

- Gallery-benchmarked construction requirements: substantial objects, meaningful joinery and interiors, material ramps, perspective and real occlusion. Compare actual rendered results with suitable references; aesthetic confidence without evidence is not a pass.
- Explicit contracts for scientific accuracy, explanatory animation, causal continuity, visual inspection, accessibility, and honest verification reports.
- Added `references/accuracy.md`, `references/engineering.md`, `references/gallery-lessons.md`, `references/dynamic-animation.md`, `references/evaluation-rubric.md` and expanded `evals/evals.json`.
- Improved animal-cell sequence: repaired schematic RNA/protein stage opacity continuity and added `model.test.mjs` and `validate.mjs`; the cell's illustrative geometry remains **legacy schematic**, not an accurate anatomical template.
- Clearer ChatGPT runtime instructions and rendering-mode guidance; the upstream drawing kit and eight original examples are preserved.

## Installation

```sh
git clone https://github.com/TahaGabroun/anatomy-plugin.git
cd anatomy-plugin
codex plugin marketplace add .
```

The local marketplace registers an Anatomy plugin for compatible ChatGPT/Codex clients. The plugin still needs to be enabled in the client and may require restarting the client. Where supported, add the marketplace directly with `codex plugin marketplace add TahaGabroun/anatomy-plugin --ref main`. Installing from the distributed ZIP is equivalent. GitHub publication alone does **not** install or update a plugin in an existing ChatGPT session.

## Usage

Ask: “Use Anatomy to create an interactive isometric explanation of ATP synthase.” The skill should default to a **biological molecular representation** (and optionally a mechanism comparison, if it adds explanatory value) rather than defaulting to machined shapes. Other scenarios: a four-stroke engine, an animal cell with true compartment geometry, a differential gear, or a ripple tank.

Review `skills/anatomy/SKILL.md` first. It routes to the relevant subguides, which are not optional acceptance criteria when applicable. A complete figure needs actual visual inspection and mechanism checks, not just a successful build.

## Checks

Requires Node.js 20.10+ for the kit. Run:

```sh
npm run validate
npm run smoke
npm run package
```

`validate` checks version coherence, reference paths, asset presence and the SHA-256 manifest; `smoke` exercises the model tests, the locked v0.6 and coordinate-derived v0.8 ATP benchmarks, the structural parser tests and adaptive-mode evaluation fixture integrity (not a claim that an AI model passed those prompts). Additional browser-dependent tests are available in `skills/anatomy/scripts/`. They require a headless Chrome/Chromium environment that permits navigating local files.

## Layout

- `skills/anatomy/` — complete v0.8.0 skill, example source/output, v0.6 ATP benchmark, real-coordinate importer/viewer, kit, references, and tests.
- `plugin.json`, `.codex-plugin/plugin.json` — portable plugin and compatibility metadata.
- `.agents/plugins/marketplace.json` — local marketplace registry.
- `source-snapshot.json` — hashes of this distribution for integrity verification.
- `scripts/` — validation, test, packaging commands.

## Provenance and licensing

Origin: [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy), pinned upstream commit `240a9bf7c50cc6226148762a1017466fcbc08523` (2026-10-11). Original author Ryan (@wheresryan22). The kit and eight original samples are unchanged; the ChatGPT/Codex adaptation, biological example, and added guides/tests are downstream work. MIT licensed. See `LICENSE` and `skills/anatomy/references/upstream.md`.
