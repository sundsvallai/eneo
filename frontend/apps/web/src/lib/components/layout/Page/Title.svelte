<script lang="ts">
  import { quadInOut } from "svelte/easing";
  import { fly } from "svelte/transition";

  export let parent: { title: string; href: string } | null = null;
</script>

<div class="grid flex-col transition-all">
  <div class="overflow-hidden pl-2 text-[1.4rem]">
    <div class="flex w-full items-baseline gap-2">
      {#if parent}
        <a
          href={parent.href}
          class="inline-block text-[1.4rem] tracking-[-0.01rem] text-[#77716DC2] hover:text-blue-600"
          >←&nbsp;{parent.title}</a
        >
        <div class=" text-[#77716DC2]">/</div>
      {/if}

      <h1
        in:fly|global={{ x: -5, duration: parent ? 300 : 0, easing: quadInOut, opacity: 0.3 }}
        class="inline-block items-center gap-2 truncate pr-4 text-[1.4rem] font-semibold leading-normal"
      >
        <slot />
      </h1>
    </div>
  </div>
</div>
