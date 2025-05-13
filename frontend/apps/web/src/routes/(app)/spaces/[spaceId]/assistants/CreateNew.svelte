<script lang="ts">
  import { goto } from "$app/navigation";
  import { getIntric } from "$lib/core/Intric";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import TemplateCreateAssistant from "$lib/features/templates/components/assistants/TemplateCreateAssistant.svelte";
  import { getTemplateController } from "$lib/features/templates/TemplateController";
  import { IconAssistant } from "@intric/icons/assistant";
  import { IconChevronDown } from "@intric/icons/chevron-down";
  import { IconPeople } from "@intric/icons/people";
  import { IntricError } from "@intric/intric-js";
  import { Button, Dialog, Dropdown, Input } from "@intric/ui";
  import { writable } from "svelte/store";

  const intric = getIntric();

  const {
    state: { showCreateDialog: showCreateAssistantDialog }
  } = getTemplateController();

  const {
    state: { currentSpace },
    refreshCurrentSpace
  } = getSpacesManager();

  const showCreateGroupChatDialog = writable(false);

  let newGroupChatName = $state("");
  let openGroupChatAfterCreation = $state(true);

  async function createNewGroupChat() {
    try {
      const newGroup = await intric.groupChats.create({
        name: newGroupChatName,
        spaceId: $currentSpace.id
      });
      refreshCurrentSpace();
      if (openGroupChatAfterCreation) {
        goto(`/spaces/${$currentSpace.routeId}/group-chats/${newGroup.id}/edit?next=default`);
      }
      newGroupChatName = "";
      $showCreateGroupChatDialog = false;
    } catch (error) {
      const message = error instanceof IntricError ? error.getReadableMessage() : String(error);
      alert(message);
    }
  }
</script>

<div class="flex gap-[1px]">
  <TemplateCreateAssistant let:trigger={createAssistantTrigger}>
    <Button variant="primary" is={createAssistantTrigger} class="!rounded-r-none"
      >Create assistant</Button
    ></TemplateCreateAssistant
  >
  <Dropdown.Root gutter={2} arrowSize={0} placement="bottom-end">
    <Dropdown.Trigger asFragment let:trigger>
      <Button padding="icon" variant="primary" is={trigger} class="!rounded-l-none"
        ><IconChevronDown></IconChevronDown></Button
      >
    </Dropdown.Trigger>
    <Dropdown.Menu let:item>
      <Button is={item} onclick={() => ($showCreateAssistantDialog = true)}>
        <IconAssistant size="sm"></IconAssistant>
        Create new assistant</Button
      >
      <Button is={item} onclick={() => ($showCreateGroupChatDialog = true)}>
        <IconPeople size="sm"></IconPeople>
        Create new group chat</Button
      >
    </Dropdown.Menu>
  </Dropdown.Root>
</div>

<Dialog.Root openController={showCreateGroupChatDialog}>
  <Dialog.Content width="dynamic">
    <Dialog.Section class="relative mt-2 -mb-0.5">
      <div class=" border-default flex w-full flex-col px-10 pt-12 pb-10">
        <h3 class="px-4 pb-1 text-2xl font-extrabold">Create a new group chat</h3>
        <p class="text-secondary max-w-[60ch] pr-36 pl-4">
          Group chats are an easy way to communicate with multiple assistants in a single session.
        </p>
        <!-- <div class="h-8"></div> -->
        <div class=" border-dimmer mt-14 mb-4 border-t"></div>
        <div class="flex flex-col gap-1 pt-6 pb-4">
          <span class="px-4 pb-1 text-lg font-medium">Group chat name</span>
          <Input.Text
            bind:value={newGroupChatName}
            hiddenLabel
            inputClass="!text-lg !py-6 !px-4"
            placeholder="Name..."
            required>Group chat name</Input.Text
          >
        </div>
      </div>
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Input.Switch bind:value={openGroupChatAfterCreation} class="flex-row-reverse p-2"
        >Open group chat editor after creation</Input.Switch
      >
      <div class="flex-grow"></div>
      <Button is={close}>Cancel</Button>
      <Button is={close} onclick={createNewGroupChat} variant="primary">Create group chat</Button>
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
