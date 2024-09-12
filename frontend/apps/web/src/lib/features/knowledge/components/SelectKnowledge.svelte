<script lang="ts">
  import type { EmbeddingModel, GroupSparse, WebsiteSparse } from "@intric/intric-js";
  import { createCombobox } from "@melt-ui/svelte";
  import IconWeb from "$lib/components/icons/IconWeb.svelte";
  import IconCollections from "$lib/components/icons/IconCollections.svelte";
  import { derived } from "svelte/store";

  // ---------- Props
  /** The ids of the user selected collections. Pass in a value to pre-select or leave empty for none. */
  export let selectedCollections: { id: string }[] | null | undefined;
  /** The ids of the user selected websites. Pass in a value to pre-select or leave empty for none. */
  export let selectedWebsites: { id: string }[] | null | undefined;
  /** All collections available to choose from */
  export let collections: GroupSparse[];
  /** All websites available to choose from */
  export let websites: WebsiteSparse[];
  /** Pass in the models that are currently available in this space */
  export let availableEmbeddingModels: EmbeddingModel[];

  // ---------- Setup UI component
  const {
    elements: { menu, input, option },
    states: { open, inputValue, touchedInput, selected },
    helpers: { isSelected }
  } = createCombobox<GroupSparse | WebsiteSparse, true>({
    portal: null,
    multiple: true,
    positioning: {
      sameWidth: true,
      fitViewport: true
    }
  });

  // ---------- Setup
  const initiallySelectedCollections = selectedCollections?.flatMap((item) => item.id) ?? [];
  const initiallySelectedWebsites = selectedWebsites?.flatMap((item) => item.id) ?? [];
  const selectedItems = [
    ...collections.filter((collection) => initiallySelectedCollections.includes(collection.id)),
    ...websites.filter((website) => initiallySelectedWebsites.includes(website.id))
  ];
  // Set pre-selected resources if any
  $selected = selectedItems.flatMap((item) => {
    return { value: item, label: item.name };
  });

  // All the models found in the provided resources
  const usedEmbeddingModels = websites
    .map((website) => website.embedding_model)
    .concat(collections.map((collection) => collection.embedding_model))
    .filter((model, index, self) => index === self.findIndex((m) => m.id === model.id));
  // All the models found but not available
  const disabledEmbeddingModels = usedEmbeddingModels.filter((embedding_model) => {
    return !availableEmbeddingModels.find(
      (enabled_model) => enabled_model.id === embedding_model.id
    );
  });

  function isDisabledEmbeddingModel(embedding_model: { id: string }) {
    return disabledEmbeddingModels.find((model) => model.id === embedding_model.id);
  }

  function isDisabledResource(resource: GroupSparse | WebsiteSparse): boolean {
    // Always allow deselecting
    if ($isSelected(resource)) {
      return false;
    }
    // Disable if model not available
    if (isDisabledEmbeddingModel(resource.embedding_model)) {
      return true;
    }
    // Disable if other model is in use
    return (
      $chosenEmbeddingModelId !== null && $chosenEmbeddingModelId !== resource.embedding_model.id
    );
  }

  // ---------- Reactivity
  const chosenEmbeddingModelId = derived(selected, ($selected) => {
    if ($selected && $selected.length > 0) {
      return $selected[0].value.embedding_model.id;
    }
    return null;
  });

  const filteredItems = derived([touchedInput, inputValue], ([$touchedInput, $inputValue]) => {
    if ($touchedInput) {
      return [
        ...collections.filter(({ name }) => name.toLowerCase().includes($inputValue.toLowerCase())),
        ...websites.filter(({ name }) => name.toLowerCase().includes($inputValue.toLowerCase()))
      ];
    }
    return [...collections, ...websites];
  });

  const itemsGroupedByModels = derived(filteredItems, ($filteredItems) => {
    return usedEmbeddingModels
      .map((embeddingModel) => {
        const items = $filteredItems.filter(
          (item) => item.embedding_model.id === embeddingModel.id
        );
        return { items, embeddingModel };
      })
      .filter((group) => group.items.length > 0);
  });

  const isAnyItemDisabled = derived(
    selected,
    ($selected) =>
      $selected?.some((item) => {
        return (
          disabledEmbeddingModels.findIndex((model) => {
            return model.id === item.value.embedding_model.id;
          }) > -1
        );
      }) ?? false
  );

  $: if (!$open) {
    $inputValue = $selected?.flatMap((item) => item.label).join(", ") ?? "";
  }

  $: if ($selected) {
    selectedCollections = $selected.flatMap((item) => {
      if ("metadata" in item.value) {
        return { id: item.value.id };
      }
      return [];
    });
    selectedWebsites = $selected.flatMap((item) => {
      if (!("metadata" in item.value)) {
        return { id: item.value.id };
      }
      return [];
    });
  }

  $: if ($isAnyItemDisabled) {
    setTimeout(() => {
      alert(
        "Some knowledge is using an embedding model that is no longer available. Please change it in the assistants settings."
      );
    }, 400);
  }

  let inputElement: HTMLInputElement;
