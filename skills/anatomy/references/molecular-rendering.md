# Molecular rendering and conformation: practical implementation

Read after `representation-routing.md` when the selected mode is BIOLOGICAL or HYBRID at a molecular scale. This is a technical pathway, not a guarantee of atomistic reconstruction or a molecular dynamics simulator.

## Structural hierarchy (source-backed when possible)

1. **Set the organism, isoform and state.** A protein name is not a unique structure. In task notes record organism, construct, modifications, ligands, state, membrane orientation (if any), and experimental method. Do not transpose a bacterial ATP synthase c-ring count or subunit arrangement onto a mammalian complex.
2. **Choose a real assembly rather than a coincidental chain.** Prefer deposited biological assembly coordinates (PDBx/mmCIF; or supported local structures), inspect the assembly operators, chain/entity IDs, missing residues, ligands and alternate conformations. The asymmetric unit need not equal the biological assembly. Source: [RCSB on biological assemblies](https://pdb101.rcsb.org/learn/guide-to-understanding-pdb-data/biological-assemblies).
3. **Select a shape representation proportionate to evidence and device.** For actual atom coordinates: ribbons/tubes for secondary structure, chain envelopes, density-like blobs or molecular/solvent-accessible surfaces for the body; pockets and ligands as purpose-built visible details. Use a viewer/geometry implementation that can render chain-aware 3D data (for example Mol* when supported, or a licensed library), rather than tracing unrelated decorative outline paths. Source: [RCSB Mol* visualization](https://www2.rcsb.org/docs/exploring-a-3d-structure/structure-3d-visualization). Respect host constraints; an offline deliverable must bundle permitted resources instead of relying on hidden online services.
4. **If molecular coordinates are unavailable**, approximate an *organic physical assembly*: coherent lobed volumes, curved secondary-structure bundles, channels and interfaces placed in biologically credible positions, with low-amplitude, continuous structure-dependent texture and no random mesh cracks. Mark this as “schematic protein geometry—not derived from atomic coordinates.” The point is faithful biological language, **not** fabricated molecular precision.
5. **Build a multiresolution hierarchy:** overall assembly → named chains/subunits → functional domains → binding/interface focus → optionally residues/ligands when the data support them. Keep chain IDs and clickable selections stable through state changes. Use consistent spatial units/camera, purposeful cutaway clipping and true depth ordering. In dense complexes, selective transparency and molecular surface/ribbon modes can reveal buried structure better than an exploded collection of disconnected blobs.

### Organic appearance without false precision

- A protein is neither a polished metal part nor a collection of identical cylinders: irregular continuous surfaces, variable local curvature, asymmetrical lobes, internal pockets and coherent adjoining subunits should be visible. The amount of granularity depends on scale and source data; avoid noisy textures that conceal topology.
- Give each persistent subunit or functional domain a **consistent distinguishable material identity**. Broad saturated but controlled colours are appropriate when they help users track mobile proteins and interfaces. Balance local contrast against occlusion; show selection via outlines/highlight and provide labels or patterns, not colour alone.
- Membranes: show a recognizable bilayer at the appropriate scale and orientation, distinct hydrophilic heads and hydrophobic region when pedagogically relevant. A decorative, rigid pedestal does not represent a fluid membrane.
- Use meaningful contact patches, interfaces, openings and real occlusion. Keep moving bodies visually registered to their enclosing constraints and each other. For higher levels (cells, tissues), use membranes and volumetric continuity; do not mistakenly force atomistic surface rendering on an organoid.
- Treat rendering richness and data confidence as **orthogonal**. A detailed procedural shape does not become PDB-derived because it resembles cryo-EM art. A low-detail but accurately sourced ribbon is not a full surface model.

## Biological motion as coupled structural change

A molecular motor can rotate *and* deform. Plan motion as **source states → physical transformation → conformational consequences → biochemical event**. Use experimentally captured states or justified structural/kinematic assumptions where possible.

- If multiple deposited conformations exist, record PDB IDs and chain correspondence; align stable regions and map homologous atoms/residues before attempting interpolation. Deposited snapshots may be different conditions or complexes; they are **not** automatically chronological frames or measured kinetic trajectories. See [RCSB PDB-101 ATP synthase structures](https://pdb101.rcsb.org/motm/72).
- If conformational data are unavailable, animate **coarse-grained illustrative** domain movements: smooth hinge changes, pocket opening/closing, elastic bridging, modest structural deformation and binding/release events, while preserving continuity. Do not add unrelated Brownian jitter merely to make the protein look alive. Small secondary changes should be linked to mechanism or marked atmospheric/illustrative.
- Couple all domains to one parameter/state model. For ATP synthase, rotor/c-ring and central shaft share rotary state; stator and fixed head do not co-rotate. The catalytic subunits respond through phase-appropriate conformational changes. H⁺ half-channel entry/release, nucleotide occupancy, coloured tracking and counters follow the same event model; avoid simple continuous through-membrane tunnels or unsupported exact rates.
- At a boundary between two structural states, visually inspect local chain continuity, ligand identity, collisions, mesh intersections, occlusion, membrane traversal and step/seek/reverse behavior. When transitioning between conformations, prefer physically legible morphing over teleportation. A blend between states is **illustrative interpolation** unless a validated trajectory supports it.
- Offer pause, step, seek and reduced-motion resting states. Do not infer milliseconds, ATP/s or proton flux from a fixed demo playback duration.

## Hybrid comparison pattern

For a protein whose mechanical analogy is pedagogically useful, use an **aligned comparison**, not a false claim that the protein is machined. A registered slider or synchronized two-view display can expose:

- Left: biologically plausible, coloured molecular surface, relevant ligands and membrane.
- Right: explicitly labelled explanatory abstraction (rotor, stator, axle, catalytic cycle).
- Shared axes, camera framing, labels, selected subunit, input and time/angle; same play, pause, step, scrub and reset states.
- Revealing the abstract right panel may hide detail; it must not change the biological facts. Use smaller insets instead of a forced comparison if the user wants only the natural molecule.

## Evidence levels (must be disclosed in the artifact)

| Geometry label | What is supported |
| --- | --- |
| `Experimental coordinate-based` | Named structure/assembly with documented transformations; identify PDB entry and unresolved regions |
| `Experimentally informed illustration` | Sourced gross topology or conformer relationships, but surfaces or interpolation are approximated |
| `Schematic organic geometry` | Physically plausible explanatory volumes, **no claim of atomic structural reconstruction** |

Also label motion independently: `experimentally sampled conformers`, `model-derived`, or `illustrative interpolation`. Never advertise a molecular-dynamics simulation without implementing and validating one.

## Reference visual characteristics and limitations

A user-supplied October 2026 video of a **Claude-generated ATP synthase explanation** showed a detailed multicolour, irregular protein complex, a separately legible mechanical interpretation and a reveal/comparison interaction. The motion **appeared** to combine rotary movement with conformational changes. This is an *appearance and pedagogy reference*, not evidence of atomic-coordinate provenance, accurate kinetics, or scientific validity. **The video is not bundled or redistributed**. The existing `examples/atp-synthase/atp-synthase.html` is a strong prior *engineering-style and interaction* baseline, **not a ceiling for biological molecular appearance**. Don't let its largely neutral shading override appropriate organic surfaces and subunit-specific colour. Preserve its useful component inspection and cutaways when building a more biological version.
