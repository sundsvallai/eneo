<script lang="ts">
  import { uid } from "uid";
  const id = uid(8);

  let containerClass = "";
  let inputElement: HTMLInputElement;

  export { containerClass as class };
  export let inputClass = "";
  export let labelClass = "";
  export let label = "";
  export let description: string | undefined = undefined;
  export let value: string;
  export let isValid: boolean = false;
  export let required: boolean = false;
</script>

<div class="flex flex-col gap-1 {containerClass}">
  <label for={id} class="pl-3 font-medium text-primary {labelClass}">
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
  <div class="flex justify-between">
    <input
      bind:this={inputElement}
      type="text"
      {id}
      {...$$restProps}
      {required}
      on:input={() => {
        isValid = inputElement?.validity.valid ?? false;
      }}
      aria-required={required}
      bind:value
      class="ult mr-4 h-10 w-full items-center
      overflow-hidden rounded-lg border border-stronger bg-primary px-3 py-2 shadow ring-default placeholder:text-muted focus-within:ring-2 hover:ring-2 focus-visible:ring-2 {inputClass}"
    />
    <input
      type="color"
      bind:value
      class="h-10 min-h-10 w-10 min-w-10 rounded-lg border border-stronger bg-primary px-1 py-0.5"
    />
  </div>
</div>
