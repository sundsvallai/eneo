<script lang="ts">
  import { IconFile } from "@intric/icons/file";
  import { IconFileText } from "@intric/icons/file-text";
  import type { AppRun } from "@intric/intric-js";
  export let run: Pick<AppRun, "input">;
</script>

{#if run.input.text || run.input.files.length > 0}
  <div class="flex gap-2">
    {#if run.input.text}
      <div
        class="flex max-w-[40ch] gap-2 rounded-lg p-1 pr-2 backdrop-blur-sm group-hover:bg-primary group-hover:shadow"
      >
        <IconFileText class="min-w-6" /><span class="truncate">
          Input: {run.input.text}
        </span>
      </div>
    {/if}
    {#each run.input.files as file}
      <div
        class="flex max-w-[40ch] gap-2 rounded-lg p-1 pr-2 backdrop-blur-sm group-hover:bg-primary group-hover:shadow"
      >
        <IconFile class="min-w-6" />
        <span class="truncate">
          {file.name}
        </span>
      </div>
    {/each}
  </div>
{:else}
  <div>This run did not receive any inputs.</div>
{/if}
