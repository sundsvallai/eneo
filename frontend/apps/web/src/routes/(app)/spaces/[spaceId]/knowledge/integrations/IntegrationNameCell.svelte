<script lang="ts">
  import IntegrationVendorIcon from "$lib/features/integrations/components/IntegrationVendorIcon.svelte";
  import type { IntegrationKnowledge } from "@intric/intric-js";

  export let knowledge: IntegrationKnowledge;
  let customClass = "";
  export { customClass as class };
</script>

<div class="flex w-full items-center justify-start {customClass} gap-2">
  <IntegrationVendorIcon size="sm" type={knowledge.integration_type}></IntegrationVendorIcon>
  <span class="truncate overflow-ellipsis">
    {knowledge.name}
  </span>
</div>
