<script lang="ts">
  import type { Job } from "@intric/intric-js";

  export let jobs: Job[];
  export let title: string;
  export let prefix: string | undefined = undefined;
</script>

{#if jobs.length > 0}
  <div class="flex flex-col gap-1 px-2 py-2">
    <span class="pl-3 font-medium">{title}</span>
    <div
      class="min-h-10 items-center justify-between rounded-lg border border-stone-300 bg-white px-3 py-2 shadow ring-stone-200 focus-within:ring-2 hover:ring-2 focus-visible:ring-2"
    >
      {#each jobs as job (job.id)}
        <div
          class="flex items-center justify-between gap-x-3 whitespace-nowrap border-b border-stone-100 px-2 py-1.5 last-of-type:border-b-0"
        >
          <div class="flex-shrink truncate pr-4">
            {prefix ? prefix + " " : ""}{job.name ?? job.id}
          </div>
          {#if job.status === "in progress" || job.status === "queued"}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="h-5 min-h-5 w-5 min-w-5 animate-spin"
              ><line x1="12" x2="12" y1="2" y2="6" /><line x1="12" x2="12" y1="18" y2="22" /><line
                x1="4.93"
                x2="7.76"
                y1="4.93"
                y2="7.76"
              /><line x1="16.24" x2="19.07" y1="16.24" y2="19.07" /><line
                x1="2"
                x2="6"
                y1="12"
                y2="12"
              /><line x1="18" x2="22" y1="12" y2="12" /><line
                x1="4.93"
                x2="7.76"
                y1="19.07"
                y2="16.24"
              /><line x1="16.24" x2="19.07" y1="7.76" y2="4.93" /></svg
            >
          {:else if job.status === "failed"}
            <div class="w-48 text-right font-medium text-red-600">Failed</div>
          {:else if job.status === "complete"}
            <div class="w-48 text-right font-medium text-teal-600">Done</div>
          {/if}
        </div>
      {/each}
    </div>
  </div>
{/if}
