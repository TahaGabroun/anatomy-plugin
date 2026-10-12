# Anatomy for ChatGPT and Codex

Create detailed interactive isometric explanations through physical mechanisms: moving pistons, springs, rails, valves, dials, pipes, and other carefully drawn parts. The motion and live readouts share one model.

This is an unofficial plugin export of [Ryan's Anatomy](https://github.com/wheresryan22/anatomy), adapted for ChatGPT and Codex. The original MIT license and attribution are preserved.

## Included

- One reusable `anatomy` skill, with the full drawing kit and reference guides.
- Eight examples, including a dial indicator, desk computer, rocket engine, ripple tank, and turning dial.
- Geometry audits and portable browser verification helpers.
- A portable Agent Plugins manifest, a Codex compatibility manifest, and a repository marketplace.
- ChatGPT/Codex guidance for standalone HTML, SVG, in-chat previews, and React/Next.js output.

The package contains the reusable skill and its bundled examples. New user projects are created outside the installed skill directory.

## Install from a checkout or export

Clone this repository or extract the ZIP. From the `anatomy-plugin` directory, register its marketplace:

```sh
codex plugin marketplace add .
```

In the ChatGPT desktop app, restart the app, open the Plugins Directory, choose **Anatomy Plugins**, and install **Anatomy**. Start a new chat and select Anatomy. Local marketplace support depends on the host; this repository includes the format documented by OpenAI.

For a trusted Codex project, enable the marketplace plugin in the project's `.codex/config.toml` if needed:

```toml
[plugins."anatomy@anatomy-plugins"]
enabled = true
```

Register this repository directly as a Git-backed marketplace:

```sh
codex plugin marketplace add TahaGabroun/anatomy-plugin --ref main
```

The [official plugin packaging guide](https://developers.openai.com/plugins/build/plugins) explains local marketplaces and installation. A GitHub repository distributes the package; listing it in the universal public plugin directory requires a separate submission and review.

## Use

Select Anatomy and ask:

> Use Anatomy to create an interactive isometric explanation of the combustion engine.

Other examples:

- Explain a token bucket using a physical mechanism with live readouts.
- Create an interactive isometric explanation of a differential gear.
- Build a detailed cache-key explainer as a pin-tumbler lock.

The skill is intended for technical mechanism illustrations. Its name refers to explaining how things work; medical atlas and diagnostic tasks fall outside its scope.

## Requirements and checks

Use Node.js 20.10 or later for the framework-free drawing kit. Python 3 is needed only to produce the distribution ZIP. React integration uses the target project's existing React tooling. Browser verification also needs Chrome or Chromium; set `CHROME_PATH` when automatic discovery is insufficient.

No npm installation is needed for the package checks or drawing kit:

```sh
npm run validate
npm run smoke
npm run package
```

Validation checks manifests, local paths, license preservation, the source snapshot, and JavaScript syntax. The smoke check builds both themes of two examples in an isolated temporary directory, leaving the bundled resources unchanged. Packaging creates `anatomy-plugin-0.1.0.zip` next to the checkout.

These checks verify packaging and standalone builds. Actual pointer, keyboard, layout, reduced-motion, and WebGL behavior still require the browser checks described in the skill. An operating-system restriction may prevent headless Chrome from launching; report that limitation instead of claiming browser verification.

## Layout

| Path | Purpose |
| --- | --- |
| `plugin.json` | Portable plugin identity and OpenAI presentation metadata |
| `.codex-plugin/plugin.json` | Compatibility manifest for earlier Codex hosts |
| `.agents/plugins/marketplace.json` | Repository marketplace pointing to this package |
| `skills/anatomy/` | Complete adapted skill and drawing resources |
| `assets/icon.svg` | Plugin icon, copied from the installed skill |
| `source-snapshot.json` | SHA-256 hashes of the exported skill files |
| `scripts/` | Distribution validation, smoke builds, and ZIP packaging |

## Attribution and license

The original drawing kit, examples, guides, and tests are by **Ryan (@wheresryan22)**. The upstream snapshot is commit `240a9bf7c50cc6226148762a1017466fcbc08523`, dated 2026-10-11. This export retains the current ChatGPT/Codex adaptation, including runtime guidance and portable browser detection.

The plugin is distributed under the [MIT license](LICENSE). Preserve that notice when redistributing the kit or copied example code. Detailed provenance is in `skills/anatomy/references/upstream.md`.
