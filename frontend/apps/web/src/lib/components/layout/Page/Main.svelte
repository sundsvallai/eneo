<script lang="ts">
  import { getContentTabs } from "./ctx";

  let div: HTMLDivElement;

  const {
    states: { value }
  } = getContentTabs();

  const scrollPositions: Record<string, number> = {};
  function loadPersistedScroll(tabKey: string) {
    const scrollY = scrollPositions[tabKey] ?? 0;

    if (div) {
      setTimeout(() => {
        div.scrollTo({
          top: scrollY,
          behavior: "instant"
        });
      }, 1);
    }
  }

  $: loadPersistedScroll($value);
</script>

<div
  bind:this={div}
  style="container-type: size;"
  class="duration-400 relative flex flex-grow flex-col overflow-y-auto pl-6 text-primary transition-colors"
  on:scroll={() => {
    scrollPositions[$value] = div.scrollTop;
  }}
>
  <slot />
</div>
