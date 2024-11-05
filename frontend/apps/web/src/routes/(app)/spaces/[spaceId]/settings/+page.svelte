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
  import { Page } from "$lib/components/layout";

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
    <Page.Title>Settings</Page.Title>
  </Page.Header>
  <Page.Main>
    <section>
      <h2
        class="sticky top-0 col-span-2 border-b border-black/5 bg-white/85 pb-3 pl-2 pt-3 font-mono text-sm backdrop-blur-sm"
      >
        General
      </h2>
      <div class="flex flex-col gap-4 py-5 pr-6 lg:gap-12">
        <EditNameAndDescription></EditNameAndDescription>
      </div>
    </section>

    <section class="relative">
      <h2
        class="sticky top-0 z-10 col-span-2 border-b border-black/5 bg-white/85 pb-3 pl-2 pt-3 font-mono text-sm backdrop-blur-sm"
      >
        AI Models
      </h2>

      <div class="relative flex flex-col gap-8 py-5 pr-6 lg:gap-12">
        <SelectCompletionModels
          selectableModels={data.completionModels.filter((model) => model.can_access)}
        ></SelectCompletionModels>

        <SelectEmbeddingModels
          selectableModels={data.embeddingModels.filter((model) => model.can_access)}
        ></SelectEmbeddingModels>
      </div>
    </section>

    {#if $currentSpace.permissions?.includes("delete")}
      <section>
        <h2
          class="sticky top-0 col-span-2 border-b border-black/5 bg-white/85 pb-3 pl-2 pt-3 font-mono text-sm backdrop-blur-sm"
        >
          Danger zone
        </h2>

        <div class="flex flex-col gap-4 py-5 pr-6 lg:flex-row lg:gap-12">
          <div class="pl-2 lg:w-2/5">
            <h3 class="pb-1 text-lg font-medium">Delete space</h3>
            <p class="text-stone-500">Delete this space and all its resources.</p>
          </div>
          <Dialog.Root alert bind:isOpen={showDeleteDialog}>
            <Dialog.Trigger asFragment let:trigger>
              <Button is={trigger} destructive class="flex-grow">Delete this space</Button>
            </Dialog.Trigger>
            <Dialog.Content form wide>
              <Dialog.Title>Delete space</Dialog.Title>

              <Dialog.Section>
                <p class="border-b border-stone-100 px-7 py-4 hover:bg-stone-50">
                  Do you really want to delete the space "<span class="italic"
                    >{$currentSpace.name}</span
                  >"? You will lose access to all applications and data in it. This cannot be
                  undone.
                </p>
                <Input.Text
                  bind:value={deleteConfirmation}
                  required
                  placeholder={$currentSpace.name}
                  class=" border-stone-100 px-4 py-4 hover:bg-stone-50"
                >
                  Enter the name of this space to confirm your deletion
                </Input.Text>
              </Dialog.Section>

              {#if showStillDeletingMessage}
                <p class="mt-2 rounded-md border border-blue-600 bg-blue-50 p-2 text-blue-700">
                  <span class="font-bold">Hint:</span>
                  Deleting a space and all its resources can take up to 30 seconds. Please do not leave
                  this page.
                </p>
              {/if}

              <Dialog.Controls let:close>
                <Button is={close} disabled={isDeleting}>Cancel</Button>
                <Button destructive on:click={deleteSpace} disabled={isDeleting}
                  >{isDeleting ? "Deleting..." : "Confirm deletion"}</Button
                >
              </Dialog.Controls>
            </Dialog.Content>
          </Dialog.Root>
        </div>
      </section>
    {/if}
    <div class="min-h-8"></div>
  </Page.Main>
</Page.Root>
