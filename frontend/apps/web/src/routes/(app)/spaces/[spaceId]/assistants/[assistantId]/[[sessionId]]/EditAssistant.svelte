<script lang="ts">
  import { invalidate } from "$app/navigation";
  import { makeEditable } from "$lib/core/editable";
  import { IntricError, type Assistant } from "@intric/intric-js";
  import { Button, Input } from "@intric/ui";
  import {
    getBehaviour,
    getKwargs,
    type ModelBehaviour
  } from "$lib/features/ai-models/ModelBehaviours";
  import { getIntric } from "$lib/core/Intric";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import SelectCompletionModel from "$lib/features/ai-models/components/SelectCompletionModel.svelte";
  import SelectBehaviour from "$lib/features/ai-models/components/SelectBehaviour.svelte";
  import SelectBehaviourCustom from "$lib/features/ai-models/components/SelectBehaviourCustom.svelte";
  import { getAppContext } from "$lib/core/AppContext";
  import SelectKnowledge from "$lib/features/knowledge/components/SelectKnowledge.svelte";

  const intric = getIntric();
  const { user } = getAppContext();
  const {
    state: { currentSpace }
  } = getSpacesManager();

  export let assistant: Assistant;
  let editableAssistant = makeEditable(assistant);

  const guardrail_config: { guardrail_active: boolean } = {
    guardrail_active: assistant.guardrail?.guardrail_active ?? false
  };

  const completion_model_config: {
    behaviour: ModelBehaviour;
    custom_kwargs: { temperature: number; top_p: number };
  } = {
    behaviour: getBehaviour(assistant.completion_model_kwargs),
    custom_kwargs: {
      temperature: assistant.completion_model_kwargs?.temperature ?? 1,
      top_p: assistant.completion_model_kwargs?.top_p ?? 1
    }
  };

  let updatingAssistant = false;
  async function updateAssistant() {
    if (editableAssistant.name !== "") {
      updatingAssistant = true;

      // Get normal edits
      const update = editableAssistant.getEdits();
      // Now overwrite custom settings
      update.guardrail =
        // Do not set guardrail if not present on assistant and user selected false, otherwise we use the user value
        !guardrail_config.guardrail_active && !assistant.guardrail ? undefined : guardrail_config;
      update.completion_model_kwargs =
        getKwargs(completion_model_config.behaviour) ?? completion_model_config.custom_kwargs;

      try {
        const updated = await intric.assistants.update({
          assistant: { id: assistant.id },
          update
        });
        // This should not be necessary as invalidate overwrites it?
        editableAssistant.updateWithValue(updated);
        invalidate("assistant:get");
        refreshCurrentSpace();
      } catch (e) {
        if (e instanceof IntricError) {
          alert(e.message);
          console.error(e);
        }
      }
      updatingAssistant = false;
    }
  }

  const { refreshCurrentSpace } = getSpacesManager();
</script>

<div class="flex min-h-full flex-grow flex-col justify-start">
  <Input.Text
    bind:value={editableAssistant.name}
    class="border-b border-stone-100 px-4 py-4 hover:bg-stone-50">Name</Input.Text
  >

  <Input.TextArea
    bind:value={editableAssistant.prompt}
    rows={6}
    class="border-b border-stone-100 px-4 py-4 hover:bg-stone-50">Prompt</Input.TextArea
  >

  <div class="flex">
    <SelectCompletionModel
      bind:value={editableAssistant.completion_model}
      selectableModels={$currentSpace.completion_models}
    />

    {#if user.hasPermission("AI")}
      <SelectBehaviour bind:value={completion_model_config.behaviour} />
    {/if}
  </div>

  {#if completion_model_config.behaviour == "custom" && user.hasPermission("AI")}
    <SelectBehaviourCustom bind:kwargs={completion_model_config.custom_kwargs} />
  {/if}
  <SelectKnowledge
    availableEmbeddingModels={$currentSpace.embedding_models}
    collections={$currentSpace.knowledge.groups}
    websites={$currentSpace.knowledge.websites}
    bind:selectedCollections={editableAssistant.groups}
    bind:selectedWebsites={editableAssistant.websites}
  />

  <!-- {#if user.hasPermission("AI")}
    <Input.Switch
      bind:value={guardrail_config.guardrail_active}
      class="border-b border-stone-100 px-6 py-4 hover:bg-stone-50"
    >
      <div class="flex items-center gap-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="h-6 w-6 text-stone-300"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z"
          />
        </svg>

        Topic guard enabled
        <span
          class="hidden rounded-md border border-purple-600 px-1 py-0.5 text-xs font-normal text-purple-600 md:block"
          >Beta</span
        >
      </div></Input.Switch
    >
  {/if}
  -->
  {#if user.hasPermission("admin")}
    <Input.Switch
      bind:value={editableAssistant.logging_enabled}
      class="border-b border-stone-100 px-6 py-4 hover:bg-stone-50"
    >
      <div class="flex gap-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="h-6 w-6 text-stone-300"
          ><path d="m3 10 2.5-2.5L3 5" /><path d="m3 19 2.5-2.5L3 14" /><path d="M10 6h11" /><path
            d="M10 12h11"
          /><path d="M10 18h11" /></svg
        >

        Logging enabled
      </div></Input.Switch
    >
  {/if}
  <div class="flex-grow"></div>

  <div class="sticky bottom-0 flex justify-end bg-gradient-to-t from-white to-transparent p-4">
    <Button variant="primary" on:click={updateAssistant} class="w-[140px]">
      {#if updatingAssistant}
        Saving...
      {:else}
        Save
      {/if}
    </Button>
  </div>
</div>
