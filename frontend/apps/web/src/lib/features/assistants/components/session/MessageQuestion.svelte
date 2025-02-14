<script lang="ts">
  import { fade, fly } from "svelte/transition";

  export let contents: string;
  export let isAnimated: boolean;

  const flyIn = (node: HTMLElement) => fly(node, { duration: 700, y: 100 });
  const noAnimation = (node: HTMLElement) => fade(node, { duration: 0 });
  const appearTransition = isAnimated ? flyIn : noAnimation;
</script>

{#if contents}
  <div
    in:appearTransition|global
    class="prose max-w-full self-end break-words rounded-3xl rounded-br-none bg-secondary px-8 py-4 md:max-w-[75%]"
  >
    <span class="sr-only">Question:</span>
    <p class="m-0 whitespace-pre-wrap text-lg">
      {contents}
    </p>
  </div>
{/if}