</script>

<div class="border-b border-stone-100 px-4 py-4">
  <div class="flex flex-col gap-1 pb-4">
    <div>
      <span class="pl-3 font-medium">Knowledge</span>
    </div>

    <div class="relative flex w-full">
      <input
        bind:this={inputElement}
        placeholder="Select knowledge..."
        {...$input}
        use:input
        class="h-10 w-full items-center justify-between overflow-hidden rounded-lg
        border {$isAnyItemDisabled ? 'border-2 border-red-500' : 'border-stone-300'}
        px-3 py-2 shadow ring-stone-200 placeholder:text-stone-400
        focus-within:ring-2 hover:ring-2 focus-visible:ring-2
        disabled:bg-stone-50 disabled:text-stone-500 disabled:shadow-none disabled:hover:ring-0"
      />
      <button
        on:click={() => {
          inputElement.focus();
          $open = true;
        }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="absolute right-4 top-2 h-6 w-6"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
        </svg>
      </button>
    </div>
  </div>
</div>

<ul
  class="relative z-10 flex flex-col gap-1 overflow-y-auto rounded-lg border border-stone-300 bg-white p-1 shadow-md shadow-stone-200 focus:!ring-0"
  {...$menu}
  use:menu
>
  {#each $itemsGroupedByModels as { items, embeddingModel }, index}
    {@const modelIsDisabled = isDisabledEmbeddingModel(embeddingModel)}
    <div class="flex flex-col gap-0 bg-white text-black">
      {#if usedEmbeddingModels.length > 1 || availableEmbeddingModels.length > 1 || modelIsDisabled}
        <span class="px-2 py-1 text-[0.7rem] font-medium uppercase tracking-wide text-stone-500">
          {embeddingModel.name}
          {modelIsDisabled ? "(disabled)" : ""}
        </span>
      {/if}
      {#each items as item}
        <li
          {...$option({
            value: item,
            label: item.name,
            disabled: isDisabledResource(item)
          })}
          use:option
          class="flex items-center gap-1 rounded-md px-2 hover:cursor-pointer hover:bg-stone-200 {modelIsDisabled &&
          $isSelected(item)
            ? 'text-red-500'
            : ''}"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="2.5"
            stroke="currentColor"
            class="h-5 w-5 {$isSelected(item) ? 'block' : 'hidden'} text-blue-600"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
          </svg>
          {#if "metadata" in item}
            <IconCollections
              class={modelIsDisabled && $isSelected(item) ? "stroke-red-500" : "stroke-stone-500"}
              size="small"
            />
          {:else}
            <IconWeb
              class={modelIsDisabled && $isSelected(item) ? "stroke-red-500" : "stroke-stone-500"}
              size="small"
            />
          {/if}
          <div class="flex w-full items-center justify-between py-1">
            <span>
              {item.name +
                (modelIsDisabled && $isSelected(item) ? " (embedding model disabled)" : "")}
            </span>
            {#if "metadata" in item}
              {#if item.metadata?.num_info_blobs > 0}
                <span
                  class="rounded-full border border-blue-600 bg-blue-50 px-2 text-sm text-blue-700"
                  >{item.metadata.num_info_blobs} files</span
                >
              {:else}
                <span
                  class="rounded-full border border-stone-500 bg-stone-50 px-2 text-sm text-stone-500"
                  >Empty</span
                >
              {/if}
            {/if}
          </div>
        </li>
      {/each}
    </div>
    {#if $itemsGroupedByModels.length > 1 && index < $itemsGroupedByModels.length - 1}
      <div class="min-h-[1px] w-full bg-stone-200"></div>
    {/if}
  {/each}
  {#if $itemsGroupedByModels.length === 0}
    <div class="flex select-none items-center gap-1 rounded-md px-2 py-1 text-stone-400">
      No available knowledge for this space
    </div>
  {/if}
</ul>

<style lang="postcss">
  li[data-highlighted] {
    @apply bg-stone-200;
  }

  li[data-disabled] {
    @apply pointer-events-none !cursor-not-allowed opacity-30 hover:bg-transparent;
  }
</style>
