<script lang="ts">
  import { getContentTabs } from "./ctx";
  export let id: string;

  const {
    elements: { content }
  } = getContentTabs();
</script>

<div {...$content(id)} use:content class="relative min-h-full w-full">
  <slot />
</div>
