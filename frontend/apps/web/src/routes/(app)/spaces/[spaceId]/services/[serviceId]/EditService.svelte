<script lang="ts">
  import { invalidate } from "$app/navigation";
  import SelectCompletionModel from "$lib/features/ai-models/components/SelectCompletionModel.svelte";
  import { IntricError, type Service } from "@intric/intric-js";
  import { Button, Input, Select } from "@intric/ui";
  import { makeEditable } from "$lib/core/editable";
  import { getIntric } from "$lib/core/Intric";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";

  export let service: Service;

  const intric = getIntric();
  const {
    state: { currentSpace }
  } = getSpacesManager();

  let editableService = makeEditable(service);
  let stringJsonSchema = editableService.json_schema
    ? JSON.stringify(editableService.json_schema)
    : "";

  let updatingService = false;
  async function updateService() {
    if (editableService.output_format === "json" && stringJsonSchema === "") {
      return;
    }

    updatingService = true;
    const update = editableService.getEdits();

    if (update.output_format === "json") {
      update.json_schema = JSON.parse(stringJsonSchema);
    } else {
      update.json_schema = undefined;
    }

    try {
      await intric.services.update({
        service: { id: service.id },
        update
      });
      invalidate("service:get");
    } catch (e) {
      if (e instanceof IntricError) {
        alert(e.message);
        console.error(e);
      }
    }
    updatingService = false;
  }
</script>

<div class="flex min-h-full flex-grow flex-col justify-start">
  <Input.Text
    bind:value={editableService.name}
    required
    class="border-b border-stone-100 px-4 py-4 hover:bg-stone-50">Name</Input.Text
  >

  <Input.TextArea
    bind:value={editableService.prompt}
    required
    rows={6}
    class="border-b border-stone-100 px-4 py-4 hover:bg-stone-50">Prompt</Input.TextArea
  >

  <SelectCompletionModel
    bind:value={editableService.completion_model}
    selectableModels={$currentSpace.completion_models}
  />

  <!-- <Input.Switch
        bind:value={editableService.logging_enabled}
        class=" border-stone-100 px-6 py-4 hover:bg-stone-50">Logging enabled</Input.Switch
      > -->

  <Select.Simple
    class="border-b border-stone-100 px-4 py-4 hover:bg-stone-50"
    options={[
      { value: "json", label: "JSON" },
      { value: "list", label: "List" },
      { value: "boolean", label: "Boolean" },
      { value: null, label: "None" }
    ]}
    bind:value={editableService.output_format}>Output format</Select.Simple
  >

  {#if editableService.output_format === "json"}
    <Input.TextArea
      bind:value={stringJsonSchema}
      class="border-b border-stone-100 px-4 py-4 hover:bg-stone-50"
      rows={15}
      required
    >
      JSON Schema</Input.TextArea
    >
  {/if}

  <div class="flex-grow"></div>

  <div class="sticky bottom-0 flex justify-end bg-gradient-to-t from-white to-transparent p-4">
    <Button variant="primary" on:click={updateService} class="w-[140px]">
      {#if updatingService}
        Saving...
      {:else}
        Save
      {/if}
    </Button>
  </div>
</div>
