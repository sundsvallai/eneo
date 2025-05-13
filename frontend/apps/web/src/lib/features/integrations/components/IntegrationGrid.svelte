<script lang="ts">
  import type { Snippet } from "svelte";

  type Props = {
    children: Snippet;
  };

  const { children }: Props = $props();
</script>

<div class="grid grid-cols-1 gap-6 pt-4 pr-32 lg:grid-cols-2 xl:grid-cols-3">
  {@render children()}
</div>
