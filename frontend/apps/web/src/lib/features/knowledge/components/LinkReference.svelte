<script lang="ts">
  import type { InfoBlob } from "@intric/intric-js";
  import { IconLinkExternal } from "@intric/icons/link-external";
  import { Button } from "@intric/ui";
  export let blob: InfoBlob;
  export let index: number | undefined = undefined;
</script>

<Button
  href={blob.metadata.url ?? ""}
  target="_blank"
  variant="simple"
  class="max-w-[30ch] border !border-default bg-primary shadow-sm"
  padding="icon-leading"
>
  {#if index}
    <span
      class="min-h-7 min-w-7 rounded-md border border-b-2 border-default bg-secondary text-center font-mono font-normal"
    >
      {index}
    </span>
  {/if}
  <span class="truncate">
    {blob.metadata.url}
  </span>
  <IconLinkExternal class="h-6 w-6 text-secondary" />
</Button>
