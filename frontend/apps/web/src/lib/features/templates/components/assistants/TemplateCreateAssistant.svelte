<script lang="ts">
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import TemplateSelector from "$lib/features/templates/components/TemplateSelector.svelte";
  import TemplateWizard from "$lib/features/templates/components/wizard/TemplateWizard.svelte";
  import { getTemplateController } from "$lib/features/templates/TemplateController";
  import { Button, Dialog, Input } from "@intric/ui";
  import CreateAssistantBackdrop from "./CreateAssistantBackdrop.svelte";
  import { goto } from "$app/navigation";

  const {
    state: { currentSpace },
    refreshCurrentSpace
  } = getSpacesManager();

  const {
    createOrContinue,
    resetForm,
    state: { currentStep, createButtonLabel, creationMode, showCreateDialog }
  } = getTemplateController();

  let openAssistantAfterCreation = true;
  let userTouchedToggle = false;

  function disableEditorOnTemplate(creationMode: "blank" | "template") {
    if (userTouchedToggle) return;
    openAssistantAfterCreation = creationMode === "blank";
  }

  $: disableEditorOnTemplate($creationMode);
</script>

<Dialog.Root openController={showCreateDialog} on:close={resetForm}>
  <Dialog.Trigger asFragment let:trigger>
    {#if $$slots.default}
      <slot {trigger}></slot>
    {:else}
      <Button is={trigger} variant="primary">Create assistant</Button>
    {/if}
  </Dialog.Trigger>

  <Dialog.Content width="medium" form>
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

    <Dialog.Section class="relative -mb-0.5 mt-2">
      {#if $currentStep === "wizard"}
        <TemplateWizard></TemplateWizard>
      {:else}
        <TemplateSelector></TemplateSelector>
        <div class="absolute right-0 top-0 h-52 w-72 overflow-hidden">
          <CreateAssistantBackdrop></CreateAssistantBackdrop>
        </div>
      {/if}
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Input.Switch
        bind:value={openAssistantAfterCreation}
        sideEffect={() => {
          userTouchedToggle = true;
        }}
        class="flex-row-reverse p-2">Open assistant editor after creation</Input.Switch
      >
      <div class="flex-grow"></div>

      {#if $currentStep === "wizard"}
        <Button
          on:click={() => {
            $currentStep = "start";
          }}>Back</Button
        >
      {:else}
        <Button is={close}>Cancel</Button>
      {/if}
      <Button
        variant="primary"
        class="w-40"
        on:click={() => {
          createOrContinue({
            onResourceCreated: ({ id }) => {
              refreshCurrentSpace();
              $showCreateDialog = false;
              resetForm();
              if (openAssistantAfterCreation) {
                goto(`/spaces/${$currentSpace.routeId}/assistants/${id}/edit`);
              }
            }
          });
        }}>{$createButtonLabel}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
