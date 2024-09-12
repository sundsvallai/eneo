<script lang="ts">
  import { getContentTabs } from "./ctx";

  /// How far the user needs to scroll down before the header gets hidden
  const scrollDownThreshold = 300;
  /// How fat the user needs to scroll up befor the header will be shown again
  const scrollUpThreshold = 50;

  const {
    states: { scrolled, value }
  } = getContentTabs();

  let showHeader = true;
  let lastActiveTab = $value;
  let lastScroll = 0;
  function setHeaderVisibility() {
    if (lastActiveTab !== $value) {
      lastActiveTab = $value;
      lastScroll = $scrolled;
      if ($scrolled > 0) {
        return;
      }
    }

    if ($scrolled > lastScroll + scrollDownThreshold) {
      showHeader = false;
      lastScroll = $scrolled;
      return;
    }

    if ($scrolled < lastScroll - scrollUpThreshold || $scrolled < scrollDownThreshold) {
      showHeader = true;
      lastScroll = $scrolled;
      return;
    }
  }

  $: setHeaderVisibility(), $scrolled;
</script>

<div
  class="header-shadow header relative top-0 z-[60] ml-6 flex h-[4.25rem] min-h-[4.25rem] items-center justify-between border-b-[0.5px] border-black/15 bg-white/50 pr-4"
  data-show-header={showHeader}
>
  <slot />
</div>

<style lang="postcss">
  .header-shadow {
    box-shadow: 2rem 0.75rem 4rem 0rem rgba(0, 0, 0, 0.03);
  }
</style>
