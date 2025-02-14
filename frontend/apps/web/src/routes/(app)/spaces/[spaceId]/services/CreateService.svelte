<script lang="ts">
  import { goto } from "$app/navigation";
  import { getIntric } from "$lib/core/Intric";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { Button, Dialog, Input } from "@intric/ui";

  const {
    state: { currentSpace },
    refreshCurrentSpace
  } = getSpacesManager();

  const intric = getIntric();

  let newServiceName = "";
  let openServiceAfterCreation = true;
  let isProcessing = false;
  async function createService() {
    if (newServiceName === "") return;
    isProcessing = true;

    try {
      const service = await intric.services.create({
        spaceId: $currentSpace.id,
        name: newServiceName
      });

      refreshCurrentSpace();
      $showCreateDialog = false;
      newServiceName = "";
      if (openServiceAfterCreation) {
        goto(`/spaces/${$currentSpace.routeId}/services/${service.id}?tab=edit`);
      }
    } catch (e) {
      alert("Error creating new service");
      console.error(e);
    }
    isProcessing = false;
  }

  let showCreateDialog: Dialog.OpenState;
</script>

<Dialog.Root alert bind:isOpen={showCreateDialog}>
  <Dialog.Trigger asFragment let:trigger>
    <Button is={trigger} variant="primary">Create service</Button>
  </Dialog.Trigger>
  <Dialog.Content width="medium" form>
    <Dialog.Title>Create a new service</Dialog.Title>

    <Dialog.Section>
      {#if $currentSpace.completion_models.length < 1}
        <p
          class="label-warning m-4 rounded-md border border-label-default bg-label-dimmer px-2 py-1 text-sm text-label-stronger"
        >
          <span class="font-bold">Warning:</span>
          This space does currently not have any completion models enabled. Enable at least one completion
          model to be able to create a service.
        </p>
        <div class="border-b border-default"></div>
      {/if}
      <Input.Text
        bind:value={newServiceName}
        label="Name!"
        required
        class="border-b border-default px-4 py-4 hover:bg-hover-dimmer"
      ></Input.Text>
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Input.Switch bind:value={openServiceAfterCreation} class="flex-row-reverse p-2"
        >Open service editor after creation</Input.Switch
      >
      <div class="flex-grow"></div>
      <Button is={close}>Cancel</Button>
      <Button
        variant="primary"
        on:click={createService}
        disabled={isProcessing || $currentSpace.completion_models.length === 0}
        >{isProcessing ? "Creating..." : "Create service"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
