<script lang="ts">
  import TemplateIcon from "../TemplateIcon.svelte";
  import { formatEmojiTitle } from "$lib/core/formatting/formatEmojiTitle";
  import { dynamicColour } from "$lib/core/colours";
  import { getTemplateController } from "../../TemplateController";

  let {
    selectTemplate,
    allTemplates,
    state: { creationMode, showCreateDialog }
  } = getTemplateController();
</script>

<div class="grid max-h-[220px] w-full grid-cols-3 gap-2 overflow-hidden p-1">
  {#each allTemplates.slice(0, 3) as template}
    <button
      on:click|preventDefault={() => {
        selectTemplate(template);
        $creationMode = "template";
        $showCreateDialog = true;
      }}
      {...dynamicColour({ basedOn: template.category })}
      class="rounded-2xl"
    >
      <div
        class="tile-bg flex h-full flex-col gap-2.5 overflow-clip rounded-2xl border border-default p-3 transition-all"
      >
        <TemplateIcon {template} size="large"></TemplateIcon>
        <div class="flex-grow"></div>
        <h4 class="line-clamp-2 text-left text-lg font-medium leading-6 text-dynamic-stronger">
          {formatEmojiTitle(template.name)}
        </h4>
      </div>
    </button>
  {/each}
</div>

<style lang="postcss">
  .tile-bg {
    background: linear-gradient(183deg, var(--dynamic-dimmer) 0%, var(--background-primary) 50%);
  }

  .tile-bg:hover {
    background: var(--dynamic-dimmer);
    @apply ring-2 ring-default;
  }
</style>
