<script lang="ts">
  import type { AssistantSparse } from "@intric/intric-js";
  import { IconEdit } from "@intric/icons/edit";
  import { IconTrash } from "@intric/icons/trash";
  import { IconEllipsis } from "@intric/icons/ellipsis";
  import { IconMove } from "@intric/icons/move";
  import { Button, Dialog, Dropdown, Input, Select } from "@intric/ui";
  import { getIntric } from "$lib/core/Intric";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
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
      refreshCurrentSpace("applications");
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

  let showActions = (["edit", "publish", "delete"] as const).some((permission) =>
    assistant.permissions?.includes(permission)
  );
</script>

{#if showActions}
  <Dropdown.Root>
    <Dropdown.Trigger let:trigger asFragment>
      <Button variant="on-fill" is={trigger} disabled={false} padding="icon">
        <IconEllipsis />
      </Button>
    </Dropdown.Trigger>
    <Dropdown.Menu let:item>
      {#if assistant.permissions?.includes("edit")}
        <Button
          is={item}
          href="/spaces/{$currentSpace.routeId}/assistants/{assistant.id}/edit"
          padding="icon-leading"
        >
          <IconEdit size="sm" />
          Edit</Button
        >
      {/if}
      {#if assistant.permissions?.includes("delete")}
        <Button
          is={item}
          on:click={() => {
            $showMoveDialog = true;
          }}
          padding="icon-leading"
        >
          <IconMove size="sm" />
          Move</Button
        >
        <Button
          is={item}
          variant="destructive"
          on:click={() => {
            $showDeleteDialog = true;
          }}
          padding="icon-leading"
        >
          <IconTrash size="sm" />Delete</Button
        >
      {/if}
    </Dropdown.Menu>
  </Dropdown.Root>
{/if}

<Dialog.Root alert bind:isOpen={showDeleteDialog}>
  <Dialog.Content width="small">
    <Dialog.Title>Delete assistant</Dialog.Title>
    <Dialog.Description
      >Do you really want to delete <span class="italic">{assistant.name}</span
      >?</Dialog.Description
    >

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button variant="destructive" on:click={deleteAssistant}
        >{isProcessing ? "Deleting..." : "Delete"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>

<Dialog.Root bind:isOpen={showMoveDialog}>
  <Dialog.Content width="medium" form>
    <Dialog.Title>Move assistant</Dialog.Title>

    <Dialog.Section scrollable={false}>
      <Select.Simple
        required
        options={$moveTargets}
        bind:value={moveDestination}
        fitViewport={true}
        resourceName="space"
        class="rounded-t-md border-b border-default px-4 py-4 hover:bg-hover-dimmer"
        >Destination</Select.Simple
      >
      <Input.Switch bind:value={moveResources} class="px-4 py-4 hover:bg-hover-dimmer"
        >Include assistant's knowledge</Input.Switch
      >
      {#if moveResources}
        <p
          class="label-warning mx-4 mb-3 rounded-md border border-label-default bg-label-dimmer px-2 py-1 text-sm text-label-stronger"
        >
          <span class="font-bold">Hint:</span>
          Moving the assistant's connected collections and websites will only work if the destination
          space uses the same embedding model. All other assistants will lose access to the moved knowledge.
        </p>
      {/if}
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button variant="destructive" on:click={moveAssistant}
        >{isProcessing ? "Moving..." : "Move assistant"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
