<script lang="ts">
  import { IconEllipsis } from "@intric/icons/ellipsis";
  import { IconEdit } from "@intric/icons/edit";
  import { IconTrash } from "@intric/icons/trash";
  import { Button, Dialog, Dropdown } from "@intric/ui";
  import type { AppSparse } from "@intric/intric-js";
  import { getIntric } from "$lib/core/Intric";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import PublishingDialog from "$lib/features/publishing/components/PublishingDialog.svelte";
  import { writable } from "svelte/store";
  import { IconArrowDownToLine } from "@intric/icons/arrow-down-to-line";
  import { IconArrowUpToLine } from "@intric/icons/arrow-up-to-line";

  export let app: AppSparse;

  const {
    state: { currentSpace },
    refreshCurrentSpace
  } = getSpacesManager();

  const intric = getIntric();

  async function deleteService() {
    isProcessing = true;
    try {
      await intric.apps.delete(app);
      refreshCurrentSpace();
      $showDeleteDialog = false;
    } catch (e) {
      alert("Could not delete app.");
      console.error(e);
    }
    isProcessing = false;
  }

  let isProcessing = false;
  let showDeleteDialog: Dialog.OpenState;
  const showPublishDialog = writable(false);

  let showActions = (["edit", "publish", "delete"] as const).some((permission) =>
    app.permissions?.includes(permission)
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
      {#if app.permissions?.includes("edit")}
        <Button
          is={item}
          href="/spaces/{$currentSpace.routeId}/apps/{app.id}/edit"
          padding="icon-leading"
        >
          <IconEdit size="sm" />
          Edit</Button
        >
      {/if}
      {#if app.permissions?.includes("publish")}
        <Button
          is={item}
          on:click={() => {
            $showPublishDialog = true;
          }}
          padding="icon-leading"
        >
          {#if app.published}
            <IconArrowDownToLine size="sm"></IconArrowDownToLine>
            Unpublish
          {:else}
            <IconArrowUpToLine size="sm"></IconArrowUpToLine>
            Publish
          {/if}
        </Button>
      {/if}
      {#if app.permissions?.includes("delete")}
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
    <Dialog.Title>Delete app</Dialog.Title>
    <Dialog.Description
      >Do you really want to delete <span class="italic">{app.name}</span>?</Dialog.Description
    >

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button variant="destructive" on:click={deleteService}
        >{isProcessing ? "Deleting..." : "Delete"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>

<PublishingDialog
  resource={app}
  endpoints={intric.apps}
  openController={showPublishDialog}
  awaitUpdate
></PublishingDialog>
