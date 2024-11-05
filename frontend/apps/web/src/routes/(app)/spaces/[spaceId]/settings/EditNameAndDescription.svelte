<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script>
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { Button, Input } from "@intric/ui";

  const spaces = getSpacesManager();
  const currentSpace = spaces.state.currentSpace;

  let currentName = "";
  let currentDescription = "";

  function watch() {
    currentName = $currentSpace.name;
    currentDescription = $currentSpace.description ?? "";
  }

  $: watch(), $currentSpace;
</script>

<form action="" class="flex flex-col gap-4 pb-2 lg:flex-row lg:gap-12">
  <div class="pl-2 pr-12 lg:w-2/5">
    <h3 class="pb-1 text-lg font-medium">Name</h3>
    <p class="text-stone-500">A name to identify this space across your organisation.</p>
  </div>
  <div class="flex-grow lg:pt-3">
    <Input.Text class="peer" labelClass="text-2xl" bind:value={currentName}></Input.Text>
    <div
      class="flex h-0 flex-row-reverse items-center justify-between overflow-hidden opacity-0 transition-all duration-300 peer-focus-within:h-12 peer-focus-within:opacity-100"
    >
      <Button
        type="submit"
        variant="primary"
        on:click={() => {
          spaces.updateSpace({ name: currentName });
        }}>Save changes</Button
      >
      <Button
        variant="outlined"
        on:click={() => {
          currentName = $currentSpace.name;
        }}>Revert changes</Button
      >
    </div>
  </div>
</form>

<form action="" class="flex flex-col gap-4 pb-2 lg:flex-row lg:gap-12">
  <div class="pl-2 pr-12 lg:w-2/5">
    <h3 class="pb-1 text-lg font-medium">Description</h3>
    <p class="text-stone-500">
      A brief description of this space that will be displayed to its users.
    </p>
  </div>
  <div class="flex-grow lg:pt-3">
    <Input.TextArea bind:value={currentDescription} class="peer"></Input.TextArea>
    <div
      class="flex h-0 items-center justify-between overflow-hidden opacity-0 transition-all duration-300 peer-focus-within:h-12 peer-focus-within:opacity-100"
    >
      <Button
        variant="outlined"
        on:click={() => {
          currentDescription = $currentSpace.description ?? "";
        }}>Revert changes</Button
      >
      <Button
        variant="primary"
        on:click={() => {
          spaces.updateSpace({ description: currentDescription });
        }}>Save changes</Button
      >
    </div>
  </div>
</form>
