<script lang="ts">
  import { Button } from "../Button/index.js";
  import { getDropdown } from "./ctx.js";

  const {
    elements: { trigger }
  } = getDropdown();

  export let asFragment = false;
</script>

{#if asFragment}
  <slot trigger={[$trigger]} />
{:else}
  <Button is={[$trigger]}>
    <slot trigger={[$trigger]} />
  </Button>
{/if}
