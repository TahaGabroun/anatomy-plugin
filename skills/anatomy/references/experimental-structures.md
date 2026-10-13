# Experimental structures: evidence-first Anatomy

Use when the user asks for an actual molecular assembly, atomic/backbone detail, or biologically plausible structural conformation. **The existence of a PDB entry alone does not mean the current illustration uses its coordinates.** This guide converts a documented biological representation into a reproducible geometry workflow.

## Evidence and coordinate acquisition

1. Choose an experimentally determined structure for the **correct organism, isoform, construct and state**. Check experimental method, resolution (where defined), missing residues and ligands. Distinguish an asymmetric unit from its author-/software-defined **biological assembly**. Prefer the assembly coordinate file when available.
2. Obtain its PDBx/mmCIF **from RCSB or a wwPDB partner**; preserve PDB ID, source URL, retrieved file SHA-256 and original citation. Never generate fictional PDB-like coordinates if the file cannot be obtained.
3. Export a backbone scaffold using `python3 skills/anatomy/tools/structure_import.py`. PDB requires only Python stdlib. **mmCIF requires `gemmi`** (`python3 -m pip install gemmi`). The exporter retains observed 3D Cα (protein) and P (nucleic-acid) positions, original residue sequence/order and author/source chain mapping in its output. It intentionally does *not* call its output an atomistic molecular surface.
4. Inspect in `skills/anatomy/examples/structure-viewer/structure-viewer.html` by loading the JSON locally. The viewer supports orbiting, chain selection and backbone representations; it does not have external dependencies and does not simulate chemical dynamics.
5. To generate a true solvent-accessible/solvent-excluded molecular surface, use a dedicated atomic geometry algorithm (e.g. MSMS or a validated viewer) and atom coordinates, not the backbone-only scaffold. For cryo-EM density views also use the **associated map**, and distinguish density from a fitted atomic model.
6. If no experimental structure is obtainable, keep a labelled **procedural/schematic** model. Do **not** mark it experimental merely because its topology was inspired by a PDB entry.

## Real human ATP synthase workflow

Primary record: **PDB 8H9S**, “Human ATP synthase state 1 (combined)”, Lai et al. (2023), *Molecular Cell*, DOI `10.1016/j.molcel.2023.04.029`; 2.53 Å cryo-electron-microscopy reconstruction. RCSB: https://www.rcsb.org/structure/8H9S. The author-defined assembly 1 is listed as a 28-chain biological assembly by PDBj: https://pdbj.org/mine/resources/8h9s.

On a network-connected machine:

```bash
python3 -m pip install gemmi
python3 skills/anatomy/tools/structure_import.py \
  --fetch-id 8H9S --assembly 1 \
  --output atp-8h9s-backbone.json
```

Then open `skills/anatomy/examples/structure-viewer/structure-viewer.html`, load `atp-8h9s-backbone.json`, and inspect each chain. If the network connection fails, download `8h9s-assembly1.cif.gz` through the PDBj resources page, then:

```bash
python3 skills/anatomy/tools/structure_import.py \
  --input 8h9s-assembly1.cif.gz --pdb-id 8H9S \
  --output atp-8h9s-backbone.json
```

For a local file the tool cannot independently establish the biological assembly identity and **must show “INPUT_FILE_UNVERIFIED”**; verify the downloaded filename/source and structure record before drawing assembly-level biological conclusions. `8H9S` experimental coordinates are **not shipped** with this plugin because the download was unavailable during release preparation. Source coordinates must be fetched or provided; the benchmarked v0.6 illustrative artwork does not silently become experimental.

## Motion: no invented structural trajectories

One state of a protein, even at high resolution, is not a time-resolved animation. If multiple experimentally determined conformational states are available, align an appropriate shared stationary frame, match residue numbering, separate rotor and stator units and quantify observed domain displacements. A smooth path between state endpoints is **interpolation**, never claimed as a measured trajectory. Annotate which parts are experimentally sourced and which motions, lipid backgrounds, proton tracks and energetic readouts remain conceptual.

For the F₀F₁ complex the α₃β₃ head, γ stalk, c ring, a-subunit and peripheral stator have distinct roles. The **8 H⁺/3 ATP per 360°** illustration is an idealized c₈ stoichiometry, not a verified mechanochemical stepping timeline. Check species-specific c-ring stoichiometry before reusing.

## Per-output provenance checklist

Every released structural figure records: `PDB ID | organism | assembly | model/state | method | resolution (when applicable) | coordinate retrieval URL | source file hash | missing chains/residues | render type (atoms, cartoon, backbone, calculated molecular surface, cryo-EM map, or procedural approximation) | motion provenance | licenses/citations`.

Fail if: coordinate claim without actual coordinate file; assembly claimed without verification; surface labelled “molecular surface” when only backbone points were rendered; time-resolved motion claimed from static structures; or coordinates mechanically distorted without noting schematic transformation.
