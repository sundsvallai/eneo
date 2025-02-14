<script lang="ts">
  import type { Tokens } from "marked";

  export let token: Tokens.Codespan;
</script>

<code class="whitespace-pre-wrap rounded-lg bg-secondary px-1.5 py-0.5 before:hidden after:hidden"
  >{token.text}</code
>

<style>
  code {
    font-weight: inherit !important;
  }
</style>
