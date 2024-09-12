# @Intric/ui

Basic UI library based on Melt UI builders.

## Installing

```bash
# Install dependencies, usually all dependencies of the monorepo get installed at once,
# so if you already installed from the base directory you will probably not have to do this
pnpm install
```

## Developing

Library dev mode is started by

```bash
pnpm run dev
```

If you want to develop the actual SvelteKit app contained in this package, run instead:

```bash
pnpm run dev:app
```

## Tailwind / PostCss / Svelte-Preprocess

This package uses `svelte-preprocess` instead of SvelteKit´s standard `vitePreprocess`, which allows an easier way to inject global css into our components (needed for the hljs powered Markdown components).

This change means there is no postcss.config.js file present, but instead the postcss is directly configured inside svelte.config.css.
