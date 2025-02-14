<svelte:head>
  <meta name="mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <link rel="manifest" href="manifest.json" crossorigin="use-credentials" />
</svelte:head>

<div class="app-container fixed inset-0 flex justify-center bg-secondary">
  <slot />
</div>

<style>
  .app-container {
    container-type: size;
    padding-bottom: env(safe-area-inset-bottom, 0);
  }
</style>
