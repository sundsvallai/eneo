<script lang="ts">
  import { page } from "$app/stores";
  import { createContentTabs } from "./ctx";

  let initialValue: string | undefined;

  if ($page.url.searchParams.has("tab")) {
    initialValue = $page.url.searchParams.get("tab")!;
  }

  const {
    elements: { root },
    states: { value }
  } = createContentTabs(initialValue);

  export const selectedTab = value;

  // When the browser back button is clicked $page changes twice in rapid succession
  // This can trip us off, as the search params will go out of sync in the url bar and $page.url
  // For this reason we use a lock to only act on the first $page change
  let locked = false;
  function selectTab() {
    if (locked) return;
    if (value) {
      // Check if we have a change in the url params
      if ($page.url.searchParams.has("tab")) {
        const tab = $page.url.searchParams.get("tab")!;
        if (tab !== $value) {
          $value = tab;
          locked = true;
          setTimeout(() => {
            locked = false;
          }, 10);
          return;
        }
      }
      // Check if we have set a tab on the page state
      if (Object.hasOwn($page.state, "tab")) {
        const tab = ($page.state as { tab: string })["tab"];
        if (tab !== $value) {
          $value = tab;
          return;
        }
      }
    }
  }

  $: selectTab(), $page;
</script>

<div {...$root} use:root class="flex flex-grow flex-col overflow-x-auto bg-white" id="content">
  <slot />
</div>
