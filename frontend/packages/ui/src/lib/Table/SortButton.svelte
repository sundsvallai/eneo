<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import Button from "$lib/Button/Button.svelte";
  import type { Readable } from "svelte/store";

  export let props: Readable<{
    sort: {
      order: "desc" | "asc" | undefined;
      toggle: (event: Event) => void;
      clear: () => void;
      disabled: boolean;
    };
  }>;

  $: sort = $props.sort;
</script>

{#if !sort.disabled}
  <Button on:click={sort.toggle}>
    <slot />
    {#if sort.order === "desc"}
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="2"
        stroke="currentColor"
        class="h-4 w-4"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M4.5 10.5 12 3m0 0 7.5 7.5M12 3v18"
        />
      </svg>
    {:else if sort.order === "asc"}
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="2"
        stroke="currentColor"
        class="h-4 w-4"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M19.5 13.5 12 21m0 0-7.5-7.5M12 21V3"
        />
      </svg>
    {:else}
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="2"
        stroke="currentColor"
        class="h-4 w-4 text-transparent group-hover:text-black"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M3 7.5 7.5 3m0 0L12 7.5M7.5 3v13.5m13.5 0L16.5 21m0 0L12 16.5m4.5 4.5V7.5"
        />
      </svg>
    {/if}
  </Button>
{:else}
  <div class="min-w-28 px-2">
    <slot />
  </div>
{/if}
