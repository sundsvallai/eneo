<script lang="ts">
  import type { AssistantSparse } from "@intric/intric-js";
  import { Button, Dialog, Dropdown, Input, Select } from "@intric/ui";
  import IconEdit from "$lib/components/icons/IconEdit.svelte";
  import IconTrash from "$lib/components/icons/IconTrash.svelte";
  import IconEllipsis from "$lib/components/icons/IconEllipsis.svelte";
  import { getIntric } from "$lib/core/Intric";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import IconMove from "$lib/components/icons/IconMove.svelte";
  import { derived } from "svelte/store";

  export let assistant: AssistantSparse;

  const {
    state: { currentSpace, accessibleSpaces },
    refreshCurrentSpace
  } = getSpacesManager();

  const intric = getIntric();

  async function deleteAssistant() {
    isProcessing = true;
    try {
      await intric.assistants.delete(assistant);
      refreshCurrentSpace();
      $showDeleteDialog = false;
    } catch (e) {
      alert("Could not delete assistant.");
      console.error(e);
    }
    isProcessing = false;
  }

  async function moveAssistant() {
    if (!moveDestination) return;
    isProcessing = true;
    try {
      await intric.assistants.transfer({ assistant, moveResources, targetSpace: moveDestination });
      refreshCurrentSpace();
      $showMoveDialog = false;
    } catch (e) {
      alert(e);
      console.error(e);
    }
    isProcessing = false;
  }

  let isProcessing = false;
  let showDeleteDialog: Dialog.OpenState;
  let showMoveDialog: Dialog.OpenState;

  const moveTargets = derived(accessibleSpaces, ($accessibleSpaces) => {
    return $accessibleSpaces.reduce(
      (acc, curr) => {
        if (curr.id !== $currentSpace.id) {
          acc.push({ label: curr.name, value: { id: curr.id } });
        }
        return acc;
      },
      [] as Array<{ label: string; value: { id: string } }>
    );
  });
  let moveDestination: { id: string } | undefined = undefined;
  let moveResources: boolean = false;
</script>

<Dropdown.Root>
  <Dropdown.Trigger let:trigger asFragment>
    <Button is={trigger} disabled={false} padding="icon">
      <IconEllipsis></IconEllipsis>
    </Button>
  </Dropdown.Trigger>
  <Dropdown.Menu let:item>
    <Button
      is={item}
      href="/spaces/{$currentSpace.routeId}/assistants/{assistant.id}?tab=edit"
      padding="icon-leading"
    >
      <IconEdit size="small"></IconEdit>
      Edit</Button
    >
    {#if assistant.permissions?.includes("delete")}
      <Button
        is={item}
        on:click={() => {
          $showMoveDialog = true;
        }}
        padding="icon-leading"
      >
        <IconMove size="small"></IconMove>
        Move</Button
      >
      <Button
        is={item}
        destructive
        on:click={() => {
          $showDeleteDialog = true;
        }}
        padding="icon-leading"
      >
        <IconTrash size="small"></IconTrash>Delete</Button
      >
    {/if}
  </Dropdown.Menu>
</Dropdown.Root>

<Dialog.Root alert bind:isOpen={showDeleteDialog}>
  <Dialog.Content>
    <Dialog.Title>Delete assistant</Dialog.Title>
    <Dialog.Description
      >Do you really want to delete <span class="italic">{assistant.name}</span
      >?</Dialog.Description
    >

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button destructive on:click={deleteAssistant}
        >{isProcessing ? "Deleting..." : "Delete"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>

<Dialog.Root bind:isOpen={showMoveDialog}>
  <Dialog.Content wide form>
    <Dialog.Title>Move assistant</Dialog.Title>

    <Dialog.Section scrollable={false}>
      <Select.Simple
        required
        options={$moveTargets}
        bind:value={moveDestination}
        fitViewport={false}
        resourceName="space"
        class="rounded-t-md border-b border-stone-100 px-4 py-4 hover:bg-stone-50"
        >Destination</Select.Simple
      >
      <Input.Switch bind:value={moveResources} class="px-4 py-4 hover:bg-stone-50"
        >Include assistant's knowledge</Input.Switch
      >
      {#if moveResources}
        <p
          class="mx-4 mb-3 rounded-md border border-amber-500 bg-amber-50 px-2 py-1 text-sm text-amber-800"
        >
          <span class="font-bold">Hint:</span>
          Moving the assistant's connected collections and websites will only work if the destination
          space uses the same embedding model. All other assistants will lose access to the moved knowledge.
        </p>
      {/if}
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button destructive on:click={moveAssistant}
        >{isProcessing ? "Moving..." : "Move assistant"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
