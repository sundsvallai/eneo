<script lang="ts">
  import { getContentTabs } from "./ctx";

  const {
    elements: { list }
  } = getContentTabs();
</script>

<div
  {...$list}
  use:list
  class="flex flex-grow items-center justify-start gap-2 pr-3"
  aria-label="Main views available for the current resource/site"
>
  <slot />
</div>
