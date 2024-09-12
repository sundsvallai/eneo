<script lang="ts">
  import { uid } from "uid";
  const id = uid(8);

  let cls = "";
  export { cls as class };
  export let value: string;
  export let rows = 4;
</script>

<fieldset class="flex flex-col gap-1 {cls}">
  <label for={id} class="pl-3 font-medium"><slot /></label>
  <textarea
    {id}
    {rows}
    bind:value
    {...$$restProps}
    class="h-full min-h-10 items-center justify-between rounded-lg border border-stone-300 bg-white px-3 py-2 shadow ring-stone-200 focus-within:ring-2 hover:ring-2 focus-visible:ring-2"
  />
</fieldset>
