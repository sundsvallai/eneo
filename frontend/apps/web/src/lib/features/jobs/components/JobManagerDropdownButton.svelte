<script>
  import { Button } from "@intric/ui";
  import { createDropdownMenu } from "@melt-ui/svelte";
  import { fly, fade } from "svelte/transition";
  import JobManagerDropdownPanel from "./JobManagerDropdownPanel.svelte";
  import { getJobManager } from "../JobManager";

  const {
    state: { currentlyRunningJobs, showJobManagerPanel }
  } = getJobManager();

  const {
    elements: { menu, trigger, overlay, arrow },
    states: { open }
  } = createDropdownMenu({
    open: showJobManagerPanel,
    positioning: {
      fitViewport: true,
      flip: true,
      placement: "bottom",
      overflowPadding: 16
    },
    forceVisible: true,
    loop: true,
    preventScroll: false,
    arrowSize: 12
  });
</script>

<Button
  is={[$trigger]}
  unstyled
  label="Notifications"
  class="flex h-[3.25rem] !min-w-[3.5rem] items-center justify-center pt-[0.1rem] text-black/60 hover:bg-blue-100 hover:text-blue-700"
>
  {#if $currentlyRunningJobs === 0}
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="1.6"
      stroke-linecap="round"
      stroke-linejoin="round"
      class="h-6 w-6 min-w-6"
      ><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" /><path
        d="M10.3 21a1.94 1.94 0 0 0 3.4 0"
      /></svg
    >
  {:else}
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="1.6"
      stroke-linecap="round"
      stroke-linejoin="round"
      class="h-6 w-6 min-w-6"
      ><path d="M19.4 14.9C20.2 16.4 21 17 21 17H3s3-2 3-9c0-3.3 2.7-6 6-6 .7 0 1.3.1 1.9.3" /><path
        d="M10.3 21a1.94 1.94 0 0 0 3.4 0"
      /><circle cx="18" cy="8" r="3" fill="#f2541b" stroke="#f2541b" /></svg
    >
  {/if}
</Button>
{#if $open}
  <div
    {...$overlay}
    use:overlay
    class="fixed inset-0 z-[40] bg-black/15"
    transition:fade={{ duration: 200 }}
  />
  <div
    {...$menu}
    use:menu
    in:fly={{ y: -15, duration: 100 }}
    out:fly={{ y: -5, duration: 200 }}
    class="items absolute z-[50] flex min-w-[22rem] -translate-y-[0.75rem] flex-col rounded-sm border-b border-black/40 bg-white p-3 shadow-md"
  >
    <p
      class="mb-2 border-b border-black/10 px-6 pb-2.5 pt-1 font-mono text-[0.85rem] font-medium tracking-[0.015rem] text-black/85"
    >
      Notifications and Jobs
    </p>
    <JobManagerDropdownPanel></JobManagerDropdownPanel>

    <div {...$arrow} use:arrow class="!z-10 border-black/35" />
  </div>
{/if}

<style>
  .items {
    box-shadow:
      0px 10px 20px -10px rgba(0, 0, 0, 0.5),
      0px 30px 50px 0px rgba(0, 0, 0, 0.2);
  }
</style>
