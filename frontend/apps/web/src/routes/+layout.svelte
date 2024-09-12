<script>
  import { page } from "$app/stores";
  import { fly } from "svelte/transition";
  import "../app.css";
  import { cubicOut } from "svelte/easing";

  $: area = $page.url.pathname.startsWith("/login") ? "public" : "app";
</script>

<div
  style={area === "public" ? "opacity: 0;" : "opacity: 1;"}
  class="fixed inset-x-0 -z-10 h-[8.275rem] bg-stone-500/20 transition-all duration-700 ease-in-out"
></div>

<div class="max-h-[100svh] overflow-hidden">
  {#key area}
    <div in:fly|global={{ y: 15, opacity: 0, duration: 500, easing: cubicOut }}>
      <slot />
    </div>
  {/key}
</div>
