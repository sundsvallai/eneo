<script lang="ts">
  import { uid } from "uid";

  export let title: string;
  export let description: string;
  export let fullWidth = false;

  export let hasChanges = false;
  export let revertFn: (() => void) | undefined = undefined;

  const labelId = uid(8);
  const descriptionId = uid(8);
</script>

<div
  class:fullWidth
  class="flex flex-col justify-between gap-y-4 px-4 lg:flex-row lg:pl-0.5 lg:pr-6"
  data-row-has-changes={hasChanges}
>
  <div class="description-section">
    <div class="flex flex-col gap-2 pl-2 pr-12">
      <h3 class="flex items-center text-lg font-medium" id={labelId}>
        <span class="change-indicator"></span>{title}
        {#if revertFn}
          <button class="revert-button" disabled={!hasChanges} on:click={revertFn}
            >Discard changes</button
          >
        {/if}
      </h3>
      <p class="text-secondary" id={descriptionId}>
        {description}
      </p>
      <slot name="description" />
    </div>
    <div class="p-4 pr-3">
      <slot name="toolbar" />
    </div>
  </div>

  <div class="input-section">
    <slot
      {labelId}
      {descriptionId}
      aria={{ "aria-labelledby": labelId, "aria-describedby": descriptionId }}
    />
  </div>
</div>

<style lang="postcss">
  .fullWidth {
    @apply !flex-col gap-y-2;
  }

  .description-section {
    @apply flex w-full justify-between lg:w-[40%];
  }

  .fullWidth > .description-section {
    @apply w-full;
  }

  .input-section {
    @apply flex w-full flex-col pt-3 lg:w-[56%];
  }

  .fullWidth > .input-section {
    @apply w-full;
  }

  .change-indicator {
    @apply h-0 w-0 bg-transparent transition-all duration-300;
  }

  .revert-button {
    @apply ml-2 -translate-y-[1px] self-end rounded-lg border border-default px-2 py-0.5 text-sm font-normal transition-all hover:bg-hover-dimmer hover:shadow disabled:opacity-0;
  }

  div[data-row-has-changes="true"] .change-indicator {
    /* TODO change this */
    @apply mr-2 h-2 w-2 rounded-full bg-[var(--change-indicator)];
  }
</style>
