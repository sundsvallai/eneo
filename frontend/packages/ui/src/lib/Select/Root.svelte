<script lang="ts">
  import type { SelectOption } from "@melt-ui/svelte";
  import { createSelect } from "./ctx.js";
  import type { Writable } from "svelte/store";

  export let multiple = false;
  export let required = false;
  export let fitViewport = true;
  export let disabled = false;
  export let customStore: Writable<SelectOption<unknown>[] | SelectOption<unknown>> | undefined =
    undefined;

  const {
    states: { selected }
  } = createSelect(multiple, customStore, fitViewport, disabled);

  let cls = "";
  export { cls as class };
  export const value = selected;

  $: hiddenInputValue = Array.isArray($selected)
    ? $selected.map((item) => item.value)
    : ($selected?.value ?? "");
</script>

<div class="flex flex-col gap-1 {cls} relative">
  <slot />
  <!-- This is  a bit of a hack to make this field required, currently not properly supported by meltui -->
  <input value={hiddenInputValue} {required} class="ml-4 h-1 w-1 opacity-0" />
</div>
