<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { Button, Dialog, Dropdown, Input } from "@intric/ui";
  import { writable } from "svelte/store";
  import { getSecurityClassificationService } from "../SecurityClassificationsService.svelte";
  import { IntricError, type SecurityClassification } from "@intric/intric-js";
  import { IconEllipsis } from "@intric/icons/ellipsis";
  import { IconTrash } from "@intric/icons/trash";
  import { IconEdit } from "@intric/icons/edit";
  import { IconArrowUpToLine } from "@intric/icons/arrow-up-to-line";
  import { IconArrowDownToLine } from "@intric/icons/arrow-down-to-line";
  import { createAsyncState } from "$lib/core/helpers/createAsyncState.svelte";

  type Props = {
    classification: SecurityClassification;
  };

  const { classification }: Props = $props();
  let name = $derived(classification.name);
  let description = $derived(classification.description ?? "");
  let hasChanges = $derived(
    classification.name !== name || classification.description !== description
  );

  const security = getSecurityClassificationService();
  const showDeleteDialog = writable(false);
  const showEditDialog = writable(false);

  // This is a bit counter intuitive as the classifications array has the highest class first (index 0)
  // Because we want to render it first, whereas the backend (and service internally) has it the other way round.
  const isHighest = $derived(
    security.classifications.findIndex(({ id }) => id === classification.id) === 0
  );
  const isLowest = $derived(
    security.classifications.findIndex(({ id }) => id === classification.id) ===
      security.classifications.length - 1
  );

  const remove = createAsyncState(async () => {
    try {
      await security.deleteClassification(classification);
      $showDeleteDialog = false;
    } catch (error) {
      alert(error instanceof IntricError ? error.getReadableMessage() : String(error));
    }
  });

  const update = createAsyncState(async () => {
    try {
      await security.updateClassification({
        id: classification.id,
        name: name === classification.name ? undefined : name,
        // Need to keep in mind description can be null, but defaults to empty string
        description: description === (classification.description ?? "") ? undefined : description
      });
      $showEditDialog = false;
    } catch (error) {
      alert(error instanceof IntricError ? error.getReadableMessage() : String(error));
    }
  });
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
      onclick={() => {
        security.move(classification, "up");
      }}
      disabled={isHighest}
      padding="icon-leading"
    >
      <IconArrowUpToLine size="sm" />
      Move up
    </Button>
    <Button
      is={item}
      onclick={() => {
        security.move(classification, "down");
      }}
      disabled={isLowest}
      padding="icon-leading"
    >
      <IconArrowDownToLine size="sm" />
      Move down
    </Button>
    <Button
      is={item}
      onclick={() => {
        $showEditDialog = true;
      }}
      padding="icon-leading"
    >
      <IconEdit size="sm" />
      Edit
    </Button>
    <Button
      is={item}
      variant="destructive"
      onclick={() => {
        $showDeleteDialog = true;
      }}
      padding="icon-leading"
    >
      <IconTrash size="sm"></IconTrash>Delete</Button
    >
  </Dropdown.Menu>
</Dropdown.Root>

<Dialog.Root openController={showDeleteDialog}>
  <Dialog.Content width="medium" form>
    <Dialog.Title>Create a new security classification</Dialog.Title>

    <Dialog.Description>
      Do you really want to delete the classification <span class="italic"
        >{classification.name}</span
      >? You will lose all associated information. This cannot be undone.
    </Dialog.Description>

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button variant="destructive" onclick={remove} type="submit" disabled={remove.isLoading}
        >{remove.isLoading ? "Deleting..." : "Delete classification"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>

<Dialog.Root openController={showEditDialog}>
  <Dialog.Content width="medium" form>
    <Dialog.Title>Edit security classification</Dialog.Title>

    <Dialog.Section>
      <Input.Text
        bind:value={name}
        label="Name"
        description="A recognisable display name."
        required
        class="border-default hover:bg-hover-dimmer border-b p-4"
      ></Input.Text>

      <Input.TextArea
        label="Description"
        class="border-default hover:bg-hover-dimmer border-b p-4"
        description="Describe when this classification should be chosen."
        bind:value={description}
      ></Input.TextArea>
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button
        variant="primary"
        onclick={update}
        type="submit"
        disabled={update.isLoading || !hasChanges}
        >{update.isLoading ? "Updating..." : "Update classification"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
