> **v0.9 noncompensatory additions:** Score source/geometry authenticity and professional visual craft independently. Real cellular volume requires calibrated segmentation or explicitly disclosed reconstruction. A polished dashboard cannot compensate for crude organelle geometry; a beautiful invented model cannot compensate for fabricated measurement. Follow [professional art direction](professional-art-direction.md) and [volume evidence rules](organelle-geometry-and-volumes.md). Browser/WebGL rendering must be tested on an actual compatible runtime before claiming success.

# Evaluate outputs, not instruction wording

Use representative tasks in `../evals/evals.json`. For a before/after comparison, give both versions the same request, tools, model, budget, and source access in separate workspaces. Record those conditions. A model-name claim or a single successful artifact does not demonstrate general superiority.

Review saved artifacts and actual test evidence. Score each dimension 0 (fails), 1 (partial), or 2 (meets the request):

| Dimension | Evidence for 2 |
|---|---|
| Mode fit | Chooses BIOLOGICAL for real molecular/cellular subjects by default, MECHANISTIC for engineered/explicit analogies, HYBRID when both views are instructionally needed; cites/labels geometry and motion provenance |
| Accuracy | Traceable consequential claims, correct structural relationships, meaningful invariant and boundary checks |
| Clarity | Subject and causal relationship readable **from the working object before the sidebar**; assumptions are understandable |
| Craft | Working illustration is independently convincing at equivalent scale; faithful assembly, depth, interfaces, refined material shading, controlled semantic accents, and purposeful detail |
| Animation | Causal transitions, continuity or justified events, physically or biologically coupled state changes, moving assemblies and readouts, predictable pause/seek/reset |
| Access | Native controls or complete semantics, keyboard/touch, reduced-motion inspection, readable phone layout |
| Delivery | Requested artifact actually saved; dependencies/attribution included; fallback and verification limits reported honestly |

A materially wrong representation mode (for example, generic gearbox geometry presented as molecular protein anatomy), a wrong core mechanism, fabricated measurement/source, broken primary control, missing requested deliverable, **or material loss of craft/structural exploration compared with a supplied predecessor** is a blocking failure regardless of total score. Do not average these away. Report observed defects and evidence, not only a number. Mark an unexecuted check as unverified.

Select regression cases that challenge the change: **biological molecules with mechanical nicknames, explicit machine analogies for biology, mixed biological/engineered systems, ambiguous tasks, and changed user preferences**, then quantitative thresholds, a biological boundary, a coupled mechanism, rapid interruption, low frame rates, reduced motion, WebGL loss, and browser unavailability. Static diagrams do not require interactive checks; effects not used do not require shader checks. Preserve user-requested scope.

## Visual comparison protocol

Use a reference of similar subject complexity; compare subject crops at comparable displayed size and in a comparable theme and pose. A thumbnail beside a full-size hero is not a useful test. Score the working picture independently of the surrounding page. Inspect an overview, an interface detail, and a changed state or transition. Record concrete observations: a disconnected shaft, a uniform slab where the subject needs a cavity, a shader crossing a foreground rim, or a text panel dominating the figure. Separate observed defects from inferred causes.

“Uses the kit,” “has many paths,” “has a slider,” and “all tests pass” are not passing craft evidence. One correct moving dot over static station icons fails an actual process-mechanism request. A simple requested object can still pass through excellent construction, composition and meaningful motion; do not force a part quota.

## Do not trade away the mechanism for a nicer dashboard

For a user-supplied predecessor, perform a **separate working-art comparison**, excluding captions, sidebars, cards, and readouts. Record the previous version's strengths and proposed improvements before editing. Keep camera, theme, picture dimensions, and assembly pose comparable across screenshots. Evaluate **structure/depth, materials, occlusion, working interfaces, available investigative views, and motion** before assessing page design. A revision that has more labels or passes more data-validation checks but offers a noticeably flatter or less investigative object is a regression.

Use `atp-benchmark.md` and the archived ATP HTML as a case study for dense mechanisms. Its user-preferred visual quality does not establish scientific or physical accuracy. Do not transfer c₈ geometry to unrelated ATP synthases, or declare a general model ranking from this one preference.

Suggested noncompensatory acceptance gates for crafted explainers (score 0/1/2 independently): **domain accuracy; rendered object construction; physically meaningful interaction; exploratory views; accessible controls; deliverable integrity.** Zero on accuracy, construction, interaction, or requested deliverable blocks acceptance. A 2 on explanatory copy may not offset a 0 on construction. If improving a specific prior version, a significant fall in construction or exploratory views must be fixed or approved by the user. However, when the user asks for a more organic molecular depiction, retaining the earlier machine-like material treatment can itself be a blocking mode-fit defect. Compare interactions and causal invariants across modes; evaluate geometry against the **selected** mode's standard, not a legacy design language.

## Adaptive rendering protocol

1. Record the selected BIOLOGICAL / MECHANISTIC / HYBRID mode **before** construction, with one-sentence rationale and requested output constraints. Use `representation-routing.md`, not a rule such as “always use isometric grey machinery.”
2. Score **mode fit, organic/engineered construction, process motion, and pedagogical interaction separately**. For a biological protein: examine molecular surface complexity, stable chain colours, contact regions, membrane and substrate, conformational changes, and distinguish data-derived from illustrative geometry. For engineered assemblies: inspect real machined construction, contact precision, rigidity and constraints. For hybrids: both depictions must be aligned and share a single causally consistent model.
3. Compare the *same task* across attempts. If a previous version used an unsuitable representation, do not demand visual imitation. Preserve its useful features, but allow a fully different biological rendering style to improve fidelity.
4. Run the routing test prompts in `../evals/representation-routing.json` as **model evaluations**. The file and validation checks only verify coverage of prompts, not the model's judgment or visual result.
