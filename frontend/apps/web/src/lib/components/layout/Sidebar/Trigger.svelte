<script lang="ts">
  import { getSidebar } from "./ctx";
  export let panel: string;
  export let label: string;

  import { Button, Tooltip } from "@intric/ui";

  const {
    elements: { trigger: sidebarTrigger }
  } = getSidebar();
</script>

<Tooltip text={label} placement="left" asFragment let:trigger>
  <Button
    is={[...trigger, $sidebarTrigger(panel)]}
    padding="icon"
    displayActiveState
    class="relative"
    tabindex="0"
  >
    <slot />
  </Button>
</Tooltip>
