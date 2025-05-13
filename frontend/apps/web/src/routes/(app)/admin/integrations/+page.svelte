<script lang="ts">
  import { Page, Settings } from "$lib/components/layout";
  import type { PageProps } from "./$types";
  import IntegrationCard from "$lib/features/integrations/components/IntegrationCard.svelte";
  import IntegrationGrid from "$lib/features/integrations/components/IntegrationGrid.svelte";
  import { Button } from "@intric/ui";
  import { createAsyncState } from "$lib/core/helpers/createAsyncState.svelte";
  import type { TenantIntegration } from "@intric/intric-js";
  import TenantConnectedSplitButton from "$lib/features/integrations/components/TenantConnectedSplitButton.svelte";

  const { data }: PageProps = $props();

  let tenantIntegrations = $derived.by(() => {
    let integrations = $state(data.tenantIntegrations);
    return integrations;
  });

  const enableIntegration = createAsyncState(async (integration: TenantIntegration) => {
    Object.assign(integration, await data.intric.integrations.tenant.enable(integration));
  });

  function onDisable(integration: TenantIntegration) {
    integration.is_linked_to_tenant = false;
  }
</script>

<svelte:head>
  <title>Intric.ai – Admin – Integrations</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title title="Integrations"></Page.Title>
  </Page.Header>
  <Page.Main>
    <Settings.Page>
      <Settings.Group title="Configure integrations">
        <Settings.Row
          fullWidth
          title="Knowledge providers"
          description="Enable an integration to allow your users to connect to external knowledge providers and import information into intric."
        >
          <IntegrationGrid>
            {#each tenantIntegrations as integration (integration.integration_id)}
              <IntegrationCard {integration}>
                {#snippet action()}
                  {#if integration.is_linked_to_tenant}
                    <TenantConnectedSplitButton {integration} {onDisable}
                    ></TenantConnectedSplitButton>
                  {:else}
                    <Button variant="primary" onclick={() => enableIntegration(integration)}
                      >Enable integration</Button
                    >
                  {/if}
                {/snippet}
              </IntegrationCard>
            {/each}
          </IntegrationGrid>
        </Settings.Row>
      </Settings.Group>
    </Settings.Page>
  </Page.Main>
</Page.Root>
