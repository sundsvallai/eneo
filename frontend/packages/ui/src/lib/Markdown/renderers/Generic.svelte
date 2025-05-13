<script lang="ts">
  import type { Tokens } from "marked";
  import Self from "./Generic.svelte";
  export let token: Tokens.Generic;
</script>

{#if token.tokens}
  {#each token.tokens as child (child)}
    <Self token={child}></Self>
  {/each}
{:else}
  {token.raw}
{/if}
