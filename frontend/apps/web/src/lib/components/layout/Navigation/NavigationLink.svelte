<script lang="ts">
  import type { Icon } from "@intric/icons";
  export let href: string;
  export let isActive: boolean;
  export let icon: Icon;
  export let label: string;
</script>

<a
  class="relative flex gap-4 bg-primary px-[1.45rem] py-2.5 tracking-[0.008rem] text-secondary hover:bg-hover-dimmer hover:font-medium hover:tracking-normal hover:text-primary"
  aria-current={isActive ? "page" : undefined}
  {href}
>
  {#if isActive}
    <div class="absolute bottom-0 left-0 top-0 w-[4px] rounded-r-full bg-dynamic-default"></div>
  {/if}
  <svelte:component this={icon} class="size-6" />
  <span>{label}</span>
  <slot />
</a>

<style lang="postcss">
  a[aria-current="page"] {
    @apply bg-hover-dimmer font-medium tracking-normal text-primary hover:bg-hover-default;
  }
</style>
