<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import type { CompletionModel, EmbeddingModel, TranscriptionModel } from "@intric/intric-js";
  import { IconEllipsis } from "@intric/icons/ellipsis";
  import { Button, Dropdown } from "@intric/ui";
  import { getIntric } from "$lib/core/Intric";
  import { invalidate } from "$app/navigation";
  import ModelCardDialog from "$lib/features/ai-models/components/ModelCardDialog.svelte";
  import { writable } from "svelte/store";
  import { IconInfo } from "@intric/icons/info";
  import { IconCancel } from "@intric/icons/cancel";
  import { IconCheck } from "@intric/icons/check";
  import { IconArrowUpToLine } from "@intric/icons/arrow-up-to-line";
  import { IconArrowDownToLine } from "@intric/icons/arrow-down-to-line";
  import ModelClassificationDialog from "$lib/features/security-classifications/components/ModelClassificationDialog.svelte";
  import { IconLockClosed } from "@intric/icons/lock-closed";

  export let model: CompletionModel | EmbeddingModel | TranscriptionModel;
  export let type: "completionModel" | "embeddingModel" | "transcriptionModel";

  const intric = getIntric();

  async function togglePreferred() {
    if (!("is_org_default" in model)) return;
    try {
      model = await intric.models.update(
        //@ts-expect-error ts doesn't understand this
        {
          [type]: model,
          update: {
            is_org_default: !model.is_org_default
          }
        }
      );
      invalidate("admin:models:load");
    } catch (e) {
      alert(`Error changing status of ${model.name}`);
    }
  }

  async function toggleEnabled() {
    try {
      model = await intric.models.update(
        //@ts-expect-error ts doesn't understand this
        {
          [type]: model,
          update: {
            is_org_enabled: !model.is_org_enabled
          }
        }
      );
      invalidate("admin:models:load");
    } catch (e) {
      alert(`Error changing status of ${model.name}`);
    }
  }

  const showCardDialog = writable(false);
  const showSecurityDialog = writable(false);
</script>

<Dropdown.Root>
  <Dropdown.Trigger let:trigger asFragment>
    <Button variant="on-fill" is={trigger} disabled={false} padding="icon">
      <IconEllipsis />
    </Button>
  </Dropdown.Trigger>
  <Dropdown.Menu let:item>
    <Button
      is={item}
      padding="icon-leading"
      on:click={() => {
        $showCardDialog = true;
      }}
    >
      <IconInfo></IconInfo>Show model info
    </Button>
    <Button
      is={item}
      padding="icon-leading"
      on:click={() => {
        $showSecurityDialog = true;
      }}
    >
      <IconLockClosed></IconLockClosed>Edit security classification
    </Button>
    {#if "is_org_default" in model}
      <Button is={item} on:click={togglePreferred} padding="icon-leading">
        {#if model.is_org_default}
          <IconArrowDownToLine></IconArrowDownToLine>Unset default status
        {:else}
          <IconArrowUpToLine></IconArrowUpToLine>Set as default model
        {/if}
      </Button>
    {/if}
    <Button
      is={item}
      padding="icon-leading"
      on:click={toggleEnabled}
      variant={model.is_org_enabled ? "destructive" : "positive-outlined"}
    >
      {#if model.is_org_enabled}
        <IconCancel></IconCancel>
        <span> Disable model </span>
      {:else}
        <IconCheck></IconCheck>
        Enable model
      {/if}
    </Button>
  </Dropdown.Menu>
</Dropdown.Root>

<ModelCardDialog {model} openController={showCardDialog} includeTrigger={false}></ModelCardDialog>

<ModelClassificationDialog {model} {type} openController={showSecurityDialog}
></ModelClassificationDialog>
