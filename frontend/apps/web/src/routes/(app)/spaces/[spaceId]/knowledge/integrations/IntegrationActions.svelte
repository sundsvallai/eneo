<script lang="ts">
  import { type IntegrationKnowledge } from "@intric/intric-js";
  import { IconEllipsis } from "@intric/icons/ellipsis";
  import { IconTrash } from "@intric/icons/trash";
  import { Button, Dialog, Dropdown } from "@intric/ui";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { getIntric } from "$lib/core/Intric";
  import { createAsyncState } from "$lib/core/helpers/createAsyncState.svelte";

  export let knowledgeItem: IntegrationKnowledge;

  const intric = getIntric();
  const {
    refreshCurrentSpace,
    state: { currentSpace }
  } = getSpacesManager();

  const deleteKnowledge = createAsyncState(async () => {
    try {
      await intric.integrations.knowledge.delete({
        knowledge: knowledgeItem,
        space: $currentSpace
      });
      refreshCurrentSpace();
      $showDeleteDialog = false;
    } catch (e) {
      alert("Could not delete crawl.");
      console.error(e);
    }
  });

  let showDeleteDialog: Dialog.OpenState;
</script>

<Dropdown.Root>
  <Dropdown.Trigger let:trigger asFragment>
    <Button is={trigger} padding="icon">
      <IconEllipsis />
    </Button>
  </Dropdown.Trigger>
  <Dropdown.Menu let:item>
    {#if knowledgeItem.permissions?.includes("delete")}
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

<Dialog.Root alert bind:isOpen={showDeleteDialog}>
  <Dialog.Content width="small">
    <Dialog.Title>Delete integration knowledge</Dialog.Title>
    <Dialog.Description>
      Do you really want to delete
      <span class="italic">
        {knowledgeItem.name}
      </span>? You will no longer be able to use this knowledge in your assistants.
    </Dialog.Description>
    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button variant="destructive" on:click={deleteKnowledge}
        >{deleteKnowledge.isLoading ? "Deleting..." : "Delete"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
