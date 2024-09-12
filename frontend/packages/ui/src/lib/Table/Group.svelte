<!-- MIT License -->

<script lang="ts" generics="T extends unknown">
  import Button from "$lib/Button/Button.svelte";

  import { derived, writable } from "svelte/store";
  import { Render, Subscribe } from "svelte-headless-table";
  import { getCardCell, getTableContext } from "./create.js";

  const tableContext = getTableContext<T>();
  const { viewModel, displayType, gapX, gapY, layout } = tableContext;
  const { rows, tableBodyAttrs } = viewModel;

  export let title: string | undefined | null = undefined;
  export let filterFn: (value: T) => boolean = () => true;

  const open = writable(true);
  // Original is not exposed on the type but present on the store...
  // Keep an eye on this in the future (here we just cast it)
  const filteredRows = derived(rows, (rows) =>
    rows.filter((row) => filterFn((row as unknown as { original: T }).original))
  );
</script>

{#if $filteredRows.length === 0}
  <div></div>
{:else if $displayType === "list"}
  <tbody {...$tableBodyAttrs}>
    {#if title}
      <tr>
        <td colspan="99" class=" !border-b-black/15 py-2 !pl-2.5">
          <Button
            on:click={() => ($open = !$open)}
            padding="icon-leading"
            class="py-2 font-mono font-medium"
          >
            <div class="flex w-full gap-2">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="{$open ? 'rotate-0' : '-rotate-90'} w-5 transition-all"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="m19.5 8.25-7.5 7.5-7.5-7.5"
                />
              </svg>
              <span>{title}</span>
            </div>
          </Button>
        </td>
      </tr>
    {/if}
    {#if $open}
      {#each $filteredRows as row (row.id)}
        <Subscribe rowAttrs={row.attrs()} let:rowAttrs>
          <tr {...rowAttrs}>
            {#each row.cells as cell (cell.id)}
              {#if cell.id !== "table-card-key"}
                <Subscribe attrs={cell.attrs()} let:attrs>
                  <td {...attrs} class={cell.id}>
                    {#if cell.id === "table-action-key"}
                      <div class="flex items-center justify-end">
                        <Render of={cell.render()} />
                      </div>
                    {:else}
                      <Render of={cell.render()} />
                    {/if}
                  </td>
                </Subscribe>
              {/if}
            {/each}
          </tr>
        </Subscribe>
      {/each}
      <div class="h-4"></div>
    {/if}
  </tbody>
{:else}
  {#if title}
    <div class="flex border-b !border-b-black/15 !pl-2.5 pb-2 pt-4">
      <Button
        on:click={() => ($open = !$open)}
        padding="icon-leading"
        class="py-2 font-mono font-medium"
      >
        <div class="flex w-full gap-2">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="{$open ? 'rotate-0' : '-rotate-90'} w-5 transition-all"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
          </svg>
          <span>{title}</span>
        </div>
      </Button>
    </div>
  {/if}
  {#if $open}
    <div
      style="column-gap: {gapX}rem; row-gap: {gapY}rem;"
      class:card-layout-flex={layout === "flex"}
      class:card-layout-grid={layout === "grid"}
      class="mt-3 pb-4 pl-0.5 pr-4 pt-2"
    >
      {#each $filteredRows as row (row.id)}
        {@const cell = getCardCell(row)}
        {#if cell}
          <Render of={cell.render()} />
        {/if}
      {/each}
    </div>
  {/if}
{/if}

<style lang="postcss">
  .card-layout-flex {
    @apply flex flex-wrap;
  }

  .card-layout-grid {
    @apply grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5;
  }

  .table-border {
    @apply overflow-clip rounded-xl border border-stone-400 bg-white shadow;
  }

  td {
    @apply w-[0%] whitespace-nowrap border-b border-black/5 px-4 pr-8  text-left font-normal first-of-type:pr-0 last-of-type:pr-4;
  }

  .th-padded {
    @apply h-14 w-[10%] border-b border-stone-300 px-2 text-left font-medium;
  }

  td.table-primary-key {
    @apply w-full max-w-[1px] overflow-hidden overflow-ellipsis whitespace-nowrap;
  }

  tbody tr {
    @apply h-16 hover:bg-stone-50;
  }
</style>
