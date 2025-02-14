<div
  class="header-shadow header relative top-0 z-[60] ml-6 flex h-[4.25rem] min-h-[4.25rem] items-center justify-between border-b-[0.5px] border-default bg-primary pr-4 text-primary"
>
  <slot />
</div>

<style lang="postcss">
  .header-shadow {
    box-shadow: 2rem 0.75rem 4rem 0rem rgba(0, 0, 0, 0.03);
  }
</style>
