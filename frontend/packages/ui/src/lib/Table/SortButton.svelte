<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import Button from "$lib/Button/Button.svelte";
  import { IconSortAsc } from "@intric/icons/sort-asc";
  import { IconSortAscDesc } from "@intric/icons/sort-asc-desc";
  import { IconSortDesc } from "@intric/icons/sort-desc";
  import type { Readable } from "svelte/store";

  export let props: Readable<{
    sort: {
      order: "desc" | "asc" | undefined;
      toggle: (event: Event) => void;
      clear: () => void;
      disabled: boolean;
    };
  }>;

  export let actionPadding: "regular" | "tight" | undefined = undefined;

  $: sort = $props.sort;
</script>

{#if !sort.disabled}
  <Button on:click={sort.toggle}>
    <slot />
    {#if sort.order === "desc"}
      <IconSortDesc size="sm" />
    {:else if sort.order === "asc"}
      <IconSortAsc size="sm" />
    {:else}
      <IconSortAscDesc size="sm" class="text-transparent group-hover:text-primary" />
    {/if}
  </Button>
{:else}
  <div class="min-w-12 px-2" class:pl-20={actionPadding === "regular"}>
    <slot />
  </div>
{/if}
