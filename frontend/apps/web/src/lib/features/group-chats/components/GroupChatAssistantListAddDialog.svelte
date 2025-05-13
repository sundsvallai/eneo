<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { IconPlus } from "@intric/icons/plus";
  import type { GroupChat } from "@intric/intric-js";
  import { Button, Dialog, Input, Select } from "@intric/ui";
  import { writable } from "svelte/store";

  type AssistantTool = GroupChat["tools"]["assistants"][number];
  type Props = {
    addAssistantToGroup: (assistant: AssistantTool) => void;
    availableAssistants: AssistantTool[];
  };

  const { addAssistantToGroup, availableAssistants }: Props = $props();

  let selectedAssistant = $state<AssistantTool | undefined>();
  let user_description = $state("");
  let isOpen = writable(false);
</script>

<Dialog.Root openController={isOpen}>
  <Dialog.Trigger let:trigger asFragment>
    <Button variant="outlined" is={trigger} class="h-12"><IconPlus></IconPlus>Add assistant</Button>
  </Dialog.Trigger>

  <Dialog.Content width="medium">
    <Dialog.Title>Add new assistant to group</Dialog.Title>
    <Dialog.Section scrollable={false}>
      <Select.Simple
        class="border-default hover:bg-hover-dimmer border-b px-4 py-4"
        options={availableAssistants.map((assistant) => {
          return {
            label: assistant.handle,
            value: assistant
          };
        })}
        bind:value={selectedAssistant}>Choose an assistant to add...</Select.Simple
      >
      <Input.TextArea
        class="border-default hover:bg-hover-dimmer border-b px-4 py-4"
        bind:value={user_description}
        placeholder={selectedAssistant?.default_description ?? "Enter a description..."}
        label="Describe responsibilities"
        description="Add a description to help intric determin which questions this assistant should answer."
      ></Input.TextArea>
    </Dialog.Section>
    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button
        variant="primary"
        disabled={!selectedAssistant}
        onclick={() => {
          if (selectedAssistant) {
            if (!user_description && selectedAssistant.default_description === null) {
              alert(
                "Description required to add this assistant to the group. Either add a description here or as an assistant description."
              );
              return;
            }
            addAssistantToGroup({ ...selectedAssistant, user_description });
            user_description = "";
            $isOpen = false;
          }
        }}>Add to group</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
