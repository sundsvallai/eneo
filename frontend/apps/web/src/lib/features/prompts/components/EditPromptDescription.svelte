<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { getAppContext } from "$lib/core/AppContext";
  import { Button, Dialog, Input, Tooltip } from "@intric/ui";
  import { getPromptManager } from "../PromptManager";
  import type { Prompt } from "@intric/intric-js";

  export let prompt: Prompt;
  let description = prompt.description ?? "";

  const { user } = getAppContext();
  const { updatePromptDescription } = getPromptManager();

  $: isPromptCreatedByUser = user.id === prompt.user.id;
</script>

<Dialog.Root>
  <Dialog.Trigger asFragment let:trigger>
    <Tooltip
      text={!isPromptCreatedByUser
        ? "Only the author of a prompt can change the description"
        : undefined}
    >
      <Button variant="outlined" disabled={!isPromptCreatedByUser} is={trigger}
        >{prompt.description ? "Edit" : "Add"} description</Button
      >
    </Tooltip>
  </Dialog.Trigger>

  <Dialog.Content width="medium" form>
    <Dialog.Title>Edit prompt description</Dialog.Title>

    <Dialog.Section>
      <Input.TextArea
        bind:value={description}
        class="border-default hover:bg-hover-dimmer border-b px-4 py-4"
        rows={3}
      >
        Description</Input.TextArea
      >
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button
        variant="primary"
        is={close}
        on:click={() => {
          updatePromptDescription({
            id: prompt.id,
            description
          });
        }}>Save changes</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
