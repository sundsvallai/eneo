<script>
  import { IconNotification } from "@intric/icons/notification";
  import { IconNotificationDot } from "@intric/icons/notification-dot";
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
  class="flex h-[3.25rem] !min-w-[3.5rem] items-center justify-center pt-[0.1rem] text-secondary hover:bg-accent-dimmer hover:text-brand-intric"
>
  {#if $currentlyRunningJobs === 0}
    <IconNotification />
  {:else}
    <IconNotificationDot class="min-w-6" />
  {/if}
</Button>
{#if $open}
  <div
    {...$overlay}
    use:overlay
    class="fixed inset-0 z-[40] bg-overlay-dimmer"
    transition:fade={{ duration: 200 }}
  />
  <div
    {...$menu}
    use:menu
    in:fly={{ y: -15, duration: 100 }}
    out:fly={{ y: -5, duration: 200 }}
    class="items absolute z-[50] flex min-w-[22rem] -translate-y-[0.75rem] flex-col rounded-sm border-b border-strongest bg-primary p-3 shadow-md"
  >
    <p
      class="mb-2 border-b border-default px-6 pb-2.5 pt-1 font-mono text-[0.85rem] font-medium tracking-[0.015rem] text-secondary"
    >
      Notifications and Jobs
    </p>
    <JobManagerDropdownPanel></JobManagerDropdownPanel>

    <div {...$arrow} use:arrow class="!z-10 border-strongest" />
  </div>
{/if}

<style>
  .items {
    box-shadow:
      0px 10px 20px -10px rgba(0, 0, 0, 0.5),
      0px 30px 50px 0px rgba(0, 0, 0, 0.2);
  }
</style>
