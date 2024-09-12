<script lang="ts">
  import { parse } from "./marked.js";

  export let source: string;
  let cls: string = "";
  export { cls as class };

  let parsed: Promise<string>;
  $: parsed = parse(source);
</script>

{#await parsed then html}
  <div class="prose prose-stone prose-p:text-black text-lg {cls} overflow-x-auto break-words">
    <!-- eslint-disable-next-line svelte/no-at-html-tags -->
    {@html html}
  </div>
{/await}
