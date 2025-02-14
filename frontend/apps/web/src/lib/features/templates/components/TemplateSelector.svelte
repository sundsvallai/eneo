<script lang="ts">
  import TemplateGallery from "./gallery/TemplateGallery.svelte";
  import { getTemplateController } from "../TemplateController";
  import { formatEmojiTitle } from "$lib/core/formatting/formatEmojiTitle";
  import TemplateIcon from "./TemplateIcon.svelte";
  import { Input } from "@intric/ui";
  import { IconChevronUpDown } from "@intric/icons/chevron-up-down";
  import { IconInfo } from "@intric/icons/info";
  import { IconCopy } from "@intric/icons/copy";
  import { IconFile } from "@intric/icons/file";
  import { getAppContext } from "$lib/core/AppContext";

  const {
    state: { name, creationMode, selectedTemplate, showTemplateGallery, hasWizard },
    resourceName
  } = getTemplateController();

  const { featureFlags } = getAppContext();
</script>

<div class="outer relative flex flex-grow flex-col items-start justify-start text-left">
  <div class=" flex w-full flex-col border-default px-10 pb-10 pt-12">
    <h3 class="px-4 pb-1 text-2xl font-extrabold">Create a new {resourceName.singular}</h3>
    <p class="max-w-[60ch] pl-4 pr-36 text-secondary">
      {#if featureFlags.showTemplates}
        Create a new {resourceName.singular} from scratch or get started with a premade {resourceName.singular}
        from our template gallery.
      {:else}
        Get started creating a new {resourceName.singular} by entering a name below. You will be able
        to edit your {resourceName.singular} after creation.
      {/if}
    </p>
    <!-- <div class="h-8"></div> -->
    <div class="mb-2 mt-14 border-t border-dimmer"></div>
    <div class="flex flex-col gap-1 pb-4 pt-6">
      <span class="px-4 pb-1 text-lg font-medium">{resourceName.singularCapitalised} name</span>
      <Input.Text bind:value={$name} hiddenLabel inputClass="!text-lg !py-6 !px-4" required
        >{resourceName.singularCapitalised} name</Input.Text
      >
    </div>
    {#if featureFlags.showTemplates}
      <div class="grid grid-cols-2 gap-4">
        <button
          data-selected={$creationMode === "blank"}
          on:click|preventDefault={() => ($creationMode = "blank")}
          class="selector"
        >
          <div class="flex w-full items-center justify-start gap-2 text-left">
            <IconFile></IconFile>
            <span class="line-clamp-2 text-dynamic-stronger">
              Create a blank {resourceName.singular}</span
            >
          </div>
        </button>
        <div class="relative flex">
          <button
            data-selected={$creationMode === "template"}
            on:click|preventDefault={() => {
              if ($creationMode === "template" || $selectedTemplate === null) {
                $showTemplateGallery = true;
              }
              $creationMode = "template";
            }}
            class="selector"
          >
            <div class="flex w-full items-center justify-start gap-2 pr-6 text-left">
              {#if $selectedTemplate}
                <TemplateIcon template={$selectedTemplate}></TemplateIcon>
                <span class="truncate text-dynamic-stronger"
                  >{formatEmojiTitle($selectedTemplate.name)}</span
                >
              {:else}
                <IconCopy></IconCopy>
                Start with a template...
              {/if}
              <div class="flex-grow"></div>
            </div>
          </button>
          <button
            class="absolute right-2 top-[50%] -translate-y-[50%] rounded border border-default p-1 text-secondary hover:bg-hover-default"
            on:click|preventDefault={() => {
              $showTemplateGallery = true;
            }}
          >
            <IconChevronUpDown></IconChevronUpDown>
          </button>
        </div>
      </div>

      {#if $hasWizard}
        <p class="translate-y-5 p-2 text-center text-secondary">
          <IconInfo class="inline"></IconInfo>
          This template offers additional options. You can configure them in the next step.
        </p>
      {/if}

      <TemplateGallery></TemplateGallery>
    {/if}
  </div>
</div>

<style lang="postcss">
  button.selector {
    @apply flex h-[3.25rem] flex-grow items-center justify-between overflow-hidden rounded-lg border border-default p-3 pr-2 text-muted shadow;
  }

  button:hover.selector {
    @apply cursor-pointer border-stronger bg-hover-default text-primary ring-2 ring-default;
  }

  button[data-selected="true"].selector {
    @apply border-accent-default bg-accent-dimmer text-accent-stronger shadow-lg shadow-accent-dimmer ring-1 ring-accent-default focus:outline-offset-4;
  }
</style>
