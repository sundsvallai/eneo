<script>
  import { IconProfile } from "@intric/icons/profile";
  import { IconAssistant } from "@intric/icons/assistant";
  import { IconKey } from "@intric/icons/key";
  import { IconLogout } from "@intric/icons/logout";
  import { Button } from "@intric/ui";
  import { createDropdownMenu } from "@melt-ui/svelte";
  import { fly, fade } from "svelte/transition";

  const {
    elements: { menu, item, trigger, overlay, arrow },
    states: { open }
  } = createDropdownMenu({
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
  label="Account and settings"
  class="relative flex h-[3.25rem] !min-w-[3.5rem] items-center justify-center text-secondary hover:bg-accent-dimmer hover:text-brand-intric"
>
  <IconProfile class="!h-7 !min-w-7 !stroke-[1.4]" />
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
    class="items absolute z-[50] flex min-w-[15rem] -translate-y-[0.75rem] flex-col rounded-sm border-b border-stronger bg-primary p-3 shadow-md"
  >
    <p
      class="border-b border-default px-6 pb-2.5 pt-1 font-mono text-[0.85rem] font-medium tracking-[0.015rem] text-secondary"
    >
      Settings
    </p>
    <Button
      unstyled
      is={[$item]}
      href="/account"
      padding="icon-leading"
      class="group relative flex h-[3.5rem] w-full items-center justify-start gap-3 border-b border-default pl-5 pr-4 text-primary last-of-type:border-b-0 hover:bg-accent-dimmer hover:text-accent-stronger"
    >
      <IconAssistant />
      My account</Button
    ><Button
      is={[$item]}
      unstyled
      href="/account/api-keys"
      padding="icon-leading"
      class="group relative flex h-[3.5rem] w-full items-center justify-start gap-3 border-b border-default pl-5 pr-4 text-primary last-of-type:border-b-0 hover:bg-accent-dimmer hover:text-accent-stronger"
    >
      <IconKey />
      My API keys</Button
    >
    <Button
      unstyled
      variant="destructive"
      is={[$item]}
      href="/logout"
      class="mt-3 flex !justify-center gap-2 rounded-lg border border-dimmer bg-primary !py-2 focus:outline-offset-4 focus:ring-offset-4"
    >
      <IconLogout />
      Logout</Button
    >

    <div {...$arrow} use:arrow class="!z-10 border-stronger" />
  </div>
{/if}

<style>
  .items {
    box-shadow:
      0px 10px 20px -10px rgba(0, 0, 0, 0.5),
      0px 30px 50px 0px rgba(0, 0, 0, 0.2);
  }
</style>
