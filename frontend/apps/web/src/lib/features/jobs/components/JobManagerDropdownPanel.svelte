<script lang="ts">
  import { derived } from "svelte/store";

  import { getJobManager } from "../JobManager";
  import JobListView from "./JobListView.svelte";
  import { ProgressBar } from "@intric/ui";
  const jobManager = getJobManager();
  const {
    state: { uploads, jobs, currentlyRunningJobs }
  } = jobManager;

  const jobsUploadingBlob = derived(jobs, (jobs) => {
    return jobs.filter((job) => job.task === "upload_info_blob");
  });
  const jobsEmbeddingGroup = derived(jobs, (jobs) => {
    return jobs.filter((job) => job.task === "embed_group");
  });
  const jobsTranscribing = derived(jobs, (jobs) => {
    return jobs.filter((job) => job.task === "transcription");
  });
  const jobsCrawling = derived(jobs, (jobs) => {
    return jobs.filter((job) => job.task === "crawl");
  });
</script>

<div class="flex h-full w-full flex-col">
  {#if $uploads.length > 0}
    <div class="flex flex-col gap-1 border-default px-2 py-2">
      <span class="pl-3 font-medium">Uploading</span>
      <div
        class="min-h-10 items-center justify-between rounded-lg border border-stronger bg-primary px-3 py-2 shadow ring-default focus-within:ring-2 hover:ring-2 focus-visible:ring-2"
      >
        {#each $uploads as upload (upload.id)}
          <div
            class="flex items-center justify-between gap-x-3 whitespace-nowrap border-b border-default px-2 py-1.5 last-of-type:border-b-0"
          >
            <div class="flex-shrink truncate pr-4">{upload.file.name}</div>
            {#if upload.status === "queued"}
              <div class="w-48 min-w-48 text-right text-secondary">Waiting...</div>
            {:else if upload.status === "completed"}
              <div class="w-48 min-w-48 text-right font-medium text-positive-default">Done</div>
            {:else if true}
              <div class="flex w-48 min-w-48 items-center gap-x-4">
                <ProgressBar progress={upload.progress}></ProgressBar>
                <div class="w-10 text-end">
                  <span class="text-sm text-primary">{upload.progress}%</span>
                </div>
              </div>
            {/if}
          </div>
        {/each}
      </div>
    </div>
  {/if}
  <JobListView jobs={$jobsUploadingBlob} title="Analysing..."></JobListView>
  <JobListView jobs={$jobsEmbeddingGroup} title="Embedding..."></JobListView>
  <JobListView jobs={$jobsTranscribing} title="Transcribing..."></JobListView>
  <JobListView jobs={$jobsCrawling} title="Crawling..."></JobListView>
  {#if $currentlyRunningJobs === 0}
    <div class="flex h-[6rem] w-full items-center justify-center text-secondary">
      <span> Everything is up-to-date </span>
    </div>
  {/if}
</div>
