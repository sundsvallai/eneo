<script lang="ts">
  import { createEventDispatcher, onMount } from "svelte";
  import { createDialog } from "./ctx.js";
  import type { Writable } from "svelte/store";

  export let alert = false;
  export let portal: string | null | undefined = undefined;
  export let openController: Writable<boolean> | undefined = undefined;

  const {
    states: { open }
  } = createDialog(alert, portal, openController);

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
