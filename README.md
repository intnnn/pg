# Sites Worker ESM starter

Use this starter for a static microsite, click counter, or simple internal UI whose state is browser-scoped. It has no dependencies and needs no install.

Edit `worker/index.js`, then publish through the Sites hosting workflow with this starter's build and validation in `commands`.

The build copies only `worker/index.js` and `.openai/hosting.json`. Do not add standalone asset files. Embed any essential raster bytes in `worker/index.js` and serve or reference them as a data URL.

Pass these argument arrays as `commands`:

```json
[
  ["bash", "scripts/build.sh"],
  ["node", "scripts/validate-artifact.mjs"]
]
```

The deterministic build produces:

```text
dist/
├── .openai/
│   └── hosting.json
└── server/
    └── index.js
```

`dist/server/index.js` is an ES module with a default export containing `fetch(request, env, ctx)`. Edit `worker/index.js`, not the generated file under `dist/`.
# pg

## Deploy to Netlify

This repository deploys to the Netlify project `cozy-moxie-cee10f`. The GitHub `main` branch is the production branch, and pushes to `main` trigger Netlify's production build automatically.

For website changes:

1. Edit `worker/index.js` and any relevant source files. Do not edit generated files in `dist/`.
2. Commit and push the changes to GitHub `main` (`https://github.com/intnnn/pg.git`).
3. Check the Netlify project's Deploys page for the build started by that push. Confirm it finishes in the `ready` state before sharing the site.

Netlify uses `netlify.toml` to run `bash scripts/build.sh && node scripts/build-netlify.mjs` and publish `dist/`. The first command builds the Worker module; the second renders the Worker response for `/` into `dist/index.html`. `netlify/edge-functions/prices.js` routes `/api/prices` to the existing Worker handler.

To reproduce the build locally, run:

```sh
bash scripts/build.sh && node scripts/build-netlify.mjs
```

The production site is currently restricted by the Netlify team's access settings (SSO). Keep that access configuration as-is unless Intan asks to change it. Never store GitHub or Netlify credentials in this repository.
