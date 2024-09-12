<script lang="ts">
  import { uid } from "uid";
  const id = uid(8);

  let cls = "";
  export { cls as class };
  export let labelClass = "";
  export let inputClass = "";
  export let value: number;
  export let step = 1;
  export let max = 100;
  export let min = 0;

  function validate() {
    if (value > max) {
      value = max;
    } else if (value < min) {
      value = min;
    }
  }
</script>

<fieldset class="flex flex-col gap-1 {cls}">
  <label for={id} class="pl-3 font-medium {labelClass}"><slot /></label>
  <input
    type="number"
    {id}
    {...$$restProps}
    {step}
    {max}
    {min}
    bind:value
    on:input={validate}
    class="h-10 items-center justify-between overflow-hidden rounded-lg border
  border-stone-300 bg-white px-3 py-2 text-center shadow ring-stone-200 placeholder:text-stone-400 focus-within:ring-2 hover:ring-2 focus-visible:ring-2 disabled:bg-stone-50 disabled:text-stone-500 disabled:shadow-none disabled:hover:ring-0 {inputClass}"
  />
</fieldset>

<style>
  input[type="number"]::-webkit-inner-spin-button,
  input[type="number"]::-webkit-outer-spin-button {
    opacity: 1;
  }
</style>
