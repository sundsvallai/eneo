<script lang="ts">
  import { Button, Dialog, Label, Tooltip } from "@intric/ui";
  import { writable } from "svelte/store";
  import ModelNameAndVendor from "./ModelNameAndVendor.svelte";
  import type { CompletionModel, EmbeddingModel, TranscriptionModel } from "@intric/intric-js";

  /** Pass in a publishable resource. Its state should be maintained from the outside */
  export let model: CompletionModel | EmbeddingModel | TranscriptionModel;

  /** A store to control the dialogs visibility*/
  export let openController = writable(false);

  /** Will render a dialog trigger buttone */
  export let includeTrigger = true;

  const vision: Label.LabelItem = {
    label: "Vision",
    color: "moss"
  };

  const reasoning: Label.LabelItem = {
    label: "Reasoning",
    color: "amethyst"
  };

  const none: Label.LabelItem = {
    label: "Basic",
    color: "gray"
  };

  const capabilities = (() => {
    if ("vision" in model && "reasoning" in model) {
      const capabilities: Label.LabelItem[] = [];
      if (model.vision) capabilities.push(vision);
      if (model.reasoning) capabilities.push(reasoning);
      if (capabilities.length === 0) capabilities.push(none);
      return capabilities;
    }
  })();
</script>

<Dialog.Root {openController}>
  {#if includeTrigger}
    <Dialog.Trigger let:trigger asFragment>
      <div class="flex items-center gap-2">
        <Button is={trigger}><ModelNameAndVendor {model} /></Button>
        {#if "is_org_default" in model && model.is_org_default}
          <Tooltip text="New apps and assistants will default to this model">
            <div
              class="border-positive-stronger text-positive-stronger w-20 cursor-default rounded-full border text-center text-sm"
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
    <Dialog.Title>Model info for {"nickname" in model ? model.nickname : model.name}</Dialog.Title>

    <Dialog.Section>
      <div class="flex flex-col gap-2 p-8">
        <ModelNameAndVendor {model} size="card"></ModelNameAndVendor>
        <div class="max-w-[60ch] pt-2 pr-12">
          {model.description}
        </div>
      </div>
      <div
        class="border-default grid w-full grid-cols-[auto_auto_auto] gap-x-8 border-t pt-4 pr-10 pb-8 pl-8"
      >
        <Label.List
          content={[
            {
              label: model.name,
              color: "blue"
            }
          ]}
          capitalize={false}
          monospaced={true}>Model</Label.List
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
        {#if capabilities}
          <Label.List content={capabilities} capitalize={false} monospaced={true}
            >Capabilities</Label.List
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
