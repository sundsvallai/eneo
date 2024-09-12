<script lang="ts">
  import { createRadioGroup } from "@melt-ui/svelte";
  import { uid } from "uid";
  const ariaLabelId = uid(8);
  let cls = "";
  export { cls as class };

  export let options: Array<{ value: unknown; label: string }>;
  export let value: unknown;
  export let required = true;
  export let disabled = false;

  const defaultValue: string = options.findIndex((option) => option.value === value).toString();

  const {
    elements: { root, item, hiddenInput },
    helpers: { isChecked },
    states: { value: selectedId }
  } = createRadioGroup({
    disabled,
    defaultValue,
    required,
    loop: true
  });

  $: value = options[parseInt($selectedId)].value;
</script>

<fieldset class="flex justify-between gap-8 {cls} items-start">
  <div id={ariaLabelId} class="max-w-[66%] pb-1.5 pl-3 font-medium"><slot /></div>

  <div
    {...$root}
    use:root
    class="flex w-auto flex-grow flex-col gap-3 rounded-lg border border-stone-300 bg-stone-50 p-4 pr-6 data-[orientation=horizontal]:flex-row"
    aria-labelledby={ariaLabelId}
  >
    {#each Object.entries(options) as [id, option]}
      <div class="flex items-center gap-3">
        <button
          {...$item(id)}
          use:item
          style="cursor: {disabled ? 'not-allowed' : 'pointer'};"
          class="grid h-6 min-w-6 place-items-center rounded-full border border-stone-300 bg-white
    shadow-sm hover:bg-blue-100"
          id={option.label}
          aria-labelledby="{option.label}-label"
        >
          {#if $isChecked(id)}
            <div class="h-3 w-3 rounded-full bg-blue-500" />
          {/if}
        </button>
        <label
          class="leading-none"
          for={option.label}
          id="{option.label}-label"
          style="cursor: {disabled ? 'not-allowed' : 'pointer'};"
        >
          {option.label}
        </label>
      </div>
    {/each}
    <input {...$hiddenInput} use:hiddenInput />
  </div>
</fieldset>
