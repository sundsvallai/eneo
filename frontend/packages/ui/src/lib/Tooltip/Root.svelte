<script lang="ts">
  import { createTooltip } from "@melt-ui/svelte";

  export let asFragment = false;
  export let text: string | undefined;
  export let placement: "left" | "bottom" | "top" = "top";
  /** Portal to display the tooltip, useful in case of overflows. A CSS selector */
  export let portal: string | null = null;

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
    disableHoverableContent: true,
    group: "sidebar"
  });
</script>

{#if !text}
  <slot />
{:else if asFragment}
  <slot trigger={[$trigger]} />

  <div {...$content} use:content class="z-[100] rounded-lg bg-stone-900 text-white">
    <p class="whitespace-pre-line px-4 py-1">{text}</p>
  </div>
{:else}
  <div {...$trigger} use:trigger>
    <slot trigger={[$trigger]} />

    <div {...$content} use:content class="z-[100] rounded-lg bg-stone-900 text-white">
      <p class="whitespace-pre-line px-4 py-1">{text}</p>
    </div>
  </div>
{/if}
