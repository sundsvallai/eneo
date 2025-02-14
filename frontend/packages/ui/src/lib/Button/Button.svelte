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

  export let variant:
    | "simple"
    | "outlined"
    | "primary"
    | "primary-outlined"
    | "destructive"
    | "positive"
    | "positive-outlined"
    | "on-fill" = "simple";
  export let padding: "icon" | "text" | "icon-leading" = "text";
  // export let size: "base" = "base";
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
  class:disabled
  class:displayActiveState
>
  <slot />
</svelte:element>

<style lang="postcss">
  .ui-btn {
    @apply flex items-center justify-center gap-3 rounded-md border border-transparent p-1 text-left mix-blend-normal outline-offset-4 hover:border-dimmer hover:bg-hover-default;
  }

  .on-fill {
    @apply hover:bg-hover-on-fill hover:text-primary;
  }

  .destructive {
    @apply border-negative-default text-negative-default hover:border-negative-default hover:bg-negative-default hover:text-on-fill;
  }

  .positive {
    @apply border-positive-stronger bg-positive-default text-on-fill hover:border-positive-default hover:bg-positive-stronger;
  }

  .positive-outlined {
    @apply border-positive-stronger text-positive-stronger hover:border-positive-default hover:bg-positive-stronger hover:text-on-fill;
  }

  .displayActiveState[data-state="active"] {
    @apply bg-accent-dimmer font-[500] tracking-normal text-accent-stronger;
  }

  .displayActiveState {
    @apply tracking-[0.01rem];
  }

  .ui-btn[data-melt-dropdown-menu-item] {
    @apply justify-start;
  }

  .primary {
    @apply border-accent-default bg-accent-default text-on-fill hover:border-accent-stronger hover:bg-accent-stronger;
  }

  .primary-outlined {
    @apply border-accent-default bg-transparent text-accent-default hover:border-accent-stronger hover:bg-accent-stronger hover:text-on-fill;
  }

  .outlined {
    @apply border-default;
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
