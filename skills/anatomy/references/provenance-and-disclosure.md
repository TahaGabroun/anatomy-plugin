# Scientific provenance and disclosure contract

Choose one or more **explicit, non-interchangeable** terms:

- **EXPERIMENTALLY_DERIVED**: observed deposited atom/backbone coordinates were actually loaded and transformed, with a source file hash retained.
- **DERIVED_MOLECULAR_SURFACE**: a documented atomic-surface construction algorithm ran on deposited atom coordinates (not merely a noisy cartoon).
- **STRUCTURE_INFORMED_SCHEMATIC**: topology or domain arrangement was informed by structural literature, but rendered geometry was not produced from experimental atomic coordinates.
- **PROCEDURAL_ANALOGY**: geometry is illustrative and not a reconstruction of the biological molecule.
- **EXPERIMENTAL_STATE_INTERPOLATION**: two or more structurally measured endpoints determine a *visual interpolation*; not a directly observed trajectory.
- **ILLUSTRATIVE_MOTION**: rotation/conformational trajectories are pedagogical reconstructions, not sampled experiment or molecular dynamics.

Independent evidence gates: **geometry provenance** and **motion provenance** must each be stated. A model may have experimental coordinates and wholly illustrative movement. A direct PDB link in a caption is insufficient to claim experimental-coordinate fidelity.

A generated artifact should include a source record (JSON or on-screen metadata) and the literature citation. Never bundle someone else's visualization/video without permission; preserve the original Anatomy MIT notice in redistributed kit/example files. External structure records are scientific data, but source notices and credits still matter.
