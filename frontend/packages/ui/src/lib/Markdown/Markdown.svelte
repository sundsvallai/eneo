<script lang="ts">
  import { intricMarkdownLexer } from "./index.js";
  import RenderToken from "./renderers/RenderToken.svelte";
  import { initReferenceContext } from "./ReferenceContext.js";
  import type { CustomRenderers } from "./CustomComponents.js";

  export let source: string;
  export let customRenderers: CustomRenderers = {};
  export let showTokenOutput = false;

  const lexer = intricMarkdownLexer();
  const {
    state: { references: refStore }
  } = initReferenceContext(customRenderers.inref ?? {});

  $: tokens = lexer.lex(source);
  $: $refStore = customRenderers.inref?.references ?? [];
</script>

<div class="prose break-words text-lg">
  {#each tokens as token}
    <RenderToken {token}></RenderToken>
  {/each}
</div>

{#if showTokenOutput}
  <pre>{JSON.stringify(tokens, undefined, 2)}</pre>
{/if}
