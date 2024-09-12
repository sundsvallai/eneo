<script lang="ts">
  let cls = "";
  export { cls as class };
  export let scrollable = true;
</script>

<section
  class="flex flex-col justify-start rounded-md border {cls} border-black/20 bg-white"
  class:overflow-y-auto={scrollable}
>
  <slot />
</section>

<style>
  section {
    box-shadow: 0px 2px 4px -2px rgba(0, 0, 0, 0.3);
  }
</style>
