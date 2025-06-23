<script lang="ts">
  import type { SvelteHTMLElements } from "svelte/elements";
  import { m } from "$lib/paraglide/messages";
  type $$Props = SvelteHTMLElements["div"];
</script>

<div 
  role="img" 
  aria-label={m.eneo_logo()}
  class="font-bold select-none cursor-default tracking-wide"
  style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-size: 18px; letter-spacing: 0.5px; color: #4f46e5;"
  {...$$restProps}
>
  Eneo
</div>