<script lang="ts">
  import { createAsyncState } from "$lib/core/helpers/createAsyncState.svelte";
  import { getIntric } from "$lib/core/Intric";
  import { IconCancel } from "@intric/icons/cancel";
  import { IconChevronDown } from "@intric/icons/chevron-down";
  import { type TenantIntegration } from "@intric/intric-js";
  import { Button, Dialog, Dropdown } from "@intric/ui";
  import { writable } from "svelte/store";

  type Props = {
    integration: TenantIntegration;
    onDisable?: (integration: TenantIntegration) => void;
  };

  let { integration, onDisable }: Props = $props();

  const intric = getIntric();
  const showDisconnectDialog = writable(false);

  const disableIntegration = createAsyncState(async () => {
    const { id } = integration;
    if (id == null) return;
    try {
      await intric.integrations.tenant.disable({ id });
      onDisable?.(integration);
      $showDisconnectDialog = false;
    } catch (e) {
      console.error(e);
    }
  });
</script>

<div class="flex w-full gap-[1px]">
  <div
    class="border-positive-stronger bg-positive-default text-on-fill hover:bg-positive-stronger flex w-full cursor-default items-center justify-center rounded-l-lg border"
  >
    Enabled
  </div>
  <Dropdown.Root gutter={2} arrowSize={0} placement="bottom-end">
    <Dropdown.Trigger asFragment let:trigger>
      <Button padding="icon" variant="positive" is={trigger} class="!rounded-l-none !rounded-r-lg"
        ><IconChevronDown></IconChevronDown></Button
      >
    </Dropdown.Trigger>
    <Dropdown.Menu let:item>
      <Button is={item} onclick={() => ($showDisconnectDialog = true)} variant="destructive">
        <IconCancel></IconCancel>
        Disable integration</Button
      >
    </Dropdown.Menu>
  </Dropdown.Root>
</div>

<Dialog.Root openController={showDisconnectDialog}>
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
