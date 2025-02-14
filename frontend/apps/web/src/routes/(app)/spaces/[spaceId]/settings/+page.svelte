<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { Button, Dialog, Input } from "@intric/ui";
  import SelectEmbeddingModels from "./SelectEmbeddingModels.svelte";
  import EditNameAndDescription from "./EditNameAndDescription.svelte";
  import SelectCompletionModels from "./SelectCompletionModels.svelte";
  import { Page, Settings } from "$lib/components/layout";
  import SpaceStorageOverview from "./SpaceStorageOverview.svelte";

  export let data;

  const spaces = getSpacesManager();
  const currentSpace = spaces.state.currentSpace;

  let showDeleteDialog: Dialog.OpenState;
  let deleteConfirmation = "";
  let isDeleting = false;
  let showStillDeletingMessage = false;
  let deletionMessageTimeout: ReturnType<typeof setTimeout>;
  async function deleteSpace() {
    if (deleteConfirmation === "") return;
    if (deleteConfirmation !== $currentSpace.name) {
      alert("You entered a wrong name.");
      return;
    }
    isDeleting = true;
    deletionMessageTimeout = setTimeout(() => {
      showStillDeletingMessage = true;
    }, 5000);
    try {
      await spaces.deleteSpace($currentSpace);
    } catch (e) {
      alert(`Error while deleting space`);
      console.error(e);
    }
    clearTimeout(deletionMessageTimeout);
    showStillDeletingMessage = false;
    isDeleting = false;
  }
</script>

<svelte:head>
  <title>Intric.ai – {$currentSpace.name} – Settings</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title title="Settings"></Page.Title>
  </Page.Header>

  <Page.Main>
    <Settings.Page>
      <Settings.Group title="General">
        <EditNameAndDescription></EditNameAndDescription>
        <SpaceStorageOverview></SpaceStorageOverview>
      </Settings.Group>

      <Settings.Group title="AI Models">
        <SelectCompletionModels
          selectableModels={data.completionModels.filter((model) => model.is_org_enabled)}
        ></SelectCompletionModels>

        <SelectEmbeddingModels
          selectableModels={data.embeddingModels.filter((model) => model.is_org_enabled)}
        ></SelectEmbeddingModels>
      </Settings.Group>

      {#if $currentSpace.permissions?.includes("delete")}
        <Settings.Group title="Danger zone">
          <Settings.Row title="Delete space" description="Delete this space and all its resources.">
            <Dialog.Root alert bind:isOpen={showDeleteDialog}>
              <Dialog.Trigger asFragment let:trigger>
                <Button is={trigger} variant="destructive" class="flex-grow"
                  >Delete this space</Button
                >
              </Dialog.Trigger>
              <Dialog.Content width="medium" form>
                <Dialog.Title>Delete space</Dialog.Title>

                <Dialog.Section>
                  <p class="border-b border-default px-7 py-4 hover:bg-hover-dimmer">
                    Do you really want to delete the space "<span class="italic"
                      >{$currentSpace.name}</span
                    >"? You will lose access to all applications and data in it. This cannot be
                    undone.
                  </p>
                  <Input.Text
                    bind:value={deleteConfirmation}
                    label="Enter the name of this space to confirm your deletion"
                    required
                    placeholder={$currentSpace.name}
                    class=" border-default px-4 py-4 hover:bg-hover-dimmer"
                  ></Input.Text>
                </Dialog.Section>

                {#if showStillDeletingMessage}
                  <p
                    class="label-info mt-2 rounded-md border border-label-default bg-label-dimmer p-2 text-label-stronger"
                  >
                    <span class="font-bold">Hint:</span>
                    Deleting a space and all its resources can take up to 30 seconds. Please do not leave
                    this page.
                  </p>
                {/if}

                <Dialog.Controls let:close>
                  <Button is={close} disabled={isDeleting}>Cancel</Button>
                  <Button variant="destructive" on:click={deleteSpace} disabled={isDeleting}
                    >{isDeleting ? "Deleting..." : "Confirm deletion"}</Button
                  >
                </Dialog.Controls>
              </Dialog.Content>
            </Dialog.Root>
          </Settings.Row>
        </Settings.Group>
      {/if}
    </Settings.Page>
  </Page.Main>
</Page.Root>
