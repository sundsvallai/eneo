<script lang="ts">
  import { type WebsiteSparse } from "@intric/intric-js";
  import { Button, Dialog, Dropdown, Select } from "@intric/ui";
  import IconEdit from "$lib/components/icons/IconEdit.svelte";
  import IconTrash from "$lib/components/icons/IconTrash.svelte";
  import IconEllipsis from "$lib/components/icons/IconEllipsis.svelte";
  import WebsiteEditor from "./WebsiteEditor.svelte";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { getIntric } from "$lib/core/Intric";
  import { derived } from "svelte/store";
  import IconMove from "$lib/components/icons/IconMove.svelte";

  export let website: WebsiteSparse;

  const intric = getIntric();
  const {
    refreshCurrentSpace,
    state: { currentSpace, accessibleSpaces }
  } = getSpacesManager();

  async function deleteWebsite() {
    isProcessing = true;
    try {
      await intric.websites.delete(website);
      refreshCurrentSpace();
      $showDeleteDialog = false;
    } catch (e) {
      alert("Could not delete crawl.");
      console.error(e);
    }
    isProcessing = false;
  }

  async function moveCollection() {
    if (!moveDestination) return;
    isProcessing = true;
    try {
      await intric.websites.transfer({ website, targetSpace: moveDestination });
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
    {#if website.permissions?.includes("delete")}
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

<Dialog.Root alert bind:isOpen={showDeleteDialog}>
  <Dialog.Content>
    <Dialog.Title>Delete crawl</Dialog.Title>
    <Dialog.Description
      >Do you really want to delete <span class="italic">{website.name}</span>?</Dialog.Description
    >
    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button destructive on:click={deleteWebsite}>{isProcessing ? "Deleting..." : "Delete"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>

<WebsiteEditor mode="update" {website} bind:showDialog={showEditDialog}></WebsiteEditor>

<Dialog.Root bind:isOpen={showMoveDialog}>
  <Dialog.Content wide form>
    <Dialog.Title>Move website</Dialog.Title>

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
        The assistants in this space will no longer have access to this website.
      </p>
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button destructive on:click={moveCollection}
        >{isProcessing ? "Moving..." : "Move website"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
