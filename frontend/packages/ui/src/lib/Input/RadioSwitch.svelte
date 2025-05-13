<script lang="ts">
  import { cva } from "class-variance-authority";
  import { uid } from "uid";

  const name = "switch_" + uid(8);

  export let value: boolean;
  export let disabled = false;
  export let labelTrue = "Enabled";
  export let labelFalse = "Disabled";
  export let sideEffect: ((params: { current: boolean; next: boolean }) => void) | undefined =
    undefined;

  let selectedValue: "on" | "off" = value ? "on" : "off";

  function updateValue(selectedValue: "on" | "off") {
    const current = value;
    const next = selectedValue === "on";
    sideEffect?.({ current, next });
    value = next;
  }

  function updateSelectedValue(value: boolean) {
    selectedValue = value ? "on" : "off";
  }

  $: updateValue(selectedValue);
  $: updateSelectedValue(value);

  const label = cva(
    "flex cursor-pointer items-center justify-start gap-3 rounded-lg border border-transparent px-4 py-2 hover:border-default hover:bg-hover-default"
  );

  const input = cva(
    "max-h-3 min-h-3 min-w-3 max-w-3 appearance-none rounded-full  outline-2 outline-offset-2 outline-accent-default",
    { variants: { active: { false: null, true: "bg-accent-default" } } }
  );
</script>

<div
  class="grid w-full grid-cols-2 gap-2"
  class:pointer-events-none={disabled}
  class:opacity-60={disabled}
>
  <label data-selected={selectedValue === "on"} class={label()}>
    <input
      type="radio"
      {name}
      value="on"
      bind:group={selectedValue}
      {disabled}
      class={input({ active: selectedValue === "on" })}
    />
    <span>{labelTrue}</span>
  </label>
  <label data-selected={selectedValue === "off"} class={label()}>
    <input
      type="radio"
      {name}
      value="off"
      bind:group={selectedValue}
      {disabled}
      class={input({ active: selectedValue === "off" })}
    />
    <span>{labelFalse}</span>
  </label>
</div>
