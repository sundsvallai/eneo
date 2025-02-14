<script lang="ts">
  // These are the props that will be typed on imported icons
  type IconProps = {
    size?: "sm" | "md" | "lg";
  };

  export let size = "md";
  export let src = "";

  /* eslint-disable @typescript-eslint/no-unused-vars */
  type $$Props = {
    src: string;
  } & IconProps;
</script>

<svg
  xmlns="http://www.w3.org/2000/svg"
  fill="none"
  stroke="currentColor"
  viewBox="0 0 24 24"
  stroke-width="1.5"
  data-size={size}
  {...$$restProps}
>
  <!-- eslint-disable svelte/no-at-html-tags -->
  {@html src}
</svg>

<style>
  svg[data-size="sm"] {
    height: 1.2rem;
    width: 1.2rem;
    min-height: 1.2rem;
    min-width: 1.2rem;
  }

  svg[data-size="md"] {
    height: 1.5rem;
    width: 1.5rem;
    min-height: 1.5rem;
    min-width: 1.5rem;
  }

  svg[data-size="lg"] {
    height: 6rem;
    width: 6rem;
    stroke-width: 1;
  }
</style>
