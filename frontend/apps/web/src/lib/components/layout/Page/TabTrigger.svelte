<script lang="ts">
  import { browser } from "$app/environment";
  import { pushState } from "$app/navigation";
  import { page } from "$app/stores";
  import { getContentTabs } from "./ctx";
  import { Button } from "@intric/ui";

  export let tab: string;
  export let padding: "icon-leading" | "text" = "text";
  export let label: string | undefined = undefined;
  export let asFragment = false;

  const {
    elements: { trigger }
  } = getContentTabs();

  function updateUrl() {
    if (browser) {
      const url = $page.url;
      url.searchParams.set("tab", tab);
      pushState(url, { ...$page.state, tab });
    }
  }
</script>

{#if asFragment}
  <slot trigger={[$trigger(tab)]} />
{:else}
  <Button is={[$trigger(tab)]} {padding} {label} on:click={updateUrl} displayActiveState>
    <slot trigger={[$trigger(tab)]} />
  </Button>
{/if}
