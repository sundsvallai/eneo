<script lang="ts">
  import { createSlider } from "@melt-ui/svelte";

  let cls = "";

  export { cls as class };
  export let value: number;
  export let min: number;
  export let max: number;
  export let step: number;

  const {
    elements: { root, range, thumbs },
    states: { value: selectedValue }
  } = createSlider({
    defaultValue: [value],
    min,
    max,
    step,
    onValueChange({ next }) {
      value = next[0];
      return next;
    }
  });

  $: $selectedValue = [value];
</script>

<div {...$root} use:root class="relative flex flex-grow items-center {cls}">
  <span class="h-[4px] min-h-[4px] w-full rounded-full bg-black/40">
    <span {...$range} use:range class="h-[4px] min-h-[4px] rounded-full bg-blue-500" />
  </span>

  <span
    {...$thumbs[0]}
    use:thumbs
    class="h-5 w-5 rounded-full border border-stone-400 bg-white shadow-md focus:ring-4 focus:!ring-black/40"
  />
</div>
