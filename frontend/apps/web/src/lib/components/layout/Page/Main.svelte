<script lang="ts">
  import { getContentTabs } from "./ctx";

  let div: HTMLDivElement;

  const {
    states: { value, scrolled }
  } = getContentTabs();

  const scrollPositions: Record<string, number> = {};
  $: $value, loadPersistedScroll();

  function loadPersistedScroll() {
    const scrollY = scrollPositions[$value] ?? 0;

    if (div) {
      setTimeout(() => {
        div.scrollTo({
          top: scrollY,
          behavior: "instant"
        });
      }, 1);
    }
  }
</script>

<div
  bind:this={div}
  class="duration-400 relative flex flex-grow flex-col overflow-y-auto border-stone-200 pl-6 transition-colors"
  on:scroll={() => {
    $scrolled = div.scrollTop;
    scrollPositions[$value] = div.scrollTop;
  }}
>
  <slot />
</div>
