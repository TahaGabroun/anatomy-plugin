> **v0.9 required:** For organelles and cells, read [experimental organelle volumes](organelle-geometry-and-volumes.md) and [professional art direction](professional-art-direction.md). Use calibrated real masks when available; distinguish composited reconstructions from same-specimen geometry. A toy-like collection of organelle symbols is a failed finished deliverable.

# Biological and scientific structures

Read this when illustrating a cell, tissue mechanism, organelle, molecule, or other real scientific structure. Use `quality-bar.md` for the visual review. A biological figure depicts a biological physical specimen, not a metaphorical factory or a clinical atlas. For a molecular subject, **first choose BIOLOGICAL or HYBRID** using `representation-routing.md`, then apply `molecular-rendering.md` for molecular surfaces, assemblies, colour and conformation.

## Build the specimen, not the stand

- Start with the real enclosing form. Give a cell an irregular curved membrane and a continuous volume of cytoplasm, not a circular base plate or a flat floor.
- Place structures at varied depths in that volume. Show posterior structures behind anterior ones and cut the enclosure deliberately to reveal the teaching target.
- Use continuous rounded profiles for membrane-bound bodies. Flattened cisternae still have rounded ends and enclosed lumens; they are not shelves or metal slabs.
- Model only intentional cut surfaces. Give each exposed lumen a distinct inner surface and a continuous boundary. Do not add openings that could be mistaken for a normal feature.
- Preserve real occlusion and continuous surfaces. **Choose a suitable palette for the organism and explanatory goal**: molecular subunits often need distinct saturated yet controlled colours to track them through a conformational cycle; restrained engineered-metal shading is not a default biological style. Change geometry before adding gradients or effects.
- Use colour purposefully for stable biological identity (chains, domains, organelles), catalytic state and active ligands. Rich subunit-specific colour is useful when tracing motion and interfaces; avoid arbitrary decorative rainbow assignment, inconsistent state colours, or relying on colour alone.

Use a detailed overview and a focus pose for important internal structures. An organelle rendered three pixels wide is not a useful explanation of its internal membrane.

## Choose purposeful detail

For a typical nucleated animal cell, a useful parts inventory includes:

| Structure | Recognisable detail | Relationship to preserve |
| --- | --- | --- |
| Plasma membrane | Thin bilayer, embedded proteins, an intentional cut rim | A flexible boundary around cytoplasm, not a rigid wall |
| Nucleus | Double envelope, pore complexes, chromatin, nucleolus | Outer envelope continuous with ER; nuclear and cytoplasmic spaces distinct |
| Rough ER | Connected flattened cisternae with ribosomes on their cytosolic faces | Translation and entry into the ER lumen occur at a membrane interface |
| Smooth ER | Branching, interconnected tubules without attached ribosomes | Continuity with the ER network |
| Golgi | Curved, enclosed cisternae, distinguishable receiving and shipping faces | ER-derived cargo enters the cis side; sorting occurs at the trans network |
| Mitochondrion | Outer membrane, folded inner membrane, matrix | Cristae are continuous inner-membrane folds, not detached zigzag marks |
| Lysosome | Enclosed lumen and material being degraded | Degradation occurs inside a membrane-delimited acidic compartment |
| Peroxisome | Enclosed oxidative compartment | Do not depict it as a duplicate lysosome or invent a universal crystalline core |
| Ribosomes | Two-subunit form or appropriately scaled surface dots | Free and ER-bound ribosomes are the same translation machinery |
| Cytoskeleton | Microtubules, actin and intermediate-filament patterns as needed | Networks support shape and transport; a radial fan alone is not the entire cytoskeleton |

Select details that distinguish the subject and teach its function. Do not use fixed organelle counts, sizes, or positions as biological data. Explain simplifications and special-cell exceptions only when relevant.

## Animate transformations and boundaries

Before animating, write a state sequence and draw a representative still for each state. Drive the caption, structure emphasis, carrier shape, and material position from one model.

