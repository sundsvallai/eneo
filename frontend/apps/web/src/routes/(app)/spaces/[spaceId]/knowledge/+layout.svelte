<script lang="ts">
  import { setAvailableIntegrations } from "$lib/features/integrations/AvailableIntegrations.js";

  let { data, children } = $props();

  setAvailableIntegrations(data.availableIntegrations);
</script>

{@render children?.()}
