<script lang="ts">
  import { createSlider } from "@melt-ui/svelte";

  let cls = "";

  export { cls as class };
  export let value: number;
  export let min: number;
  export let max: number;
  export let step: number;
  export let onInput: ((value: number) => void) | undefined = undefined;

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
      onInput?.(value);
      return next;
    }
  });

  $: $selectedValue = [value];
</script>

<div {...$root} use:root class="relative flex flex-grow items-center {cls}">
  <span class="bg-tertiary h-[4px] min-h-[4px] w-full rounded-full">
    <span {...$range} use:range class="bg-accent-default h-[4px] min-h-[4px] rounded-full"></span>
  </span>

  <span
    {...$thumbs[0]}
    use:thumbs
    class="border-strongest bg-primary focus:ring-default h-5 w-5 rounded-full border shadow-md focus:ring-4"
  ></span>
</div>
