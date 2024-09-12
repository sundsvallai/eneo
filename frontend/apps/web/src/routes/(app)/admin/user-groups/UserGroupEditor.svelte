<!-- MIT License -->

<script lang="ts">
  import { invalidate } from "$app/navigation";
  import { makeEditable } from "$lib/core/editable";
  import { getIntric } from "$lib/core/Intric";
  import type { UserGroup } from "@intric/intric-js";
  import { Dialog, Button, Input } from "@intric/ui";

  const emptyUserGroup: UserGroup = {
    id: "",
    name: ""
  };

  const intric = getIntric();

  export let mode: "update" | "create" = "create";
  export let userGroup: UserGroup = emptyUserGroup;

  let showDialog: Dialog.OpenState;
  let isProcessing = false;

  const editableUserGroup = makeEditable(userGroup ?? emptyUserGroup);

  // Instead of deleting and re-creating this component, sveltekit will update the userGroup variable
  // We update this component's view based on the userGroup's value
  async function listenToChanges() {
    if (userGroup !== editableUserGroup.getOriginal()) {
      editableUserGroup.updateWithValue(userGroup);
    }
  }
  $: userGroup, listenToChanges();

  async function edit() {
    isProcessing = true;
    try {
      const updated = await intric.userGroups.update({
        userGroup: { id: userGroup.id },
        update: editableUserGroup.getEdits()
      });
      editableUserGroup.updateWithValue(updated);
      invalidate("admin:user-groups:load");
      $showDialog = false;
    } catch (error) {
      alert(error);
      console.error(error);
    }
    isProcessing = false;
  }

  async function create() {
    isProcessing = true;
    try {
      await intric.userGroups.create(editableUserGroup);
      invalidate("admin:user-groups:load");
      $showDialog = false;
      editableUserGroup.updateWithValue(emptyUserGroup);
    } catch (error) {
      alert(error);
      console.error(error);
    }
    isProcessing = false;
  }
</script>

<Dialog.Root bind:isOpen={showDialog}>
  {#if mode === "create"}
    <Dialog.Trigger asFragment let:trigger>
      <Button variant="primary" is={trigger}>Create user group</Button>
    </Dialog.Trigger>
  {:else}
    <Dialog.Trigger asFragment let:trigger>
      <Button is={trigger}>Edit</Button>
    </Dialog.Trigger>
  {/if}

  <Dialog.Content form wide>
    {#if mode === "create"}
      <Dialog.Title>Create a new user group</Dialog.Title>
    {:else}
      <Dialog.Title>Edit user group</Dialog.Title>
    {/if}

    <Dialog.Section>
      <div class="hover:bg-stone-50">
        <Input.Text
          bind:value={editableUserGroup.name}
          required
          class="border-stone-100 px-4 py-4  {mode === 'create' ? 'border-b' : ''}"
        >
          <div class="flex items-baseline justify-between">
            Group name<span class="px-2 text-[0.9rem] font-normal text-stone-400"
              >A descriptive name for this group</span
            >
          </div></Input.Text
        >
      </div>
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      {#if mode === "create"}
        <Button variant="primary" on:click={create} type="submit" disabled={isProcessing}
          >{isProcessing ? "Creating..." : "Create user group"}</Button
        >
      {:else}
        <Button variant="primary" on:click={edit} disabled={isProcessing}
          >{isProcessing ? "Saving..." : "Save changes"}</Button
        >
      {/if}
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
