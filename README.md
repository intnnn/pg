# Public Gold advisor website

Primary site: [publicgold.intnnn.com](https://publicgold.intnnn.com/), published with GitHub Pages.

The same site is also hosted at [publicgoldintan.netlify.app](https://publicgoldintan.netlify.app/) on Netlify. GitHub Pages serves the static site; Netlify provides the live price endpoint through its Edge Function.

## Live price endpoint

The Netlify Edge Function at `netlify/edge-functions/prices.js` handles `/api/prices` as configured in `netlify.toml`, then delegates to the shared handler in `worker/index.js`. The handler reads the latest Public Gold price tables and returns them without caching.

When the site is opened at `publicgold.intnnn.com`, the browser requests `https://publicgoldintan.netlify.app/api/prices`. The endpoint returns CORS headers only for `https://publicgold.intnnn.com`. On the Netlify-hosted copy and the ChatGPT Site, the browser uses the same-origin `/api/prices` route.

Keep the Netlify production site public so visitors to the GitHub Pages site can read the endpoint. The endpoint is public and read-only; do not put secrets in the frontend or repository.

## Build and deployment

Pushes to GitHub `main` trigger both the GitHub Pages workflow and the Netlify production build:

- `.github/workflows/deploy-pages.yml` builds `dist/` and publishes it to GitHub Pages.
- `netlify.toml` runs `bash scripts/build.sh && node scripts/build-netlify.mjs` and publishes `dist/` on Netlify.

For site or price-endpoint changes, edit `worker/index.js` and other source files as needed. Do not edit generated files in `dist/`. Commit and push changes to [intnnn/pg](https://github.com/intnnn/pg), then confirm the GitHub Pages Actions run and Netlify production deploy both succeed.

To reproduce the Netlify build locally:

```sh
bash scripts/build.sh && node scripts/build-netlify.mjs
```

The ChatGPT Site is published separately from the same Worker source.
