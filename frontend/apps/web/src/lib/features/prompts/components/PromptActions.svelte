<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { IconTrash } from "@intric/icons/trash";
  import { IconEllipsis } from "@intric/icons/ellipsis";
  import { Button, Dialog, Dropdown, Tooltip } from "@intric/ui";
  import { getPromptManager } from "../PromptManager";
  import type { PromptSparse } from "@intric/intric-js";
  import { IconInfo } from "@intric/icons/info";

  export let prompt: PromptSparse;
  let showDeleteDialog: Dialog.OpenState;
  let isProcessing = false;

  const {
    state: { previewedPrompt },
    deletePrompt,
    loadPreview
  } = getPromptManager();

  $: isPromptPreviewed = prompt.id === $previewedPrompt?.id;

  $: description =
    prompt.description && prompt.description.length > 50
      ? prompt.description?.substring(0, 45) + "..."
      : prompt.description;
</script>

<button
  on:click={() => loadPreview({ id: prompt.id })}
  class="absolute inset-0"
  data-prompt-previewed={isPromptPreviewed}
  aria-label="Open this prompt in the preview panel."
></button>

<div class="flex w-full items-center justify-end gap-2">
  {#if description}
    <Tooltip text={description} class="pointer-events-auto z-[1000] text-accent-stronger">
      <IconInfo></IconInfo>
    </Tooltip>
  {/if}
  <Dropdown.Root>
    <Dropdown.Trigger let:trigger asFragment>
      <Button is={trigger} disabled={false} padding="icon">
        <IconEllipsis />
      </Button>
    </Dropdown.Trigger>
    <Dropdown.Menu let:item>
      <Button
        is={item}
        variant="destructive"
        disabled={prompt.is_selected}
        on:click={() => {
          $showDeleteDialog = true;
        }}
        padding="icon-leading"
        label="Delete prompt"
        class="relative"
      >
        <IconTrash size="sm" />Delete
      </Button>
    </Dropdown.Menu>
  </Dropdown.Root>

  <Dialog.Root alert bind:isOpen={showDeleteDialog}>
    <Dialog.Content>
      <Dialog.Title>Delete prompt</Dialog.Title>
      <Dialog.Description>Do you really want to delete this version?</Dialog.Description>

      <Dialog.Controls let:close>
        <Button is={close}>Cancel</Button>
        <Button
          is={close}
          variant="destructive"
          on:click={() => {
            deletePrompt(prompt);
          }}>{isProcessing ? "Deleting..." : "Delete"}</Button
        >
      </Dialog.Controls>
    </Dialog.Content>
  </Dialog.Root>
</div>

<style lang="postcss">
  button[data-prompt-previewed="true"] {
    @apply pointer-events-none z-[-1] bg-accent-dimmer mix-blend-multiply;
  }
</style>
