# ATP synthase benchmark: mechanism first, interface second

## Provenance and scope

A user supplied an **earlier interactive ATP synthase HTML** as the preferred outcome in a direct visual comparison against an Anatomy v0.4 reproduction on 2026-10-13. The self-contained example is archived at [`../examples/atp-synthase/atp-synthase.html`](../examples/atp-synthase/atp-synthase.html). Its original source notice, including Ryan's MIT attribution, is retained. This is a **user-selected design benchmark**, not an upstream Anatomy gallery sample, experimentally confirmed molecular reconstruction, atomic coordinate model, or validated kinetic simulator.

The observed earlier composition features a large, light-theme isometric molecular assembly (subunits, shaft, membrane and rotor) with precise four-tone shading, restrained line weight and small semantic accents. A compact inspector complements rather than displaces the mechanism. The controls include a **whole-complex view, F₀ motor view, F₁ head view, cutaway, part separation, named component inspection, three β-site states, cycle slider, play/pause, advance 120°, reset, gradient toggle, animation speed and readouts**. These features are explicitly visible in the supplied artifact; verify their behavior in a browser separately.

The v0.4 comparison, as reported in the project session, presented a less anatomically persuasive rotor/head and distributed information into additional panels. Extra polish, colours, cards, and readouts did not compensate for lower *mechanism fidelity and exploratory value*. No unblinded or independent human experiment established relative quality across other subjects or models.

## Scope update for adaptive biological rendering (v0.6)

This archived model is a **user-preferred v0.5-era engineering-style interpretation**, not the final organic rendering target. A later user-supplied Claude-produced ATP synthase video shows irregular colourful molecular surfaces and apparently coupled conformational changes, paired with a mechanically abstracted comparison view. These visual design observations are documented in [molecular rendering](molecular-rendering.md); the video is not included in the public package. Its structural and kinetic accuracy cannot be concluded from frames alone. **Preserve the archived HTML as a benchmark for exploration and non-regression of useful controls, but do not require its predominantly neutral four-tone protein shapes for a task seeking biological realism.** Follow [representation routing](representation-routing.md).

## How to use this benchmark

1. **Study the working illustration, not its page chrome.** Open the archived page, select its cutaway and subsystem views, look at the c-ring/membrane interface and the central shaft/stator relationship, then compare the same framing in your candidate. Inspect overview, a sectional pose and an active or stepped state. Review phone layout separately.
2. **Preserve form:** dense but distinguishable protein shapes, protein-to-protein assembly relationships, purposeful hairpin/subunit repetition, convincingly thick membrane sections, non-cartoonish texture, true depth ordering, bounded four-tone shading and consistent isometric projection. Preserve scientific recognizability without implying an atomic structure.
3. **Preserve investigation:** named pieces selected from the figure or inspector; genuine differences between overall, F₀, F₁ and cutaway states; an apart view that remains oriented and identifiable; three β-sites with distinct meaningful states. All views derive from one model snapshot, not disconnected illustrations.
4. **Keep colour semantic:** the archived specimen's neutral/subtle palette is appropriate to its engineering illustration style. In a **BIOLOGICAL** rendering, richer persistent colours for protein chains, subunits and domains may be essential for tracking molecular changes. A rich palette is not automatically decorative; a colour is useful when it tracks identity, structure or function. Honour a specifically requested monochrome theme with alternative encodings.
5. **Keep narration secondary:** the assembly should dominate the page and remain intelligible without the explanatory cards. Use a slender inspector and concise controls; avoid converting the explanation into cards with a small decorative picture.
6. **Retain correctness and accessibility:** a convincing illustration can still get proton channels, coupling, or catalytic states wrong. Cross-check real structure and quantitative assertions independently; clarify that a human mitochondrial c₈ ring gives an *idealized* 8 H⁺/3 ATP rotor ratio, not the cell's total effective H⁺/ATP cost. Ensure play/stop/restart and reduced motion, native controls, and phone inspection behave correctly.

## Mandatory visual regression comparison for improvements

When revising an interactive artifact, compare old/new in the same browser at matching subject crop, scale, theme, and representative state. Evaluate separately:

| Factor | Favor the revision only when | Typical v0.4 failure mode |
|---|---|---|
| 3D assembly & topology | Contacts, containment, thickness and spatial relationships remain at least as legible | Generic silhouettes or floating protein pods |
| Construction & shading | Curvature, edges, occlusion, facets and material treatment are at least as deliberate | Broad saturated blocks instead of fine four-tone surfaces |
| Explorability | Working sectional/focus/apart poses still expose the same interfaces | Selection swaps commentary while geometry stays static |
| Process coupling | Input physically propagates through the rotor, γ shaft and catalytic states with consistent counters | Independent showy motion or counters disconnected from model |
| Editorial hierarchy | Primary mechanism keeps comparable prominence and visual acreage | Giant control/dashboard blocks displace the molecular object |
| Scientific truth | Errors corrected without discarding a capability unless correction requires it | Attractive diagram that inaccurately represents mechanism |

**Regression disposition:** *improved*, *preserved*, *regressed* or *not verified* for each factor, with observed evidence. A candidate that clearly regresses the mechanism or available inspection modes is **not accepted** merely because it gains labels, scientific caveats, an additional card, or a cleaner toolbar. If the old sample contains an error, preserve the *craft goal*, not the incorrect fact. Do not demand molecular-level intricacy for intentionally simple figures or tasks that explicitly request a flat diagram.

## Acceptance example: ATP synthase

Require an identifiable mitochondrial membrane, distinct membrane-embedded c-ring and stationary half-channel structure, a γ shaft connected to the rotor, a peripheral stalk supporting a fixed α₃β₃ head, and three visually inspectable β pockets. Expose both assembled and cutaway/isolated modes; show 120° binding-change stepping and model-consistent readouts. The head remains stationary as rotor/shaft turn. The complex's intermembrane-side orientation and proton path must be unambiguous; the path is **two non-continuous half-channels**, never a straight transmembrane tunnel. If the user asks for another organism, c-ring stoichiometry must be changed or explicitly labelled illustrative rather than silently applying mammalian c₈ everywhere.

Do not assert that the bundled exemplar satisfies every criterion without testing; its inclusion documents what the user preferred visually, not a certified mechanism.


## Protected v0.6 hybrid benchmark (v0.7)

In addition to the older v0.5-era benchmark, the user-approved organic/hybrid ATP implementation is preserved byte-for-byte at `../benchmarks/atp-synthase/v06/ATP_Synthase_Anatomy_v06.html`. See [non-regression](benchmark-nonregression.md). **It remains a procedural representation**, not a deposited coordinate model. New experimentally grounded views should complement and improve it, never silently relabel the procedural baseline as atomic structure.
