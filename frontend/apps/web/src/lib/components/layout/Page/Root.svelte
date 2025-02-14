<script lang="ts">
  import { page } from "$app/stores";
  import { createContentTabs } from "./ctx";

  const {
    elements: { root },
    states: { value: tabState }
  } = createContentTabs($page.url.searchParams.get("tab") ?? undefined);

  export const selectedTab = tabState;

  function watchTabChange(pageStore: typeof $page) {
    // Only run if tabs have been initialised
    if (!tabState) return;
    const currentTab = pageStore.state.tab ?? pageStore.url.searchParams.get("tab");
    if (!currentTab) return;
    if (currentTab === $tabState) return;
    $tabState = currentTab;
  }

  $: watchTabChange($page);
</script>

<div {...$root} use:root class="flex flex-grow flex-col overflow-x-auto bg-primary" id="content">
  <slot />
</div>
