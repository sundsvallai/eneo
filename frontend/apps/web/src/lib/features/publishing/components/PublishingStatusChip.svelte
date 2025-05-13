<script lang="ts">
  import { IconCheck } from "@intric/icons/check";
  import type { PublishableResource } from "../Publisher";

  export let resource: PublishableResource;
</script>

{#if resource.published}
  <div
    class="border-positive-default bg-positive-dimmer text-positive-stronger flex w-full items-center justify-center gap-2 rounded-lg border px-2 py-1"
  >
    <IconCheck></IconCheck>
    Published
  </div>
{:else}
  <div
    class="text-secondary flex w-full items-center justify-center gap-2 rounded-lg border px-2 py-1"
  >
    Draft
  </div>
{/if}
