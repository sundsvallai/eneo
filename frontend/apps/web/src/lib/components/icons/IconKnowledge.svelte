<script lang="ts">
  export let size: "base" | "large" | "small" = "base";
  let cls = "";
  export { cls as class };
</script>

<svg
  xmlns="http://www.w3.org/2000/svg"
  fill="none"
  viewBox="0 0 24 24"
  stroke="currentColor"
  class="icon-{size} {cls}"
  stroke-linecap="round"
  stroke-linejoin="round"
  stroke-width="1.5"
>
  <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20" /><polyline
    points="10 2 10 10 13 7 16 10 16 2"
  /></svg
>
