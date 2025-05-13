<script lang="ts">
  import { createAsyncState } from "$lib/core/helpers/createAsyncState.svelte";
  import { getIntric } from "$lib/core/Intric";
  import type { TenantIntegration } from "@intric/intric-js";
  import { Button, Dialog } from "@intric/ui";

  type Props = {
    integration: TenantIntegration;
    update: (integration: Partial<TenantIntegration>) => void;
  };

  let { integration, update }: Props = $props();

  const intric = getIntric();

  const disableIntegration = createAsyncState(async () => {
    const { id } = integration;
    if (id == null) return;
    try {
      await intric.integrations.tenant.disable({ id });
      $isOpen = false;

      setTimeout(() => {
        update({ is_linked_to_tenant: false });
      }, 250);
    } catch (e) {
      console.error(e);
    }
  });

  let isOpen = $state<Dialog.OpenState>();
</script>

<Dialog.Root bind:isOpen>
  <Dialog.Trigger asFragment let:trigger>
    <Button variant="destructive" is={trigger}>Disable integration</Button>
  </Dialog.Trigger>

  <Dialog.Content>
    <Dialog.Title>Disable {integration.name} integration</Dialog.Title>
    <Dialog.Description>
      Do you really want to disable the integration for <span class="italic"
        >{integration.name}</span
      >?<br /><br />Disabling an integration will disconnect all users and remove all knowledge
      across all spaces that was previously imported via this integration.
    </Dialog.Description>

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button on:click={disableIntegration} variant="destructive">
        {disableIntegration.isLoading ? "Loading..." : "Disable"}
      </Button>
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
