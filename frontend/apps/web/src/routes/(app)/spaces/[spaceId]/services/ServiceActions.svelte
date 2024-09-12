<script lang="ts">
  import type { ServiceSparse } from "@intric/intric-js";
  import { Button, Dialog, Dropdown, Select } from "@intric/ui";
  import IconEdit from "$lib/components/icons/IconEdit.svelte";
  import IconTrash from "$lib/components/icons/IconTrash.svelte";
  import IconEllipsis from "$lib/components/icons/IconEllipsis.svelte";
  import { getIntric } from "$lib/core/Intric";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import IconMove from "$lib/components/icons/IconMove.svelte";
  import { derived } from "svelte/store";

  export let service: ServiceSparse;

  const {
    state: { currentSpace, accessibleSpaces },
    refreshCurrentSpace
  } = getSpacesManager();

  const intric = getIntric();

  async function deleteService() {
    isProcessing = true;
    try {
      await intric.services.delete(service);
      refreshCurrentSpace();
      $showDeleteDialog = false;
    } catch (e) {
      alert("Could not delete service.");
      console.error(e);
    }
    isProcessing = false;
  }

  async function moveService() {
    if (!moveDestination) return;
    isProcessing = true;
    try {
      await intric.services.transfer({
        service,
        moveResources: false,
        targetSpace: moveDestination
      });
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
      href="/spaces/{$currentSpace.routeId}/services/{service.id}?tab=edit"
      padding="icon-leading"
    >
      <IconEdit size="small"></IconEdit>
      Edit</Button
    >
    {#if service.permissions?.includes("delete")}
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
    <Dialog.Title>Delete service</Dialog.Title>
    <Dialog.Description
      >Do you really want to delete <span class="italic">{service.name}</span>?</Dialog.Description
    >

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button destructive on:click={deleteService}>{isProcessing ? "Deleting..." : "Delete"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>

<Dialog.Root bind:isOpen={showMoveDialog}>
  <Dialog.Content wide form>
    <Dialog.Title>Move service</Dialog.Title>

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
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button destructive on:click={moveService}
        >{isProcessing ? "Moving..." : "Move service"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
