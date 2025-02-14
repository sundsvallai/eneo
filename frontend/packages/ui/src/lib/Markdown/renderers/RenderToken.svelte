<script lang="ts">
  import type { Token } from "marked";
  import { isSupportedToken, renderers } from ".";
  import type { IntricToken } from "../CustomComponents";

  export let token: (Token | IntricToken) & { tokens?: Token[] };
</script>

{#if isSupportedToken(token.type)}
  {#if token.tokens && token.tokens.length > 0}
    <svelte:component this={renderers[token.type]} {token}>
      {#each token.tokens as children}
        <svelte:self token={children}></svelte:self>
      {/each}
    </svelte:component>
  {:else}
    <svelte:component this={renderers[token.type]} {token}></svelte:component>
  {/if}
{/if}
