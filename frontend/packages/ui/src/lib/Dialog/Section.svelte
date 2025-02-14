<script lang="ts">
  let cls = "";
  export { cls as class };
  export let scrollable = true;
</script>

<section
  class="flex flex-col justify-start rounded-md border {cls} border-stronger bg-primary shadow-md"
  class:overflow-y-auto={scrollable}
>
  <slot />
</section>
