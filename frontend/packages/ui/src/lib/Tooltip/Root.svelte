<script lang="ts">
  import { createTooltip } from "@melt-ui/svelte";

  export let asFragment = false;
  let cls = "";
  export { cls as class };
  export let text: string | undefined;
  export let placement: "left" | "bottom" | "top" | "right" = "top";
  /** Portal to display the tooltip, useful in case of overflows. A CSS selector */
  export let portal: string | null = "body";
  /** Will render the element as "inline", use this when showing tooltips inside text blocks. (e.g when rendering references) */
  export let renderInline = false;

  // Tootltip
  const {
    elements: { trigger, content }
  } = createTooltip({
    positioning: {
      placement,
      sameWidth: false
    },
    openDelay: 350,
    closeDelay: 0,
    closeOnPointerDown: true,
    forceVisible: false,
    portal,
    disableHoverableContent: true
  });
</script>

{#if !text}
  <slot />
{:else if asFragment}
  <slot trigger={[$trigger]} />

  <div
    {...$content}
    use:content
    class="z-[100] line-clamp-1 rounded-lg bg-overlay-stronger text-on-fill"
  >
    <p class="whitespace-pre-line px-4 py-1">{text}</p>
  </div>
{:else}
  <div {...$trigger} use:trigger class={cls} class:renderInline>
    <slot trigger={[$trigger]} />

    <div
      {...$content}
      use:content
      class="z-[100] line-clamp-1 rounded-lg bg-overlay-stronger text-on-fill"
    >
      <p class="whitespace-pre-line px-4 py-1">{text}</p>
    </div>
  </div>
{/if}

<style lang="postcss">
  .renderInline {
    @apply -mr-[0.2rem] ml-0.5 inline;
  }
</style>
