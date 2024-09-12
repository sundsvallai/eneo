<script lang="ts">
  import { getSelect } from "./ctx.js";

  export let label: string;

  const {
    elements: { group, groupLabel }
  } = getSelect();
</script>

<div {...$group(label)} use:group>
  <div
    class="px-2 py-1 text-[0.7rem] font-medium uppercase tracking-wide text-stone-500"
    {...$groupLabel(label)}
    use:groupLabel
  >
    {label}
  </div>
  <slot />
</div>
