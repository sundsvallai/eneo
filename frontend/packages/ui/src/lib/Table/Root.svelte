<!-- MIT License -->

<script lang="ts" generics="T extends unknown">
  import { writable } from "svelte/store";
  import type { ComponentType, SvelteComponent } from "svelte";
  import { Button, Input } from "$lib/index.js";
  import { Subscribe, Render } from "svelte-headless-table";
  import { getCardCell, setTableContext, type ResourceTableViewModel } from "./create.js";
  import SortButton from "./SortButton.svelte";
  import Group from "./Group.svelte";

  export let displayAs: "cards" | "list" = "list";
  const displayType = writable<"cards" | "list">(displayAs);

  /** Vertical gap in `rem` in grid layout */
  export let gapX: string | number = "2";
  /** Horizontal gap in `rem` in grid layout */
  export let gapY: string | number = "2";
  export let layout: "flex" | "grid" = "flex";

  export let filter: boolean = true;
  export let viewModel: ResourceTableViewModel<T>;

  export let resourceName = "item";

  export let emptyMessage: string | undefined = undefined;
  export let emptyIcon:
    | ComponentType<SvelteComponent<{ size?: "small" | "base" | "large"; class?: string }>>
    | undefined = undefined;

  setTableContext({
    displayType,
    viewModel,
    gapX,
    gapY,
    layout
  });

  const { headerRows, rows, tableAttrs } = viewModel;
  const { filterValue } = viewModel.pluginStates.tableFilter;
  const showCardSwitch = getCardCell($rows[0]) !== undefined;
</script>

<div class="flex w-full flex-col">
  <div class="flex items-center justify-between gap-4 pb-1 pr-4 pt-3.5">
    {#if filter}
      <Input.Text
        bind:value={$filterValue}
        class="flex-grow"
        placeholder={`Filter ${resourceName}s...`}
        labelClass="hidden"
        inputClass="!px-4">Filter</Input.Text
      >
    {/if}

    <div class="flex gap-1 rounded-xl">
      <Button
        on:click={() => {
          $displayType = "list";
        }}
        displayActiveState
        data-state={$displayType === "list" ? "active" : ""}
        padding="icon-leading"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="h-6 w-6 min-w-6"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
          />
        </svg>
        List
      </Button>
      {#if showCardSwitch}
        <Button
          padding="icon-leading"
          on:click={() => {
            $displayType = "cards";
          }}
          displayActiveState
          data-state={$displayType === "cards" ? "active" : ""}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="h-6 w-6 min-w-6"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25A2.25 2.25 0 0 1 13.5 18v-2.25Z"
            />
          </svg>
          Cards
        </Button>
      {/if}
    </div>
  </div>
  <!-- <div class="rounded-bl-lg bg-blue-600 p-2 px-4 font-medium text-white">
    <p>2 rows selected</p>
  </div> -->
  <div class="w-full">
    {#if $rows.length > 0}
      {#if $displayType === "list"}
        <table {...$tableAttrs} class="w-full">
          <thead class="sticky top-0 z-30 bg-white/50 backdrop-blur">
            {#each $headerRows as headerRow (headerRow.id)}
              <Subscribe rowAttrs={headerRow.attrs()} let:rowAttrs>
                <tr {...rowAttrs}>
                  {#each headerRow.cells as cell (cell.id)}
                    {#if cell.id !== "table-card-key"}
                      <Subscribe attrs={cell.attrs()} let:attrs>
                        <th {...attrs} class={cell.id}>
                          <SortButton props={cell.props()}>
                            <Render of={cell.render()} />
                          </SortButton>
                        </th>
                      </Subscribe>
                    {/if}
                  {/each}
                </tr>
              </Subscribe>
            {/each}
          </thead>
          <slot>
            <Group />
          </slot>
          <!-- If there arent slots I want to show a div that says no slots -->
        </table>
      {:else}
        <slot>
          <Group />
        </slot>
        <!-- If there arent slots I want to show a div that says no slots -->
      {/if}
    {:else}
      <div
        class="pointer-events-none absolute inset-0 flex items-center justify-center text-stone-500"
      >
        <div class="flex flex-col items-center gap-2">
          {#if emptyIcon}
            <svelte:component this={emptyIcon} size="large" class="h-24 w-24 text-stone-200"
            ></svelte:component>
          {:else}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1"
              stroke="currentColor"
              class="h-24 w-24 text-stone-200"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M3.75 9.776c.112-.017.227-.026.344-.026h15.812c.117 0 .232.009.344.026m-16.5 0a2.25 2.25 0 0 0-1.883 2.542l.857 6a2.25 2.25 0 0 0 2.227 1.932H19.05a2.25 2.25 0 0 0 2.227-1.932l.857-6a2.25 2.25 0 0 0-1.883-2.542m-16.5 0V6A2.25 2.25 0 0 1 6 3.75h3.879a1.5 1.5 0 0 1 1.06.44l2.122 2.12a1.5 1.5 0 0 0 1.06.44H18A2.25 2.25 0 0 1 20.25 9v.776"
              />
            </svg>
          {/if}
          {#if $filterValue === ""}
            {emptyMessage ?? `You do not have any ${resourceName}s configured yet`}
          {:else}
            Found no {resourceName}s matching your criteria
          {/if}
        </div>
      </div>
    {/if}
  </div>
</div>

<style lang="postcss">
  .table-border {
    @apply overflow-clip rounded-xl border border-stone-400 bg-white shadow;
  }

  table {
    @apply w-full border-separate border-spacing-0;
  }

  th {
    @apply h-14 w-[10%] border-b border-stone-200 px-2 text-left font-medium;
  }

  th.table-action-key {
    @apply w-[1%];
  }
</style>
