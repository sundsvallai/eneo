<script lang="ts">
  import { uid } from "uid";
  const id = uid(8);

  let containerClass = "";

  export { containerClass as class };
  export let label = "";
  export let description: string | undefined = undefined;
  export let value: string;
  export let rows = 4;
  export let required = false;
</script>

<div class="flex flex-col gap-1 {containerClass}">
  <label for={id} class="pl-3 font-medium text-primary">
    {#if $$slots.default}
      <slot />
    {:else}
      <div class="flex items-baseline justify-between">
        <div>
          {label}
          {#if required}
            <span class="px-2 text-[0.9rem] font-normal text-muted" aria-hidden="true"
              >(required)</span
            >
          {/if}
        </div>
        {#if description}
          <span class="px-2 text-[0.9rem] font-normal text-muted">{description}</span>
        {/if}
      </div>
    {/if}
  </label>
  <textarea
    {id}
    {rows}
    {required}
    aria-required={required}
    on:change
    bind:value
    {...$$restProps}
    class="h-full min-h-10 items-center justify-between rounded-lg border border-stronger bg-primary px-3 py-2 text-primary shadow ring-default placeholder:text-muted focus-within:ring-2 hover:ring-2 focus-visible:ring-2"
  />
</div>
