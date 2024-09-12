<!-- MIT License -->

<script lang="ts">
  import Button from "$lib/Button/Button.svelte";
  import { Tooltip } from "$lib/Tooltip/index.js";
  import type { ComponentType, SvelteComponent } from "svelte";

  export let customClass: string = "";
  export let tooltip: string = "";
  export let label: string;
  export let link: string | undefined = undefined;
  export let icon:
    | ComponentType<SvelteComponent<{ size?: "small" | "base" | "large"; class?: string }>>
    | undefined = undefined;
</script>

<Tooltip text={tooltip} placement="top" asFragment let:trigger>
  <div class="flex w-full items-center justify-start {customClass}">
    {#if link}
      <Button
        href={link}
        is={trigger}
        padding={icon ? "icon-leading" : undefined}
        class="{icon ? '-ml-1' : '-ml-2'} max-w-full"
      >
        {#if icon}
          <svelte:component
            this={icon}
            size="base"
            class="min-w-6 text-stone-400 group-hover:text-black"
          ></svelte:component>
        {/if}
        <span class="truncate overflow-ellipsis">
          {label}
        </span>
      </Button>
    {:else}
      {#if icon}
        <svelte:component this={icon} size="base" class="min-w-6"></svelte:component>
      {/if}
      <span class="truncate overflow-ellipsis" {...trigger[0]}>
        {label}
      </span>
    {/if}
  </div>
</Tooltip>
