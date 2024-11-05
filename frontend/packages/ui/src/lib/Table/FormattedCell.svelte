<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  export let value: string | number;

  export let align: "start" | "end" | "center" = "start";
  export let monospaced = false;
  export let italic = false;
  export let bold = false;

  let cls = "";
  export { cls as class };
</script>

<div
  class="flex w-full items-center {cls}"
  style="justify-content: flex-{align}"
  class:font-mono={monospaced}
  class:italic
  class:font-semibold={bold}
>
  {value}
</div>
