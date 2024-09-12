<script lang="ts">
  import { getDialog } from "./ctx.js";
  import { Button } from "../Button/index.js";

  export let destructive = false;

  const {
    elements: { trigger }
  } = getDialog();

  export let asFragment = false;
</script>

{#if asFragment}
  <slot trigger={[$trigger]} {destructive} />
{:else}
  <Button is={[$trigger]} {destructive}><slot trigger={[$trigger]} /></Button>
{/if}
