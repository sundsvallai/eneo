<script lang="ts">
  import { Page, Settings } from "$lib/components/layout";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager.js";
  import { Button } from "@intric/ui";
  import { afterNavigate, beforeNavigate } from "$app/navigation";
  import { initAssistantEditor } from "$lib/features/assistants/AssistantEditor.js";
  import { fade } from "svelte/transition";
  import AssistantSettingsAttachments from "./AssistantSettingsAttachments.svelte";
  import SelectCompletionModelV2 from "$lib/features/ai-models/components/SelectCompletionModelV2.svelte";
  import SelectBehaviourV2 from "$lib/features/ai-models/components/SelectBehaviourV2.svelte";
  import SelectKnowledgeV2 from "$lib/features/knowledge/components/SelectKnowledgeV2.svelte";
  import PromptVersionDialog from "$lib/features/prompts/components/PromptVersionDialog.svelte";
  import dayjs from "dayjs";

  export let data;

  const {
    state: { currentSpace },
    refreshCurrentSpace
  } = getSpacesManager();

  const {
    state: { resource, update, currentChanges, isSaving },
    saveChanges,
    discardChanges
  } = initAssistantEditor({
    assistant: data.assistant,
    intric: data.intric,
    onUpdateDone() {
      refreshCurrentSpace("applications");
    }
  });

  let cancelUploadsAndClearQueue: () => void;

  beforeNavigate((navigate) => {
    if (
      $currentChanges.hasUnsavedChanges &&
      !confirm("You have unsaved changes. Do you want to discard all changes?")
    ) {
      navigate.cancel();
      return;
    }
    // Discard changes that have been made, this is only important so we delete uploaded
    // files that have not been saved to the assistant
    discardChanges();
  });

  let showSavesChangedNotice = false;

  let previousRoute = `/spaces/${$currentSpace.routeId}/assistants/${data.assistant.id}`;
  afterNavigate(({ from }) => {
    if (from) previousRoute = from.url.toString();
  });
</script>

<svelte:head>
  <title
    >Intric.ai – {data.currentSpace.personal ? "Personal" : data.currentSpace.name} – {$resource.name}</title
  >
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title
      parent={{
        title: $resource.name,
        href: `/spaces/${$currentSpace.routeId}/assistants/${data.assistant.id}`
      }}
      title="Edit"
    ></Page.Title>

    <Page.Flex>
      {#if $currentChanges.hasUnsavedChanges}
        <Button
          variant="destructive"
          disabled={$isSaving}
          on:click={() => {
            cancelUploadsAndClearQueue();
            discardChanges();
          }}>Discard all changes</Button
        >

        <Button
          variant="positive"
          class="w-32"
          on:click={async () => {
            cancelUploadsAndClearQueue();
            await saveChanges();
            showSavesChangedNotice = true;
            setTimeout(() => {
              showSavesChangedNotice = false;
            }, 5000);
          }}>{$isSaving ? "Saving..." : "Save changes"}</Button
        >
      {:else}
        {#if showSavesChangedNotice}
          <p class="px-4 text-positive-stronger" transition:fade>All changes saved!</p>
        {/if}
        <Button variant="primary" class="w-32" href={previousRoute}>Done</Button>
      {/if}
    </Page.Flex>
  </Page.Header>

  <Page.Main>
    <Settings.Page>
      <Settings.Group title="General">
        <Settings.Row
          title="Name"
          description="Give this assistant a name that will be displayed to its users."
          hasChanges={$currentChanges.diff.name !== undefined}
          revertFn={() => {
            discardChanges("name");
          }}
          let:aria
        >
          <input
            type="text"
            {...aria}
            bind:value={$update.name}
            class="rounded-lg border border-default bg-primary px-3 py-2 shadow ring-default focus-within:ring-2 hover:ring-2 focus-visible:ring-2"
          />
        </Settings.Row>
      </Settings.Group>

      <Settings.Group title="Instructions">
        <Settings.Row
          title="Prompt"
          description="Describe how this assistant should behave and how it will answer questions."
          hasChanges={$currentChanges.diff.prompt !== undefined}
          revertFn={() => {
            discardChanges("prompt");
          }}
          fullWidth
          let:aria
        >
          <div slot="toolbar" class="text-secondary">
            <PromptVersionDialog
              title="Prompt history for {$resource.name}"
              loadPromptVersionHistory={() => {
                return data.intric.assistants.listPrompts({ id: data.assistant.id });
              }}
              onPromptSelected={(prompt) => {
                const restoredDate = dayjs(prompt.created_at).format("YYYY-MM-DD HH:mm");
                $update.prompt.text = prompt.text;
                $update.prompt.description = `Restored prompt from ${restoredDate}`;
              }}
            ></PromptVersionDialog>
          </div>
          <textarea
            rows={4}
            {...aria}
            bind:value={$update.prompt.text}
            on:change={() => {
              $update.prompt.description = "";
            }}
            class="min-h-24 rounded-lg border border-default bg-primary px-6 py-4 text-lg shadow ring-default focus-within:ring-2 hover:ring-2 focus-visible:ring-2"
          ></textarea>
        </Settings.Row>

        <Settings.Row
          title="Attachments"
          description="Attach further instructions, for example guidelines or important information. The assistant will always see everything included as an attachment."
          hasChanges={$currentChanges.diff.attachments !== undefined}
          revertFn={() => {
            cancelUploadsAndClearQueue();
            discardChanges("attachments");
          }}
        >
          <AssistantSettingsAttachments bind:cancelUploadsAndClearQueue
          ></AssistantSettingsAttachments>
        </Settings.Row>

        <Settings.Row
          title="Knowledge"
          description="Select additional knowledge sources that this assistant will be able to search for relevant answers."
          hasChanges={$currentChanges.diff.groups !== undefined ||
            $currentChanges.diff.websites !== undefined}
          revertFn={() => {
            discardChanges("groups");
            discardChanges("websites");
          }}
        >
          <SelectKnowledgeV2
            bind:selectedWebsites={$update.websites}
            bind:selectedCollections={$update.groups}
          ></SelectKnowledgeV2>
        </Settings.Row>
      </Settings.Group>

      <Settings.Group title="AI Settings">
        <Settings.Row
          title="Completion model"
          description="This model will be used to process the assistant's input and generate a response."
          hasChanges={$currentChanges.diff.completion_model !== undefined}
          revertFn={() => {
            discardChanges("completion_model");
          }}
          let:aria
        >
          <SelectCompletionModelV2
            bind:selectedModel={$update.completion_model}
            availableModels={$currentSpace.completion_models}
            {aria}
          ></SelectCompletionModelV2>
        </Settings.Row>

        <Settings.Row
          title="Model behaviour"
          description="Select a preset for how this model should behave, or configure its parameters manually."
          hasChanges={$currentChanges.diff.completion_model_kwargs !== undefined}
          revertFn={() => {
            discardChanges("completion_model_kwargs");
          }}
          let:aria
        >
          <SelectBehaviourV2 bind:kwArgs={$update.completion_model_kwargs} {aria}
          ></SelectBehaviourV2>
        </Settings.Row>
      </Settings.Group>

      <div class="min-h-24"></div>
    </Settings.Page>
  </Page.Main>
</Page.Root>
