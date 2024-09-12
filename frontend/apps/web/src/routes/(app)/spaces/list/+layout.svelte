<!-- MIT License -->

<script lang="ts">
  import { page } from "$app/stores";
  import Squares from "$lib/components/icons/Squares.svelte";
  import SpaceSelector from "$lib/features/spaces/components/SpaceSelector.svelte";

  $: section = $page.url.pathname.split("/")[3] ?? "list";
</script>

<svelte:head>
  <title>intric.ai – Spaces</title>
</svelte:head>

<div class="lightblue absolute inset-0 flex flex-grow justify-stretch">
  <div class="flex flex-col border-r-[0.5px] border-black/10 md:min-w-[17rem] md:max-w-[17rem]">
    <SpaceSelector showSelectPrompt={true}></SpaceSelector>
    <nav class="layout-menu flex flex-grow flex-col gap-0.5 py-3">
      <a href="/spaces/list" data-current={section === "list" ? "page" : undefined}>
        <Squares></Squares>
        <span>Your spaces</span>
      </a>
    </nav>
  </div>
  <slot />
  <div
    class="pointer-events-none absolute inset-0 -z-0 flex flex-grow shadow-xl md:left-[17rem]"
  ></div>
</div>

<style lang="postcss">
  .lightblue {
    --space-color: #104dd0;
    --space-color-light: #104dd022;
  }
</style>
