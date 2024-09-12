<script lang="ts">
  import { fade, scale } from "svelte/transition";
  import { getDialog } from "./ctx.js";
  import { cubicOut } from "svelte/easing";

  const {
    elements: { overlay, content, portalled },
    states: { open }
  } = getDialog();

  export let wide = false;
  /** Render Dialog into a form element, useful for input validation */
  export let form = false;
</script>

{#if $open}
  <div {...$portalled} use:portalled>
    <div
      {...$overlay}
      use:overlay
      class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm backdrop-saturate-[0.7]"
      in:fade={{ duration: 170, easing: cubicOut }}
      out:fade={{ duration: 230 }}
    ></div>
    <svelte:element
      this={form ? "form" : "div"}
      class="dialog-shadow fixed inset-0 z-[51] m-auto flex
         h-fit max-h-[85vh] max-w-[90vw] flex-col gap-2
           rounded-sm border-b-2 border-black/70 bg-stone-100 p-5 pt-4 lg:max-w-[350px]"
      class:wide
      {...$content}
      in:scale={{ start: 1.03, duration: 200, easing: cubicOut }}
      out:scale={{ start: 1.03, duration: 200 }}
      use:content
    >
      <slot />
    </svelte:element>
  </div>
{/if}

<style lang="postcss">
  .wide {
    @apply lg:!max-w-[50vw];
  }

  .dialog-shadow::before {
    content: "";
    @apply absolute inset-0 -z-10 rounded-sm mix-blend-multiply;
    box-shadow:
      0px 1px 5px 1px rgb(0, 0, 0, 0.2),
      0px 10px 20px 0px rgba(0, 0, 0, 0.1);
  }
</style>
