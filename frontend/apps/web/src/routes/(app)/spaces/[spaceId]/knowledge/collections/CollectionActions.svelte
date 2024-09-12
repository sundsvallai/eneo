<script lang="ts">
  import type { GroupSparse } from "@intric/intric-js";
  import { Button, Dialog, Dropdown, Select } from "@intric/ui";
  import CollectionEditor from "./CollectionEditor.svelte";
  import IconEllipsis from "$lib/components/icons/IconEllipsis.svelte";
  import IconEdit from "$lib/components/icons/IconEdit.svelte";
  import IconTrash from "$lib/components/icons/IconTrash.svelte";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { getIntric } from "$lib/core/Intric";
  import IconMove from "$lib/components/icons/IconMove.svelte";
  import { derived } from "svelte/store";

  const {
    refreshCurrentSpace,
    state: { accessibleSpaces, currentSpace }
  } = getSpacesManager();
  const intric = getIntric();

  export let collection: GroupSparse;

  async function deleteResource() {
    isProcessing = true;
    try {
      await intric.groups.delete(collection);
      refreshCurrentSpace();
      $showDeleteDialog = false;
    } catch (e) {
      alert("Could not delete collection.");
      console.error(e);
    }
    isProcessing = false;
  }

  async function moveCollection() {
    if (!moveDestination) return;
    isProcessing = true;
    try {
      await intric.groups.transfer({ group: collection, targetSpace: moveDestination });
      refreshCurrentSpace();
      $showMoveDialog = false;
    } catch (e) {
      alert(e);
      console.error(e);
    }
    isProcessing = false;
  }

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

  let isProcessing = false;
  let showEditDialog: Dialog.OpenState;
  let showDeleteDialog: Dialog.OpenState;
  let showMoveDialog: Dialog.OpenState;
</script>

<Dropdown.Root>
  <Dropdown.Trigger let:trigger asFragment>
    <Button is={trigger} padding="icon">
      <IconEllipsis></IconEllipsis>
    </Button>
  </Dropdown.Trigger>
  <Dropdown.Menu let:item>
    <Button
      is={item}
      on:click={() => {
        $showEditDialog = true;
      }}
      padding="icon-leading"
    >
      <IconEdit size="small"></IconEdit>
      Edit</Button
    >
    {#if collection.permissions?.includes("delete")}
      <Button
        is={item}
        on:click={() => {
          $showMoveDialog = true;
        }}
        padding="icon-leading"
      >
        <IconMove size="small"></IconMove>Move</Button
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

<CollectionEditor mode="update" {collection} bind:showDialog={showEditDialog}></CollectionEditor>

<Dialog.Root alert bind:isOpen={showDeleteDialog}>
  <Dialog.Content>
    <Dialog.Title>Delete collection</Dialog.Title>
    <Dialog.Description
      >Do you really want to delete <span class="italic">{collection.name}</span
      >?</Dialog.Description
    >

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button destructive on:click={deleteResource}
        >{isProcessing ? "Deleting..." : "Delete"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>

<Dialog.Root bind:isOpen={showMoveDialog}>
  <Dialog.Content wide form>
    <Dialog.Title>Move collection</Dialog.Title>

    <Dialog.Section scrollable={false}>
      <Select.Simple
        required
        options={$moveTargets}
        bind:value={moveDestination}
        fitViewport={false}
        class="rounded-t-md  border-stone-100 px-4 pt-4 hover:bg-stone-50"
        >Destination</Select.Simple
      >
      <p
        class="mx-4 mb-4 mt-1.5 rounded-md border border-amber-500 bg-amber-50 px-2 py-1 text-sm text-amber-800"
      >
        <span class="font-bold">Hint:</span>
        The assistants in this space will no longer have access to this collection.
      </p>
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button destructive on:click={moveCollection}
        >{isProcessing ? "Moving..." : "Move collection"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
