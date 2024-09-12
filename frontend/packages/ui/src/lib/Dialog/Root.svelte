<script lang="ts">
  import { createEventDispatcher, onMount } from "svelte";
  import { createDialog } from "./ctx.js";

  export let alert = false;
  export let portal: string | null | undefined = undefined;

  const {
    states: { open }
  } = createDialog(alert, portal);

  export { open as isOpen };

  const dispatch = createEventDispatcher();
  onMount(() => {
    return open.subscribe((visible) => {
      if (visible) {
        dispatch("open");
      } else {
        dispatch("close");
      }
    });
  });
</script>

<slot />
