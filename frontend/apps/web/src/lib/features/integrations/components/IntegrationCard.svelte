<script lang="ts">
  import type { Integration } from "@intric/intric-js";
  import type { Snippet } from "svelte";
  import IntegrationVendorIcon from "./IntegrationVendorIcon.svelte";
  import { integrationData } from "../IntegrationData";

  type Props = {
    integration: Omit<Integration, "id">;
    action: Snippet;
  };

  let { integration, action }: Props = $props();

  const description = $derived(integrationData[integration.integration_type].description);
  const name = $derived(integrationData[integration.integration_type].displayName);
</script>

<div
  class="border-default flex flex-col overflow-y-auto rounded-lg border p-4 shadow-md hover:shadow-lg"
>
  <div
    class="from-accent-dimmer -mx-4 -mt-4 bg-gradient-to-b to-[var(--background-primary)] px-4 pt-4"
  >
    <div class="border-default bg-primary -ml-0.5 w-fit rounded-lg border p-2 shadow-md">
      <IntegrationVendorIcon size="lg" type={integration.integration_type}></IntegrationVendorIcon>
    </div>
  </div>
  <div class="flex flex-col gap-1 pt-4 pb-4">
    <h2 class="text-2xl font-extrabold">{name}</h2>
    <p class=" text-secondary">
      {description}
    </p>
  </div>
  <div class="h-1 flex-grow"></div>
  {@render action()}
</div>
