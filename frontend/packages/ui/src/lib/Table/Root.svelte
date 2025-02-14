<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts" generics="T extends unknown">
  import { IconList } from "@intric/icons/list";
  import { IconSquares } from "@intric/icons/squares";
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
  /** Use this option if the table is used within a clearly outlined area;
   * It will add symmetric padding to the filter bar and add a slight internal shadow
   */
  export let fitted = false;

  export let filter: boolean = true;
  export let viewModel: ResourceTableViewModel<T>;

  export let resourceName = "item";
  /**
   * Left padding of action column, in big tables this can be left as is.
   * If the table is in a thight place you can set this to tight to free up some space
   */
  export let actionPadding: "regular" | "tight" = "regular";

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
  <div class:fitted class="flex items-center justify-between gap-4 pb-1 pr-3 pt-3.5">
    {#if filter}
      <Input.Text
        bind:value={$filterValue}
        label="Filter"
        class="flex-grow"
        placeholder={`Filter ${resourceName}s...`}
        hiddenLabel={true}
        inputClass="!px-4"
      ></Input.Text>
    {/if}

    <div class="flex justify-stretch gap-1 rounded-xl">
      <Button
        on:click={() => {
          $displayType = "list";
        }}
        displayActiveState
        data-state={$displayType === "list" ? "active" : ""}
        padding="icon-leading"
      >
        <IconList />
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
          <IconSquares />
          Cards
        </Button>
      {/if}
    </div>
  </div>
  <div class="w-full">
    {#if $rows.length > 0}
      {#if $displayType === "list"}
        <table {...$tableAttrs} class="w-full">
          <thead class="bg-frosted-glass-primary sticky top-0 z-30">
            {#each $headerRows as headerRow (headerRow.id)}
              <Subscribe rowAttrs={headerRow.attrs()} let:rowAttrs>
                <tr {...rowAttrs}>
                  {#each headerRow.cells as cell (cell.id)}
                    {#if cell.id !== "table-card-key"}
                      <Subscribe attrs={cell.attrs()} let:attrs>
                        <th {...attrs} class={cell.id}>
                          <SortButton
                            props={cell.props()}
                            actionPadding={cell.id === "table-action-key"
                              ? actionPadding
                              : undefined}
                          >
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
        class="pointer-events-none absolute inset-0 flex min-h-[500px] items-center justify-center text-secondary"
      >
        <div class="flex flex-col items-center gap-2">
          {#if emptyIcon}
            <svelte:component this={emptyIcon} size="large" class="h-24 w-24"></svelte:component>
          {:else}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1"
              stroke="currentColor"
              class="h-24 w-24 opacity-20"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M3.75 9.776c.112-.017.227-.026.344-.026h15.812c.117 0 .232.009.344.026m-16.5 0a2.25 2.25 0 0 0-1.883 2.542l.857 6a2.25 2.25 0 0 0 2.227 1.932H19.05a2.25 2.25 0 0 0 2.227-1.932l.857-6a2.25 2.25 0 0 0-1.883-2.542m-16.5 0V6A2.25 2.25 0 0 1 6 3.75h3.879a1.5 1.5 0 0 1 1.06.44l2.122 2.12a1.5 1.5 0 0 0 1.06.44H18A2.25 2.25 0 0 1 20.25 9v.776"
              />
            </svg>
          {/if}
          {#if $filterValue === ""}
            {emptyMessage ?? `There are currently no ${resourceName}s configured`}
          {:else}
            Found no {resourceName}s matching your criteria
          {/if}
        </div>
      </div>
    {/if}
  </div>
</div>

<style lang="postcss">
  .fitted {
    @apply pl-3;
  }

  .table-border {
    @apply overflow-clip rounded-xl border border-default bg-primary shadow;
  }

  table {
    @apply w-full border-separate border-spacing-0;
  }

  th {
    @apply h-14 w-[10%] border-b border-default px-2 text-left font-medium;
  }

  th.table-action-key {
    @apply w-[1%];
  }
</style>
