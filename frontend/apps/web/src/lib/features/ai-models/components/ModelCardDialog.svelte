<script lang="ts">
  import { Button, Dialog, Label, Tooltip } from "@intric/ui";
  import { writable } from "svelte/store";
  import ModelNameAndVendor from "./ModelNameAndVendor.svelte";
  import type { CompletionModel, EmbeddingModel } from "@intric/intric-js";

  /** Pass in a publishable resource. Its state should be maintained from the outside */
  export let model: CompletionModel | EmbeddingModel;

  /** A store to control the dialogs visibility*/
  export let openController = writable(false);

  /** Will render a dialog trigger buttone */
  export let includeTrigger = true;
</script>

<Dialog.Root {openController}>
  {#if includeTrigger}
    <Dialog.Trigger let:trigger asFragment>
      <div class="flex items-center gap-2">
        <Button is={trigger}><ModelNameAndVendor {model} /></Button>
        {#if "is_org_default" in model && model.is_org_default}
          <Tooltip text="New apps and assistants will default to this model">
            <div
              class="w-20 cursor-default rounded-full border border-positive-stronger text-center text-sm text-positive-stronger"
            >
              Default
            </div>
          </Tooltip>
        {:else}
          <div class="w-20"></div>
        {/if}
      </div>
    </Dialog.Trigger>
  {/if}

  <Dialog.Content width="dynamic">
    <Dialog.Title>Model info for {model.name}</Dialog.Title>

    <Dialog.Section>
      <div class="flex flex-col gap-2 p-8">
        <ModelNameAndVendor {model} size="card"></ModelNameAndVendor>
        <div class="max-w-[60ch] pr-12 pt-2">
          {model.description}
        </div>
      </div>
      <div
        class="grid w-full grid-cols-[auto_auto_auto] gap-x-8 border-t border-default pb-8 pl-8 pr-10 pt-4"
      >
        <Label.List
          content={[
            {
              label: model.name,
              color: "blue"
            }
          ]}
          capitalize={false}
          monospaced={true}>Full name</Label.List
        >
        {#if "token_limit" in model && model.token_limit !== null}
          <Label.List
            content={[
              {
                label: model.token_limit / 1000 + "K tokens",
                color: "blue"
              }
            ]}
            capitalize={false}
            monospaced={true}>Context size</Label.List
          >
        {/if}
        <Label.List
          content={[
            {
              label: model.hosting.toUpperCase(),
              color: model.hosting === "usa" ? "orange" : "green"
            }
          ]}
          capitalize={false}
          monospaced={true}>Hosting region</Label.List
        >
        {#if "vision" in model}
          <Label.List
            content={[
              {
                label: model.vision ? "Yes" : "No",
                color: model.vision ? "green" : "orange"
              }
            ]}
            capitalize={false}
            monospaced={true}>Vision</Label.List
          >
        {/if}
        <Label.List
          content={[
            {
              label: model.open_source ? "Yes" : "No",
              color: model.open_source ? "green" : "orange"
            }
          ]}
          capitalize={false}
          monospaced={true}>Open Source</Label.List
        >
        <Label.List
          content={[
            {
              label: model.stability,
              color: model.stability === "stable" ? "green" : "orange"
            }
          ]}
          capitalize={true}
          monospaced={true}>Stability</Label.List
        >
      </div>
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Button is={close} variant="primary" class="!px-8">Done</Button>
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
