<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { Button, Dialog, Input } from "@intric/ui";
  import { writable } from "svelte/store";
  import { getSecurityClassificationService } from "../SecurityClassificationsService.svelte";
  import { IntricError } from "@intric/intric-js";
  import { Settings } from "$lib/components/layout";
  import { createAsyncState } from "$lib/core/helpers/createAsyncState.svelte";

  const security = getSecurityClassificationService();

  let isEnabled = $derived(security.isSecurityEnabled);
  let showEnableDialog = writable(false);
  let showDisableDialog = writable(false);

  function onValueChange({ current, next }: { current: boolean; next: boolean }) {
    if (current !== next) {
      $showEnableDialog = next;
      $showDisableDialog = !next;
    }
  }

  const enable = createAsyncState(async () => {
    try {
      await security.enable();
      $showEnableDialog = false;
    } catch (e) {
      alert(e instanceof IntricError ? e.getReadableMessage() : String(e));
    }
  });

  const disable = createAsyncState(async () => {
    try {
      await security.disable();
      $showDisableDialog = false;
    } catch (e) {
      alert(e instanceof IntricError ? e.getReadableMessage() : String(e));
    }
  });
</script>

<Settings.Row
  title="Security classification"
  description="Enable security classifications across your organisation's spaces."
>
  <div class="border-default flex h-14 border-b py-2">
    <Input.RadioSwitch bind:value={isEnabled} sideEffect={onValueChange}></Input.RadioSwitch>
  </div>
</Settings.Row>

<Dialog.Root openController={showEnableDialog}>
  <Dialog.Content>
    <Dialog.Title>Enable security classifications</Dialog.Title>

    <Dialog.Description>
      Do you want to enable security classifications for your organisation? This will limit the
      availablity of AI models based on their respective security setting.
    </Dialog.Description>

    <Dialog.Controls>
      <Button
        onclick={() => {
          isEnabled = security.isSecurityEnabled;
          $showEnableDialog = false;
        }}>Cancel</Button
      >
      <Button variant="primary" onclick={enable} disabled={enable.isLoading}>Enable</Button>
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>

<Dialog.Root openController={showDisableDialog}>
  <Dialog.Content>
    <Dialog.Title>Disable security classifications</Dialog.Title>

    <Dialog.Description>
      Do you want to disable security classifications for your organisation? This will remove model
      restrictions from your spaces.
    </Dialog.Description>

    <Dialog.Controls>
      <Button
        onclick={() => {
          isEnabled = security.isSecurityEnabled;
          $showDisableDialog = false;
        }}>Cancel</Button
      >
      <Button variant="destructive" onclick={disable} disabled={disable.isLoading}>Disable</Button>
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
