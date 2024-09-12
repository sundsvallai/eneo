<script lang="ts">
  import { getSidebar } from "./ctx";
  const {
    elements: { list }
  } = getSidebar();
</script>

<div class="order-last flex bg-white/80">
  <div
    {...$list}
    use:list
    class="flex min-w-[3.5rem] flex-col items-center gap-2.5 border-l-[0.5px] border-black/20 pb-2.5 pt-3"
    aria-label="Advanced actions for this resource"
  >
    <slot />
    <div class="flex-grow"></div>
    <div class="flex w-full items-center justify-center border-stone-200/60 pb-1 pt-3"></div>
  </div>
</div>
