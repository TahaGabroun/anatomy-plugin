# Professional scientific art direction — mandatory for every Anatomy task

**This is a release-blocking quality standard, not a promise of automatic equivalence to professional human work.** Match the compositional and illustrative craft of specialist scientific visual communicators, technical illustrators or product designers, while retaining scientific fidelity. Applied equally to BIOLOGICAL, MECHANISTIC and HYBRID work, all subjects and all form factors. Meeting documentation/tests alone cannot certify professional visual quality.

## Two independent layers

1. **Evidence model**: sourced geometry, real connectivity, labels, measurements, states, uncertainties and provenance. Retain raw coordinates/segments separately from art direction. Never stretch actual coordinates to fit an attractive layout without tracking the transform and scale distortion.
2. **Presentation model**: camera, cut plane, material, volumetric transfer functions, light/shadow, palette, visual hierarchy, annotations and paced state transitions. Artistic changes cannot invent organelles, repair unknown contact surfaces by guessing, or claim measured kinetics.

## Render-directed workflow, with actual blocking gates

1. Build a compact **reference board** for the same kind of specimen or engineered object. Establish relevant scientific references, *one* appropriate professional design benchmark, and the best working previous version if one exists. List what the reference does well: silhouette, geometry, texture, depth, labels, animation, light and styling.
2. Produce and inspect **two framing/cutaway options** for complex specimens before UI polish. Inspect at full screen and at **390 CSS px**. Start with the working subject dominating the visible frame, not decorative surrounding cards. Check legible internal structure and true occlusion.
3. Finish at least one **representative difficult component at full quality**: e.g. mitochondrion with actual membranes and credible internal folds; folded ER contacts; engine housing/bearing; protein subunit surface. Do not propagate simple polished ellipsoids as substitute for detail.
4. Choose disciplined palette and materials: semantically distinct components, tasteful saturation, local colour contrast, surface responses appropriate to tissue/protein/metal, lighting that reveals actual shape, and purposeful soft contact shadows. No default toy-gloss, neon outlines, decorative bloom, random noise, plastic spheres or iconised stacks.
5. Design structural labeling **outside the visual silhouette** wherever possible. Fewer anchored labels are better than arrows that obscure working interfaces. Typography: clear hierarchy, readable sizes, consistent alignment, contrast and breathing room. Controls should feel purpose-built and secondary to the specimen.
6. Test a useful mechanism and all view states (assembled, section, isolated, transition). Inspect real frame captures at representative timestamps, including mobile; explicitly test playback, pause, seek, disabled motion and mode switching when present.
7. Compare against saved previous working artwork at **equivalent image area, angle and theme**. Assign independent 0/1/2 scores to anatomical/engineering correctness, construction/detail, composition, materials, state animation, interaction and information clarity. **A 0 in science, construction, or professional visual craft is a fail even if interface or data tests pass.** Any material regression in an existing user-valued capability is blocking.
8. Repair the largest visually observable deficiency, re-render, and assess again. Use screenshot diffs and human/vision inspection; a file hash or DOM contract never proves design quality. If the renderer/device does not support high-quality volumetrics, disclose fallback and provide an equally thoughtful static illustration or orthoslice instead of presenting a crude toy as the finished professional figure.

## Typical disqualifying signs

- Conspicuously repeated primitives pretending to be complex biological surfaces; identical cylinders for membranes; flat slabs for Golgi; confetti-like organelles in a ball; unsupported 'microscopy realism'.
- Neon cell shells, arbitrary primary/rainbow palette, harsh uniform specularity, floating objects disconnected from compartments, impossible organelle proportions or membranes without thickness.
- Huge information panels squeezing the actual working picture into a thumbnail; decorative badges for each organelle; crowded labels touching or obscuring the model; illegible mobile rendering.
- Photorealistic lighting used to imply false measurement, static science claimed as actual dynamic trajectory, or synthetic fixtures labelled as experimental anatomy.
- Regression concealed by additional controls, high pixel count, attractive typography or persuasive write-up.

## Benchmarks and scope

- **Molecular hybrid:** locked v0.6 ATP synthase interaction benchmark plus coordinate-derived v0.8 source; inspect actual rendered comparison.
- **Animal cell:** `benchmarks/animal-cell/v09/Animal_Cell_Anatomy_Professional.html` is an archived **transitional schematic**, not an approved gold standard and *not* experimental geometry. Use to check whether clarity and anatomy descriptions were lost, not as permission to freeze its visual limitations.
- **Organelle:** `examples/volume-atlas` demonstrates real-mask ingestion, source fidelity and slice/volume control. The bundled fixture is synthetic and does not demonstrate expert cell illustration quality.
- **Engineering:** retain full construction detail, material hierarchy, precise cutaways and understandable motion from the original gallery benchmarks.

## Review record template

For every substantial output, record `domain`, `chosen mode`, `scientific sources and gaps`, `renderer/fallback`, `reference art`, `rendered overview screenshot`, `macro/detail screenshots`, `390px screenshot`, `actual interactions tested`, `scores [science, construction, composition, materials, motion, interaction, accessibility]`, `known limitations`, and `specific repairs`. Mark dimensions “NOT TESTED” rather than inventing favorable scores. Finalize only if all applicable hard gates pass; where constraints prevent it, explicitly identify the delivered work as a prototype or limited illustration.