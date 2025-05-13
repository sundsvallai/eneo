<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { Button, Dialog, Input } from "@intric/ui";
  import { writable } from "svelte/store";
  import { getSecurityClassificationService } from "../SecurityClassificationsService.svelte";
  import { IntricError } from "@intric/intric-js";
  import { createAsyncState } from "$lib/core/helpers/createAsyncState.svelte";

  let name = $state("");
  let description = $state("");
  const showDialog = writable(false);
  const security = getSecurityClassificationService();

  const create = createAsyncState(async () => {
    if (!name) return;
    try {
      await security.createClassification({ name, description });
      $showDialog = false;
      name = "";
      description = "";
    } catch (error) {
      alert(error instanceof IntricError ? error.getReadableMessage() : String(error));
    }
  });
</script>

<Dialog.Root openController={showDialog}>
  <Dialog.Trigger asFragment let:trigger>
    <Button variant="primary" is={trigger}>Create new</Button>
  </Dialog.Trigger>

  <Dialog.Content width="medium" form>
    <Dialog.Title>Create a new security classification</Dialog.Title>

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
      <Button variant="primary" onclick={create} type="submit" disabled={create.isLoading}
        >{create.isLoading ? "Creating..." : "Create classification"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
