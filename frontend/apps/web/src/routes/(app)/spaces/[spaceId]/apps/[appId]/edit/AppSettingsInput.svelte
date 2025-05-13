<script lang="ts">
  import { Settings } from "$lib/components/layout";
  import { getAppEditor } from "$lib/features/apps/AppEditor";
  import AppSettingsInputType from "./AppSettingsInputType.svelte";

  const {
    state: { resource, update }
  } = getAppEditor();
</script>

{#each $update.input_fields as input, currentIndex (input)}
  <Settings.Row
    title="Input description"
    description="A label telling this app's users what data to provide via this input."
    hasChanges={$update.input_fields?.[currentIndex]?.description !==
      $resource.input_fields?.[currentIndex]?.description}
    let:aria
    revertFn={() => {
      $update.input_fields[currentIndex].description =
        $resource.input_fields?.[currentIndex]?.description;
    }}
  >
    <input
      type="text"
      {...aria}
      bind:value={input.description}
      class="border-stronger bg-primary ring-default rounded-lg border px-3 py-2 shadow focus-within:ring-2 hover:ring-2 focus-visible:ring-2"
    />
  </Settings.Row>

  <Settings.Row
    title="Input type"
    description="Select what type of media this input accepts and the kind of interface to display."
    hasChanges={$update.input_fields?.[currentIndex]?.type !==
      $resource.input_fields?.[currentIndex]?.type}
    revertFn={() => {
      $update.input_fields[currentIndex].type = $resource.input_fields?.[currentIndex]?.type;
    }}
    let:aria
  >
    <AppSettingsInputType bind:value={input.type} {aria}></AppSettingsInputType>
  </Settings.Row>
{/each}
