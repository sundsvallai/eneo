<script lang="ts">
  import { type AppRun } from "@intric/intric-js";
  import { IconTrash } from "@intric/icons/trash";
  import { IconEllipsis } from "@intric/icons/ellipsis";
  import { Button, Dialog, Dropdown } from "@intric/ui";
  import { getIntric } from "$lib/core/Intric";
  import { getResultTitle } from "$lib/features/apps/getResultTitle";

  export let result: Pick<AppRun, "id" | "input">;
  export let onResultDeleted: ((result: Pick<AppRun, "id" | "input">) => void) | undefined =
    undefined;

  const intric = getIntric();

  let isProcessing = false;
  async function deleteResult() {
    isProcessing = true;
    try {
      await intric.apps.runs.delete(result);
      onResultDeleted?.(result);
      $showDeleteDialog = false;
    } catch (e) {
      alert("Could not delete crawl.");
      console.error(e);
    }
    isProcessing = false;
  }

  let showDeleteDialog: Dialog.OpenState;
</script>

<Dropdown.Root>
  <Dropdown.Trigger let:trigger asFragment>
    <Button is={trigger} padding="icon">
      <IconEllipsis />
    </Button>
  </Dropdown.Trigger>
  <Dropdown.Menu let:item>
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
  </Dropdown.Menu>
</Dropdown.Root>

<Dialog.Root alert bind:isOpen={showDeleteDialog}>
  <Dialog.Content width="small">
    <Dialog.Title>Delete result</Dialog.Title>
    <Dialog.Description
      >Do you really want to delete the result <span class="italic">{getResultTitle(result)}</span
      >?</Dialog.Description
    >
    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button variant="destructive" on:click={deleteResult}
        >{isProcessing ? "Deleting..." : "Delete"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
