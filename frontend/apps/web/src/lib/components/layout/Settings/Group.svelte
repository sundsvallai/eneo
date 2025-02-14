<script lang="ts">
  export let title: string;
</script>

<section>
  <h2
    class="bg-frosted-glass-primary sticky top-0 z-10 col-span-2 border-b border-dimmer px-6 py-3 font-mono text-sm backdrop-blur-sm lg:px-2.5"
  >
    {title}
  </h2>

  <div class="relative flex w-full flex-col gap-12 pb-24 pt-4">
    <slot />
  </div>
</section>
