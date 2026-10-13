# Anatomy for ChatGPT and Codex — v0.4.0

An unofficial ChatGPT/Codex adaptation of [Ryan’s Anatomy](https://github.com/wheresryan22/anatomy), with the original MIT attribution preserved. Creates detailed interactive isometric illustrations of real mechanisms, including scientific cutaways and mechanism-led animations. It is **not** a diagnostic imaging system or clinical anatomy atlas.

## Improvements in v0.4.0

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

Ask: “Use Anatomy to create an interactive isometric explanation of ATP synthase.” Other scenarios: a four-stroke engine, an animal cell with true compartment geometry, a differential gear, or a ripple tank.

Review `skills/anatomy/SKILL.md` first. It routes to the relevant subguides, which are not optional acceptance criteria when applicable. A complete figure needs actual visual inspection and mechanism checks, not just a successful build.

## Checks

Requires Node.js 20.10+ for the kit. Run:

```sh
npm run validate
npm run smoke
npm run package
```

`validate` checks version coherence, reference paths, asset presence and the SHA-256 manifest; `smoke` exercises the animal-cell model and source syntax. Additional browser-dependent tests are available in `skills/anatomy/scripts/`. They require a headless Chrome/Chromium environment that permits navigating local files.

## Layout

- `skills/anatomy/` — complete v0.4.0 skill, example source/output, kit, references, and tests.
- `plugin.json`, `.codex-plugin/plugin.json` — portable plugin and compatibility metadata.
- `.agents/plugins/marketplace.json` — local marketplace registry.
- `source-snapshot.json` — hashes of this distribution for integrity verification.
- `scripts/` — validation, test, packaging commands.

## Provenance and licensing

Origin: [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy), pinned upstream commit `240a9bf7c50cc6226148762a1017466fcbc08523` (2026-10-11). Original author Ryan (@wheresryan22). The kit and eight original samples are unchanged; the ChatGPT/Codex adaptation, biological example, and added guides/tests are downstream work. MIT licensed. See `LICENSE` and `skills/anatomy/references/upstream.md`.
