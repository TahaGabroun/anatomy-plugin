# Locked ATP synthase v0.6 benchmark

The user-approved ATP synthase hybrid implementation is pinned at [`../benchmarks/atp-synthase/v06/ATP_Synthase_Anatomy_v06.html`](../benchmarks/atp-synthase/v06/ATP_Synthase_Anatomy_v06.html). The source file is **byte-for-byte unchanged** from the v0.6 deliverable. SHA-256 is stored in its `manifest.json`; `npm run smoke` verifies it and a core feature contract. Do not overwrite this baseline as part of a release. Promote a new version only via an explicit separately named baseline and a documented side-by-side review.

## Acceptance criteria

Compare old and new artifacts at matching viewport/zoom, biological mode, compare mode and mechanical mode. Examine structural complexity, subunit-specific colour, coherent organic surface treatment, membrane geometry and actual model depth, not just UI chrome. Then test:

1. Protein / compare / machine modes; synchronized camera, rotor and catalytic states.
2. Drag orbit, reset camera, cutaway, separation, selection, proton overlay, play/pause, +45°, +120°, reset and timeline scrubbing.
3. Eight idealized proton transfers and three ATP outputs per full turn **in the illustrative kinetics mode**.
4. Reduced-motion support, keyboard focus, 390px mobile responsive layout and desktop layout.
5. Clear difference between experimental coordinate-derived geometry (if used) and **procedural/motion schematic**.

Visual quality and correctness are **non-compensatory**: better copy or brighter colour cannot excuse lost molecular detail, missing exploration controls, broken state coherence or unsupported scientific claims. Tests for source hashes and UI selectors are only a regression *contract*, not substitutes for screen-based tests. Render at least one overview, one separated/cutaway pose and one working state in every style before marking a model accepted. Browser tests require an available browser; if missing, report the gap.
