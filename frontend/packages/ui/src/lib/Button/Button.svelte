<script lang="ts">
  import type { Action } from "svelte/action";

  export let label: string | undefined = undefined;
  export let href: string | undefined = undefined;
  export let type: HTMLButtonElement["type"] | undefined = undefined;
  export let unstyled = false;

  /**
   * Pass melt-ui builders into the `is` property to apply them to this button
   * Typically you would do this when you have a trigger as fragment, so the child
   * actually does the triggering.
   */
  export let is: {
    [x: PropertyKey]: unknown;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    action: Action<HTMLElement, any, Record<string, unknown>>;
  }[] = [];

  let cls = "";
  export { cls as class };

  export let variant: "simple" | "outlined" | "primary" | "primary-outlined" = "simple";
  export let padding: "icon" | "text" | "icon-leading" = "text";
  // export let size: "base" = "base";
  export let destructive = false;
  export let disabled: boolean | undefined = undefined;
  export let displayActiveState: boolean = false;

  export let actions: Action[] = [() => {}];

  const combinedActions = (node: HTMLElement) => {
    const destructors = actions.map((action) => action(node));
    const meltDestructurs = is.map((builder) => builder.action(node));

    return {
      destroy() {
        destructors.forEach((destructor) => {
          if (typeof destructor?.destroy == "function") destructor.destroy();
        });
        meltDestructurs.forEach((destructor) => {
          if (typeof destructor?.destroy == "function") destructor.destroy();
        });
      }
    };
  };

  $: meltAttributes = is.reduce(
    (attrs, melt) => {
      Object.keys(melt).forEach((key) => {
        if (key !== "action") {
          attrs[key] = melt[key];
        }
      });
      return attrs;
    },
    {} as { [x: PropertyKey]: unknown }
  );
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<svelte:element
  this={href ? "a" : "button"}
  type={href ? undefined : type}
  {href}
  aria-label={label}
  aria-disabled={disabled}
  disabled={disabled ? true : undefined}
  on:click
  on:change
  on:keydown
  on:keyup
  on:mouseenter
  on:mouseleave
  tabindex="0"
  use:combinedActions
  {...meltAttributes}
  {...$$restProps}
  class=" group {cls} {variant} padding-{unstyled ? 'none' : padding}"
  class:ui-btn={!unstyled}
  class:destructive
  class:disabled
  class:displayActiveState
>
  <slot />
</svelte:element>

<style lang="postcss">
  .ui-btn {
    @apply flex items-center justify-center gap-3 rounded-md  border border-transparent p-1 text-left mix-blend-normal outline-offset-4 hover:border-stone-200 hover:bg-stone-200;
  }

  .displayActiveState[data-state="active"] {
    @apply bg-blue-100 font-[500] tracking-normal text-blue-700;
  }

  .displayActiveState {
    @apply tracking-[0.01rem];
  }

  .ui-btn[data-melt-dropdown-menu-item] {
    @apply justify-start;
  }

  .destructive {
    @apply border-red-500 text-red-500 hover:border-red-500 hover:bg-red-500 hover:text-white;
  }

  .primary {
    @apply border-blue-600 bg-blue-600 text-white hover:border-blue-800 hover:bg-blue-800;
  }

  .primary-outlined {
    @apply border-blue-600 bg-transparent text-blue-700 hover:border-blue-800 hover:bg-blue-800 hover:text-white;
  }

  .outlined {
    @apply border-stone-300;
  }

  .padding-text {
    @apply px-2;
  }

  .padding-icon-leading {
    @apply pr-2;
  }

  .disabled {
    @apply pointer-events-none cursor-not-allowed opacity-50;
  }
</style>
