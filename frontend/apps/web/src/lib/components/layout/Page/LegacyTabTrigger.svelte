<script lang="ts">
  import { browser } from "$app/environment";
  import { pushState } from "$app/navigation";
  import { page } from "$app/stores";
  import { getContentTabs } from "./ctx";
  import { Button } from "@intric/ui";

  export let tab: string;
  export let padding: "icon-leading" | "text" = "text";
  export let label: string | undefined = undefined;

  // Sidebar
  const {
    elements: { trigger },
    states: { value }
  } = getContentTabs();

  function updateUrl() {
    if (browser) {
      const url = $page.url;
      url.searchParams.set("tab", tab);
      pushState(url, { ...$page.state, tab });
    }
  }
</script>

<div
  class=" border-y-[0.25rem] border-transparent p-2 text-stone-500 hover:text-black"
  class:active={$value === tab}
>
  <Button is={[$trigger(tab)]} {padding} {label} on:click={updateUrl}>
    <span class={$value === tab ? "tracking-normal" : "tracking-[0.007rem]"}>
      <slot />
    </span>
  </Button>
</div>

<style lang="postcss">
  .active {
    @apply border-b-blue-600 font-medium !tracking-normal text-black;
  }
</style>
