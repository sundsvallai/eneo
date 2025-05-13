<script lang="ts">
  import { Tooltip } from "@intric/ui";
  import type { PublishableResource, PublishableResourceEndpoints } from "../Publisher";
  import PublishingDialog from "./PublishingDialog.svelte";
  import { IconLoadingSpinner } from "@intric/icons/loading-spinner";
  import PublishingStatusChip from "./PublishingStatusChip.svelte";

  export let resource: PublishableResource;
  export let endpoints: PublishableResourceEndpoints;
  export let hasUnsavedChanges: boolean;

  let isLoading = false;

  const wrappedPublisher = {
    publish: async () => {
      isLoading = true;
      try {
        resource = await endpoints.publish(resource);
      } catch (e) {
        alert(`Could not publish ${resource.name}.`);
      }
      isLoading = false;
      return resource;
    },
    unpublish: async () => {
      isLoading = true;
      try {
        resource = await endpoints.unpublish(resource);
      } catch (e) {
        alert(`Could not unpublish ${resource.name}.`);
      }
      isLoading = false;
      return resource;
    }
  };
</script>

<div class="border-default flex h-14 items-center justify-between gap-4 border-b p-2">
  <div class="text-muted flex flex-grow items-center justify-center gap-2">
    {#if isLoading}
      <IconLoadingSpinner class="ml-2 animate-spin"></IconLoadingSpinner>
      <span>Updating...</span>
    {:else}
      <PublishingStatusChip {resource}></PublishingStatusChip>
    {/if}
  </div>
  <Tooltip
    text={hasUnsavedChanges
      ? "Save or discard your changes before updating the status."
      : undefined}
  >
    <PublishingDialog
      {resource}
      endpoints={wrappedPublisher}
      includeTrigger
      isDisabled={hasUnsavedChanges}
    ></PublishingDialog>
  </Tooltip>
</div>
