<script lang="ts">
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import { createSidebar } from "./ctx";

  const {
    elements: { root },
    states: { value }
  } = createSidebar();

  onMount(() => {
    if ($page.url.searchParams.has("panel")) {
      $value = $page.url.searchParams.get("panel")!;
    }
  });

  export const selectedPanel = value;
  const { panelVisible } = value;
</script>

<div {...$root} use:root class="sidebar-wrapper flex" data-expanded={$panelVisible}>
  <slot />
</div>

<style>
  .sidebar-wrapper[data-expanded="true"] {
    box-shadow: -1px 50px 20px 0px rgba(190, 190, 190, 0.2);
  }
  .sidebar-wrapper[data-expanded="false"] {
    box-shadow: -1px 20px 20px 0px rgba(190, 190, 190, 0.05);
  }
</style>
