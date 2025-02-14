<div class="mx-auto w-full max-w-[1100px]">
  <slot />
</div>

<style>
  div {
    padding-top: 2.5rem;
    padding-top: min(calc((100cqw - 1100px) * 0.35), 2.5rem);
  }
</style>
