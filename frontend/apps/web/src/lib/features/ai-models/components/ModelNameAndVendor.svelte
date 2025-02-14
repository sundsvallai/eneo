<script context="module" lang="ts">
  export type OrgInfo = {
    logo: string;
  };

  export const modelOrgs: Record<ModelCreatorOrg, OrgInfo> = {
    OpenAI: {
      logo: "/logos/openai.jpg"
    },
    Anthropic: {
      logo: "/logos/anthropic.jpg"
    },
    Microsoft: {
      logo: "/logos/ms.jpg"
    },
    Meta: {
      logo: "/logos/meta.jpg"
    }
  };
</script>

<script lang="ts">
  import { IconCPU } from "@intric/icons/CPU";
  import type { CompletionModel, EmbeddingModel, ModelCreatorOrg } from "@intric/intric-js";
  import { Tooltip } from "@intric/ui";

  export let model: CompletionModel | EmbeddingModel;
  export let size: "card" | "table" = "table";

  $: logo = model.org && model.org in modelOrgs ? modelOrgs[model.org].logo : null;
</script>

{#if size === "card"}
  <div class="flex items-center justify-start gap-4">
    <div
      class="flex h-12 w-12 items-center justify-center overflow-clip rounded-lg border border-default bg-secondary"
    >
      {#if logo}
        <img src={logo} class="h-full w-full object-cover" alt="{model.org} logo" />
      {:else}
        <IconCPU class="text-muted"></IconCPU>
      {/if}
    </div>
    <h4 class="text-xl font-bold leading-6 text-primary">
      {"nickname" in model ? model.nickname : model.name}
    </h4>
  </div>
{:else}
  <div class="flex items-center justify-start gap-3">
    <div
      class="flex h-7 w-7 items-center justify-center overflow-clip rounded-lg border border-default bg-secondary"
    >
      {#if logo}
        <img src={logo} class="h-full w-full object-cover" alt="{model.org} logo" />
      {:else}
        <IconCPU class="text-muted"></IconCPU>
      {/if}
    </div>
    <Tooltip text={model.description ?? model.name}>
      <h4 class=" text-primary">
        {"nickname" in model ? model.nickname : model.name}
      </h4>
    </Tooltip>
  </div>
{/if}
