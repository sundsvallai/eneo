<script lang="ts" generics="T extends unknown">
  import { writable } from "svelte/store";
  import { Item, Label, Options, Root, Trigger } from "./index.js";

  export let options: Array<{ value: T | null | undefined; label: string }>;
  export let value: T | null | undefined;
  export let required = false;
  export let fitViewport = true;
  export let resourceName = "option";

  function getInitiallySelected() {
    if (value) {
      return options.find((option) => option.value === value);
    } else {
      return undefined;
    }
  }

  let store = writable(getInitiallySelected());

  $: {
    if ($store) {
      value = $store.value;
    }
  }

  let cls = "";
  export { cls as class };
</script>

<Root customStore={store} class={cls} {required} {fitViewport}>
  <Label><slot /></Label>
  <Trigger placeholder="Select..."></Trigger>
  <Options>
    {#each options as option (option.value)}
      <Item value={option.value} label={option.label}></Item>
    {/each}
    {#if !options.length}
      <Item disabled label="No available {resourceName}s" value={null}></Item>
    {/if}
  </Options>
</Root>
