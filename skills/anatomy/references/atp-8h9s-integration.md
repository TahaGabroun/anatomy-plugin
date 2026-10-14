# Human ATP synthase: experimental structure in the hybrid Anatomy scene (v0.8)

**Start here for ATP synthase requests.** This reference provides a working, self-contained example that uses coordinates from a user-supplied PDBx/mmCIF assembly, while retaining the approved v0.6 protein/machine interaction model. Do not confuse it with a time-resolved cryo-EM movie.

## Open the working model

`../benchmarks/atp-synthase/v08/ATP_Synthase_Anatomy_Experimental_8H9S.html` is a standalone, offline HTML file. Its default Protein view **replaces** v0.6's procedurally generated protein particles with points sampled from heavy-atom coordinates in the supplied structure. It is not an overlay. It preserves Compare (movable separator), Machine, orbit, timeline, pause/play, +45°/+120°, component isolation, separation, cutaway and proton controls. The `Illustrated` geometry button switches back to the exact v0.6-style organic model for visual comparison.

The scene embeds `8h9s-render-data.json` directly in the HTML; no network fetch is required. The source code that creates both is `../tools/build_atp_8h9s.py` (requires Python, `gemmi`, `numpy`, `scipy`). The author-approved v0.6 original remains separately SHA-256 locked at `../benchmarks/atp-synthase/v06/`.

## Coordinate identity and provenance

- Reference structure: [RCSB PDB 8H9S](https://www.rcsb.org/structure/8H9S), human ATP synthase state 1 (combined), cryo-EM, reported resolution 2.53 Å (Lai et al., *Molecular Cell*, 2023).
- Input: user-supplied `8h9s-assembly1.cif.gz`, SHA-256 `04a25a99eed85038da529bfe7c14504f574e5d73157a71e6877166fb83995d25`.
- The input has the expected human ATP synthase state-1 title and chain composition, but its `_entry.id` is **`XXXX`**, not `8H9S`. Treat the identity as **user-supplied/title-matched, not independently verified against the wwPDB archive**. This status is recorded in the embedded data and benchmark manifest. Do not claim that the source file's identity was cryptographically authenticated.
- 28 protein chains; 38,630 original heavy-atom coordinates from the protein components and 7,546 display points (all Cα atoms plus a reproducible subset of additional surface-proximal heavy atoms). Positions are quantized to 0.1 Å for compact offline rendering. Five bound nucleotide positions (3 ATP and 2 ADP) are shown separately, derived from deposited ligand coordinates.
- **Not a computed molecular surface.** The visible beads are shaded sprites centred on deposited atom coordinates, not a solvent-accessible surface, cryo-EM density map, or molecular-dynamics model.

## Chain → functional assembly mapping

| Assembly | Source author chain IDs | Visual behaviour |
|---|---|---|
| F₁ alpha | A, B, C | stationary |
| F₁ beta | E, F, D | stationary base coordinates; small illustrative upper-domain deformation |
| Central stalk | G (gamma), H (delta), I (epsilon) | rotates as a rigid group about the c-ring axis |
| F₀ c₈ rotor | 1, 2, 3, 4, 5, 6, 7, 8 | rotates as a rigid group |
| F₀ a-subunit | N | stationary |
| Peripheral/other stator | K, L, M, O, P, Q, R, S, T | stationary |
| ATPase inhibitor | J | stationary in this teaching depiction |

For the scene coordinate frame, the c-ring Cα mean XY position defines the rotation axis (source coordinates: approximately x=164.797 Å, y=181.948 Å). The deposited Z direction becomes the vertical scene axis. Uniform scaling preserves the source geometry's relative positions, but the displayed Å-to-screen-unit conversion is a visual scale, not a ruler.

## What the animation does and does not establish

The v0.6 machine comparison and all controls are retained. One timeline controls both representations. The c-ring and central stalk are rigidly rotated around the measured axis. β-subunit upper-domain displacement is a small **illustrative deformation** of the single experimental state, not an interpolation between measured conformers. Proton motion, bilayer geometry, release particles, ATP/H⁺ counters and energetic speed are pedagogical abstractions. The 8 H⁺ per 3 ATP per 360° counter represents an idealized c₈ stoichiometry, not a measured stepping trajectory.

## Reproduce from the original input

From the repository root, with the supplied input available:

```bash
python3 -m pip install gemmi numpy scipy
python3 skills/anatomy/tools/build_atp_8h9s.py \
  --input 8h9s-assembly1.cif.gz \
  --template skills/anatomy/benchmarks/atp-synthase/v06/ATP_Synthase_Anatomy_v06.html \
  --output skills/anatomy/benchmarks/atp-synthase/v08/ATP_Synthase_Anatomy_Experimental_8H9S.html \
  --data-output skills/anatomy/benchmarks/atp-synthase/v08/8h9s-render-data.json
```

Check `node --test skills/anatomy/benchmarks/atp-synthase/v08/experimental-benchmark.test.mjs` for pinned input/output hashes, chain mapping, coordinate embedding, v0.6 non-regression and control preservation. A browser interaction/visual check is still required for presentation quality; tests alone do not establish molecular correctness or performance on every device.

**Future improvement:** match additional experimentally resolved rotary states by chain/residue correspondence and a shared stationary frame, and replace the atom-centred sprites with a computed solvent-accessible surface mesh. Never claim either capability is already implemented.