For production and secretion of a soluble protein:

1. Show transcription and RNA processing in the nucleus. Keep DNA in the nucleus.
2. Show processed mRNA crossing a nuclear pore. Do not draw a protein or a transport vesicle coming out of the nucleus in its place.
3. Show a ribosome translating the message. An ER-targeting signal in the nascent chain directs the complex to the rough ER; depict translation into its lumen.
4. Show a polypeptide becoming a folded cargo representation in the ER. Distinguish the transcript from the newly made protein.
5. Show an ER-derived carrier budding with cargo inside its lumen. Hide the cargo from the cytosol.
6. Show delivery to the cis Golgi and processing/sorting towards the trans side. State when a simplified model omits intermediate compartments or recycling traffic.
7. Show a secretory carrier dock at the plasma membrane.
8. Show fusion as a change in membrane continuity and release of soluble cargo to extracellular space.

Do not move one unchanged marker across these stages and call it a mechanistic explanation. Do not infer measured transport paths, durations, energy consumption, or particle counts from the teaching sequence.

## Scientific verification

Use authoritative, original scientific sources for unfamiliar or consequential claims. Keep source identifiers or URLs alongside the relevant model descriptions. Separate established structure/function from deliberate visual simplifications.

For mechanical figures, retain the original support, terminal, clearance, and depth audits. For biological geometry, use checks that describe the actual tissue/compartment model: intentional contacts and shared boundaries, interior containment, cut-surface continuity, layer order, and carrier cargo containment. Do not falsely pass an engineering audit using substitute shapes, and do not label an unrun audit as passed.

Inspect overview, focus poses, and representative process states at normal size and at 4×. Correct a scientifically misleading silhouette even when the numbers and code are valid.

## Limits of the bundled specimen

The animal-cell example illustrates a schematic presentation approach. Its model checks do not prove cargo containment, membrane continuity, accurate targeting, or phase-boundary continuity. Before reuse, inspect those properties separately. Never infer scientific validity from its inclusion in the skill. Record the sources and any omitted pathways for the actual requested subject using `accuracy.md`.

## Molecular assemblies: do not turn proteins into labelled cylinders

For molecular motors, preserve the assembly hierarchy: membrane-spanning elements, anchored interfaces, central rotating elements, peripheral stationary supports, and catalytic domains. Prefer structurally sourced organic surfaces where feasible; otherwise explicitly schematic, irregular continuous volumes that preserve known arrangement, coherent depth and real interface logic. Coupled conformational changes matter alongside shaft/rotor motion; do not accept simple rigid rotation as a complete organic model when binding-site changes are central. The archived `examples/atp-synthase/atp-synthase.html` demonstrates a user-preferred approach to cutaway and part inspection. Study its **craft** with `references/atp-benchmark.md`; validate all scientific structure and kinetics separately. A picture of three colored cylinders marked O/L/T can explain a *mechanical analogy* but does not substitute for a biological protein cutaway. The archived ATP benchmark preserves strong exploration interactions, **not a cap on molecular realism, colour, or movement**.

## Geometry before selectors

The supplied cell's static art was rendered and inspected during the gallery comparison. Its cytosol is represented by a broad horizontal cut-plane path; many organelles are shallow extrusions above it. This reads as objects on a tray despite the rounded lower shell. A large menu and more descriptions cannot repair that geometry.

For a new figure, establish the specimen volume and a deliberate sectional opening first. Render organelles at meaningful varied depths, with rounded enclosing surfaces and real lumen interiors. Define each process interface in world coordinates and share those coordinates with both static and moving geometry. Reserve back/front layers or split moving pieces as needed; appending every process path after all organelles puts cargo in front of structures it should pass behind.

For budding or fusion, show the boundary itself opening, joining or separating as justified by the subject; a circle growing next to an unchanged surface is only a symbol. If using a schematic symbol, label it and do not describe the topology as physically modelled. Inspect the action at its interface in a useful detail view before building the remaining stages. More stage names do not create a more complete mechanism.
