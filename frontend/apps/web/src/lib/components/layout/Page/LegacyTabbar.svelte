<script lang="ts">
  import { getContentTabs } from "./ctx";

  const {
    elements: { list }
  } = getContentTabs();
</script>

<div
  {...$list}
  use:list
  class="header-shadow ml-6 flex items-center justify-between gap-2 border-b-[0.5px] border-default pr-3"
  aria-label="Main views available for the current resource/site"
>
  <slot />
</div>

<style lang="postcss">
  .header-shadow {
    box-shadow: 2rem 0.75rem 4rem 0rem rgba(0, 0, 0, 0.03);
  }
</style>
