<script lang="ts">
  import { Button, Dialog } from "@intric/ui";
  import type { PublishableResource, PublishableResourceEndpoints } from "../Publisher";
  import { writable } from "svelte/store";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";

  const { refreshCurrentSpace } = getSpacesManager();

  /** Pass in a publishable resource. Its state should be maintained from the outside */
  export let resource: PublishableResource;
  export let endpoints: PublishableResourceEndpoints;
  /** A store to control the dialogs visibility*/
  export let openController = writable(false);
  /** Should the dialog await the resource update before colsing? */
  export let awaitUpdate = false;
  /** Will render a dialog trigger buttone */
  export let includeTrigger = false;
  /** Should the included trigger be disabled? */
  export let isDisabled = false;

  let isLoading = false;
  async function toggleState() {
    try {
      const fn = resource.published ? endpoints.unpublish : endpoints.publish;
      if (awaitUpdate) {
        isLoading = true;
        await fn(resource);
        refreshCurrentSpace();
        isLoading = false;
      } else {
        fn(resource).then(() => refreshCurrentSpace());
      }
      $openController = false;
    } catch (e) {
      alert(`Could not change ${resource.name}'s status.`);
      console.error(e);
    }
  }

  function updateStrings(resource: PublishableResource) {
    if (resource.published) {
      return {
        action: "Unpublish",
        description: `Do you really want to unpublish "${resource.name}"? Viewers in this space will no longer be able to access this resource.`
      };
    } else {
      return {
        action: "Publish",
        description: `Do you want to publish "${resource.name}"? This will allow all users (including viewers) in this space to view and access this resource.`
      };
    }
  }

  $: strings = updateStrings(resource);
</script>

<Dialog.Root {openController}>
  {#if includeTrigger}
    <Dialog.Trigger let:trigger asFragment>
      <Button
        variant={resource.published ? "destructive" : "positive"}
        is={trigger}
        class="w-24 transition-colors duration-300"
        disabled={isDisabled}>{strings.action}</Button
      >
    </Dialog.Trigger>
  {/if}

  <Dialog.Content>
    <Dialog.Title>{strings.action} {resource.name}</Dialog.Title>

    <Dialog.Description>{strings.description}</Dialog.Description>

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button variant={resource.published ? "destructive" : "primary"} on:click={toggleState}
        >{isLoading ? "Loading..." : strings.action}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
