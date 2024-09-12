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

  let newAssistantName = "";
  let openAssistantAfterCreation = true;
  let isProcessing = false;
  async function createAssistant() {
    if (newAssistantName === "") return;
    isProcessing = true;

    try {
      const assistant = await intric.assistants.create({
        spaceId: $currentSpace.id,
        name: newAssistantName
      });

      refreshCurrentSpace();
      $showCreateDialog = false;
      newAssistantName = "";
      if (openAssistantAfterCreation) {
        goto(`/spaces/${$currentSpace.routeId}/assistants/${assistant.id}?tab=edit`);
      }
    } catch (e) {
      alert("Error creating new assistant");
      console.error(e);
    }
    isProcessing = false;
  }

  let showCreateDialog: Dialog.OpenState;
</script>

<Dialog.Root alert bind:isOpen={showCreateDialog}>
  <Dialog.Trigger asFragment let:trigger>
    <Button is={trigger} variant="primary">Create assistant</Button>
  </Dialog.Trigger>
  <Dialog.Content wide form>
    <Dialog.Title>Create a new assistant</Dialog.Title>

    <Dialog.Section>
      {#if $currentSpace.completion_models.length < 1}
        <p
          class="m-4 rounded-md border border-amber-500 bg-amber-50 px-2 py-1 text-sm text-amber-800"
        >
          <span class="font-bold">Warning:</span>
          This space does currently not have any completion models enabled. Enable at least one completion
          model to be able to create an assistant.
        </p>
        <div class="border-b border-stone-100"></div>
      {/if}
      <Input.Text
        bind:value={newAssistantName}
        required
        class="border-b border-stone-100 px-4 py-4 hover:bg-stone-50">Name</Input.Text
      >
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Input.Switch bind:value={openAssistantAfterCreation} class="flex-row-reverse  px-2 py-4"
        >Open assistant editor after creation</Input.Switch
      >
      <div class="flex-grow"></div>
      <Button is={close}>Cancel</Button>
      <Button
        variant="primary"
        on:click={createAssistant}
        disabled={isProcessing || $currentSpace.completion_models.length === 0}
        >{isProcessing ? "Creating..." : "Create assistant"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
