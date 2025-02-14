<script lang="ts">
  import type { Job } from "@intric/intric-js";
  import { IconLoadingSpinner } from "@intric/icons/loading-spinner";

  export let jobs: Job[];
  export let title: string;
  export let prefix: string | undefined = undefined;
</script>

{#if jobs.length > 0}
  <div class="flex flex-col gap-1 px-2 py-2">
    <span class="pl-3 font-medium">{title}</span>
    <div
      class="min-h-10 items-center justify-between rounded-lg border border-default bg-primary px-3 py-2 shadow ring-default focus-within:ring-2 hover:ring-2 focus-visible:ring-2"
    >
      {#each jobs as job (job.id)}
        <div
          class="flex items-center justify-between gap-x-3 whitespace-nowrap border-b border-dimmer px-2 py-1.5 last-of-type:border-b-0"
        >
          <div class="flex-shrink truncate pr-4">
            {prefix ? prefix + " " : ""}{job.name ?? job.id}
          </div>
          {#if job.status === "in progress" || job.status === "queued"}
            <IconLoadingSpinner class="animate-spin" />
          {:else if job.status === "failed"}
            <div class="w-48 text-right font-medium text-negative-default">Failed</div>
          {:else if job.status === "complete"}
            <div class="w-48 text-right font-medium text-positive-default">Done</div>
          {/if}
        </div>
      {/each}
    </div>
  </div>
{/if}
