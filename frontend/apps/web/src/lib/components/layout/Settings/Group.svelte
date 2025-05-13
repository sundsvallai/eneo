<script lang="ts">
  export let title: string;
</script>

<section>
  <h2
    class="bg-frosted-glass-primary border-dimmer sticky top-0 z-10 col-span-2 border-b px-6 py-3 font-mono text-sm backdrop-blur-sm lg:px-2.5"
  >
    {title}
  </h2>

  <div class="relative flex w-full flex-col gap-12 pt-4 pb-24">
    <slot />
  </div>
</section>
