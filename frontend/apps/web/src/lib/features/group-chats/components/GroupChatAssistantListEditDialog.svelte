<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { IconCog } from "@intric/icons/cog";
  import type { GroupChat } from "@intric/intric-js";
  import { Button, Dialog, Input } from "@intric/ui";
  import { writable } from "svelte/store";

  type AssistantTool = GroupChat["tools"]["assistants"][number];
  type Props = {
    updateAssistant: (assistant: AssistantTool) => void;
    assistant: AssistantTool;
  };

  const { assistant, updateAssistant }: Props = $props();

  let descriptionProxy = $derived.by(() => {
    let value = $state(assistant.user_description ?? "");
    return { value };
  });

  let isOpen = writable(false);
</script>

<Dialog.Root openController={isOpen}>
  <Dialog.Trigger let:trigger asFragment>
    <Button variant="outlined" is={trigger} padding="icon"><IconCog></IconCog></Button>
  </Dialog.Trigger>

  <Dialog.Content width="medium">
    <Dialog.Title>Edit assistant description</Dialog.Title>
    <Dialog.Section scrollable={false}>
      <Input.Text
        class="border-default hover:bg-hover-dimmer border-b px-4 py-4"
        inputClass="pointer-events-none text-secondary"
        value={assistant.handle}
        disabled
      >
        Assistant
      </Input.Text>
      <Input.TextArea
        class=" border-default hover:bg-hover-dimmer px-4 py-4"
        label="Description"
        description="Will help intric to determine which assistant should answer a question."
        bind:value={descriptionProxy.value}
        placeholder={assistant?.default_description}
      ></Input.TextArea>
    </Dialog.Section>
    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button
        variant="primary"
        onclick={() => {
          const user_description =
            descriptionProxy.value.trim() === "" ? null : descriptionProxy.value;
          if (!user_description && !assistant.default_description) {
            alert(
              "A description is required for this assistant. Either add a description here or as an assistant description."
            );
            return;
          }
          updateAssistant({ ...assistant, user_description });
          $isOpen = false;
        }}>Accept changes</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
