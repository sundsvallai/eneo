<script lang="ts">
  import { invalidate } from "$app/navigation";
  import { getIntric } from "$lib/core/Intric";
  import { IconRefresh } from "@intric/icons/refresh";
  import type { Website } from "@intric/intric-js";
  import { Button, Dialog, Tooltip } from "@intric/ui";

  export let website: Website;
  export let isDisabled = false;

  const intric = getIntric();

  let isProcessing = false;
  let showDialog: Dialog.OpenState;

  async function createRun() {
    isProcessing = true;
    try {
      intric.websites.crawlRuns.create(website).then(() => {
        isProcessing = false;
        invalidate("crawlruns:list");
      });
      $showDialog = false;
    } catch (error) {
      console.error(error);
      alert("Error when trying to create a new crawl run.");
    }
  }
</script>

<Dialog.Root bind:isOpen={showDialog}>
  <Dialog.Trigger let:trigger asFragment>
    <Tooltip text={isDisabled ? "Can't sync while a crawl is already running" : undefined}>
      <Button is={trigger} variant="primary" disabled={isDisabled}>
        <IconRefresh></IconRefresh>
        Sync now</Button
      >
    </Tooltip>
  </Dialog.Trigger>
  <Dialog.Content width="small">
    <Dialog.Title>Sync website</Dialog.Title>
    <Dialog.Description>
      Do you want to synchronise
      <span class="italic">
        {website.name ? `${website.name} (${website.url})` : website.url}
      </span> now by starting a new crawl run?
    </Dialog.Description>
    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      <Button variant="primary" on:click={createRun} disabled={isProcessing}
        >{isProcessing ? "Starting..." : "Start crawl"}</Button
      >
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
