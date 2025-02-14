<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { Settings } from "$lib/components/layout";
  import { formatBytes } from "$lib/core/formatting/formatBytes";
  import { formatPercent } from "$lib/core/formatting/formatPercent";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";

  const {
    state: { currentSpace }
  } = getSpacesManager();

  function prepareData(
    categories: { label: string; colour: string; items: { metadata: { size: number } }[] }[]
  ) {
    let items: ((typeof categories)[number] & { size: number })[] = [];
    let total = 0;

    categories.forEach((category) => {
      const categorySize = category.items.reduce((total, item) => (total += item.metadata.size), 0);
      total += categorySize;
      items.push({
        ...category,
        size: categorySize
      });
    });

    return [items, total] as const;
  }

  // For the colours we're currently using names of css variables
  const [items, total] = prepareData([
    {
      label: "Collections",
      items: $currentSpace.knowledge.groups,
      colour: "chart-green"
    },
    {
      label: "Websites",
      items: $currentSpace.knowledge.websites,
      colour: "accent-default"
    }
  ]);
</script>

<Settings.Row
  title="Storage"
  description="See how much storage this space's knowledge is taking up."
>
  <div class="flex flex-col gap-4">
    <div class="flex h-4 w-full overflow-clip rounded-full bg-secondary lg:mt-2">
      {#each items.filter((item) => item.size > 0) as item}
        <div
          class="last-of-type:!border-none"
          style="width: {formatPercent(
            item.size / total
          )}; background: var(--{item.colour}); border-right: 3px solid var(--background-primary)"
        ></div>
      {/each}
    </div>
    <div class="flex flex-wrap gap-x-6">
      <div>
        <span class="font-medium">Total</span>: {formatBytes(total)}
      </div>
      {#each items as item}
        <div class="flex items-center gap-2">
          <div
            style="background: var(--{item.colour})"
            class="h-3 w-3 rounded-full border border-stronger"
          ></div>
          <p>
            <span class="font-medium">{item.label}</span>: {formatBytes(item.size)}
            <span class="pl-2 text-muted">({formatPercent(item.size / total, 1)})</span>
          </p>
        </div>
      {/each}
    </div>
  </div>
</Settings.Row>
