<script lang="ts">
  import { uid } from "uid";
  const id = uid(8);

  let cls = "";
  let inputElement: HTMLInputElement;

  export { cls as class };
  export let labelClass = "";
  export let inputClass = "";
  export let value: string;
  export let isValid = false;

  $: (isValid = inputElement?.validity.valid ?? false), value;
</script>

<fieldset class="flex flex-col gap-1 {cls}">
  <label for={id} class="pl-3 font-medium {labelClass}"><slot /></label>
  <input
    bind:this={inputElement}
    type="text"
    {id}
    {...$$restProps}
    bind:value
    class="h-10 items-center justify-between overflow-hidden rounded-lg
  border border-stone-300 bg-white px-3 py-2 shadow ring-stone-200 placeholder:text-stone-400 focus-within:ring-2 hover:ring-2 focus-visible:ring-2 disabled:bg-stone-50 disabled:text-stone-500 disabled:shadow-none disabled:hover:ring-0 {inputClass}"
  />
</fieldset>
