# ChatGPT and Codex runtime

## Load the resources

Use the skill's resolved local directory, not a hardcoded Claude path. If the skill is supplied through `skills.read`, use its returned `skill_root` when present. Otherwise locate the installed `anatomy/SKILL.md` in the skill workspace. Resolve `kit/`, `scripts/`, `references/`, and `examples/` relative to that directory. For a provider-backed reference, use its advertised read mechanism rather than treating a `skill://` URI as a filesystem path.

Read `craft.md` before designing and `kit.md` for API details. Read the closest example's build script, not every example at once. Load `webgl.md`, `3d.md`, or `react.md` only for the chosen output mode.

## Build outside the installed skill

Treat the installed skill as a read-only dependency. Copy the required `kit/`, `scripts/`, and `examples/<closest-example>/` into a task directory, retaining their relative layout. Write new models, build scripts, pages, and verification output there. Preserve `LICENSE` with copied code. Do not overwrite the bundled examples while building a user's figure.

Use the available `node`, or `CODEX_PRIMARY_RUNTIME_NODE` if Node is exposed through that runtime. Require Node 20.10 or newer. The kit and its browser checks use built-in modules; an API key, an AI SDK, and package installation are unnecessary. React output additionally needs the target project's React tooling.

For the first smoke check in the copied directory, run:

```sh
node examples/dial-indicator/build.mjs
node examples/dial-indicator/build.mjs --light
node scripts/capture.mjs examples/dial-indicator/dial-indicator-light.html --out shots/light.png
node scripts/capture.mjs examples/dial-indicator/dial-indicator.html --out shots/phone.png --width 390
```

Adapt the example's subject, model, title, hint, readout, caption, and accessibility text to the actual requested concept. Do not deliver an unchanged example as a newly created explanation. Drive the drawing and the numbers from one model, and state assumptions where a model is illustrative.

## Show and deliver the result

Choose the format the user requested. For a standalone interactive figure, default to one complete HTML page with inline SVG, styles, scripts, and any shaders; it should work without a framework or a CDN. For an existing project, integrate the figure with the project's established components and verify there.

For an in-chat interactive explanation, use the installed visualization skill if available and follow its current instructions. Use Sites when the user requests a website or hosting; use the appropriate preview skill when it supports the requested standalone artifact. Discover and read the actual capability before calling it. Do not invent a Claude Artifact tool, a preview directive, or a tool that is unavailable.

Create a static SVG or PNG when the requested medium cannot execute JavaScript, such as a document or presentation. Label a still preview as a still; its appearance alone does not prove the interactive behavior. Use the relevant document or presentation skill for those final artifacts.

Save requested user-facing files with the current file-saving workflow, including Library when available; repository-backed project changes follow the project's Git workflow. Keep disposable verification output in scratch. Provide clickable artifact links or the supported inline preview. Do not claim a file was saved, a site was published, or a skill was installed until its save step succeeds.

## Verify in an isolated browser

Use the bundled `capture.mjs`, `drive.mjs`, `lines.mjs`, and applicable geometry audits. They launch a separate headless browser with a temporary profile; they do not use a user's signed-in browser. The shared `browser-runtime.mjs` detects system Chrome/Chromium and standard Playwright caches across Linux, macOS, and Windows. `CHROME_PATH` can name another executable.

The helpers disable the Chrome sandbox only when running as root on Linux, where Chrome requires it for these isolated local checks. Normal-user launches retain the default Chrome sandbox. They also avoid depending on a large `/dev/shm` in Linux containers.

If no browser exists, check the runtime's installed browser tooling and use its supported provisioning path when available. Do not block an SVG build on missing preview tooling. Keep checks that can run locally, and report any browser behavior that remains unverified. Do not claim `audit passed` or `line ends: 0` without running the corresponding check.

If Chrome reports an operating-system permission error, including a blocked socket, preserve that failure and use the build and geometry checks that remain available. Do not treat an environmental failure as an illustration defect, weaken checks to hide it, or try to bypass the restriction. A non-browser SVG renderer can provide a static visual check when available; it cannot prove JavaScript, WebGL, or interaction behavior.

Check that a static renderer supports CSS custom properties. If it turns the art into black silhouettes, resolve the chosen theme's `--anatomy-*` properties in a disposable SVG render copy. Keep the original page and drawing kit unchanged, and identify the result as a static SVG check.

At minimum, check desktop and 390-pixel layouts, both themes, one real pointer interaction, keyboard operation, reduced motion, and clean browser output. Inspect every screenshot you generate with the available image-viewing tool. Add close-ups and all relevant audit checks described in `verify.md`; use WebGL-disabled checks for shaders and the orbit checks for moving 3D geometry. A failed check calls for a geometry or behavior fix, not a relaxed tolerance or an invented passing result.

Run long checks asynchronously so progress remains visible. Match claims to what was actually tested and preserve the original kit's limits, including the experimental status of its 3D mode.
